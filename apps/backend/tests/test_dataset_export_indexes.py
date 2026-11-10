"""Index tables: every row read from a published file and naming it; nothing untraceable ships."""

from __future__ import annotations

import csv
import io

import pytest
from openpyxl import Workbook

from experiments.dataset_export.build import Entry, Release, provenance
from experiments.dataset_export.indexes import RATINGS_WORKBOOK, indexed
from experiments.dataset_export.rewrite import ExportError

PART1 = "ratings/delivered/Part 1 - Class revision material"
PART2 = "ratings/delivered/Part 2 - Student-specific revision material"
H1_HEADER = ("rater", "external_packet_id", "criterion", "score", "comment")
H2_HEADER = ("rater", "external_packet_id", "criterion", "chose", "favoured_arm")
DOCUMENTS_HEADER = ("rater", "external_packet_id", "state", "date_completed", "closing_comment")
DOCUMENTS = [
    ("rater-2", "h1-pkt-033", "complete", "September 2nd, 2026.", "Clear throughout."),
    ("rater-1", "h2-pkt-004", "complete", "", ""),
]


def _copied(path: str, body: bytes = b"x") -> Entry:
    return Entry(path, body, body)


def _workbook(h1_rows: list[tuple], h2_rows: list[tuple]) -> bytes:
    book = Workbook()
    book.remove(book.active)
    for title, header, rows in (
        ("H1 scores", H1_HEADER, h1_rows),
        ("H2 comparisons", H2_HEADER, h2_rows),
        ("Coverage", DOCUMENTS_HEADER, DOCUMENTS),
    ):
        sheet = book.create_sheet(title)
        sheet.append(header)
        for row in rows:
            sheet.append(row)
    out = io.BytesIO()
    book.save(out)
    return out.getvalue()


def _ratings_release(h1_rows: list[tuple]) -> Release:
    entries = (
        _copied(
            RATINGS_WORKBOOK,
            _workbook(h1_rows, [("rater-1", "h2-pkt-004", 1, "B clearly better", "P1")]),
        ),
        _copied(f"{PART1}/Rater 2/R2-P1-01 h1-pkt-033.docx"),
        _copied(f"{PART1}/Rater 2/R2-00 General instructions.docx"),
        _copied(f"{PART2}/Rater 1/R1-P2-01 h2-pkt-004.docx"),
    )
    return Release("ng-jss1-math-alignment-ratings", (), entries, ())


def _table(release: Release, path: str) -> list[list[str]]:
    body = next(entry.body for entry in release.entries if entry.path == path)
    return list(csv.reader(io.StringIO(body.decode("utf-8"))))


def test_each_rating_is_a_row_that_names_the_document_it_was_returned_in():
    release = indexed(_ratings_release([("rater-2", "h1-pkt-033", 1, 5, None)]))
    part1 = _table(release, "ratings/part1_ratings.csv")
    assert part1 == [
        [*H1_HEADER, "document"],
        ["rater-2", "h1-pkt-033", "1", "5", "", f"{PART1}/Rater 2/R2-P1-01 h1-pkt-033.docx"],
    ]
    part2 = _table(release, "ratings/part2_judgements.csv")
    assert part2[1][-1] == f"{PART2}/Rater 1/R1-P2-01 h2-pkt-004.docx"


def test_each_returned_document_is_a_row_with_its_date_and_closing_comment():
    documents = _table(
        indexed(_ratings_release([("rater-2", "h1-pkt-033", 1, 5, None)])),
        "ratings/documents.csv",
    )
    assert documents == [
        [*DOCUMENTS_HEADER, "document"],
        [*DOCUMENTS[0], f"{PART1}/Rater 2/R2-P1-01 h1-pkt-033.docx"],
        [*DOCUMENTS[1], f"{PART2}/Rater 1/R1-P2-01 h2-pkt-004.docx"],
    ]


def test_a_rating_with_no_returned_document_stops_the_export():
    with pytest.raises(ExportError, match="rater-3 and h1-pkt-099"):
        indexed(_ratings_release([("rater-3", "h1-pkt-099", 1, 4, None)]))


LESSON = "\n".join(
    (
        '<lesson id="t9-w01" term="First Term" week="1" topic="Fractions" subtopic="Adding">',
        '  <objectives><objective id="lo-1" curriculum="po-1" kc-type="procedure">',
        "    add two fractions</objective></objectives>",
        '  <step id="s-1" kind="intro" minutes="5" title="Step I">',
        "    <plan-content>Recall   halves.</plan-content></step>",
        '  <step id="s-2" kind="core" objective="lo-1" minutes="10" title="Step II">',
        "    <plan-content>Work an example.</plan-content>",
        '    <note src="../notes-clean/t9-w01/s-2.md" sha256="00"/>',
        "  </step>",
        "</lesson>",
    )
).encode("utf-8")


def _lesson_release(*extra: str) -> Release:
    files = ("lessons/t9-w01.xml", "transcripts/t9-w01/teacher-cleaned.md", *extra)
    entries = tuple(_copied(path, LESSON if path.endswith(".xml") else b"x") for path in files)
    return Release("ng-jss1-math-lesson-plans", (), entries, ())


def test_each_lesson_step_is_a_row_that_points_at_its_lesson_note_and_transcript():
    rows = _table(indexed(_lesson_release("notes/t9-w01/s-2.md")), "lessons/steps.csv")
    header, intro, core = rows
    step = dict(zip(header, core, strict=True))
    assert dict(zip(header, intro, strict=True))["plan_content"] == "Recall halves."
    assert step["objective"] == "add two fractions"
    assert step["knowledge_component_type"] == "procedure"
    assert step["note_file"] == "notes/t9-w01/s-2.md"
    assert step["transcript_file"] == "transcripts/t9-w01/teacher-cleaned.md"
    assert step["classwork_file"] == ""


def test_a_step_whose_note_is_not_published_stops_the_export():
    with pytest.raises(ExportError, match="notes/t9-w01/s-2.md"):
        indexed(_lesson_release())


def test_provenance_marks_an_index_as_built_from_the_files_it_names():
    release = indexed(_lesson_release("notes/t9-w01/s-2.md"))
    record = {file["path"]: file for file in provenance(release)["files"]}
    assert record["lessons/steps.csv"]["derived_from"] == ["lessons", "notes", "transcripts"]
    assert "derived_from" not in record["lessons/t9-w01.xml"]


def test_a_dataset_without_an_index_is_left_as_it_is():
    release = Release("ng-jss1-math-curriculum", (), (_copied("curriculum/a.json"),), ())
    assert indexed(release) is release
