"""Build + validate the per-step evidence plan.

Three concerns:
- ``build_supported_evidence_plan`` picks one concept + (for procedure/
  representation KCs) one modeling + one practice record from the KC's support
  inventory, plus a visual.
- ``ensure_evidence_matches_objective`` validates a step's evidence plan: every
  selected id is known + within the KC's support + has the right record_type
  for its group + matches the KC's evidence policy.
- ``summarize_evidence_bundle`` renders an evidence bundle as a small DTO for
  downstream logging.

Imports from ``textbook_support`` for the support inventory + constants;
imports from the model_io helpers transitively (for the record-object dict).
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import textbook_record_id
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.textbook_support import (
    kc_support_inventory,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    LessonPlanObjective,
    StepEvidencePlan,
)
from app.shared.json_types import JsonObject


def build_supported_evidence_plan(
    *,
    lesson_objective: LessonPlanObjective,
    candidate_kc: CandidateKC,
    textbook_records: Sequence[JsonObject],
) -> StepEvidencePlan | None:
    """Pick the evidence records for one step (concept-only or concept+modeling+practice)."""
    inventory = kc_support_inventory(candidate_kc, textbook_records)
    concept_record_ids = inventory["concept_ids"][:1]
    visual_record_ids = inventory["visual_ids"][:1]

    if lesson_objective.kc_type == "concept":
        return _build_concept_only_plan(
            lesson_objective=lesson_objective,
            concept_record_ids=concept_record_ids,
            visual_record_ids=visual_record_ids,
        )

    return _build_full_evidence_plan(
        lesson_objective=lesson_objective,
        concept_record_ids=concept_record_ids,
        visual_record_ids=visual_record_ids,
        modeling_candidates=inventory["worked_example_ids"] or inventory["exercise_item_ids"],
        practice_candidates=inventory["exercise_block_ids"] or inventory["exercise_item_ids"],
    )


def _build_concept_only_plan(
    *,
    lesson_objective: LessonPlanObjective,
    concept_record_ids: list[str],
    visual_record_ids: list[str],
) -> StepEvidencePlan | None:
    """Build the concept-only plan; ``None`` if the concept ids are empty."""
    if not concept_record_ids:
        return None
    selected_record_ids = list(dict.fromkeys([*concept_record_ids, *visual_record_ids]))
    return StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": lesson_objective.lesson_objective_id,
            "selected_record_ids": selected_record_ids,
            "concept_record_ids": concept_record_ids,
            "visual_record_ids": visual_record_ids,
        }
    )


def _build_full_evidence_plan(
    *,
    lesson_objective: LessonPlanObjective,
    concept_record_ids: list[str],
    visual_record_ids: list[str],
    modeling_candidates: list[str],
    practice_candidates: list[str],
) -> StepEvidencePlan | None:
    """Build the concept+modeling+practice plan; ``None`` if any required group is empty."""
    if not concept_record_ids or not modeling_candidates or not practice_candidates:
        return None

    modeling_record_ids = modeling_candidates[:1]
    remaining_practice_ids = [
        record_id for record_id in practice_candidates if record_id not in modeling_record_ids
    ]
    practice_record_ids = (remaining_practice_ids or practice_candidates)[:1]
    selected_record_ids = list(
        dict.fromkeys(
            [
                *concept_record_ids,
                *modeling_record_ids,
                *practice_record_ids,
                *visual_record_ids,
            ]
        )
    )
    return StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": lesson_objective.lesson_objective_id,
            "selected_record_ids": selected_record_ids,
            "concept_record_ids": concept_record_ids,
            "modeling_record_ids": modeling_record_ids,
            "practice_record_ids": practice_record_ids,
            "visual_record_ids": [
                record_id for record_id in visual_record_ids if record_id in selected_record_ids
            ],
        }
    )


# ===== Evidence plan assertions =====


def ensure_evidence_matches_objective(
    evidence_plan: StepEvidencePlan,
    *,
    lesson_objective: LessonPlanObjective,
    textbook_records: list[JsonObject],
    candidate_kc: CandidateKC | None = None,
) -> None:
    """Validate a step's evidence plan against the source records + the KC's evidence policy."""
    record_map = _record_map_by_id(textbook_records)
    valid_ids = set(record_map)
    _assert_known_selected_records(evidence_plan, valid_ids=valid_ids)

    support_ids = set(candidate_kc.supporting_record_ids) if candidate_kc is not None else valid_ids
    _assert_selected_records_within_support(evidence_plan, support_ids=support_ids)
    _assert_evidence_record_type_groups(evidence_plan, record_map=record_map)

    worked_example_support_ids, exercise_item_support_ids = _modeling_support_candidates(
        support_ids=support_ids,
        record_map=record_map,
    )
    _assert_evidence_policy_for_kc_type(
        evidence_plan=evidence_plan,
        kc_type=lesson_objective.kc_type,
        worked_example_support_ids=worked_example_support_ids,
        exercise_item_support_ids=exercise_item_support_ids,
    )


def summarize_evidence_bundle(
    *,
    lesson_objective_id: str,
    evidence_bundle: list[JsonObject],
) -> JsonObject:
    """Render an evidence bundle as a small DTO (title + section_ref + record_type + asset_refs)."""
    return {
        "lesson_objective_id": lesson_objective_id,
        "records": [
            {
                "title": item.get("title"),
                "section_ref": item.get("section_ref"),
                "record_type": item.get("record_type"),
                "asset_refs": item.get("asset_refs"),
            }
            for item in evidence_bundle
        ],
    }


# ===== Private assertion helpers =====


def _record_map_by_id(textbook_records: list[JsonObject]) -> dict[str, JsonObject]:
    """Index ``textbook_records`` by their record id (skips records with no id)."""
    return {
        textbook_record_id(record): record
        for record in textbook_records
        if textbook_record_id(record)
    }


def _assert_known_selected_records(
    evidence_plan: StepEvidencePlan,
    *,
    valid_ids: set[str],
) -> None:
    """Every selected id must be a known textbook record id."""
    for record_id in evidence_plan.selected_record_ids:
        if record_id not in valid_ids:
            raise ValueError(f"step evidence plan references unknown record_id: {record_id}")


def _assert_selected_records_within_support(
    evidence_plan: StepEvidencePlan,
    *,
    support_ids: set[str],
) -> None:
    """Every selected id must stay within the KC's stated supporting_record_ids."""
    invalid_support_ids = [
        record_id for record_id in evidence_plan.selected_record_ids if record_id not in support_ids
    ]
    if invalid_support_ids:
        raise ValueError(
            "step evidence plan selected_record_ids must stay within KC supporting_record_ids: "
            f"{invalid_support_ids}"
        )


