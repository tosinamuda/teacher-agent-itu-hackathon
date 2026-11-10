"""Folding a lesson's curated objectives down to the cap on core objectives."""

from __future__ import annotations

from collections.abc import Callable, Mapping

from ...validation.session_plan_rules import MAX_LESSON_OBJECTIVES
from .curated_objectives import CuratedObjective


def _merge_curated_objectives(
    objectives: list[CuratedObjective], *, objective_text: str | None = None
) -> CuratedObjective:
    """Fold several curated objectives into one.

    Evidence record ids are unioned (order-stable, de-duplicated) so the merged
    objective keeps every curated record; the lowest-order objective's identity is
    kept as the stable id, and the first available curated assessment is reused.
    It reads ``objective_text`` when given, else the distinct objective texts joined.
    kc_type then follows the merged evidence shape (procedure if any member carried
    a worked example).
    """
    if len(objectives) == 1:
        return objectives[0]
    ordered = sorted(objectives, key=lambda objective: objective.ao_order)
    primary = ordered[0]

    def _union(select: Callable[[CuratedObjective], list[str]]) -> list[str]:
        merged: list[str] = []
        seen: set[str] = set()
        for objective in ordered:
            for record_id in select(objective):
                if record_id and record_id not in seen:
                    seen.add(record_id)
                    merged.append(record_id)
        return merged

    texts: list[str] = []
    for objective in ordered:
        text = objective.objective_text.strip()
        if text and text not in texts:
            texts.append(text)

    assessment = next((objective.assessment for objective in ordered if objective.assessment), None)
    return CuratedObjective(
        ao_id=primary.ao_id,
        ao_order=primary.ao_order,
        curriculum_objective_id=primary.curriculum_objective_id,
        objective_text=objective_text or "; ".join(texts),
        bloom_level=primary.bloom_level,
        concept_record_ids=_union(lambda objective: objective.concept_record_ids),
        modeling_record_ids=_union(lambda objective: objective.modeling_record_ids),
        practice_record_ids=_union(lambda objective: objective.practice_record_ids),
        assessment=assessment,
    )


def compress_curated_objectives(
    objectives: list[CuratedObjective],
    *,
    curriculum_texts: Mapping[str, str],
    max_objectives: int = MAX_LESSON_OBJECTIVES,
) -> list[CuratedObjective]:
    """Deterministically fold curated objectives down to the lesson cap.

    A single lesson may define at most ``max_objectives`` core objectives, but an
    expert linkage can curate more atomic objectives than that (e.g. several
    "apply X in everyday life" sub-objectives under one performance objective).
    Rather than letting the strict validator hard-fail the request with a 422,
    consolidate the finest decomposition back toward the authoritative
    curriculum-objective level: repeatedly collapse the largest
    same-curriculum-objective group into one, worded as that curriculum objective in
    ``curriculum_texts``, until the count fits. The curation's evidence is preserved.
    This is the curated-path counterpart to ``compress_knowledge_components`` on the
    LLM planning path.
    """
    if len(objectives) <= max_objectives:
        return objectives
    groups = _by_curriculum_objective(objectives)
    _collapse_largest_groups(groups, curriculum_texts, max_objectives)
    merged = [objective for members in groups.values() for objective in members]
    merged.sort(key=lambda objective: objective.ao_order)
    return _merge_adjacent(merged, max_objectives)


def _by_curriculum_objective(
    objectives: list[CuratedObjective],
) -> dict[str, list[CuratedObjective]]:
    """The objectives grouped under their curriculum objective, groups in first-seen order."""
    groups: dict[str, list[CuratedObjective]] = {}
    for objective in objectives:
        groups.setdefault(objective.curriculum_objective_id or objective.ao_id, []).append(
            objective
        )
    return groups


def _collapse_largest_groups(
    groups: dict[str, list[CuratedObjective]],
    curriculum_texts: Mapping[str, str],
    max_objectives: int,
) -> None:
    """Collapse the largest multi-member group into one, largest first, until in cap."""
    while sum(len(members) for members in groups.values()) > max_objectives:
        candidate = max(
            (key for key, members in groups.items() if len(members) > 1),
            key=lambda key: len(groups[key]),
            default=None,
        )
        if candidate is None:
            return
        groups[candidate] = [
            _merge_curated_objectives(
                groups[candidate], objective_text=curriculum_texts.get(candidate)
            )
        ]


def _merge_adjacent(merged: list[CuratedObjective], max_objectives: int) -> list[CuratedObjective]:
    """Merge neighbours by order while there are more curriculum objectives than the cap.

    A last resort that crosses curriculum-objective boundaries, so the request can still
    produce a capped plan.
    """
    while len(merged) > max_objectives:
        merged[0:2] = [_merge_curated_objectives(merged[0:2])]
    return merged
