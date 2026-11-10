"""Recompute every reported result from the study workbook, and write the register into it.

    uv run python -m experiments.human_rating.register            # check, write nothing
    uv run python -m experiments.human_rating.register --write    # also write sheets 60 to 62

A check fits Appendix D's mixed models, reads the comment coding, recomputes every result, and
prints how many reproduce the figure the dissertation prints, and every one that does not. A write
adds or replaces 60_Results_Register, 61_Mixed_Models and 62_Comment_Coding. It refuses to proceed
unless only the parts ``xlsx.edited_parts`` names would change; it writes beside the workbook,
re-reads what it wrote, keeps a dated backup of the original, and only then replaces it.
"""

from __future__ import annotations

import argparse
import os
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

import openpyxl

from . import comments, models, register, xlsx
from .record import Result
from .sources import AUX, RUN_RECORD, WORKBOOK, Sources

#: Sheets the start sheet's index must list, with the layer each belongs to.
INDEXED = {
    "44_Archive_Reported_Statistics": "ARCHIVE",
    "45_Archive_P2_Result_History": "ARCHIVE",
    "56_Aggregation_Routes": "AUDIT",
    "57_Interval_Diagnostics": "AUDIT",
    "58_Agreement_Recomputed": "AUDIT",
    "59_Number_Provenance": "AUDIT",
    xlsx.REGISTER: "RESULTS",
    models.SHEET: "CALCULATED",
    comments.SHEET: "QUALITATIVE",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--workbook", type=Path, default=WORKBOOK)
    parser.add_argument("--run-record", type=Path, default=RUN_RECORD)
    parser.add_argument("--aux", type=Path, default=AUX)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    sources = Sources(args.workbook, args.run_record, args.aux)
    results = register.results(sources)
    failed = _report(results)
    if args.write:
        generated = [
            xlsx.Sheet(
                xlsx.REGISTER,
                register.TITLE,
                register.NOTE,
                register.COLUMNS,
                [register.cells(result) for result in results],
                register.WIDTHS,
                keys=4,
            ),
            models.sheet(sources),
            comments.sheet(sources),
        ]
        _write(args.workbook, generated)
    return 1 if failed else 0


def _report(results: list[Result]) -> int:
    reported = [r for r in results if not r.status.startswith("archived")]
    tally = Counter(r.reproduces().split(" (")[0] for r in reported)
    print(f"{len(reported)} reported results, {len(results) - len(reported)} archived")
    print("  " + ", ".join(f"{verdict}: {count}" for verdict, count in sorted(tally.items())))
    for result in reported:
        verdict = result.reproduces()
        if verdict != "yes":
            print(f"  {verdict:<16} {result.id:<22} {result.quantity}")
    unresolved = [r.id for r in reported if "unresolved" in r.location]
    if unresolved:
        print(f"  locations not found in the aux file: {', '.join(unresolved)}")
    return tally["NO"]


def _write(workbook: Path, generated: list[xlsx.Sheet]) -> None:
    parts, infos = xlsx.read(str(workbook))
    updated = xlsx.with_sheets(parts, generated, _index(workbook, generated))
    allowed = xlsx.edited_parts(updated, [sheet.name for sheet in generated])
    stray = sorted(
        name for name in updated if parts.get(name) != updated[name] and name not in allowed
    )
    if stray:
        raise SystemExit(f"refusing to write: the register would also change {', '.join(stray)}")
    staged = workbook.with_name(f".{workbook.stem}.staging.xlsx")
    xlsx.write(str(staged), updated, infos)
    _confirm(staged, parts, allowed, generated)
    backup = workbook.with_name(
        f"{workbook.stem}.BACKUP-{datetime.now():%Y%m%d-%H%M%S}{workbook.suffix}"
    )
    shutil.copy2(workbook, backup)
    os.replace(staged, workbook)
    written = ", ".join(f"{sheet.name} ({len(sheet.rows)} rows)" for sheet in generated)
    print(f"wrote {written} into {workbook.name}; original kept as {backup.name}")


def _index(workbook: Path, generated: list[xlsx.Sheet]) -> list[xlsx.IndexEntry]:
    book = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    written = {sheet.name: sheet for sheet in generated}
    entries = []
    for name, layer in INDEXED.items():
        if sheet := written.get(name):
            entries.append(xlsx.IndexEntry(name, layer, sheet.title, len(sheet.rows), sheet.note))
            continue
        prefix = name.split("_", 1)[0] + "_"
        sheet = book[next(title for title in book.sheetnames if title.startswith(prefix))]
        values = list(sheet.iter_rows(min_row=1, max_row=2, max_col=1, values_only=True))
        title = str(values[0][0])
        if layer == "ARCHIVE" and not title.startswith(xlsx.SUPERSEDED):
            title = xlsx.SUPERSEDED + title
        data_rows = sum(
            1
            for row in sheet.iter_rows(min_row=6, values_only=True)
            if any(v is not None for v in row)
        )
        entries.append(xlsx.IndexEntry(name, layer, title, data_rows, str(values[1][0] or "")))
    return entries


def _confirm(
    staged: Path, original: xlsx.Parts, allowed: set[str], generated: list[xlsx.Sheet]
) -> None:
    """Unchanged parts stay byte-identical, charts included, and every sheet reads back."""
    written, _ = xlsx.read(str(staged))
    moved = sorted(
        name for name in original if name not in allowed and written.get(name) != original[name]
    )
    if moved:
        raise SystemExit(f"refusing to replace the workbook: {', '.join(moved)} changed")
    charts = [name for name in original if "/charts/" in name or "/drawings/" in name]
    if any(written.get(name) != original[name] for name in charts):
        raise SystemExit("refusing to replace the workbook: a chart or drawing changed")
    book = openpyxl.load_workbook(staged, read_only=True)
    for sheet in generated:
        body = sum(1 for row in book[sheet.name].iter_rows(min_row=6, values_only=True) if row[0])
        if body != len(sheet.rows):
            raise SystemExit(
                f"refusing to replace the workbook: {sheet.name} read back {body} rows, "
                f"not {len(sheet.rows)}"
            )
    print(
        f"checked: {len(original) - len(allowed & original.keys())} parts unchanged, "
        f"{len(charts)} chart and drawing parts intact, "
        f"{sum(len(sheet.rows) for sheet in generated)} generated rows read back"
    )


if __name__ == "__main__":
    raise SystemExit(main())
