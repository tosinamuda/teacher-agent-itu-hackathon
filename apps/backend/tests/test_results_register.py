"""The results register: its reproduction check, its exact tests, and its XML-only write."""

from __future__ import annotations

import zipfile
from fractions import Fraction
from pathlib import Path

import numpy
import openpyxl
import pytest

from experiments.human_rating.register import comments, xlsx
from experiments.human_rating.register.exact import (
    cluster_sign_flip,
    sign_flip,
    signed_rank,
    signed_rank_two_sided,
)
from experiments.human_rating.register.record import Printed, Result, agrees


@pytest.mark.parametrize(
    ("value", "printed", "expected"),
    [
        (0.3333, "+0.333", True),
        (0.0136, ".0136", True),
        (0.01361, ".0136", True),
        (0.0139, ".0136", False),
        (0.9406, "94.1%", True),
        (8422.2, "8,422", True),
        (-0.0032, "-0.003", True),
        (-0.0032, "−0.003", True),
        (0.3125, ".313", True),
    ],
)
def test_a_value_agrees_with_a_figure_to_the_precision_it_is_printed(value, printed, expected):
    assert agrees(value, printed) is expected


def _result(*figures: Printed) -> Result:
    return Result(
        id="x",
        part="p",
        question="q",
        quantity="q",
        estimate=figures[0],
        also=tuple(("also", f) for f in figures[1:]),
    )


def test_a_row_reports_how_many_of_its_printed_figures_were_recomputed():
    assert _result(Printed("0.5", 0.5), Printed("95/101", "95/101")).reproduces() == "yes"
    assert _result(Printed("0.5", 0.6)).reproduces() == "NO"
    assert _result(Printed("0.5", 0.5), Printed("7", None)).reproduces() == "partly (1 of 2)"
    assert _result(Printed("0.5", None)).reproduces() == "not recomputed"


def test_equal_differences_share_a_midrank_because_they_are_carried_exactly():
    third = Fraction(1, 3)
    exact = [third, -(Fraction(2, 3) - third), Fraction(1, 2)]
    split = [third + Fraction(1, 10**12), -third, Fraction(1, 2)]
    assert signed_rank(exact) == (0.375, 3)
    assert signed_rank(split) == (0.25, 3)


def test_the_exact_tests_reach_their_design_floors():
    assert sign_flip([1, 2, 3, 4, 5]) == 1 / 32
    assert cluster_sign_flip({str(i): [Fraction(1)] for i in range(6)}) == 1 / 64
    assert signed_rank([Fraction(1)] * 6)[0] == 1 / 64
    assert signed_rank_two_sided([Fraction(-1)] * 6) == 2 / 64


# A workbook in the Open XML SDK's prefixed form, with a chart part the write must not touch.
MAIN = xlsx.MAIN
REL = xlsx.RELATIONSHIPS
SHEETS = [
    "00_Start",
    "44_Reported_Statistics",
    "45_P2_Result_History",
    "58_Agreement_Recomputed",
    "59_Number_Provenance",
]


DECLARATION = '<?xml version="1.0" encoding="utf-8"?>'
PACKAGE = "http://schemas.openxmlformats.org/package/2006"
BOM = "\ufeff"


def _sheet_xml(title: str, note: str, rows: list[list[str]], table: bool) -> str:
    body = [
        f'<x:row r="1"><x:c r="A1" s="58" t="str"><x:v>{title}</x:v></x:c></x:row>',
        f'<x:row r="2"><x:c r="A2" s="59" t="str"><x:v>{note}</x:v></x:c></x:row>',
    ]
    for number, row in enumerate(rows, start=5):
        cells = "".join(
            f'<x:c r="{xlsx.column(i)}{number}" s="20" t="str"><x:v>{v}</x:v></x:c>'
            for i, v in enumerate(row)
        )
        body.append(f'<x:row r="{number}">{cells}</x:row>')
    part = f'<x:tableParts count="1"><x:tablePart r:id="Rt" xmlns:r="{REL}" />' if table else ""
    part += "</x:tableParts>" if table else ""
    sheet = f'<x:worksheet xmlns:x="{MAIN}"><x:sheetData>{"".join(body)}</x:sheetData>'
    return f"{DECLARATION}{sheet}{part}</x:worksheet>"


def _relationships(*links: tuple[str, str, str]) -> str:
    body = "".join(
        f'<Relationship Type="{t}" Target="{target}" Id="{i}" />' for t, target, i in links
    )
    return (
        f'{BOM}{DECLARATION}<Relationships xmlns="{PACKAGE}/relationships">{body}</Relationships>'
    )


