"""Experiment-local scored generation (does NOT modify production code).

`ScoredLessonGenerationService` subclasses the real `LessonGenerationService` and
reuses ALL its components (generation_program, session_plan_assembler,
semantic_validator, diagnostic_writer). It adds `generate_scored()`, which runs
the same orchestration as the production `generate()` but:

  * calls `semantic_validator.collect_issues()` (non-raising) instead of
    `validate()` (raising), so a failing plan is returned WITH its violations
    rather than crashing — required to score strategies; and
  * returns a `ScoredGeneration` (plan + violations + latency + metadata) instead
    of only the plan.

Production `generate()` is untouched: this is a faithful copy of its body kept in
the experiment package, per the experiment-before-prod decision. If this body
drifts from production it should be re-synced (the parent is ~lines 129-229 of
runtime/service.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter

from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.service import (
    LessonGenerationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    PreparedGenerationInputs,
    build_run_metadata,
    prepare_generation_inputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.generator import (
    LessonGenerationArtifacts,
)
from app.shared.json_types import JsonObject

from .monolithic_signature import MonolithicArtifacts


@dataclass
class ScoredGeneration:
    """One generation attempt with its semantic violations and cost."""

    session_plan: JsonObject | None
    violations: list[str]
    latency_ms: float
    llm_calls: int | None
    run_metadata: JsonObject = field(default_factory=dict)
    error: str | None = None

    @property
    def semantic_valid(self) -> bool:
        return self.error is None and not self.violations


class ScoredLessonGenerationService(LessonGenerationService):
    """Production generation, but scored (non-raising) for the bake-off."""

    def _prepare_inputs(
        self,
        *,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        requested_strategy: str | None,
    ) -> PreparedGenerationInputs:
        """Build generation inputs. Overridden by the cold-start backend to inject
        a synthetic curriculum-derived record when no textbook records exist."""
        return prepare_generation_inputs(
            session_context=session_context,
            curriculum_context=curriculum_context,
            reference_context=reference_context,
            requested_strategy=requested_strategy,
            default_strategy=self.default_evidence_selection_strategy,
        )

    def _generation_program_kwargs(
        self,
        inputs: PreparedGenerationInputs,
        prior_violations: list[str] | None,
    ) -> dict[str, object]:
        """Kwargs for the generation program. The staged (production) program does
        not accept a feedback channel; the monolithic backend overrides this to
        forward `prior_violations` (the refine self-correction signal)."""
        return {"request": inputs}

    async def generate_scored(
        self,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        evidence_selection_strategy: str | None = None,
        prior_violations: list[str] | None = None,
    ) -> ScoredGeneration:
        started_at = perf_counter()
        lm_calls_before = self.status_logger.lm_call_count() if self.status_logger else None

        try:
            inputs = self._prepare_inputs(
                session_context=session_context,
                curriculum_context=curriculum_context,
                reference_context=reference_context,
                requested_strategy=evidence_selection_strategy,
            )
            artifacts = await self._run_generation_stage(
                stage_name="lesson_plan_generation",
                runner=self.generation_program,
                strategy=inputs.evidence_selection_strategy,
                record_count=len(inputs.textbook_records),
                objective_count=len(inputs.curriculum_objectives),
                **self._generation_program_kwargs(inputs, prior_violations),
            )
            # Accept the staged artifacts OR the monolithic backend's duck-typed
            # twin (both expose the same attribute surface the scorer reads).
            if not isinstance(artifacts, (LessonGenerationArtifacts, MonolithicArtifacts)):
                raise ValueError("lesson_generation_program returned unsupported payload")

            normalized_draft = self.session_plan_assembler.normalize_draft(
                artifacts=artifacts,
                inputs=inputs,
            )
            # NON-RAISING: the only behavioural change vs production generate().
            violations = self.semantic_validator.collect_issues(
                lesson_plan_objectives=artifacts.lesson_plan_objectives,
                resolved_kcs=artifacts.resolved_kcs,
                step_evidence_by_objective=artifacts.step_evidence_plans,
                global_steps=normalized_draft.global_steps,
                textbook_records=inputs.textbook_records,
                curriculum_context=inputs.curriculum,
            )
            session_plan_content = self.session_plan_assembler.build_content(
                session=inputs.session,
                inputs=inputs,
                artifacts=artifacts,
                draft=normalized_draft,
            )
            session_plan = self.session_plan_assembler.assemble(
                session=inputs.session,
                session_plan_content=session_plan_content,
            )
            run_metadata = build_run_metadata(
                model_name=self.model_name,
                generated_at=datetime.now(timezone.utc).isoformat(),
                inputs=inputs,
                final_writer_mode=self.final_writer_mode,
                dspy_status_logging=self.status_logger is not None,
            )
        except Exception as exc:  # noqa: BLE001 - bake-off records failures, never aborts
            latency_ms = round((perf_counter() - started_at) * 1000, 1)
            return ScoredGeneration(
                session_plan=None,
                violations=[f"generation_error: {type(exc).__name__}: {exc}"],
                latency_ms=latency_ms,
                llm_calls=self._llm_calls_since(lm_calls_before),
                error=str(exc),
            )

        latency_ms = round((perf_counter() - started_at) * 1000, 1)
        return ScoredGeneration(
            session_plan=session_plan,
            violations=violations,
            latency_ms=latency_ms,
            llm_calls=self._llm_calls_since(lm_calls_before),
            run_metadata=run_metadata,
        )

    def _llm_calls_since(self, lm_calls_before: int | None) -> int | None:
        if self.status_logger is None:
            return None
        return max(self.status_logger.lm_call_count() - (lm_calls_before or 0), 0)
