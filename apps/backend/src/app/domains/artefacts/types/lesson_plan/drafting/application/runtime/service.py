from __future__ import annotations

import inspect
import logging
from collections.abc import Awaitable, Callable
from dataclasses import asdict
from datetime import datetime, timezone
from time import perf_counter
from typing import TypeVar, cast

import dspy
from pydantic import ValidationError

from app.config import CONFIG
from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification
from app.infra.dspy_lm import active_model_name
from app.shared.json_types import JsonObject
from app.shared.readers import reader_for

from ....domain.lesson_document import as_document, violations
from ....domain.plan_requirements import unmet
from ...domain.generation_inputs import (
    PreparedGenerationInputs,
    build_run_metadata,
    prepare_generation_inputs,
)
from ...infrastructure.dspy.modules.artifacts import GenerationArtifacts
from ...infrastructure.dspy.modules.generator import (
    LessonGenerationArtifacts,
    LessonGenerationModule,
)
from ...infrastructure.dspy.modules.whole_lesson_generator import (
    WholeLessonArtifacts,
    WholeLessonGenerationModule,
)
from ..precompute import GenerationMetrics
from .assembly import SessionPlanAssembler
from .diagnostics import DiagnosticLogWriter
from .semantic_validation import SemanticPlanValidator
from .status import DspyStatusLogger, log_timestamp
from .types import GeneratedLessonPlan, NormalizedLessonDraft

StageResultT = TypeVar("StageResultT")


def seeded_brief(grade: str) -> ArtefactSpec:
    """The lesson-plan spec as seeded, for a generation no caller briefed."""
    return seed_specification(ArtefactType.LESSON_PLAN.value).brief(reader_for(grade))


class _UnsupportedGenerationPayloadError(Exception):
    """Sentinel: the generation program returned a payload of the wrong type.

    A contract/programming error (not a refinable structural slip), so it bypasses
    the refine loop's soft-issue safety net and fails fast.
    """


