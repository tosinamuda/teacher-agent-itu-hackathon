"""Statistics + results reads for the evaluation dashboard.

H1/H2 hypothesis tests, inter-rater reliability, rating-progress summaries and the
investigation roll-up — split out of the evaluation service so each stays focused.
"""

from __future__ import annotations

import math
import uuid
from collections import defaultdict

from app.domains.evaluation.application import statistics as st
from app.domains.evaluation.application.constants import H1_RUBRIC
from app.domains.evaluation.application.rating_metrics import (
    h2_pack_section_means,
    mean_score,
)
from app.domains.evaluation.infrastructure.models import EvaluationRating
from app.shared.experiment_enums import Hypothesis
from app.shared.json_types import JsonObject, JsonValue


def _contrast(treatment: list[float], baseline: list[float]) -> JsonObject | None:
    if not treatment or not baseline:
        return None
    return {
        "mean_diff": round(sum(treatment) / len(treatment) - sum(baseline) / len(baseline), 4),
        "mann_whitney_p": st.mann_whitney_p(treatment, baseline),
        "cliffs_delta": st.cliffs_delta(treatment, baseline),
        "cohens_d": st.cohens_d(treatment, baseline),
    }


def _with_ci(scores: list[float]) -> JsonObject:
    summary = st.summarize(scores)
    n = summary.get("n") or 0
    std = summary.get("std")
    summary["ci"] = (
        round(1.96 * float(std) / math.sqrt(n), 4)
        if (std and isinstance(n, int) and n > 1)
        else 0.0
    )
    return summary


def _build_h1(
    ratings: list[EvaluationRating],
    cond_scores: dict[str, list[float]],
    packet_code: dict[uuid.UUID, str | None],
    h1_codes: list[str],
) -> tuple[dict[str, object], int]:
    """H1 grounding-ablation block (C0-C3): per-condition CIs, per-dimension means,.

    adjacent pairwise effects, omnibus Kruskal-Wallis, and the C0-vs-strongest effect.
    """
    dimension_ids = [str(criterion["criterion_id"]) for criterion in H1_RUBRIC]
    dim_scores: dict[tuple[str, str], list[float]] = defaultdict(list)
    for rating in ratings:
        if rating.hypothesis != Hypothesis.H1:
            continue
        code = packet_code.get(rating.evaluation_packet_db_id)
        rubric = rating.rubric_scores or {}
        if not code or not isinstance(rubric, dict):
            continue
        for criterion_id, value in rubric.items():
            if isinstance(value, (int, float)):
                dim_scores[(str(criterion_id), code)].append(float(value))
    dimensions = {
        criterion_id: {
            code: mean_score(dim_scores.get((criterion_id, code), [])) for code in h1_codes
        }
        for criterion_id in dimension_ids
    }
    contrasts: list[JsonObject] = []
    for previous, current in zip(h1_codes, h1_codes[1:], strict=False):
        effect = _contrast(cond_scores.get(current, []), cond_scores.get(previous, []))
        if effect:
            contrasts.append({"from": previous, "to": current, **effect})
    n_ratings = sum(len(cond_scores.get(code, [])) for code in h1_codes)
    h1: dict[str, object] = {
        "conditions": {code: _with_ci(cond_scores.get(code, [])) for code in h1_codes},
        "dimensions": dimensions,
        "contrasts": contrasts,
        "kruskal_p": st.kruskal_p([cond_scores.get(code, []) for code in h1_codes]),
        "c0_vs_strongest": _contrast(
            cond_scores.get(h1_codes[-1], []) if h1_codes else [],
            cond_scores.get("C0", []),
        ),
        "n_ratings": n_ratings,
    }
    return h1, n_ratings


