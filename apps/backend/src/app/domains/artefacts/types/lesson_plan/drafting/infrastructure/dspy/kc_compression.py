"""KC (Knowledge Component) compression + the derived ``LessonStructure``.

When the planner emits more KCs than the lesson budget allows, this module
merges *adjacent* compatible KCs (same curriculum objective, mergeable types,
or overlapping support records) until the count fits ``max_kcs``. The merged
result then drives ``build_lesson_structure_from_kcs`` which assigns lesson-
objective ids + core-step blueprints.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.model_io import (
    to_record_object,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    CoreStepBlueprint,
    LessonPlanObjective,
    required_block_types_for_kc,
)


@dataclass(frozen=True)
class LessonStructure:
    """Derived per-lesson IDs + blueprints assigned from the compressed KC set."""

    objectives: list[LessonPlanObjective]
    blueprints: list[CoreStepBlueprint]
    objectives_by_id: dict[str, LessonPlanObjective]
    kcs_by_objective_id: dict[str, CandidateKC]


def compress_knowledge_components(
    candidate_kcs: list[CandidateKC],
    *,
    max_kcs: int = 4,
) -> list[CandidateKC]:
    """Merge adjacent compatible KCs until the set is no longer than ``max_kcs``."""
    compressed = list(candidate_kcs)
    if not compressed:
        raise ValueError("kc_plan produced no candidate_kcs")

    merge_index = 1
    while len(compressed) > max_kcs:
        merged = False
        for index in range(len(compressed) - 1):
            if not can_merge_adjacent_kcs(compressed[index], compressed[index + 1]):
                continue
            merged_kc = merge_adjacent_kcs(
                compressed[index],
                compressed[index + 1],
                merged_index=merge_index,
            )
            compressed = [*compressed[:index], merged_kc, *compressed[index + 2 :]]
            merge_index += 1
            merged = True
            break
        if merged:
            continue
        merged_kc = merge_adjacent_kcs(
            compressed[-2],
            compressed[-1],
            merged_index=merge_index,
        )
        compressed = [*compressed[:-2], merged_kc]
        merge_index += 1

    return compressed


def can_merge_adjacent_kcs(first: CandidateKC, second: CandidateKC) -> bool:
    """Whether two adjacent KCs can be merged (same curriculum objective + compatible types)."""
    if first.curriculum_objective_id != second.curriculum_objective_id:
        return False

    pair = {first.kc_type, second.kc_type}
    if first.kc_type == second.kc_type:
        return True
    if pair in ({"concept", "representation"}, {"procedure", "representation"}):
        return True

    return bool(set(first.supporting_record_ids) & set(second.supporting_record_ids))


def merge_adjacent_kcs(
    first: CandidateKC, second: CandidateKC, *, merged_index: int
) -> CandidateKC:
    """Merge two adjacent KCs field-by-field per the merge policy."""
    return CandidateKC.model_validate(
        {
            "kc_id": f"kc{merged_index:02d}",
            "kc_type": _merge_kc_type(first, second),
            "objective_text": _merge_appended_text(first.objective_text, second.objective_text),
            "curriculum_objective_id": first.curriculum_objective_id,
            "kc_focus": _merge_appended_text(first.kc_focus, second.kc_focus),
            "source_form": _merge_form(first.source_form, second.source_form),
            "target_form": _merge_form(first.target_form, second.target_form),
            "supporting_record_ids": _merge_dedup_ids(
                first.supporting_record_ids, second.supporting_record_ids
            ),
            "ordering_notes": _merge_joined_notes(first.ordering_notes, second.ordering_notes),
        }
    )


def _merge_kc_type(first: CandidateKC, second: CandidateKC) -> str:
    """Pick the merged ``kc_type``: representation downgrades to its companion, else first wins."""
    pair = {first.kc_type, second.kc_type}
    if pair == {"procedure", "representation"}:
        return "procedure"
    if pair == {"concept", "representation"}:
        return "concept"
    return first.kc_type


def _merge_appended_text(first: str, second: str) -> str:
    """Append ``second`` after ``; `` only if it's non-empty and not already a substring."""
    base = first.strip()
    extra = second.strip()
    if extra and extra.lower() not in base.lower():
        return f"{base}; {extra}"
    return base


def _merge_dedup_ids(first: list[str], second: list[str]) -> list[str]:
    """Preserve first-occurrence order across both id lists, dropping blanks + duplicates."""
    merged: list[str] = []
    for record_id in [*first, *second]:
        if record_id and record_id not in merged:
            merged.append(record_id)
    return merged


def _merge_joined_notes(first: str | None, second: str | None) -> str | None:
    """Join non-empty stripped notes with ``; ``; ``None`` if both are empty."""
    joined = "; ".join(note for note in [first, second] if isinstance(note, str) and note.strip())
    return joined or None


def _merge_form(first: str | None, second: str | None) -> str | None:
    """Keep the form only when both sides agree (stripped equal); else ``None``."""
    return first if (first or "").strip() == (second or "").strip() else None


def build_lesson_structure_from_kcs(
    candidate_kcs: list[CandidateKC],
    *,
    curriculum_objectives: Sequence[Mapping[str, object]],
) -> LessonStructure:
    """Assign lesson-objective ids + core-step blueprints over the compressed KC set."""
    curriculum_by_id = {
        str(item["curriculum_objective_id"]): to_record_object(item)
        for item in curriculum_objectives
        if item.get("curriculum_objective_id")
    }

    objectives: list[LessonPlanObjective] = []
    blueprints: list[CoreStepBlueprint] = []
    kcs_by_objective_id: dict[str, CandidateKC] = {}
    for index, kc in enumerate(candidate_kcs, start=1):
        curriculum_objective = curriculum_by_id.get(kc.curriculum_objective_id)
        if curriculum_objective is None:
            raise ValueError(
                f"kc_plan references unknown curriculum objective: {kc.curriculum_objective_id}"
            )
        lesson_objective_id = f"lop{index:02d}"
        objectives.append(
            LessonPlanObjective.model_validate(
                {
                    "lesson_objective_id": lesson_objective_id,
                    "objective_text": kc.objective_text,
                    "objective_order": index,
                    "curriculum_objective_id": kc.curriculum_objective_id,
                    "curriculum_objective_text": curriculum_objective["objective_text"],
                    "kc_type": kc.kc_type,
                    "kc_focus": kc.kc_focus,
                    "source_form": kc.source_form,
                    "target_form": kc.target_form,
                }
            )
        )
        blueprints.append(
            CoreStepBlueprint.model_validate(
                {
                    "step_id": f"step{index:02d}",
                    "lesson_objective_id": lesson_objective_id,
                    "kc_type": kc.kc_type,
                    "required_block_types": required_block_types_for_kc(kc.kc_type),
                }
            )
        )
        kcs_by_objective_id[lesson_objective_id] = kc

    return LessonStructure(
        objectives=objectives,
        blueprints=blueprints,
        objectives_by_id={item.lesson_objective_id: item for item in objectives},
        kcs_by_objective_id=kcs_by_objective_id,
    )
