"""Sheet helpers shared by the run log and the comparison view."""

from __future__ import annotations

from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="44546A")
WORSE = PatternFill("solid", fgColor="F8CBAD")
BETTER = PatternFill("solid", fgColor="C6E0B4")
INSIDE_NOISE = PatternFill("solid", fgColor="D9D9D9")
"""Grey, deliberately: a delta inside the run-to-run floor is neither good nor bad news."""


def sheet(book: Workbook, title: str, columns: list[str]) -> Any:
    """The named sheet, created with these columns if it is not there yet."""
    if title in book.sheetnames:
        return book[title]
    created = book.create_sheet(title)
    created.append(columns)
    style_header(created, columns)
    created.freeze_panes = "A2"
    return created


def style_header(target: Any, columns: list[str], first: int = 1) -> None:
    """Format a header run starting at ``first``, sizing each column to its name."""
    for offset, name in enumerate(columns):
        index = first + offset
        cell = target.cell(row=1, column=index)
        cell.font, cell.fill = HEADER_FONT, HEADER_FILL
        cell.alignment = Alignment(horizontal="center")
        target.column_dimensions[get_column_letter(index)].width = max(12, len(name) + 2)


def ensure_columns(target: Any, columns: list[str]) -> list[str]:
    """The sheet's columns, extended with any of ``columns`` it does not carry yet.

    The log is a tracked workbook with history in it, so a new metric has to arrive as an
    added column rather than a rewritten header — otherwise every past row shifts under it.
    """
    header = [cell.value for cell in target[1] if cell.value is not None]
    missing = [name for name in columns if name not in header]
    if missing:
        for offset, name in enumerate(missing):
            target.cell(row=1, column=len(header) + offset + 1, value=name)
        style_header(target, missing, first=len(header) + 1)
        header += missing
    return [str(name) for name in header]
