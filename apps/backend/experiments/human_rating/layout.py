"""How the written document looks: page, fonts, tables, footer, breaks.

The look follows the worksheet raters have seen before — an institution band over a
serif A4 page, reference tables with a shaded label column, hairline grids, and a
footer naming the set on the left and the page on the right — so a set reads as the
next sheet in the same study, not a new instrument.
"""

from __future__ import annotations

from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor
from docx.text.paragraph import Paragraph

from app.config import CONFIG

from .forms import (
    BOX,
    GRID,
    GUIDE,
    KEY_VALUE,
    LEAN,
    LEARNER,
    RUBRIC,
    STEPS,
    kind_of,
)

#: Each is a paragraph of its own in the markdown. The page after a break starts on a
#: new sheet; a rule becomes a hairline under the paragraph that precedes it.
PAGE_BREAK = "[[[page-break]]]"
RULE = "[[[rule]]]"
#: The shape the pages after this sentinel are cut to. A landscape run gives a
#: side-by-side comparison a column each that is wider than the drawings in it, so
#: nothing has to be shrunk to be set beside anything else.
PORTRAIT, LANDSCAPE = "portrait", "landscape"
SHAPE = {PORTRAIT: "[[[portrait]]]", LANDSCAPE: "[[[landscape]]]"}
_SHAPE_OF = {sentinel: shape for shape, sentinel in SHAPE.items()}
PAGE_MM = {PORTRAIT: (210, 297), LANDSCAPE: (297, 210)}
MARGIN = Mm(16)
#: A block of one comparison, opened by its own label over a hairline. The two blocks a
#: rater weighs against each other are too long to sit in columns, so they are stacked at
#: full width and told apart by their labels.
PANEL = "**{}**"


def titled_page(title: str) -> list[str]:
    """A page of its own, opening with its title.

    Not ``section``: both documents bind that name to a pack's sections while iterating.
    """
    return [PAGE_BREAK, "", f"## {title}", ""]


def shaped_page(title: str, shape: str) -> list[str]:
    """A page of its own in the given shape. The break between shapes opens the page."""
    return [SHAPE[shape], "", f"## {title}", ""]


FONT = "Times New Roman"
BODY = Pt(10)
SMALL = Pt(8.5)
INK = RGBColor(0x11, 0x11, 0x11)
MUTED = RGBColor(0x55, 0x55, 0x55)
RULE_GREY = "9A9A9A"
#: The instruction on a page, in the one colour nothing else in the document uses.
INSTRUCTION_RED = "C00000"
GRID_GREY = "CFCFCF"
FILL = "F2F2F2"
HEADINGS = {"Heading 1": 18, "Heading 2": 14, "Heading 3": 11.5, "Heading 4": 10.5, "Heading 5": 10}
SMALL_PRINT = (CONFIG.study_title,)
_BOOKMARK_TAGS = {qn("w:bookmarkStart"), qn("w:bookmarkEnd")}


def finish(document, footer_left: str) -> None:
    kinds = _table_kinds(document)
    _strip_bookmarks(document)
    _break_pages(document)
    _rules(document)
    _tables(document, kinds)
    _shape_pages(document)
    _fit_tables(document)
    _small_print(document)
    _footer(document, footer_left)


def _table_kinds(document) -> dict:
    """Which authored table each pandoc bookmark names: the bookmark sits just before it."""
    kinds = {}
    pending = None
    for element in document.element.body.iterchildren():
        if element.tag == qn("w:bookmarkStart"):
            pending = kind_of(element.get(qn("w:name")) or "") or pending
        elif element.tag == qn("w:tbl"):
            if pending:
                kinds[element] = pending
            pending = None
        elif element.tag not in _BOOKMARK_TAGS:
            pending = None
    return kinds


def _strip_bookmarks(document) -> None:
    """pandoc bookmarks every heading; Google Docs shows each as a flag a rater can see."""
    body = document.element.body
    for element in [el for el in body.iter() if el.tag in _BOOKMARK_TAGS]:
        element.getparent().remove(element)


