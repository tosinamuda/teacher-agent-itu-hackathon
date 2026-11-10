"""A delta only means something beside the movement its metric shows when nothing changed.

Re-running the same condition on unchanged data moved recall by a median of 0.094 across
four runs (t3-w09: 0.182). The comparison used to colour any non-zero delta as better or
worse, on counts with no measured variance at all, while recall — the one number with a
known floor — was computed on every cell and then dropped before it reached the sheet.
"""

from __future__ import annotations

import dataclasses

import pytest
from openpyxl import Workbook

from experiments.h1_condition_eval import comparison
from experiments.h1_condition_eval.comparison import COMPARED, SCORED, ComparedMetric
from experiments.h1_condition_eval.log import RUN_COLUMNS
from experiments.h1_condition_eval.workbook import BETTER, INSIDE_NOISE, WORSE, sheet

RECALL = next(metric for metric in COMPARED if metric.key == "recall")
LEAK = next(metric for metric in COMPARED if metric.key == "inline_ref_markers")


def _cell(row: dict) -> dict:
    return {
        "run_at": "t",
        "lesson": "t2-w09",
        "units": 3,
        "evidence_items": 1,
        "evidence_chars": 100,
        "sections": 3,
        "blocks": 9,
        "chars": 2900,
        "blocks_with_source_refs": 9,
        "inline_ref_markers": 0,
        "raw_latex_markers": 0,
        "invention": 0.0,
        **row,
    }


def _book(*rows: dict) -> Workbook:
    book = Workbook()
    book.remove(book.active)
    runs = sheet(book, "Runs", RUN_COLUMNS)
    for row in rows:
        record = _cell(row)
        runs.append([record.get(column, "") for column in RUN_COLUMNS])
    return book


def _delta_fill(book: Workbook, metric: str) -> str:
    comparison.rebuild(book)
    target = book["Comparison"]
    header = [cell.value for cell in target[1]]
    return target.cell(row=2, column=header.index(f"{metric}_delta") + 1).fill.fgColor.rgb


@pytest.mark.parametrize(
    ("delta", "expected"),
    [
        (0.094, INSIDE_NOISE),
        (0.093, INSIDE_NOISE),
        (0.095, BETTER),
        (-0.095, WORSE),
        (-0.094, INSIDE_NOISE),
    ],
)
def test_a_recall_delta_is_scored_against_the_measured_floor(
    delta: float, expected: object
) -> None:
    """The floor is inclusive: a move the size of run-to-run noise is not a result."""
    assert RECALL.verdict(delta) is expected


def test_recall_reaches_the_sheet_at_all() -> None:
    """It was computed on every cell and dropped by the column list for the whole study."""
    assert "recall" in RUN_COLUMNS

    book = _book(
        {"run_label": "before", "condition": "C2", "recall": 0.500},
        {"run_label": "after", "condition": "C2", "recall": 0.700},
    )

    assert _delta_fill(book, "recall") == BETTER.fgColor.rgb


def test_a_move_inside_the_floor_is_reported_but_not_called_a_win() -> None:
    book = _book(
        {"run_label": "before", "condition": "C2", "recall": 0.500},
        {"run_label": "after", "condition": "C2", "recall": 0.540},
    )

    assert _delta_fill(book, "recall") == INSIDE_NOISE.fgColor.rgb


def test_a_leak_has_no_floor_because_one_marker_is_one_too_many() -> None:
    assert LEAK.noise_floor == 0.0
    assert LEAK.verdict(1) is WORSE
    assert LEAK.verdict(-1) is BETTER


def test_a_metric_with_no_measured_direction_is_never_coloured() -> None:
    """`chars` and `evidence_chars` say what a run did, not whether it did better."""
    unscored = [metric for metric in COMPARED if metric.higher_is_better is None]

    assert {metric.key for metric in unscored} == {
        "invention",
        "evidence_items",
        "evidence_chars",
        "chars",
        "blocks",
    }
    assert all(metric.verdict(999) is None for metric in unscored)


def test_findings_count_is_not_a_compared_metric() -> None:
    """It moved sd 2.03 on a mean of 1.53 across identical draws — unusable for comparison."""
    assert "findings" not in {metric.key for metric in COMPARED}


def test_every_scored_metric_states_a_floor_it_was_given_not_one_it_borrowed() -> None:
    """Invention shares recall's scale but not its measurement, so it stays unscored."""
    assert {metric.key for metric in SCORED} == {"recall", "inline_ref_markers"}
    assert RECALL.noise_floor == 0.094


def test_a_first_run_has_nothing_to_compare_against() -> None:
    book = _book({"run_label": "only", "condition": "C2", "recall": 0.5})

    comparison.rebuild(book)

    assert "Comparison" not in book.sheetnames


def test_a_new_metric_column_does_not_shift_the_rows_already_logged() -> None:
    """The log is tracked and has the study's history in it."""
    book = _book({"run_label": "before", "condition": "C2", "recall": 0.5})
    runs = book["Runs"]
    before = [cell.value for cell in runs[2]]

    from experiments.h1_condition_eval.workbook import ensure_columns

    columns = ensure_columns(runs, [*RUN_COLUMNS, "a_later_metric"])

    assert columns[-1] == "a_later_metric"
    # The row widens by an empty cell under the new header; nothing already in it moves.
    assert [cell.value for cell in runs[2]][: len(before)] == before


def test_a_floor_cannot_be_loosened_at_the_call_site() -> None:
    """A metric declares its floor once; raising it to fit a result is not available."""
    metric = ComparedMetric("x", higher_is_better=True, noise_floor=0.1)

    with pytest.raises(dataclasses.FrozenInstanceError):
        metric.noise_floor = 0.2  # type: ignore[misc]
