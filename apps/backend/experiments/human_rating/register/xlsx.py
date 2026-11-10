"""Write the register into the workbook by editing its XML parts, and nothing else.

The workbook holds native charts and Excel tables that openpyxl drops when it saves, so each
generated sheet — the register and the sheets it is computed through — is written as parts added
beside the existing ones: a worksheet, its table and their relationships. The only existing parts
edited are the ones that name sheets — the workbook's sheet list and relationships, the content
types, the start sheet's index and its table, the two archived sheets' titles, and two notes that
name the first archived sheet. ``edited_parts`` states that set, and a write fails if any other
part would change.
"""

from __future__ import annotations

import re
import zipfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from xml.sax.saxutils import escape

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RELATIONSHIPS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORKSHEET_TYPE = f"{RELATIONSHIPS}/worksheet"
TABLE_TYPE = f"{RELATIONSHIPS}/table"
WORKSHEET_CONTENT = "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"
TABLE_CONTENT = "application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"

REGISTER = "60_Results_Register"
ARCHIVED = {
    "44_Reported_Statistics": "44_Archive_Reported_Statistics",
    "45_P2_Result_History": "45_Archive_P2_Result_History",
}
SUPERSEDED = f"ARCHIVE, SUPERSEDED BY {REGISTER} | "
TITLE_STYLE, NOTE_STYLE, HEADER_STYLE, KEY_STYLE, BODY_STYLE, INDEX_STYLE = 58, 59, 62, 72, 18, 20
#: The workbook's own four-decimal number style, for every fractional value a sheet carries.
DECIMAL_STYLE = 40
HEADER_ROW = 5

Parts = dict[str, bytes]


@dataclass(frozen=True)
class Sheet:
    """A generated sheet: a title, a note, and one table under a header on row 5."""

    name: str
    title: str
    note: str
    header: Sequence[str]
    rows: Sequence[Sequence[object]]
    widths: Sequence[int]
    #: Leading columns that identify a row, set in the key style.
    keys: int = 1


@dataclass(frozen=True)
class IndexEntry:
    sheet: str
    layer: str
    contents: str
    rows: int
    note: str


def read(path: str) -> tuple[Parts, list[zipfile.ZipInfo]]:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        return {info.filename: archive.read(info.filename) for info in infos}, infos


def write(path: str, parts: Parts, infos: Sequence[zipfile.ZipInfo]) -> None:
    """The parts in the original order, each with its original compression; new parts last."""
    known = {info.filename for info in infos}
    with zipfile.ZipFile(path, "w") as archive:
        for info in infos:
            archive.writestr(info, parts[info.filename], compress_type=info.compress_type)
        for name in sorted(parts.keys() - known):
            archive.writestr(name, parts[name], compress_type=zipfile.ZIP_DEFLATED)


def edited_parts(parts: Parts, generated: Iterable[str]) -> set[str]:
    """Every part a write may add or change; any other difference is a failure."""
    sheets = _sheet_parts(parts)
    written = [part for name in generated if (part := sheets.get(name))]
    return {
        "[Content_Types].xml",
        "xl/workbook.xml",
        "xl/_rels/workbook.xml.rels",
        sheets["00_Start"],
        _table_of(parts, sheets["00_Start"]),
        *(sheets.get(old) or sheets[new] for old, new in ARCHIVED.items()),
        sheets["58_Agreement_Recomputed"],
        sheets["59_Number_Provenance"],
        *written,
        *(_rels_of(part) for part in written),
        *(_table_of(parts, part) for part in written),
    }


def with_sheets(parts: Parts, generated: Sequence[Sheet], index: Sequence[IndexEntry]) -> Parts:
    """The parts with each sheet written, the archived sheets marked, and the index set."""
    out = dict(parts)
    sheets = _sheet_parts(out)
    for old, new in ARCHIVED.items():
        if old in sheets:
            _rename_sheet(out, sheets, old, new)
    sheets = _sheet_parts(out)
    for new in ARCHIVED.values():
        out[sheets[new]] = _mark_superseded(out[sheets[new]])
    for sheet in generated:
        _put(out, sheet)
    _index(out, sheets["00_Start"], index)
    return out


