"""Where the register reads from: the study workbook, the run record, and the dissertation's
cross-reference file for section and table numbers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

import openpyxl

THESIS = Path.home() / "Documents/Unilag/Masters/Thesis"
DATASET = THESIS / "Dataset"
WORKBOOK = DATASET / "report/Lesson_Plan_Study_Raw_to_Charts.xlsx"
RUN_RECORD = DATASET / "public/ng-jss1-math-alignment-ratings/runs/h2/h2-deepseek-clean/run.json"
AUX = THESIS / "writing/latex/main.aux"

#: Every sheet the workbook builds puts its column names on row 5, under a title and a note.
HEADER_ROW = 5

Row = dict[str, Any]


@dataclass(frozen=True)
class Sources:
    workbook: Path = WORKBOOK
    run_record: Path = RUN_RECORD
    aux: Path = AUX

    def sheet(self, name: str) -> list[Row]:
        return _sheet(self.workbook, name)

    def run(self) -> dict[str, Any]:
        record: dict[str, Any] = json.loads(self.run_record.read_text(encoding="utf-8"))
        return record

    def where(self, *labels: str) -> str:
        """The dissertation's numbers for these labels, e.g. '6.4.2, Table 6.3'."""
        numbers = _labels(self.aux)
        return ", ".join(_named(label, numbers.get(label)) for label in labels)


@cache
def _sheet(workbook: Path, name: str) -> list[Row]:
    """A sheet's rows by column name; a renamed sheet is found by its number, e.g. '44_'."""
    book = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    if name not in book.sheetnames:
        prefix = name.split("_", 1)[0] + "_"
        name = next(title for title in book.sheetnames if title.startswith(prefix))
    rows = book[name].iter_rows(min_row=HEADER_ROW, values_only=True)
    header = [str(value) for value in next(rows)]
    return [dict(zip(header, row, strict=False)) for row in rows if any(v is not None for v in row)]


@cache
def _labels(aux: Path) -> dict[str, str]:
    """Every label's number, following the ``\\@input`` of each chapter's own aux file."""
    if not aux.exists():
        return {}
    text = aux.read_text(encoding="utf-8", errors="ignore")
    labels = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", text))
    for included in re.findall(r"\\@input\{([^}]+)\}", text):
        labels |= _labels(aux.parent / included)
    return labels


def _named(label: str, number: str | None) -> str:
    if number is None:
        return f"unresolved: {label}"
    if label.startswith("tab:"):
        return f"Table {number}"
    if number[:1].isalpha():
        return f"Appendix {number}"
    return f"§{number}"