def _content_types() -> str:
    overrides = [(f"/xl/worksheets/sheet{i}.xml", xlsx.WORKSHEET_CONTENT) for i in range(1, 6)]
    overrides += [("/xl/tables/table1.xml", xlsx.TABLE_CONTENT)]
    defaults = [
        ("xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"),
        ("rels", "application/vnd.openxmlformats-package.relationships+xml"),
    ]
    body = "".join(f'<Default Extension="{ext}" ContentType="{kind}" />' for ext, kind in defaults)
    body += "".join(
        f'<Override PartName="{name}" ContentType="{kind}" />' for name, kind in overrides
    )
    return f'{BOM}{DECLARATION}<Types xmlns="{PACKAGE}/content-types">{body}</Types>'


def _fixture(path: Path) -> None:
    index = [["Worksheet", "Layer", "Contents", "Rows", "Traceability note"]] + [
        [name, "LAYER", f"{name} TITLE", "1", "note"] for name in SHEETS
    ]
    sheets = {
        "00_Start": _sheet_xml("RESEARCH DATA WORKBOOK", "guide", index, table=True),
        "44_Reported_Statistics": _sheet_xml("REPORTED STATISTICS", "kept", [["Study"]], False),
        "45_P2_Result_History": _sheet_xml("PART 2 HISTORY", "kept", [["result_id"]], False),
        "58_Agreement_Recomputed": _sheet_xml(
            "AGREEMENT", "44_Reported_Statistics carries kappas", [["Study"]], False
        ),
        "59_Number_Provenance": _sheet_xml(
            "PROVENANCE", "every number", [["Paper"], ["44_Reported_Statistics"]], False
        ),
    }
    sheet_list = "".join(
        f'<x:sheet name="{n}" sheetId="{i}" r:id="Rs{i}" xmlns:r="{REL}" />'
        for i, n in enumerate(SHEETS, start=1)
    )
    columns = "".join(f'<x:tableColumn id="{i}" name="{n}" />' for i, n in enumerate(index[0], 1))
    parts = {
        "[Content_Types].xml": _content_types(),
        "_rels/.rels": _relationships((f"{REL}/officeDocument", "/xl/workbook.xml", "R1")),
        "xl/workbook.xml": f'{DECLARATION}<x:workbook xmlns:x="{MAIN}"><x:sheets>{sheet_list}'
        "</x:sheets></x:workbook>",
        "xl/_rels/workbook.xml.rels": _relationships(
            *((xlsx.WORKSHEET_TYPE, f"/xl/worksheets/sheet{i}.xml", f"Rs{i}") for i in range(1, 6))
        ),
        "xl/worksheets/_rels/sheet1.xml.rels": _relationships(
            (xlsx.TABLE_TYPE, "/xl/tables/table1.xml", "Rt")
        ),
        "xl/tables/table1.xml": f'{DECLARATION}<x:table id="1" name="T_Index" '
        'displayName="T_Index" '
        f'ref="A5:E{5 + len(SHEETS)}" headerRowCount="1" xmlns:x="{MAIN}">'
        f'<x:tableColumns count="5">{columns}</x:tableColumns></x:table>',
        "xl/charts/chart1.xml": f"{DECLARATION}<chart>a chart the write must not touch</chart>",
    }
    for number, name in enumerate(SHEETS, start=1):
        parts[f"xl/worksheets/sheet{number}.xml"] = sheets[name]
    with zipfile.ZipFile(path, "w") as archive:
        for name, text in parts.items():
            archive.writestr(name, text.encode())


GENERATED = [
    xlsx.Sheet(
        xlsx.REGISTER,
        "RESULTS REGISTER",
        "one list",
        ["ID", "Estimate"],
        [["P1-H1c", "+0.333"], ["P2-H2", "+0.455"]],
        (14, 12),
    ),
    xlsx.Sheet(
        "61_Mixed_Models",
        "MIXED MODELS",
        "fits",
        ["Fit", "Observations", "Estimate"],
        [["primary", 405, numpy.float64(0.30784)]],
        (14, 12, 12),
    ),
]


def _write(path: Path) -> xlsx.Parts:
    parts, infos = xlsx.read(str(path))
    index = [
        xlsx.IndexEntry(
            "44_Archive_Reported_Statistics", "ARCHIVE", "44_Reported_Statistics TITLE", 1, "note"
        ),
        *(xlsx.IndexEntry(s.name, "RESULTS", s.title, len(s.rows), s.note) for s in GENERATED),
    ]
    updated = xlsx.with_sheets(parts, GENERATED, index)
    allowed = xlsx.edited_parts(updated, [sheet.name for sheet in GENERATED])
    stray = [n for n in updated if parts.get(n) != updated[n] and n not in allowed]
    assert stray == []
    xlsx.write(str(path), updated, infos)
    return parts


