"""Two runs side by side, scored against what the metric does on its own.

A delta only means something next to the movement that metric shows when nothing changed.
Re-running the SAME condition on unchanged data moved recall by a median of 0.094 across
four runs, with t3-w09 at 0.182 — wider than almost every arm difference measured with it.
So a recall delta inside that floor is reported and left grey, never coloured as a win.

Only metrics with a measured floor are scored. The rest are reported because they say what
a run did, not whether it did better: `chars` and `blocks` have no target, and
`evidence_chars` describes the input rather than the outcome. Colouring them would invent
a direction nobody measured.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from openpyxl import Workbook

from experiments.h1_condition_eval.workbook import BETTER, INSIDE_NOISE, WORSE, sheet


@dataclass(frozen=True)
class ComparedMetric:
    """One column of the comparison, and what a change in it is worth."""

    key: str
    higher_is_better: bool | None
    """None means reported but never scored — no measured direction, no colour."""
    noise_floor: float
    """A delta at or inside this is run-to-run movement. 0.0 means every change counts,
    which is only honest for a defect count."""

    def verdict(self, delta: float) -> Any | None:
        """The fill this delta earns, or None to leave it alone."""
        if self.higher_is_better is None or delta == 0:
            return None
        if abs(delta) <= self.noise_floor:
            return INSIDE_NOISE
        improved = delta > 0 if self.higher_is_better else delta < 0
        return BETTER if improved else WORSE


COMPARED = (
    # Measured floor: metrics.py, median same-condition movement across four runs.
    ComparedMetric("recall", higher_is_better=True, noise_floor=0.094),
    # Same scale and same source as recall, but its own run-to-run spread was never
    # measured, so it is reported and not scored rather than given a borrowed floor.
    ComparedMetric("invention", higher_is_better=None, noise_floor=0.0),
    # A defect count, not a score: one leaked marker is one too many.
    ComparedMetric("inline_ref_markers", higher_is_better=False, noise_floor=0.0),
    ComparedMetric("evidence_items", higher_is_better=None, noise_floor=0.0),
    ComparedMetric("evidence_chars", higher_is_better=None, noise_floor=0.0),
    ComparedMetric("chars", higher_is_better=None, noise_floor=0.0),
    ComparedMetric("blocks", higher_is_better=None, noise_floor=0.0),
)

SCORED = tuple(metric for metric in COMPARED if metric.higher_is_better is not None)


def rebuild(book: Workbook) -> None:
    """Two most recent labels side by side. Rewritten each run, never appended to."""
    records = _records(book["Runs"])
    labels = _labels(records)
    if len(labels) < 2:
        return
    before, after = labels[-2], labels[-1]

    if "Comparison" in book.sheetnames:
        book.remove(book["Comparison"])
    columns = ["lesson", "condition"] + [
        f"{metric.key}_{tag}" for metric in COMPARED for tag in (before, after, "delta")
    ]
    target = sheet(book, "Comparison", columns)

    keyed = {(r["run_label"], r["lesson"], r["condition"]): r for r in records}
    for lesson, condition in _pairs(records, after):
        old, new = keyed.get((before, lesson, condition)), keyed[(after, lesson, condition)]
        target.append(_row(lesson, condition, old, new))
        _paint(target, old is not None)


def _row(lesson: Any, condition: Any, old: dict | None, new: dict) -> list[Any]:
    row: list[Any] = [lesson, condition]
    for metric in COMPARED:
        new_value = _number(new.get(metric.key))
        if old is None:
            row += ["", new_value, ""]
            continue
        old_value = _number(old.get(metric.key))
        row += [old_value, new_value, round(new_value - old_value, 3)]
    return row


def _paint(target: Any, comparable: bool) -> None:
    """Colour each delta cell of the row just appended."""
    if not comparable:
        return
    for offset, metric in enumerate(COMPARED):
        cell = target.cell(row=target.max_row, column=5 + offset * 3)
        fill = metric.verdict(float(cell.value or 0))
        if fill is not None:
            cell.fill = fill


def _number(value: Any) -> float | int:
    if value in (None, ""):
        return 0
    number = float(value)
    return int(number) if number.is_integer() else round(number, 3)


def _records(runs: Any) -> list[dict]:
    header = [cell.value for cell in runs[1]]
    return [
        dict(zip(header, [cell.value for cell in row], strict=False))
        for row in runs.iter_rows(min_row=2)
    ]


def _labels(records: list[dict]) -> list[str]:
    labels: list[str] = []
    for record in records:
        if record["run_label"] not in labels:
            labels.append(str(record["run_label"]))
    return labels


def _pairs(records: list[dict], label: str) -> list[tuple]:
    return sorted(
        {(r["lesson"], r["condition"]) for r in records if r["run_label"] == label},
        key=str,
    )
