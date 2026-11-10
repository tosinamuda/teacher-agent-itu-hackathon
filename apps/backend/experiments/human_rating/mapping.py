"""The assignment design, read from the two rater-mapping workbooks.

The workbooks are the study's allocation: which rater sees which packet, in which
order, under which external id. The internal id in them reveals the condition and the
version; it is parsed here for assembly and the de-anonymisation key, and appears
nowhere a rater looks. The row order in each `Rater_N` sheet is the delivery order and
is never sorted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
H1_WORKBOOK = HERE / "mapping" / "h1.xlsx"
H2_WORKBOOK = HERE / "mapping" / "h2.xlsx"

_H1_INTERNAL = re.compile(
    r"^h1-(?P<lesson>l\d\d)-c(?P<condition>\d)-v(?P<version>\d)-c(?P<copy>\d)$"
)
_H2_INTERNAL = re.compile(r"^h2-(?P<lesson>l\d\d)-s(?P<student>\d\d)-c(?P<copy>\d)$")
RATERS: tuple[str, ...] = ("rater-1", "rater-2", "rater-3", "rater-4")


@dataclass(frozen=True)
class H1Assignment:
    rater: str
    order: int
    external_id: str
    internal_id: str
    lesson: str
    """The lesson code, e.g. ``t3-w06``."""
    condition: str
    """``C0``…``C3``."""
    version: int
    """The generation draw, 1-based — the run's ``repeat``."""

    @property
    def rater_number(self) -> int:
        return int(self.rater.split("-")[1])


@dataclass(frozen=True)
class H2Assignment:
    rater: str
    order: int
    external_id: str
    internal_id: str
    lesson: str
    student: str
    """The dataset's student id, e.g. ``student-04``."""
    a: str
    """Which condition Material A is: ``P0`` or ``P1``."""
    b: str
    learner_card_id: str
    a_id: str
    b_id: str

    @property
    def rater_number(self) -> int:
        return int(self.rater.split("-")[1])


def _rows(sheet) -> list[dict[str, str]]:
    rows = list(sheet.iter_rows(values_only=True))
    head = [str(h).strip() if h is not None else "" for h in rows[0]]
    return [
        {head[i]: ("" if v is None else str(v).strip()) for i, v in enumerate(row)}
        for row in rows[1:]
        if any(v is not None and str(v).strip() for v in row)
    ]


def load_h1(path: Path = H1_WORKBOOK) -> list[H1Assignment]:
    book = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out: list[H1Assignment] = []
    for rater in RATERS:
        sheet = book[f"Rater_{rater.split('-')[1]}"]
        for order, row in enumerate(_rows(sheet), start=1):
            match = _H1_INTERNAL.match(row["internal_packet_id"])
            if not match:
                raise ValueError(
                    f"{path.name}: unreadable internal id {row['internal_packet_id']!r}"
                )
            out.append(
                H1Assignment(
                    rater=rater,
                    order=order,
                    external_id=row["external_packet_id"],
                    internal_id=row["internal_packet_id"],
                    lesson=row["lesson_code"],
                    condition=f"C{match['condition']}",
                    version=int(match["version"]),
                )
            )
    return out


def load_h2(path: Path = H2_WORKBOOK) -> list[H2Assignment]:
    book = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ids = {row["external_packet_id"]: row for row in _rows(book["H2_Packet_Map"])}
    out: list[H2Assignment] = []
    for rater in RATERS:
        sheet = book[f"Rater_{rater.split('-')[1]}"]
        for order, row in enumerate(_rows(sheet), start=1):
            match = _H2_INTERNAL.match(row["internal_packet_id"])
            if not match:
                raise ValueError(
                    f"{path.name}: unreadable internal id {row['internal_packet_id']!r}"
                )
            external = ids[row["external_packet_id"]]
            out.append(
                H2Assignment(
                    rater=rater,
                    order=order,
                    external_id=row["external_packet_id"],
                    internal_id=row["internal_packet_id"],
                    lesson=row["lesson_code"],
                    student=f"student-{match['student']}",
                    a=row["a"].upper(),
                    b=row["b"].upper(),
                    learner_card_id=external["external_learner_card_id"],
                    a_id=external["external_candidate_a_id"],
                    b_id=external["external_candidate_b_id"],
                )
            )
    return out


def expected_checks(path: Path) -> dict[str, dict[str, str]]:
    """The workbook's own `Checks` sheet: what each rater's allocation must add up to.

    Read by position, not by header: a second block follows under its own header
    ("structural check"), and it describes the workbook rather than any rater.
    """
    book = openpyxl.load_workbook(path, data_only=True, read_only=True)
    rows = list(book["Checks"].iter_rows(values_only=True))
    head = [str(h).strip() if h is not None else "" for h in rows[0]]
    columns = {rater: head.index(rater) for rater in RATERS if rater in head}
    out: dict[str, dict[str, str]] = {}
    for row in rows[1:]:
        cells = ["" if value is None else str(value).strip() for value in row]
        if not cells or not cells[0] or cells[0] == "structural check":
            break
        out[cells[0]] = {rater: cells[index] for rater, index in columns.items()}
    return out
