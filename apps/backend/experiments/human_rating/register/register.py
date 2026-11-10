"""The register as one list: every reported result, then every archived one."""

from __future__ import annotations

from dataclasses import replace

from . import appendix, archive, instrument, part1, part2
from .record import Result
from .sources import Sources

#: Results the abstract also prints, so a reader of the abstract can find where each comes from.
IN_ABSTRACT = frozenset({"P1-H1a", "P1-H1c", "P1-H1c-cluster", "P2-H2-count", "P2-H2"})

TITLE = "RESULTS REGISTER | EVERY RESULT THE DISSERTATION REPORTS"
NOTE = (
    "One row per result, and the single list of the study's results. Each reported result is "
    "recomputed from this workbook's raw and calculated sheets, or read from a recorded output "
    "where the status says so, and checked against the figure the dissertation prints: "
    "'Reproduces' records that check, and 'Recomputed' the values it compared. Archived rows are "
    "earlier results kept for the record with their status; the dissertation does not report "
    "them. The mixed models are fitted into 61_Mixed_Models and the comments coded in "
    "62_Comment_Coding. Written by experiments.human_rating.register in the code repository; "
    "rerun it after any change to the raw sheets or to the dissertation."
)
WIDTHS = (14, 14, 26, 40, 12, 18, 10, 12, 30, 22, 24, 30, 12, 34, 22, 26, 50)
COLUMNS = (
    "ID",
    "Part",
    "Question",
    "Quantity",
    "Estimate",
    "Interval",
    "p",
    "Sidedness",
    "Test",
    "Unit",
    "Thesis location",
    "Status",
    "Reproduces",
    "Also printed",
    "Recomputed",
    "Computed from",
    "Note",
)


def results(sources: Sources) -> list[Result]:
    reported = [
        *instrument.results(sources),
        *part1.results(sources),
        *part2.results(sources),
        *appendix.results(sources),
    ]
    reported = [
        replace(r, location=f"{r.location}; abstract") if r.id in IN_ABSTRACT else r
        for r in reported
    ]
    return reported + archive.results(sources)


def cells(result: Result) -> tuple[str, ...]:
    """The row as the sheet shows it, one string per column of ``COLUMNS``."""
    interval = f"[{result.interval[0].text}, {result.interval[1].text}]" if result.interval else ""
    return (
        result.id,
        result.part,
        result.question,
        result.quantity,
        result.estimate.text,
        interval,
        result.p.text if result.p else "",
        result.sidedness,
        result.test,
        result.unit,
        result.location,
        result.status,
        result.reproduces(),
        result.also_text(),
        _recomputed(result),
        result.computed_from,
        result.note,
    )


def _recomputed(result: Result) -> str:
    values = [figure.value for figure in result.figures() if figure.value is not None]
    return "; ".join(value if isinstance(value, str) else f"{float(value):.4g}" for value in values)