def _put(parts: Parts, sheet: Sheet) -> None:
    existing = _sheet_parts(parts).get(sheet.name)
    sheet_part, table_part = (
        (existing, _table_of(parts, existing)) if existing else _new_parts(parts, sheet.name)
    )
    table_rid = f"{_rid(sheet.name)}table"
    parts[sheet_part] = _worksheet(sheet, table_rid)
    parts[_rels_of(sheet_part)] = _relationships([(table_rid, TABLE_TYPE, f"/{table_part}")])
    parts[table_part] = _table(parts, table_part, sheet, HEADER_ROW + len(sheet.rows))


def _rid(name: str) -> str:
    return "R" + re.sub(r"[^a-z0-9]", "", name.lower())


def _sheet_parts(parts: Parts) -> dict[str, str]:
    """Sheet name to worksheet part, read from the workbook and its relationships."""
    workbook = parts["xl/workbook.xml"].decode("utf-8")
    targets = dict(
        re.findall(
            r'Target="/?([^"]+)" Id="([^"]+)"',
            parts["xl/_rels/workbook.xml.rels"].decode("utf-8-sig"),
        )
    )
    by_id = {rid: target for target, rid in targets.items()}
    return {
        name: by_id[rid]
        for name, rid in re.findall(
            r'<x:sheet name="([^"]+)" sheetId="\d+" r:id="([^"]+)"', workbook
        )
    }


def _rels_of(part: str) -> str:
    folder, name = part.rsplit("/", 1)
    return f"{folder}/_rels/{name}.rels"


def _table_of(parts: Parts, sheet_part: str) -> str:
    rels = parts[_rels_of(sheet_part)].decode("utf-8-sig")
    found = re.search(r'Target="/?(xl/tables/[^"]+)"', rels)
    if found is None:
        raise ValueError(f"{sheet_part}: no table relationship")
    return found.group(1)


