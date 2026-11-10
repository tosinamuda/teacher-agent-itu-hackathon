"""Results kept for the record: the earlier reported statistics and the earlier Part 2 register.

They were computed at the lesson level or on the Part 2 handoff before the dissertation settled its
analysis. Each stays in the register, read verbatim from its archived sheet, with its status, so the
workbook holds one list of results and not an old one beside a new one.
"""

from __future__ import annotations

from .record import NOT_REPORTED, Printed, Result
from .sources import Row, Sources

STATISTICS = "44_Archive_Reported_Statistics"
HISTORY = "45_Archive_P2_Result_History"

#: Rows of the archived sheets whose figure the dissertation still prints, and the register row
#: that carries it.
STILL_REPORTED = {("Part 1", "C3 − C0", "Packet cluster bootstrap"): "D-H1c-bootstrap"}


def results(sources: Sources) -> list[Result]:
    statistics = [
        _statistic(index, row) for index, row in enumerate(sources.sheet(STATISTICS), start=1)
    ]
    history = [_history(row) for row in sources.sheet(HISTORY)]
    return statistics + history


def _text(value: object) -> str:
    return "" if value is None else str(value)


def _statistic(index: int, row: Row) -> Result:
    carried_by = STILL_REPORTED.get((row["Study"], row["Contrast / quantity"], row["Method"]))
    low, high = _text(row["CI lower"]), _text(row["CI upper"])
    return Result(
        id=f"A44-{index:02d}",
        part=f"{row['Study']} (archived)",
        question="Earlier reported statistic",
        quantity=_text(row["Contrast / quantity"]),
        estimate=Printed(_text(row["Estimate"]), None),
        interval=(Printed(low, None), Printed(high, None)) if low and high else None,
        p=Printed(_text(row["p reported"]), None) if row["p reported"] is not None else None,
        test=_text(row["Method"]),
        location="not reported"
        if carried_by is None
        else f"printed in Appendix D; see {carried_by}",
        status=NOT_REPORTED
        if carried_by is None
        else f"archived; the figure is carried by {carried_by}",
        computed_from=f"{STATISTICS} (verbatim)",
        note=_text(row["Status"])
        + ("; " + _text(row["Caveat / source"]) if row["Caveat / source"] else ""),
    )


def _history(row: Row) -> Result:
    interval = _text(row["interval"]).strip("[]").split(", ")
    return Result(
        id=_text(row["result_id"]),
        part="Part 2 (archived)",
        question="Earlier Part 2 register",
        quantity=_text(row["quantity"]),
        estimate=Printed(_text(row["estimate"]), None),
        interval=(Printed(interval[0], None), Printed(interval[1], None))
        if len(interval) == 2
        else None,
        p=Printed(_text(row["p_value"]), None) if row["p_value"] not in (None, "n/a") else None,
        sidedness=_text(row["sidedness"]),
        test=_text(row["test"]),
        unit=f"{_text(row['analysis_unit'])} (n = {_text(row['n_units'])})",
        location="not reported",
        status=f"{NOT_REPORTED} (earlier status: {_text(row['status'])})",
        computed_from=f"{HISTORY} (verbatim)",
        note=_text(row["note"]),
    )
