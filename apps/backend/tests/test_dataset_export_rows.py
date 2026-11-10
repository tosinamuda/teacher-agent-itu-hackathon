"""Unit tests for the flat dataset-export row builders (evaluation domain).

The H1 save path normalises rubric scores to floats
(``validate_h1_rubric_scores``), so the export coercion must accept
whole-valued floats — a regression here silently nulls every dimension
column in the analysis dataset while ``h1_composite`` stays populated.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

from app.domains.evaluation.application.dataset_queries import _h1_row, _int_or_none
from app.domains.evaluation.application.export_schemas import RatingRowBase
from app.domains.evaluation.infrastructure.models import EvaluationRating

BASE = RatingRowBase(
    experiment_id="EXP-1",
    lesson_id="EXP-1",
    condition_code="C0",
    packet_id="EPK-1",
    rater_id="rater-1",
    synthetic=False,
)


def test_int_or_none_accepts_ints_and_whole_floats() -> None:
    assert _int_or_none(4) == 4
    assert _int_or_none(4.0) == 4
    assert _int_or_none(3.25) is None
    assert _int_or_none(True) is None
    assert _int_or_none("4") is None
    assert _int_or_none(None) is None


def test_h1_row_keeps_float_normalised_rubric_scores() -> None:
    rating = cast(
        EvaluationRating,
        SimpleNamespace(
            overall_score=4.0,
            rubric_scores={
                "objective_curriculum_alignment": 4.0,
                "taught_lesson_alignment": 4.0,
                "scope_conceptual_correctness": 3.0,
                "clarity_usefulness": 4.0,
            },
            notes={"major_issues": ["misses_objective"], "major_issue_other": None},
        ),
    )
    row = _h1_row(BASE, rating)
    assert row.objective_curriculum_alignment == 4
    assert row.taught_lesson_alignment == 4
    assert row.scope_conceptual_correctness == 3
    assert row.clarity_usefulness == 4
    assert row.major_issues == ["misses_objective"]