def _break_pages(document) -> None:
    """Each sentinel paragraph becomes a page break before the paragraph that follows it."""
    for paragraph in list(document.paragraphs):
        if paragraph.text.strip() != PAGE_BREAK:
            continue
        following = paragraph._p.getnext()
        if following is None or following.tag != qn("w:p"):
            raise RuntimeError("a page break must be followed by a paragraph")
        Paragraph(following, paragraph._parent).paragraph_format.page_break_before = True
        paragraph._p.getparent().remove(paragraph._p)


def _rules(document) -> None:
    for paragraph in document.paragraphs:
        if paragraph.text.strip() != RULE:
            continue
        for run in paragraph.runs:
            run._r.getparent().remove(run._r)
        border = OxmlElement("w:bottom")
        for key, value in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", RULE_GREY)):
            border.set(qn(f"w:{key}"), value)
        properties = paragraph._p.get_or_add_pPr()
        frame = OxmlElement("w:pBdr")
        frame.append(border)
        properties.append(frame)
        # The rule belongs under the line it follows, so the empty paragraph carrying it
        # is given no height of its own.
        marks = properties.find(qn("w:rPr")) or OxmlElement("w:rPr")
        size = OxmlElement("w:sz")
        size.set(qn("w:val"), "2")
        marks.append(size)
        properties.append(marks)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(5)
        previous = paragraph._p.getprevious()
        if previous is not None and previous.tag == qn("w:p"):
            Paragraph(previous, paragraph._parent).paragraph_format.space_after = Pt(1)


def _tables(document, kinds: dict) -> None:
    for table in document.tables:
        kind = kinds.get(table._tbl)
        if kind is None:
            continue
        _borders(table)
        if kind == GUIDE:
            _shade(table.cell(0, 0))
            _borders(table, colour=INSTRUCTION_RED)
            for paragraph in table.cell(0, 0).paragraphs:
                for run in paragraph.runs:
                    run.font.color.rgb = RGBColor.from_string(INSTRUCTION_RED)
            continue
        labels = [row.cells[0] for row in table.rows] if kind == KEY_VALUE else table.rows[0].cells
        for cell in labels:
            _shade(cell)
            _muted_bold(cell)
        if kind in (GRID, LEAN, BOX, KEY_VALUE):
            for row in table.rows:
                row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        if kind == BOX:
            table.rows[1].height = Cm(6)
            table.rows[1].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        if kind in (RUBRIC, LEARNER, STEPS, LEAN):
            _font_size(table, SMALL)
        if kind == LEAN:
            _centre_choices(table)


def _shape_pages(document) -> None:
    """Cut each run of pages to the shape its sentinel asks for.

    Word keeps a section's page setup in the last paragraph of that section, so a
    sentinel carries the shape of the run it closes and the body's own setup carries the
    shape of the last one. The break starts its own page; nothing else has to.
    """
    shape = PORTRAIT
    for paragraph in list(document.paragraphs):
        wanted = _SHAPE_OF.get(paragraph.text.strip())
        if wanted is None:
            continue
        for run in paragraph.runs:
            run._r.getparent().remove(run._r)
        properties = paragraph._p.get_or_add_pPr()
        properties.append(_page_setup(OxmlElement("w:sectPr"), shape))
        shape = wanted
    _page_setup(document.element.body.find(qn("w:sectPr")), shape)


def _page_setup(section_properties, shape: str):
    """A section's paper and margins, on a new or an existing ``sectPr``."""
    width, height = PAGE_MM[shape]
    for tag, values in (
        ("w:type", {"w:val": "nextPage"}),
        ("w:pgSz", {"w:w": Mm(width).twips, "w:h": Mm(height).twips, "w:orient": shape}),
        (
            "w:pgMar",
            {f"w:{edge}": MARGIN.twips for edge in ("top", "right", "bottom", "left")}
            | {"w:header": 708, "w:footer": 708, "w:gutter": 0},
        ),
    ):
        element = section_properties.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            section_properties.append(element)
        for key, value in values.items():
            element.set(qn(key), str(value))
    return section_properties


