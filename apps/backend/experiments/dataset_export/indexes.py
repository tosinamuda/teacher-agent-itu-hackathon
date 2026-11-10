"""Tables that index a dataset's own files, so the Hub's Dataset Viewer can show them.

Every row is read from a file the dataset already publishes and names that file, so an index adds
no data: it lays out what is there as rows, with a path back to the original. A row that cannot be
traced to its file stops the export rather than shipping without its reference.
"""

from __future__ import annotations

import csv
import io
import re
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterable, Mapping
from pathlib import PurePosixPath

from openpyxl import load_workbook

from .build import Entry, Release
from .rewrite import ExportError
from .sources import COMPLETE_RATINGS

RATINGS_WORKBOOK = f"ratings/workbooks/{COMPLETE_RATINGS}"
DELIVERED = "ratings/delivered"
RATER_FOLDER = re.compile(r"/Rater (\d+)/")
PACKET = re.compile(r"\bh[12]-pkt-\d+\b")

LESSON_STEP_COLUMNS = (
    "lesson_id",
    "term",
    "week",
    "topic",
    "subtopic",
    "step_id",
    "step_order",
    "step_kind",
    "step_title",
    "minutes",
    "instructional_type",
    "objective_id",
    "objective",
    "knowledge_component_type",
    "curriculum_objective_id",
    "plan_content",
    "lesson_file",
    "note_file",
    "transcript_file",
    "classwork_file",
)

Files = Mapping[str, Entry]


def indexed(release: Release) -> Release:
    """The release with its index tables added, or unchanged if it has none."""
    build = INDEXES.get(release.name)
    if build is None:
        return release
    tables = build({entry.path: entry for entry in release.entries})
    return Release(release.name, release.sources, release.entries + tuple(tables), release.left_out)


def _ratings(files: Files) -> list[Entry]:
    workbook = load_workbook(
        io.BytesIO(files[RATINGS_WORKBOOK].body), read_only=True, data_only=True
    )
    documents = _delivered_documents(files)
    return [
        _rating_table(
            "ratings/part1_ratings.csv",
            workbook["H1 scores"].iter_rows(values_only=True),
            documents,
        ),
        _rating_table(
            "ratings/part2_judgements.csv",
            workbook["H2 comparisons"].iter_rows(values_only=True),
            documents,
        ),
        _rating_table(
            "ratings/documents.csv",
            workbook["Coverage"].iter_rows(values_only=True),
            documents,
        ),
    ]


def _delivered_documents(files: Files) -> dict[tuple[str, str], str]:
    """Each returned rating document, by the rater and external packet it belongs to."""
    documents: dict[tuple[str, str], str] = {}
    for path in files:
        if not (path.startswith(f"{DELIVERED}/") and path.endswith(".docx")):
            continue
        rater, packet = RATER_FOLDER.search(path), PACKET.search(PurePosixPath(path).name)
        if rater is None or packet is None:
            continue
        key = (f"rater-{rater.group(1)}", packet.group(0))
        if key in documents:
            raise ExportError(f"{path}: a second document for {key[0]} and {key[1]}")
        documents[key] = path
    return documents


def _rating_table(
    path: str, rows: Iterable[tuple[object, ...]], documents: Mapping[tuple[str, str], str]
) -> Entry:
    rows = iter(rows)
    header = [str(name) for name in next(rows)]
    table = [[*header, "document"]]
    for row in rows:
        if all(value is None for value in row):
            continue
        record = dict(zip(header, row, strict=True))
        key = (str(record["rater"]), str(record["external_packet_id"]))
        if key not in documents:
            raise ExportError(f"{path}: no returned document for {key[0]} and {key[1]}")
        table.append([_cell(value) for value in row] + [documents[key]])
    return _csv_entry(path, table, (RATINGS_WORKBOOK, DELIVERED))


def _lesson_steps(files: Files) -> list[Entry]:
    lessons = sorted(path for path in files if re.fullmatch(r"lessons/[^/]+\.xml", path))
    table = [list(LESSON_STEP_COLUMNS)]
    for path in lessons:
        table += _steps_of(path, ET.fromstring(files[path].body), files)
    return [_csv_entry("lessons/steps.csv", table, ("lessons", "notes", "transcripts"))]


def _steps_of(path: str, lesson: ET.Element, files: Files) -> list[list[str]]:
    lesson_id = lesson.attrib["id"]
    objectives = {item.attrib["id"]: item for item in lesson.iterfind("objectives/objective")}
    transcript = _present(files, f"transcripts/{lesson_id}/teacher-cleaned.md", required=True)
    classwork = _present(files, f"transcripts/{lesson_id}/classwork.xml", required=False)
    rows = []
    for order, step in enumerate(lesson.iterfind("step"), start=1):
        objective = objectives.get(step.attrib.get("objective", ""))
        note = step.find("note")
        rows.append(
            [
                lesson_id,
                lesson.attrib.get("term", ""),
                lesson.attrib.get("week", ""),
                lesson.attrib.get("topic", ""),
                lesson.attrib.get("subtopic", ""),
                step.attrib["id"],
                str(order),
                step.attrib.get("kind", ""),
                step.attrib.get("title", ""),
                step.attrib.get("minutes", ""),
                step.attrib.get("instructional-type", ""),
                step.attrib.get("objective", ""),
                _text(objective),
                objective.attrib.get("kc-type", "") if objective is not None else "",
                objective.attrib.get("curriculum", "") if objective is not None else "",
                _text(step.find("plan-content")),
                path,
                _note_path(files, lesson_id, note) if note is not None else "",
                transcript,
                classwork,
            ]
        )
    return rows


def _note_path(files: Files, lesson_id: str, note: ET.Element) -> str:
    """Where a step's note is published; the lesson points at it by its name in the study's tree."""
    return _present(
        files, f"notes/{lesson_id}/{PurePosixPath(note.attrib['src']).name}", required=True
    )


def _present(files: Files, path: str, *, required: bool) -> str:
    if path in files:
        return path
    if required:
        raise ExportError(f"{path}: an index points at it, but the dataset does not hold it")
    return ""


def _text(element: ET.Element | None) -> str:
    return " ".join("".join(element.itertext()).split()) if element is not None else ""


def _cell(value: object) -> str:
    return "" if value is None else str(value)


def _csv_entry(path: str, table: list[list[str]], sources: tuple[str, ...]) -> Entry:
    out = io.StringIO()
    csv.writer(out, lineterminator="\n").writerows(table)
    body = out.getvalue().encode("utf-8")
    return Entry(path, body, body, derived_from=sources)


INDEXES: dict[str, Callable[[Files], list[Entry]]] = {
    "ng-jss1-math-lesson-plans": _lesson_steps,
    "ng-jss1-math-alignment-ratings": _ratings,
}
