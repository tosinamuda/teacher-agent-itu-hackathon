"""Shared metrics + predicates over evaluation ratings.

Used by both the statistics reads and the dataset export, so they live here rather
than in either service.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from app.domains.evaluation.infrastructure.models import EvaluationRating


def mean_score(scores: list[float]) -> float | None:
    return round(sum(scores) / len(scores), 3) if scores else None


def _section_score(value: object) -> float | None:
    """The numeric ``section_score`` of one pack's per-section scores, or None."""
    if not isinstance(value, Mapping):
        return None
    score = cast("Mapping[str, object]", value).get("section_score")
    if isinstance(score, bool) or not isinstance(score, int | float):
        return None
    return float(score)


def h2_pack_section_means(rating: EvaluationRating) -> tuple[float | None, float | None]:
    """Mean section score for the base (P0) and candidate (P1) packs of one H2 rating.

    Reads the nested per-section shape
    ``{section_id: {"candidate": {... "section_score"}, "base": {...} | None}}``.
    Legacy flat rows are candidate-only, so their base mean is ``None``. Returns
    ``(p0_base_mean, p1_candidate_mean)``; either side is ``None`` when that pack has
    no scored sections (so a paired P0-vs-P1 comparison can skip it).
    """
    sections = rating.section_scores or {}
    base_scores: list[float] = []
    candidate_scores: list[float] = []
    for raw_entry in sections.values():
        if not isinstance(raw_entry, Mapping):
            continue
        entry = cast("Mapping[str, object]", raw_entry)
        nested = entry.get("candidate")
        if isinstance(nested, Mapping):
            candidate = _section_score(nested)
            base = _section_score(entry.get("base"))
        else:  # legacy flat row: the entry itself is the candidate's scores
            candidate = _section_score(entry)
            base = None
        if candidate is not None:
            candidate_scores.append(candidate)
        if base is not None:
            base_scores.append(base)
    return (
        mean_score(base_scores) if base_scores else None,
        mean_score(candidate_scores) if candidate_scores else None,
    )


def is_synthetic(rating: EvaluationRating) -> bool:
    """Return True when the rating is from the synthetic-rater dry run.

    Marked by ``notes.synthetic == True`` on the persisted rating.

    Synthetic ratings are a development proxy and must be excluded from every reported
    (expert) aggregate; they are surfaced separately, clearly labelled.
    """
    notes = rating.notes or {}
    return bool(notes.get("synthetic")) if isinstance(notes, Mapping) else False
