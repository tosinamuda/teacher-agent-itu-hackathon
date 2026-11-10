"""Adapt authoritative curated planning into the pipeline's KCPlanningResult.

`build_curated_planning` produces evidence/KCs/assessments keyed by atomic
objective id (`ao_id`). The drafting stage (`CachedLessonDraftingModule`) consumes
a `KCPlanningResult` whose `lesson_structure` re-keys objectives to `lopNN` ids
(via `build_lesson_structure_from_kcs`). This adapter bridges the two so the
curated (manual_linkage) path reuses the EXISTING drafting stage unchanged:

  curated_objectives -> build_curated_planning -> [this adapter] -> KCPlanningResult
                                                                 -> draft_builder

The LLM planning stage (KC extraction + evidence selection) is skipped entirely;
the deterministic curated structure is authoritative.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    build_lesson_structure_from_kcs,
)
from app.shared.json_types import JsonObject

from .curated_planning import CuratedPlanningArtifacts
from .types import KCPlanningResult, derive_scope_keys


def curated_artifacts_to_kc_planning_result(
    artifacts: CuratedPlanningArtifacts,
    *,
    scope_context: JsonObject,
    curriculum_objectives: Sequence[Mapping[str, object]],
) -> KCPlanningResult:
    """Build a KCPlanningResult from curated planning artifacts (no LLM)."""
    topic_key, subtopic_id = derive_scope_keys(scope_context)
    lesson_structure = build_lesson_structure_from_kcs(
        artifacts.resolved_kcs,
        curriculum_objectives=curriculum_objectives,
    )

    # Re-key curated evidence (ao_id) -> the lopNN ids the lesson_structure uses.
    # curated_planning inserts step_evidence_plans in resolved_kcs order, so the
    # dict values align positionally with lesson_structure.objectives.
    ao_to_lesson_objective: dict[str, str] = {}
    step_evidence_plans = {}
    for objective, (ao_id, plan) in zip(
        lesson_structure.objectives,
        artifacts.step_evidence_plans.items(),
        strict=True,
    ):
        lesson_objective_id = objective.lesson_objective_id
        ao_to_lesson_objective[ao_id] = lesson_objective_id
        step_evidence_plans[lesson_objective_id] = plan.model_copy(
            update={"lesson_objective_id": lesson_objective_id}
        )

    assessment_items = {}
    assessment_items_by_atomic_objective: dict[str, list] = {}
    for ao_id, item in artifacts.assessment_items.items():
        mapped_objective_id = ao_to_lesson_objective.get(ao_id)
        if mapped_objective_id is None:
            continue
        rekeyed = item.model_copy(update={"lesson_objective_id": mapped_objective_id})
        assessment_items[mapped_objective_id] = rekeyed
        assessment_items_by_atomic_objective[ao_id] = [rekeyed]

    return KCPlanningResult(
        subtopic_id=subtopic_id,
        topic_key=topic_key,
        atomic_objectives=artifacts.atomic_objectives,
        kc_plans=artifacts.kc_plans,
        step_evidence_plans=step_evidence_plans,
        assessment_items_by_atomic_objective=assessment_items_by_atomic_objective,
        assessment_items=assessment_items,
        lesson_structure=lesson_structure,
        combined_kc_plan=artifacts.combined_kc_plan,
        resolved_kcs=artifacts.resolved_kcs,
        violations_by_atomic_objective={},
        violations=[],
        from_cache=False,
        planning_duration_ms=0,
        llm_calls_planning=0,
    )