def test_the_register_is_written_beside_the_existing_parts_without_touching_the_chart(tmp_path):
    path = tmp_path / "book.xlsx"
    _fixture(path)
    before = _write(path)
    after, _ = xlsx.read(str(path))
    assert after["xl/charts/chart1.xml"] == before["xl/charts/chart1.xml"]
    book = openpyxl.load_workbook(path, read_only=True)
    assert book.sheetnames == [
        "00_Start",
        "44_Archive_Reported_Statistics",
        "45_Archive_P2_Result_History",
        "58_Agreement_Recomputed",
        "59_Number_Provenance",
        xlsx.REGISTER,
        "61_Mixed_Models",
    ]
    register = list(book[xlsx.REGISTER].iter_rows(min_row=5, values_only=True))
    assert register == [("ID", "Estimate"), ("P1-H1c", "+0.333"), ("P2-H2", "+0.455")]
    archived = next(book["44_Archive_Reported_Statistics"].iter_rows(max_row=1, values_only=True))[
        0
    ]
    assert archived == f"{xlsx.SUPERSEDED}REPORTED STATISTICS"
    note = next(book["58_Agreement_Recomputed"].iter_rows(min_row=2, max_row=2, values_only=True))[
        0
    ]
    assert note.startswith("44_Archive_Reported_Statistics carries")
    models = list(book["61_Mixed_Models"].iter_rows(min_row=6, values_only=True))
    assert models == [("primary", 405, 0.30784)]
    index = [row[0] for row in book["00_Start"].iter_rows(min_row=6, values_only=True)]
    assert index[-2:] == [xlsx.REGISTER, "61_Mixed_Models"]
    assert f'ref="A5:E{5 + len(SHEETS) + 2}"' in after["xl/tables/table1.xml"].decode()
    tables = {after[name] for name in after if name.startswith("xl/tables/")}
    assert len(tables) == 3


def test_writing_the_register_again_changes_nothing(tmp_path):
    path = tmp_path / "book.xlsx"
    _fixture(path)
    _write(path)
    first, _ = xlsx.read(str(path))
    _write(path)
    second, _ = xlsx.read(str(path))
    assert [name for name in first if first[name] != second[name]] == []


class _Comments:
    """A stand-in for the workbook's sources, holding only the comments sheet."""

    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows

    def sheet(self, name: str) -> list[dict[str, object]]:
        assert name == comments.COMMENTS
        return self.rows


def _comment(key: tuple[str, str, str, str], text: str, arm: str) -> dict[str, object]:
    rater, learner, objective, criterion = key
    return {
        "Rater": rater,
        "Learner": learner,
        "Objective": objective,
        "Criterion": criterion,
        "Comment": text,
        "Preferred arm": arm,
    }


def _all_comments() -> list[dict[str, object]]:
    arm = {reading: recorded for recorded, reading in comments.ARM.items()}
    return [
        _comment(key, f"... {coding.quote} ...", arm[coding.favours])
        for key, coding in comments.CODED.items()
    ]


def test_every_comment_carries_one_code_from_the_fixed_set_and_a_reading():
    assert {coding.code for coding in comments.CODED.values()} <= comments.CODEBOOK.keys()
    assert all(coding.reading for coding in comments.CODED.values())
    coded = comments.coded(_Comments(_all_comments()))  # type: ignore[arg-type]
    assert len(coded) == len(comments.CODED)


def test_a_comment_without_a_coding_or_with_other_words_is_refused():
    rows = _all_comments()
    with pytest.raises(ValueError, match="out of step"):
        comments.coded(_Comments(rows[1:]))  # type: ignore[arg-type]
    rows[0] = {**rows[0], "Comment": "a comment the coding does not quote"}
    with pytest.raises(ValueError, match="deciding words"):
        comments.coded(_Comments(rows))  # type: ignore[arg-type]


def test_a_comment_read_as_favouring_the_other_material_is_refused():
    rows = _all_comments()
    rows[0] = {**rows[0], "Preferred arm": "P0" if rows[0]["Preferred arm"] == "P1" else "P1"}
    with pytest.raises(ValueError, match="read as favouring"):
        comments.coded(_Comments(rows))  # type: ignore[arg-type]


def test_only_the_error_codes_take_a_side_on_personalisation():
    sided = {name: code.direction for name, code in comments.CODEBOOK.items()}
    assert sided.pop(comments.OWN_ERROR) == comments.FOR
    assert sided.pop(comments.ERROR_TYPE) == comments.AGAINST
    assert set(sided.values()) == {comments.EITHER}