def _replace_once(text: str, old: str, new: str, where: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{where}: expected one {old[:60]!r}, found {text.count(old)}")
    return text.replace(old, new)


def _rename_sheet(parts: Parts, sheets: dict[str, str], old: str, new: str) -> None:
    workbook = parts["xl/workbook.xml"].decode("utf-8")
    parts["xl/workbook.xml"] = _replace_once(
        workbook, f'name="{old}"', f'name="{new}"', "workbook"
    ).encode("utf-8")
    for name in ("00_Start", "58_Agreement_Recomputed", "59_Number_Provenance"):
        part = sheets[name]
        parts[part] = renamed(parts[part].decode("utf-8")).encode("utf-8")


def renamed(text: str) -> str:
    """The text with every archived sheet called by its archive name."""
    for old, new in ARCHIVED.items():
        text = re.sub(rf"(?<![\w]){re.escape(old)}(?![\w])", new, text)
    return text


def _mark_superseded(body: bytes) -> bytes:
    text = body.decode("utf-8")
    if SUPERSEDED in text:
        return body
    return re.sub(
        r'(<x:c r="A1" [^>]*><x:v>)', rf"\g<1>{escape(SUPERSEDED)}", text, count=1
    ).encode("utf-8")


def _new_parts(parts: Parts, name: str) -> tuple[str, str]:
    sheet_numbers = [
        int(n)
        for n in re.findall(r"xl/worksheets/sheet(\d+)\.xml$", "\n".join(parts), re.MULTILINE)
    ]
    table_numbers = [
        int(n) for n in re.findall(r"xl/tables/table(\d+)\.xml$", "\n".join(parts), re.MULTILINE)
    ]
    sheet_part = f"xl/worksheets/sheet{max(sheet_numbers) + 1}.xml"
    table_part = f"xl/tables/table{max(table_numbers) + 1}.xml"
    workbook = parts["xl/workbook.xml"].decode("utf-8")
    sheet_id = max(int(n) for n in re.findall(r'sheetId="(\d+)"', workbook)) + 1
    entry = (
        f'<x:sheet name="{name}" sheetId="{sheet_id}" r:id="{_rid(name)}" '
        f'xmlns:r="{RELATIONSHIPS}" />'
    )
    parts["xl/workbook.xml"] = _replace_once(
        workbook, "</x:sheets>", f"{entry}</x:sheets>", "workbook"
    ).encode("utf-8")
    rels = parts["xl/_rels/workbook.xml.rels"].decode("utf-8-sig")
    link = f'<Relationship Type="{WORKSHEET_TYPE}" Target="/{sheet_part}" Id="{_rid(name)}" />'
    parts["xl/_rels/workbook.xml.rels"] = _bom(
        _replace_once(rels, "</Relationships>", f"{link}</Relationships>", "rels")
    )
    types = parts["[Content_Types].xml"].decode("utf-8-sig")
    overrides = (
        f'<Override PartName="/{sheet_part}" ContentType="{WORKSHEET_CONTENT}" />'
        f'<Override PartName="/{table_part}" ContentType="{TABLE_CONTENT}" />'
    )
    parts["[Content_Types].xml"] = _bom(
        _replace_once(types, "</Types>", f"{overrides}</Types>", "content types")
    )
    return sheet_part, table_part


def _bom(text: str) -> bytes:
    """The byte-order mark the workbook's package parts carry, kept so they stay as written."""
    return ("\ufeff" + text).encode("utf-8")


def _relationships(links: Sequence[tuple[str, str, str]]) -> bytes:
    body = "".join(
        f'<Relationship Type="{kind}" Target="{target}" Id="{rid}" />'
        for rid, kind, target in links
    )
    return _bom(
        f'<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>'
    )


def column(index: int) -> str:
    """Spreadsheet column letters for a zero-based index."""
    letters = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def _cell(row: int, index: int, value: object, style: int) -> str:
    reference = f"{column(index)}{row}"
    if value is None or value == "":
        return f'<x:c r="{reference}" s="{style}" />'
    if isinstance(value, float):
        return f'<x:c r="{reference}" s="{style}" t="n"><x:v>{float(value)!r}</x:v></x:c>'
    if isinstance(value, int) and not isinstance(value, bool):
        return f'<x:c r="{reference}" s="{style}" t="n"><x:v>{value}</x:v></x:c>'
    return f'<x:c r="{reference}" s="{style}" t="str"><x:v>{escape(str(value))}</x:v></x:c>'


def _row(
    number: int, values: Sequence[object], styles: Sequence[int], height: int | None = None
) -> str:
    size = f' ht="{height}" customHeight="1"' if height else ""
    cells = "".join(
        _cell(number, i, v, s) for i, (v, s) in enumerate(zip(values, styles, strict=True))
    )
    return f'<x:row r="{number}"{size}>{cells}</x:row>'


def _body_style(index: int, value: object, keys: int) -> int:
    if isinstance(value, float):
        return DECIMAL_STYLE
    return KEY_STYLE if index < keys else BODY_STYLE


def _worksheet(sheet: Sheet, table_rid: str) -> bytes:
    width = len(sheet.header)
    last = column(width - 1)
    cols = "".join(
        f'<x:col min="{i}" max="{i}" width="{w}" customWidth="1" />'
        for i, w in enumerate(sheet.widths[:width], start=1)
    )
    body = [
        _row(1, [sheet.title] + [None] * (width - 1), [TITLE_STYLE] * width, 34),
        _row(2, [sheet.note] + [None] * (width - 1), [NOTE_STYLE] * width, 40),
        _row(3, [None] * width, [NOTE_STYLE] * width, 40),
        _row(HEADER_ROW, list(sheet.header), [HEADER_STYLE] * width, 34),
        *(
            _row(
                HEADER_ROW + 1 + i,
                row,
                [_body_style(c, value, sheet.keys) for c, value in enumerate(row)],
            )
            for i, row in enumerate(sheet.rows)
        ),
    ]
    return (
        f'<?xml version="1.0" encoding="utf-8"?><x:worksheet xmlns:x="{MAIN}">'
        '<x:sheetViews><x:sheetView workbookViewId="0">'
        '<x:pane ySplit="5" topLeftCell="A6" activePane="bottomLeft" '
        'state="frozen" /></x:sheetView></x:sheetViews><x:sheetFormatPr defaultRowHeight="15" />'
        f"<x:cols>{cols}</x:cols><x:sheetData>{''.join(body)}</x:sheetData>"
        f'<x:mergeCells count="2"><x:mergeCell ref="A1:{last}1" />'
        f'<x:mergeCell ref="A2:{last}3" /></x:mergeCells>'
        '<x:pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" '
        'header="0.3" footer="0.3" />'
        f'<x:tableParts count="1"><x:tablePart r:id="{table_rid}" '
        f'xmlns:r="{RELATIONSHIPS}" /></x:tableParts>'
        "</x:worksheet>"
    ).encode()


def _table(parts: Parts, table_part: str, sheet: Sheet, last_row: int) -> bytes:
    existing = parts.get(table_part)
    ids = [
        int(n)
        for name, body in parts.items()
        if name.startswith("xl/tables/") and body is not existing
        for n in re.findall(rb'<x:table id="(\d+)"', body)
    ]
    table_id = int(_table_id(existing)) if existing else max(ids) + 1
    columns = "".join(
        f'<x:tableColumn id="{i}" name="{escape(name)}" />'
        for i, name in enumerate(sheet.header, start=1)
    )
    return (
        f'<?xml version="1.0" encoding="utf-8"?><x:table id="{table_id}" '
        f'name="T_{sheet.name}" displayName="T_{sheet.name}" '
        f'ref="A{HEADER_ROW}:{column(len(sheet.header) - 1)}{last_row}" headerRowCount="1" '
        f'totalsRowCount="0" totalsRowShown="0" xmlns:x="{MAIN}">'
        f'<x:tableColumns count="{len(sheet.header)}">{columns}</x:tableColumns>'
        '<x:tableStyleInfo name="TableStyleMedium2" showFirstColumn="0" showLastColumn="0" '
        'showRowStripes="1" showColumnStripes="0" /></x:table>'
    ).encode()


def _index(parts: Parts, start_part: str, index: Sequence[IndexEntry]) -> None:
    """Set each listed sheet's row in the start sheet's index, appending those it lacks."""
    text = parts[start_part].decode("utf-8")
    rows = {
        m.group(2): m
        for m in re.finditer(
            r'<x:row r="(\d+)"[^>]*><x:c r="A\d+" [^>]*><x:v>([^<]+)</x:v>.*?</x:row>', text
        )
    }
    last = max(int(m.group(1)) for m in rows.values())
    appended = []
    for entry in index:
        values = [
            entry.sheet,
            entry.layer,
            renamed(entry.contents),
            entry.rows,
            renamed(entry.note),
        ]
        if entry.sheet in rows:
            row = rows[entry.sheet].group(0)
            text = text.replace(row, _set_cells(row, int(rows[entry.sheet].group(1)), values))
        else:
            last += 1
            appended.append(_row(last, values, [INDEX_STYLE] * 5, 38))
    text = _replace_once(
        text, "</x:sheetData>", "".join(appended) + "</x:sheetData>", "start sheet"
    )
    parts[start_part] = text.encode("utf-8")
    table_part = _table_of(parts, start_part)
    table = parts[table_part].decode("utf-8")
    parts[table_part] = re.sub(r'ref="A5:E\d+"', f'ref="A5:E{last}"', table, count=1).encode(
        "utf-8"
    )


def _set_cells(row: str, number: int, values: Sequence[object]) -> str:
    """The row with its first cells replaced by ``values``; any cell further along is kept."""
    for index, value in enumerate(values):
        reference = f"{column(index)}{number}"
        pattern = rf'<x:c r="{reference}" [^>]*?(?:/>|>.*?</x:c>)'
        row = _replace_count(row, pattern, _cell(number, index, value, INDEX_STYLE), reference)
    return row


def _replace_count(text: str, pattern: str, new: str, where: str) -> str:
    replaced, count = re.subn(pattern, lambda _: new, text, count=1)
    if count != 1:
        raise ValueError(f"{where}: cell not found")
    return replaced


def _table_id(table: bytes) -> bytes:
    found = re.search(rb'<x:table id="(\d+)"', table)
    if found is None:
        raise ValueError("table part has no id")
    return found.group(1)
