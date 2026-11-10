from __future__ import annotations

import logging
from typing import cast

from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.status import (
    log_timestamp,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonCurriculumContext,
    TextbookRecordPayload,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    LessonPlanObjective,
    StepEvidencePlan,
    activities_of,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.session_plan_rules import (
    MAX_LESSON_OBJECTIVES,
)
from app.shared.json_types import JsonObject


def _normalize_semantic_key(value: str | None) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _record_type_lookup(textbook_records: list[TextbookRecordPayload]) -> dict[str, str]:
    return {
        record.record_id: record.record_type or ""
        for record in textbook_records
        if record.record_id
    }


def _as_list(value: object) -> list[object]:
    return cast(list[object], value) if isinstance(value, list) else []


def _as_strings(value: object) -> list[str]:
    return [str(item) for item in _as_list(value)]


class SemanticPlanValidator:
    def __init__(self, *, logger: logging.Logger) -> None:
        self._logger = logger

    def _index_objectives(
        self,
        *,
        lesson_plan_objectives: list[LessonPlanObjective],
        resolved_kcs: list[CandidateKC],
    ) -> tuple[dict[str, LessonPlanObjective], dict[str, CandidateKC]]:
        objective_by_id = {
            lesson_objective.lesson_objective_id: lesson_objective
            for lesson_objective in lesson_plan_objectives
        }
        # Positional pairing (objective[i] <-> resolved_kc[i]). The staged
        # pipeline guarantees equal counts, but the monolithic no-linkage model
        # can emit mismatched lists, so pair over the shorter one rather than
        # raising — collect_issues() must stay non-raising. Any unmatched
        # objective then surfaces a `missing_resolved_kc` issue downstream, and
        # collect_issues() reports the count mismatch itself.
        kc_by_objective_id = {
            lesson_objective.lesson_objective_id: resolved_kc
            for lesson_objective, resolved_kc in zip(
                lesson_plan_objectives,
                resolved_kcs,
                strict=False,
            )
        }
        return objective_by_id, kc_by_objective_id

    def _collect_objective_count_issues(
        self,
        *,
        lesson_plan_objectives: list[LessonPlanObjective],
    ) -> list[str]:
        if len(lesson_plan_objectives) <= MAX_LESSON_OBJECTIVES:
            return []
        # Refinable, actionable feedback: the monolithic no-linkage drafter can emit
        # more than the cap. Tell the next attempt exactly how to fix it (merge, not
        # truncate) so it reduces the count instead of the request hard-failing 422.
        return [
            "too_many_objectives: the plan defines "
            f"{len(lesson_plan_objectives)} core lesson objectives but at most "
            f"{MAX_LESSON_OBJECTIVES} are allowed. Merge the most closely related "
            "objectives (folding their KCs, evidence plans and core steps together) "
            f"so no more than {MAX_LESSON_OBJECTIVES} core lesson objectives remain."
        ]

    def _collect_duplicate_focus_issues(
        self,
        *,
        lesson_plan_objectives: list[LessonPlanObjective],
    ) -> list[str]:
        issues: list[str] = []
        seen_focuses: set[tuple[str, str, str, str]] = set()
        for lesson_objective in lesson_plan_objectives:
            focus_key = (
                _normalize_semantic_key(lesson_objective.curriculum_objective_id),
                _normalize_semantic_key(lesson_objective.kc_focus),
                _normalize_semantic_key(lesson_objective.source_form),
                _normalize_semantic_key(lesson_objective.target_form),
            )
            if focus_key in seen_focuses:
                issues.append(
                    "duplicate_kc_focus: lesson objectives repeat the same kc_focus/source-target "
                    f"signature for {lesson_objective.lesson_objective_id}"
                )
            seen_focuses.add(focus_key)
        return issues

    def _collect_evidence_alignment_issues(
        self,
        *,
        lesson_plan_objectives: list[LessonPlanObjective],
        step_evidence_by_objective: dict[str, StepEvidencePlan],
        kc_by_objective_id: dict[str, CandidateKC],
    ) -> tuple[list[str], dict[str, list[str]]]:
        issues: list[str] = []
        modeling_usage: dict[str, list[str]] = {}
        for lesson_objective in lesson_plan_objectives:
            evidence_plan = step_evidence_by_objective.get(lesson_objective.lesson_objective_id)
            if evidence_plan is None:
                issues.append(f"missing_evidence_plan: {lesson_objective.lesson_objective_id}")
                continue
            kc = kc_by_objective_id.get(lesson_objective.lesson_objective_id)
            if kc is None:
                issues.append(f"missing_resolved_kc: {lesson_objective.lesson_objective_id}")
                continue
            support_ids = set(kc.supporting_record_ids)
            selected_ids = set(evidence_plan.selected_record_ids)
            outside_support_ids = sorted(selected_ids - support_ids)
            if outside_support_ids:
                issues.append(
                    "mixed_direction_evidence: selected ids fall outside KC supporting_record_ids "
                    f"for {lesson_objective.lesson_objective_id}: {outside_support_ids}"
                )
            for record_id in evidence_plan.modeling_record_ids:
                modeling_usage.setdefault(record_id, []).append(
                    lesson_objective.lesson_objective_id
                )
        return issues, modeling_usage

    def _collect_reused_modeling_issues(
        self,
        *,
        modeling_usage: dict[str, list[str]],
        kc_by_objective_id: dict[str, CandidateKC],
        record_types: dict[str, str],
    ) -> list[str]:
        issues: list[str] = []
        for record_id, objective_ids in modeling_usage.items():
            if len(objective_ids) < 2:
                continue
            alternatives_exist = False
            for lesson_objective_id in objective_ids:
                kc = kc_by_objective_id[lesson_objective_id]
                alternative_ids = [
                    support_id
                    for support_id in kc.supporting_record_ids
                    if support_id != record_id
                    and record_types.get(support_id) in {"worked_example", "exercise_item"}
                ]
                if alternative_ids:
                    alternatives_exist = True
                    break
            if alternatives_exist:
                issues.append(
                    "reused_modeling_record: modeling record reused across distinct KCs despite "
                    f"available alternatives: {record_id} -> {objective_ids}"
                )
        return issues

    def _collect_evaluation_coverage_issues(
        self,
        *,
        global_steps: dict[str, JsonObject],
        objective_by_id: dict[str, LessonPlanObjective],
    ) -> tuple[list[str], JsonObject]:
        issues: list[str] = []
        evaluation_step: JsonObject = global_steps.get("evaluation_step") or {}
        evaluation_blocks: list[JsonObject] = []
        for raw_block in _as_list(evaluation_step.get("blocks")):
            if not isinstance(raw_block, dict):
                continue
            block_payload = cast(JsonObject, raw_block)
            if block_payload.get("type") == "practice":
                evaluation_blocks.append(block_payload)
        covered_objectives = {
            str(block.get("lesson_objective_id") or "").strip()
            for block in evaluation_blocks
            if str(block.get("lesson_objective_id") or "").strip()
        }
        missing_coverage = sorted(set(objective_by_id) - covered_objectives)
        if missing_coverage:
            issues.append(
                "missing_evaluation_coverage: evaluation does not cover "
                + ", ".join(missing_coverage)
            )
        return issues, evaluation_step

    def _collect_ungrounded_material_issues(
        self,
        *,
        curriculum_context: LessonCurriculumContext,
        evaluation_step: JsonObject,
    ) -> list[str]:
        issues: list[str] = []
        allowed_materials_text = " ".join(curriculum_context.instructional_materials).lower()
        evaluation_text = " ".join(
            str(part or "")
            for part in [
                evaluation_step.get("content"),
                *activities_of(evaluation_step, "teacher"),
                *activities_of(evaluation_step, "student"),
            ]
        ).lower()
        for disallowed_term in (
            "worksheet",
            "answer key",
            "attached",
            "response cards",
            "response card",
        ):
            if disallowed_term in evaluation_text and disallowed_term not in allowed_materials_text:
                issues.append(
                    f"ungrounded_evaluation_material: evaluation mentions '{disallowed_term}'"
                )
        return issues

    def collect_issues(
        self,
        *,
        lesson_plan_objectives: list[LessonPlanObjective],
        resolved_kcs: list[CandidateKC],
        step_evidence_by_objective: dict[str, StepEvidencePlan],
        global_steps: dict[str, JsonObject],
        textbook_records: list[TextbookRecordPayload],
        curriculum_context: LessonCurriculumContext,
    ) -> list[str]:
        issues: list[str] = []
        issues.extend(
            self._collect_objective_count_issues(
                lesson_plan_objectives=lesson_plan_objectives,
            )
        )
        if len(lesson_plan_objectives) != len(resolved_kcs):
            issues.append(
                "objective_kc_count_mismatch: "
                f"{len(lesson_plan_objectives)} lesson objectives vs "
                f"{len(resolved_kcs)} resolved KCs (expected one KC per objective)"
            )
        record_types = _record_type_lookup(textbook_records)
        objective_by_id, kc_by_objective_id = self._index_objectives(
            lesson_plan_objectives=lesson_plan_objectives,
            resolved_kcs=resolved_kcs,
        )
        issues.extend(
            self._collect_duplicate_focus_issues(lesson_plan_objectives=lesson_plan_objectives)
        )
        evidence_issues, modeling_usage = self._collect_evidence_alignment_issues(
            lesson_plan_objectives=lesson_plan_objectives,
            step_evidence_by_objective=step_evidence_by_objective,
            kc_by_objective_id=kc_by_objective_id,
        )
        issues.extend(evidence_issues)
        issues.extend(
            self._collect_reused_modeling_issues(
                modeling_usage=modeling_usage,
                kc_by_objective_id=kc_by_objective_id,
                record_types=record_types,
            )
        )
        evaluation_issues, evaluation_step = self._collect_evaluation_coverage_issues(
            global_steps=global_steps,
            objective_by_id=objective_by_id,
        )
        issues.extend(evaluation_issues)
        issues.extend(
            self._collect_ungrounded_material_issues(
                curriculum_context=curriculum_context,
                evaluation_step=evaluation_step,
            )
        )
        return issues

    def validate(
        self,
        *,
        session_id: str,
        lesson_plan_objectives: list[LessonPlanObjective],
        resolved_kcs: list[CandidateKC],
        step_evidence_by_objective: dict[str, StepEvidencePlan],
        global_steps: dict[str, JsonObject],
        textbook_records: list[TextbookRecordPayload],
        curriculum_context: LessonCurriculumContext,
    ) -> list[str]:
        issues = self.collect_issues(
            lesson_plan_objectives=lesson_plan_objectives,
            resolved_kcs=resolved_kcs,
            step_evidence_by_objective=step_evidence_by_objective,
            global_steps=global_steps,
            textbook_records=textbook_records,
            curriculum_context=curriculum_context,
        )
        if issues:
            self._logger.warning(
                "%s lesson-plan semantic validation failed session_id=%s checks=%s",
                log_timestamp(),
                session_id,
                issues,
            )
            raise ValueError("lesson_plan semantic validation failed: " + "; ".join(issues))
        return issues
