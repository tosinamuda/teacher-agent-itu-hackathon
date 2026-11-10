"""Unit tests for surfacing the H2 base (P0) pack alongside the candidate (P1).

Covers the read side of the paired base/candidate scores added by the H2 rating
model: the per-pack section means helper, the within-rating paired P0-vs-P1
statistics block, the flat dataset export's ``base_*`` columns, and the Wilcoxon
signed-rank helper. Pure functions over rating-shaped objects — no DB.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

from app.domains.evaluation.application import statistics as st
from app.domains.evaluation.application.dataset_queries import _h2_rows
from app.domains.evaluation.application.export_schemas import RatingRowBase
from app.domains.evaluation.application.rating_metrics import h2_pack_section_means
from app.domains.evaluation.application.reporting_queries import _build_h2_paired
from app.shared.experiment_enums import Hypothesis


def _pack(fit: int, *, section_score: float, misconception: int | None = 3) -> dict[str, object]:
    """One pack's per-section scores (5 dims + section_score)."""
    return {
        "learner_state_suitability": fit,
        "scaffolding_appropriateness": fit,
        "challenge_calibration": fit,
        "misconception_support": misconception,
        "objective_preservation": fit,
        "section_score": section_score,
    }


def _nested(candidate_fit: int, base_fit: int, *, base: bool = True) -> dict[str, object]:
    return {
        "candidate": _pack(candidate_fit, section_score=float(candidate_fit)),
        "base": _pack(base_fit, section_score=float(base_fit)) if base else None,
    }


def _rating(section_scores: dict[str, object], *, overall: float = 4.0, **extra: Any) -> Any:
    return SimpleNamespace(
        hypothesis=Hypothesis.H2,
        section_scores=section_scores,
        overall_score=overall,
        evaluation_packet_db_id=extra.get("packet_db_id", uuid4()),
        **{k: v for k, v in extra.items() if k != "packet_db_id"},
    )


def test_h2_pack_section_means_reads_base_and_candidate() -> None:
    rating = _rating({"s1": _nested(4, 3), "s2": _nested(5, 2)})
    base_mean, candidate_mean = h2_pack_section_means(rating)
    assert candidate_mean == 4.5  # (4 + 5) / 2
    assert base_mean == 2.5  # (3 + 2) / 2


def test_h2_pack_section_means_flat_row_has_no_base() -> None:
    # Legacy flat row: the section value IS the candidate's scores, no base.
    flat = {"s1": _pack(4, section_score=4.0)}
    base_mean, candidate_mean = h2_pack_section_means(_rating(flat))
    assert candidate_mean == 4.0
    assert base_mean is None


def test_h2_rows_emit_base_columns_from_nested() -> None:
    base = RatingRowBase(
        experiment_id="EXP-1",
        lesson_id="EXP-1",
        condition_code="P1",
        packet_id="EPK-1",
        rater_id="r1",
        synthetic=False,
    )
    rating = _rating({"s1": _nested(4, 3)}, overall=4.0)
    packet = SimpleNamespace(experiment_focal_case_id="EFC-1")
    rows = _h2_rows(base, rating, packet)
    assert len(rows) == 1
    row = rows[0]
    assert row.section_score == 4.0  # candidate (P1)
    assert row.base_section_score == 3.0  # base (P0)
    assert row.base_learner_state_suitability == 3.0


def test_h2_rows_base_columns_none_for_flat_row() -> None:
    base = RatingRowBase(
        experiment_id="EXP-1",
        lesson_id="EXP-1",
        condition_code="P1",
        packet_id="EPK-1",
        rater_id="r1",
        synthetic=False,
    )
    rating = _rating({"s1": _pack(4, section_score=4.0)})
    packet = SimpleNamespace(experiment_focal_case_id="EFC-1")
    row = _h2_rows(base, rating, packet)[0]
    assert row.section_score == 4.0
    assert row.base_section_score is None
    assert row.base_learner_state_suitability is None


def test_build_h2_paired_computes_paired_contrast() -> None:
    # Six ratings where the candidate (P1) consistently beats the base (P0).
    ratings = []
    packet_focal: dict[Any, str] = {}
    for _index in range(6):
        pid = uuid4()
        ratings.append(_rating({"s1": _nested(4, 2)}, packet_db_id=pid))
        packet_focal[pid] = "EFC-1"
    paired = _build_h2_paired(ratings, packet_focal)
    assert paired["n_pairs"] == 6
    assert paired["p0"]["mean"] == 2.0
    assert paired["p1"]["mean"] == 4.0
    assert paired["mean_diff"] == 2.0
    assert paired["wilcoxon_p"] is not None
    assert paired["by_focal"] == [{"label": "EFC-1", "p0": 2.0, "p1": 4.0}]


def test_build_h2_paired_skips_ratings_without_base() -> None:
    pid = uuid4()
    ratings = [_rating({"s1": _nested(4, 3, base=False)}, packet_db_id=pid)]
    paired = _build_h2_paired(ratings, {pid: "EFC-1"})
    assert paired["n_pairs"] == 0
    assert paired["by_focal"] == []


def test_wilcoxon_p_handles_ties_and_short_input() -> None:
    assert st.wilcoxon_p([1.0], [1.0]) is None  # too short
    assert st.wilcoxon_p([3.0, 3.0, 3.0], [3.0, 3.0, 3.0]) is None  # all tied
    p = st.wilcoxon_p([4.0, 5.0, 4.0, 5.0, 4.0], [2.0, 3.0, 2.0, 3.0, 2.0])
    assert p is not None and 0.0 <= p <= 1.0
