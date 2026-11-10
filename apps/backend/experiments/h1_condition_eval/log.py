"""The running experiment log — one workbook, appended to by every run.

A workbook rather than a CSV because the log is not one table: the raw per-condition
rows, the run register, and the before/after comparison are three views that want to sit
together and be read side by side.

Sheets
------
``Runs``        one row per (run, lesson, condition) — the raw record, never rewritten.
``Register``    one row per run: label, when, how many lessons, and the run's totals.
``Comparison``  the two most recent labels side by side, scored in ``comparison.py``
                against each metric's own run-to-run movement.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook

from experiments.h1_condition_eval import comparison
from experiments.h1_condition_eval.workbook import ensure_columns, sheet

LOG_PATH = Path(__file__).parent / "experiment-log.xlsx"

RUN_COLUMNS = [
    "run_label",
    "run_at",
    "lesson",
    "condition",
    "units",
    "evidence_items",
    "evidence_chars",
    "sections",
    "blocks",
    "chars",
    "blocks_with_source_refs",
    "inline_ref_markers",
    "raw_latex_markers",
    # The screening metrics. Both are computed on every cell and were being dropped here:
    # the log compared runs on counts with no measured variance while the one number with
    # a known floor never reached the sheet.
    "recall",
    "invention",
]

REGISTER_COLUMNS = [
    "run_label",
    "run_at",
    "lessons",
    "conditions",
    "evidence_chars",
    "chars",
    "inline_ref_markers",
    "notes",
]


def _load() -> Workbook:
    if LOG_PATH.exists():
        return load_workbook(LOG_PATH)
    book = Workbook()
    book.remove(book.active)
    return book


def append_run(label: str, rows: list[dict[str, Any]], notes: str = "") -> Path:
    """Add one run to the log and refresh the register and comparison sheets."""
    book = _load()
    run_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    runs = sheet(book, "Runs", RUN_COLUMNS)
    columns = ensure_columns(runs, RUN_COLUMNS)
    for row in rows:
        record: dict[str, Any] = {"run_label": label, "run_at": run_at, **row}
        runs.append([record.get(column, "") for column in columns])

    _append_register(book, label, run_at, rows, notes)
    comparison.rebuild(book)
    book.save(LOG_PATH)
    return LOG_PATH


def _append_register(
    book: Workbook, label: str, run_at: str, rows: list[dict[str, Any]], notes: str
) -> None:
    register = sheet(book, "Register", REGISTER_COLUMNS)
    register.append(
        [
            label,
            run_at,
            len({row["lesson"] for row in rows}),
            len({row["condition"] for row in rows}),
            sum(int(row.get("evidence_chars") or 0) for row in rows),
            sum(int(row.get("chars") or 0) for row in rows),
            sum(int(row.get("inline_ref_markers") or 0) for row in rows),
            notes,
        ]
    )