def _record_type_for(record_map: dict[str, JsonObject], record_id: str) -> str:
    """Return ``record_map[record_id].record_type`` (stripped) or ``""`` if absent."""
    return str(record_map.get(record_id, {}).get("record_type") or "").strip()


def _assert_record_types(
    *,
    record_map: dict[str, JsonObject],
    group_name: str,
    record_ids: list[str],
    allowed_types: set[str],
) -> None:
    """Every record in ``record_ids`` must have a ``record_type`` in ``allowed_types``."""
    for record_id in record_ids:
        record_type = _record_type_for(record_map, record_id)
        if record_type not in allowed_types:
            raise ValueError(
                f"{group_name} must use record types {sorted(allowed_types)}: {record_id}"
            )


def _assert_evidence_record_type_groups(
    evidence_plan: StepEvidencePlan,
    *,
    record_map: dict[str, JsonObject],
) -> None:
    """concept_record_ids + practice_record_ids must each use the right record types."""
    _assert_record_types(
        record_map=record_map,
        group_name="concept_record_ids",
        record_ids=evidence_plan.concept_record_ids,
        allowed_types={"definition", "exposition", "summary", "note"},
    )
    _assert_record_types(
        record_map=record_map,
        group_name="practice_record_ids",
        record_ids=evidence_plan.practice_record_ids,
        allowed_types={"exercise_block", "exercise_item"},
    )


def _modeling_support_candidates(
    *,
    support_ids: set[str],
    record_map: dict[str, JsonObject],
) -> tuple[list[str], list[str]]:
    """Partition the KC's support set into ``(worked_example_ids, exercise_item_ids)``."""
    support_record_types = {
        record_id: _record_type_for(record_map, record_id)
        for record_id in support_ids
        if record_id in record_map
    }
    worked_example_support_ids = [
        record_id
        for record_id, record_type in support_record_types.items()
        if record_type == "worked_example"
    ]
    exercise_item_support_ids = [
        record_id
        for record_id, record_type in support_record_types.items()
        if record_type == "exercise_item"
    ]
    return worked_example_support_ids, exercise_item_support_ids


def _assert_has_required_groups(evidence_plan: StepEvidencePlan, *, kc_type: str) -> None:
    """concept_record_ids always; procedure/representation also need modeling + practice."""
    if not evidence_plan.concept_record_ids:
        raise ValueError(f"{kc_type} lesson objectives require concept_record_ids")
    if kc_type in {"procedure", "representation"}:
        if not evidence_plan.modeling_record_ids:
            raise ValueError(f"{kc_type} lesson objectives require modeling_record_ids")
        if not evidence_plan.practice_record_ids:
            raise ValueError(f"{kc_type} lesson objectives require practice_record_ids")


def _assert_modeling_ids_from_support(
    *,
    kc_type: str,
    evidence_plan: StepEvidencePlan,
    worked_example_support_ids: list[str],
    exercise_item_support_ids: list[str],
) -> None:
    """modeling_record_ids must come from worked-example support (or exercise-item fallback)."""
    if worked_example_support_ids:
        invalid_modeling_ids = [
            record_id
            for record_id in evidence_plan.modeling_record_ids
            if record_id not in worked_example_support_ids
        ]
        if invalid_modeling_ids:
            raise ValueError(
                f"{kc_type} modeling_record_ids must come from worked_example support: "
                f"{invalid_modeling_ids}"
            )
        return
    if exercise_item_support_ids:
        invalid_modeling_ids = [
            record_id
            for record_id in evidence_plan.modeling_record_ids
            if record_id not in exercise_item_support_ids
        ]
        if invalid_modeling_ids:
            raise ValueError(
                f"{kc_type} modeling_record_ids must come from exercise_item support "
                f"when no worked_example exists: {invalid_modeling_ids}"
            )
        return
    raise ValueError(f"{kc_type} lesson objectives require modeling support in KC records")


def _assert_evidence_policy_for_kc_type(
    *,
    evidence_plan: StepEvidencePlan,
    kc_type: str,
    worked_example_support_ids: list[str],
    exercise_item_support_ids: list[str],
) -> None:
    """Concept KCs reject modeling ids; procedure/representation require them from support."""
    _assert_has_required_groups(evidence_plan, kc_type=kc_type)

    if kc_type == "concept":
        if evidence_plan.modeling_record_ids:
            raise ValueError("concept lesson objectives must not define modeling_record_ids")
        return

    if kc_type in {"procedure", "representation"}:
        _assert_modeling_ids_from_support(
            kc_type=kc_type,
            evidence_plan=evidence_plan,
            worked_example_support_ids=worked_example_support_ids,
            exercise_item_support_ids=exercise_item_support_ids,
        )