def _build_h2_paired(
    ratings: list[EvaluationRating],
    packet_focal: dict[uuid.UUID, str | None],
) -> JsonObject:
    """Within-rating PAIRED P0 (base) vs P1 (candidate) comparison.

    The personalisation test proper: each H2 rating scores BOTH the base pack (P0)
    and the personalised pack (P1) for the same focal learner, so P0 and P1 are
    paired by rating (same rater, same packet). Aggregates the per-rating pack means
    into a paired contrast — Wilcoxon signed-rank + Cliff's delta — plus per-focal
    paired means. Ratings without base scores (legacy candidate-only) are skipped.
    """
    p0_means: list[float] = []
    p1_means: list[float] = []
    focal_pairs: dict[str, tuple[list[float], list[float]]] = defaultdict(lambda: ([], []))
    for rating in ratings:
        if rating.hypothesis != Hypothesis.H2:
            continue
        base_mean, candidate_mean = h2_pack_section_means(rating)
        if base_mean is None or candidate_mean is None:
            continue
        p0_means.append(base_mean)
        p1_means.append(candidate_mean)
        focal = packet_focal.get(rating.evaluation_packet_db_id)
        if focal:
            focal_pairs[focal][0].append(base_mean)
            focal_pairs[focal][1].append(candidate_mean)
    by_focal: list[JsonValue] = [
        {"label": focal, "p0": mean_score(base), "p1": mean_score(candidate)}
        for focal, (base, candidate) in sorted(focal_pairs.items())
    ]
    return {
        "n_pairs": len(p0_means),
        "p0": _with_ci(p0_means),
        "p1": _with_ci(p1_means),
        "mean_diff": round(sum(p1_means) / len(p1_means) - sum(p0_means) / len(p0_means), 4)
        if p0_means
        else None,
        "wilcoxon_p": st.wilcoxon_p(p1_means, p0_means),
        "cliffs_delta": st.cliffs_delta(p1_means, p0_means),
        "by_focal": by_focal,
    }


def _build_h2(
    ratings: list[EvaluationRating],
    cond_scores: dict[str, list[float]],
    packet_code: dict[uuid.UUID, str | None],
    packet_focal: dict[uuid.UUID, str | None],
    h2_codes: list[str],
) -> tuple[dict[str, object], int]:
    """H2 personalisation block: per-focal-learner P0->P1 pairs + the P1-vs-P0 effect.

    ``p1_vs_p0`` / ``pairs`` are the legacy separate-packet contrast (P0 and P1 as
    distinct condition packets). ``paired_p0_p1`` is the within-rating paired contrast
    built from each rating's base + candidate pack scores — the design where one rater
    scores both packs for the same learner.
    """
    focal_cond: dict[tuple[str, str], list[float]] = defaultdict(list)
    for rating in ratings:
        if rating.hypothesis != Hypothesis.H2:
            continue
        code = packet_code.get(rating.evaluation_packet_db_id)
        focal = packet_focal.get(rating.evaluation_packet_db_id)
        if code and focal:
            focal_cond[(focal, code)].append(float(rating.overall_score))
    pairs: list[JsonObject] = []
    for focal in sorted({focal for (focal, _code) in focal_cond}):
        p0 = focal_cond.get((focal, "P0"))
        p1 = focal_cond.get((focal, "P1"))
        if p0 and p1:
            pairs.append({"label": focal, "p0": mean_score(p0), "p1": mean_score(p1)})
    n_ratings = sum(len(cond_scores.get(code, [])) for code in h2_codes)
    h2: dict[str, object] = {
        "conditions": {code: _with_ci(cond_scores.get(code, [])) for code in h2_codes},
        "pairs": pairs,
        "p1_vs_p0": _contrast(cond_scores.get("P1", []), cond_scores.get("P0", [])),
        "paired_p0_p1": _build_h2_paired(ratings, packet_focal),
        "n_ratings": n_ratings,
    }
    return h2, n_ratings


def _inter_rater(ratings: list[EvaluationRating]) -> JsonObject:
    """Krippendorff's alpha over the rater x packet overall-score matrix."""
    rater_ids = sorted({rating.rater_db_id for rating in ratings}, key=str)
    item_ids = sorted({rating.evaluation_packet_db_id for rating in ratings}, key=str)
    item_index = {pid: i for i, pid in enumerate(item_ids)}
    rater_index = {rid: i for i, rid in enumerate(rater_ids)}
    matrix: list[list[float | None]] = [[None] * len(item_ids) for _ in rater_ids]
    for rating in ratings:
        matrix[rater_index[rating.rater_db_id]][item_index[rating.evaluation_packet_db_id]] = float(
            rating.overall_score
        )
    return {
        "krippendorff_alpha": st.krippendorff_alpha(matrix),
        "n_raters": len(rater_ids),
        "n_items": len(item_ids),
    }


def _underpowered_notes(
    synthetic_basis: bool, h1_n_ratings: int, h2_n_ratings: int, inter_rater: JsonObject
) -> list[str]:
    notes: list[str] = []
    if synthetic_basis:
        notes.append(
            "Shown from synthetic dry-run ratings (no expert ratings yet) — illustrative only."
        )
    if h1_n_ratings < 20:
        notes.append("H1 underpowered — few ratings per condition (pilot data).")
    if h2_n_ratings < 20:
        notes.append("H2 underpowered — few ratings per condition (pilot data).")
    if inter_rater["krippendorff_alpha"] is None:
        notes.append("Inter-rater alpha needs overlapping ratings from >= 2 raters.")
    return notes
