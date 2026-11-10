"""The reference document pandoc sizes the page and the tables against.

pandoc fixes a table's grid, the page and the styles while it writes the docx, from
whatever reference document it is given. Handed its own default, it sizes an A4 page's
tables for US Letter and we would have to rescale every grid afterwards. Handed this one,
it gets the geometry right the first time.

Regenerate with::

    uv run python -m experiments.human_rating.template
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

PATH = Path(__file__).resolve().parent / "reference.docx"
FONT = "Times New Roman"
BODY = Pt(10)
INK = RGBColor(0x11, 0x11, 0x11)
HEADINGS = {"Heading 1": 18, "Heading 2": 14, "Heading 3": 11.5, "Heading 4": 10.5, "Heading 5": 10}


def build(path: Path = PATH) -> Path:
    """pandoc's own default, with this study's page and type."""
    default = subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        check=True,
        capture_output=True,
    ).stdout
    path.write_bytes(default)
    document = Document(str(path))
    for section in document.sections:
        section.page_width, section.page_height = Mm(210), Mm(297)
        section.left_margin = section.right_margin = Mm(16)
        section.top_margin = section.bottom_margin = Mm(16)
    _typeface(document.styles["Normal"], BODY, bold=False)
    for name, size in HEADINGS.items():
        try:
            style = document.styles[name]
        except KeyError:
            continue
        _typeface(style, Pt(size), bold=True)
    document.save(str(path))
    return path


def _typeface(style, size, *, bold: bool) -> None:
    style.font.name, style.font.size, style.font.bold = FONT, size, bold
    style.font.color.rgb = INK
    fonts = style.element.get_or_add_rPr().find(qn("w:rFonts"))
    if fonts is not None:
        fonts.set(qn("w:eastAsia"), FONT)
        fonts.set(qn("w:cs"), FONT)


if __name__ == "__main__":
    print(build())