class LessonGenerationService:
    def __init__(self, *, final_writer_mode: str | None = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.model_name = active_model_name()
        self.lm = getattr(dspy.settings, "lm", None)
        self.final_writer_mode = (
            final_writer_mode or CONFIG.lesson_plan.final_writer_mode
        ).strip() or CONFIG.lesson_plan.final_writer_mode
        self.status_logger = next(
            (
                callback
                for callback in getattr(dspy.settings, "callbacks", []) or []
                if isinstance(callback, DspyStatusLogger)
            ),
            None,
        )
        self.generation_program = LessonGenerationModule(
            final_writer_mode=self.final_writer_mode,
            model_name=self.model_name,
        )
        # No-linkage (curriculum_only) layer: single-call monolithic drafter
        # (the bake-off winner for ungrounded/cold-start). Both layers share the
        # bounded refine loop below.
        self.no_linkage_program = WholeLessonGenerationModule(
            final_writer_mode=self.final_writer_mode,
            use_optimized=CONFIG.lesson_plan.use_optimized_program,
            optimized_program_path=CONFIG.lesson_plan.optimized_program_path,
        )
        self.max_refine_attempts = CONFIG.lesson_plan.max_refine_attempts
        self.default_evidence_selection_strategy = CONFIG.lesson_plan.evidence_selection_strategy
        self.semantic_validator = SemanticPlanValidator(logger=self.logger)
        self.session_plan_assembler = SessionPlanAssembler()
        self.diagnostic_writer = DiagnosticLogWriter()

    async def _run_generation_stage(
        self,
        *,
        stage_name: str,
        runner: Callable[..., StageResultT | Awaitable[StageResultT]],
        strategy: str,
        record_count: int,
        objective_count: int,
        **kwargs: object,
    ) -> StageResultT:
        started_at = perf_counter()
        self.logger.info(
            "%s Lesson-plan stage start: stage=%s selection_mode=%s records=%s objectives=%s",
            log_timestamp(),
            stage_name,
            strategy,
            record_count,
            objective_count,
        )
        result = runner(**kwargs)
        if inspect.isawaitable(result):
            result = await result
        elapsed_ms = round((perf_counter() - started_at) * 1000, 1)
        trajectory = getattr(result, "trajectory", None)
        trajectory_steps = len(trajectory) if isinstance(trajectory, list) else None
        final_reasoning = getattr(result, "final_reasoning", None)
        self.logger.info(
            "%s Lesson-plan stage done: stage=%s selection_mode=%s "
            "elapsed_ms=%s trajectory_steps=%s final_reasoning=%s",
            log_timestamp(),
            stage_name,
            strategy,
            elapsed_ms,
            trajectory_steps if trajectory_steps is not None else "-",
            str(final_reasoning or "-")[:200],
        )
        return cast(StageResultT, result)

    def _build_generation_metrics(
        self,
        *,
        session_subtopic: str,
        artifacts: LessonGenerationArtifacts,
        lm_calls_before: int | None,
    ) -> GenerationMetrics:
        planning_duration_ms = artifacts.planning_duration_ms
        drafting_duration_ms = artifacts.drafting_duration_ms
        total_duration_ms = planning_duration_ms + drafting_duration_ms
        planning_llm_calls = artifacts.planning_result.llm_calls_planning

        total_llm_calls: int | None = None
        if self.status_logger is not None:
            total_llm_calls = max(self.status_logger.lm_call_count() - (lm_calls_before or 0), 0)
        if total_llm_calls is None:
            total_llm_calls = planning_llm_calls + artifacts.drafting_llm_call_estimate
        drafting_llm_calls = max(total_llm_calls - planning_llm_calls, 0)

        return GenerationMetrics(
            subtopic_id=artifacts.planning_result.subtopic_id or session_subtopic or "unknown",
            cached_planning=bool(artifacts.planning_result.from_cache),
            llm_calls_planning=planning_llm_calls,
            llm_calls_drafting=drafting_llm_calls,
            total_llm_calls=total_llm_calls,
            planning_duration_ms=planning_duration_ms,
            drafting_duration_ms=drafting_duration_ms,
            total_duration_ms=total_duration_ms,
            violations=len(artifacts.planning_result.violations),
            is_valid=not any(
                violation.severity == "error" for violation in artifacts.planning_result.violations
            ),
        )

    async def generate(
        self,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        evidence_selection_strategy: str | None = None,
        grounding_mode: str = "manual_linkage",
        curated_objectives: list[JsonObject] | None = None,
        brief: ArtefactSpec | None = None,
    ) -> GeneratedLessonPlan:
        inputs = prepare_generation_inputs(
            session_context=session_context,
            curriculum_context=curriculum_context,
            reference_context=reference_context,
            requested_strategy=evidence_selection_strategy,
            default_strategy=self.default_evidence_selection_strategy,
            grounding_mode=grounding_mode,
            curated_objectives=curated_objectives,
            brief=brief or seeded_brief(str(session_context.get("grade") or "")),
        )

        lm_calls_before = self.status_logger.lm_call_count() if self.status_logger else None

        # Two layers, one shared in-loop refine. curriculum_only -> single-call
        # monolithic drafter; otherwise the staged/curated pipeline. Both feed the
        # FULL semantic check back into each attempt and keep the best one.
        if inputs.grounding_mode == "curriculum_only":
            runner, stage_name = self.no_linkage_program, "lesson_plan_no_linkage"
        else:
            runner, stage_name = self.generation_program, "lesson_plan_generation"

        artifacts, normalized_draft, residual, attempts = await self._refine_attempts(
            inputs=inputs, runner=runner, stage_name=stage_name
        )

        session_plan_content = self.session_plan_assembler.build_content(
            session=inputs.session,
            inputs=inputs,
            artifacts=artifacts,
            draft=normalized_draft,
        )
        try:
            session_plan = self.session_plan_assembler.assemble(
                session=inputs.session,
                session_plan_content=session_plan_content,
            )
        except Exception as exc:
            self.logger.exception(
                "session_plan assembly failed",
                extra={"model": self.model_name},
            )
            raise ValueError("session_plan assembly failed") from exc

        run_metadata = build_run_metadata(
            model_name=self.model_name,
            generated_at=datetime.now(timezone.utc).isoformat(),
            inputs=inputs,
            final_writer_mode=self.final_writer_mode,
            dspy_status_logging=self.status_logger is not None,
        )
        run_metadata["generation_metrics"] = self._refined_generation_metrics(
            inputs=inputs,
            artifacts=artifacts,
            attempts=attempts,
            lm_calls_before=lm_calls_before,
        )
        # Best-effort policy: if violations remain after bounded refine, persist
        # with needs_review rather than hard-failing (keeps expert eval unblocked).
        run_metadata["needs_review"] = bool(residual)
        run_metadata["semantic_violations"] = list(residual)

        try:
            run_metadata["diagnostic_log_path"] = self.diagnostic_writer.write(
                session=inputs.session,
                inputs=inputs,
                artifacts=artifacts,
                draft=normalized_draft,
                consistency_checks=list(residual),
                session_plan=session_plan,
            )
        except Exception as exc:  # noqa: BLE001 - diagnostics are best-effort
            self.logger.warning(
                "%s lesson-plan diagnostic log write failed session_id=%s error=%s",
                log_timestamp(),
                inputs.session.session_id,
                exc,
            )
            run_metadata["diagnostic_log_path"] = None

        return GeneratedLessonPlan(
            session_plan=session_plan,
            run_metadata=run_metadata,
        )

    async def _refine_attempts(
        self,
        *,
        inputs: PreparedGenerationInputs,
        runner: Callable[..., GenerationArtifacts | Awaitable[GenerationArtifacts]],
        stage_name: str,
    ) -> tuple[GenerationArtifacts, NormalizedLessonDraft, list[str], int]:
        """Bounded in-loop refine shared by both layers: generate -> collect_issues.

        (non-raising) -> feed the FULL violation set back -> keep the best attempt.
        Returns (artifacts, normalized_draft, residual_issues, attempts).
        """
        best_artifacts: GenerationArtifacts | None = None
        best_draft: NormalizedLessonDraft | None = None
        best_issues: list[str] | None = None
        prior_violations: list[str] | None = None
        attempts = 0
        for attempt in range(self.max_refine_attempts):
            attempts = attempt + 1
            try:
                artifacts = await self._run_generation_stage(
                    stage_name=stage_name,
                    runner=runner,
                    strategy=inputs.evidence_selection_strategy,
                    record_count=len(inputs.textbook_records),
                    objective_count=len(inputs.curriculum_objectives),
                    request=inputs,
                    prior_violations=prior_violations,
                )
                if not isinstance(artifacts, (LessonGenerationArtifacts, WholeLessonArtifacts)):
                    raise _UnsupportedGenerationPayloadError
                normalized_draft = self.session_plan_assembler.normalize_draft(
                    artifacts=artifacts,
                    inputs=inputs,
                )
                issues = [
                    *self.semantic_validator.collect_issues(
                        lesson_plan_objectives=artifacts.lesson_plan_objectives,
                        resolved_kcs=artifacts.resolved_kcs,
                        step_evidence_by_objective=artifacts.step_evidence_plans,
                        global_steps=normalized_draft.global_steps,
                        textbook_records=inputs.textbook_records,
                        curriculum_context=inputs.curriculum,
                    ),
                    *self._specification_issues(inputs, artifacts, normalized_draft),
                ]
            except _UnsupportedGenerationPayloadError:
                raise ValueError("lesson_generation_program returned unsupported payload") from None
            except (ValueError, ValidationError) as exc:
                # A hard structural violation escaped generation/normalization (e.g. a
                # malformed core step). Degrade it to a soft issue fed into the next attempt
                # rather than crashing the request — the refine loop is meant to be
                # non-raising. If every attempt fails this way, the guard below raises.
                self.logger.warning(
                    "%s lesson plan generation attempt %d raised a structural violation: %s",
                    log_timestamp(),
                    attempts,
                    exc,
                )
                prior_violations = [f"structural_violation: {exc}"]
                continue
            if best_issues is None or len(issues) < len(best_issues):
                best_artifacts, best_draft, best_issues = artifacts, normalized_draft, issues
            if not issues:
                break
            prior_violations = issues  # full violation set fed back into the next attempt

        if best_artifacts is None or best_draft is None:
            raise ValueError("lesson plan generation produced no candidate plan")
        return best_artifacts, best_draft, list(best_issues or []), attempts

    def _specification_issues(
        self,
        inputs: PreparedGenerationInputs,
        artifacts: GenerationArtifacts,
        draft: NormalizedLessonDraft,
    ) -> list[str]:
        """Where the plan this attempt makes breaks the lesson document or the plan spec."""
        plan = self.session_plan_assembler.assemble(
            session=inputs.session,
            session_plan_content=self.session_plan_assembler.build_content(
                session=inputs.session, inputs=inputs, artifacts=artifacts, draft=draft
            ),
        )
        return [
            *violations(as_document(plan)),
            *unmet(plan, duration_minutes=inputs.session.duration_minutes),
        ]

    def _refined_generation_metrics(
        self,
        *,
        inputs: PreparedGenerationInputs,
        artifacts: GenerationArtifacts,
        attempts: int,
        lm_calls_before: int | None,
    ) -> JsonObject:
        """Return generation metrics for either artifact type (staged or monolithic)."""
        if isinstance(artifacts, LessonGenerationArtifacts):
            metrics = self._build_generation_metrics(
                session_subtopic=inputs.session.subtopic,
                artifacts=artifacts,
                lm_calls_before=lm_calls_before,
            )
            return {
                **asdict(metrics),
                "grounding_mode": inputs.grounding_mode,
                "refine_attempts": attempts,
                "planning_violations": [
                    asdict(violation) for violation in artifacts.planning_result.violations
                ],
                "assessment_item_count": len(artifacts.assessment_items),
            }
        total_llm_calls = None
        if self.status_logger is not None:
            total_llm_calls = max(self.status_logger.lm_call_count() - (lm_calls_before or 0), 0)
        return {
            "grounding_mode": inputs.grounding_mode,
            "generator": "monolithic_refine",
            "refine_attempts": attempts,
            "total_llm_calls": total_llm_calls,
            "objective_count": len(artifacts.lesson_plan_objectives),
            "assessment_item_count": len(artifacts.assessment_items),
        }