def _text_widths(document) -> dict:
    """The text column each table sits in, which is not the same one on every page."""
    widths, pending = {}, []
    for element in document.element.body.iterchildren():
        if element.tag == qn("w:tbl"):
            pending.append(element)
        elif element.tag == qn("w:p"):
            properties = element.find(qn("w:pPr"))
            found = None if properties is None else properties.find(qn("w:sectPr"))
            if found is not None:
                widths |= dict.fromkeys(pending, _text_width(found))
                pending = []
    return widths | dict.fromkeys(pending, _text_width(document.element.body.find(qn("w:sectPr"))))


def _text_width(section_properties) -> int:
    """Twips between the margins of a section, read from its own setup."""
    size = section_properties.find(qn("w:pgSz"))
    margins = section_properties.find(qn("w:pgMar"))
    page = int(size.get(qn("w:w")))
    return page - int(margins.get(qn("w:left"))) - int(margins.get(qn("w:right")))


def _centre_choices(table) -> None:
    """The boxes a rater picks from, set in the middle of their own cell.

    They are the only thing on the row that is aimed at rather than read, so they are
    left at reading size while the criterion beside them is set small.
    """
    for row in table.rows[1:]:
        for cell in row.cells[1:-1]:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.font.size = BODY


def _fit_tables(document) -> None:
    """Rescale every table's grid to the real text column.

    The reference document sets the page and the type, but pandoc still lays a table's
    grid against a width of its own choosing — measured at 78% of this page's text
    column — so the grid, and only the grid, is corrected here.
    """
    widths = _text_widths(document)
    for table in document.tables:
        grid = table._tbl.find(qn("w:tblGrid"))
        if grid is None:
            continue
        columns = grid.findall(qn("w:gridCol"))
        total = sum(int(column.get(qn("w:w")) or 0) for column in columns)
        if not total:
            continue
        scale = widths[table._tbl] / total
        for column in columns:
            column.set(qn("w:w"), str(round(int(column.get(qn("w:w"))) * scale)))
        for row in table.rows:
            for cell in row.cells:
                properties = cell._tc.tcPr
                width = None if properties is None else properties.find(qn("w:tcW"))
                if width is not None and width.get(qn("w:type")) == "dxa":
                    width.set(qn("w:w"), str(round(int(width.get(qn("w:w"))) * scale)))
        table.autofit = False


def _borders(table, colour: str = RULE_GREY) -> None:
    properties = table._tbl.tblPr
    for existing in properties.findall(qn("w:tblBorders")):
        properties.remove(existing)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        line = OxmlElement(f"w:{edge}")
        outer = edge in ("top", "left", "bottom", "right")
        for key, value in (
            ("val", "single"),
            ("sz", "6" if outer else "4"),
            ("space", "0"),
            ("color", colour if outer else GRID_GREY),
        ):
            line.set(qn(f"w:{key}"), value)
        borders.append(line)
    properties.insert_element_before(
        borders, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption"
    )


def _shade(cell) -> None:
    shading = OxmlElement("w:shd")
    for key, value in (("val", "clear"), ("color", "auto"), ("fill", FILL)):
        shading.set(qn(f"w:{key}"), value)
    cell._tc.get_or_add_tcPr().append(shading)


def _muted_bold(cell) -> None:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.bold = True
            run.font.color.rgb = MUTED


def _font_size(table, size) -> None:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = size


def _small_print(document) -> None:
    for paragraph in document.paragraphs:
        if paragraph.text.strip() in SMALL_PRINT:
            for run in paragraph.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = MUTED


def _footer(document, left: str) -> None:
    for section in document.sections:
        section.footer.is_linked_to_previous = False
        paragraph = section.footer.paragraphs[0]
        paragraph.text = ""
        width = section.page_width - section.left_margin - section.right_margin
        paragraph.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT)
        runs = [paragraph.add_run(left), paragraph.add_run("\tPage ")]
        runs.append(_field(paragraph.add_run(), "PAGE"))
        runs.append(paragraph.add_run(" of "))
        runs.append(_field(paragraph.add_run(), "NUMPAGES"))
        for run in runs:
            run.font.size = Pt(8)
            run.font.color.rgb = MUTED


def _field(run, instruction: str):
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    text = OxmlElement("w:instrText")
    text.set(qn("xml:space"), "preserve")
    text.text = instruction
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, text, end):
        run._r.append(element)
    return run
