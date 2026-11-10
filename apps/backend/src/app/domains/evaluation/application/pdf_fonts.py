"""Computer Modern font registration for the printed expert rater packs.

The H1/H2 worksheets and the source-grounding audit pack render with Computer
Modern (the thesis typeface) instead of the reportlab built-in Helvetica, so the
printed rater materials match the report. The four faces are vendored under
``fonts/`` (see ``fonts/README.md``) and registered here exactly once — system
font installation is never assumed, so this works identically on CI/Docker.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

# Public face names — import these instead of hardcoding "Helvetica".
FONT_REGULAR = "CMUSerif"
FONT_BOLD = "CMUSerif-Bold"
FONT_ITALIC = "CMUSerif-Italic"
FONT_BOLD_ITALIC = "CMUSerif-BoldItalic"

_FONT_DIR = Path(__file__).resolve().parent / "fonts"
_FACES: tuple[tuple[str, str], ...] = (
    (FONT_REGULAR, "cmunrm.ttf"),
    (FONT_BOLD, "cmunbx.ttf"),
    (FONT_ITALIC, "cmunti.ttf"),
    (FONT_BOLD_ITALIC, "cmunbi.ttf"),
)

_registered = False


def ensure_fonts_registered() -> None:
    """Register the Computer Modern faces with reportlab (idempotent).

    Safe to call on every render; the work happens only on the first call. Also
    wires the bold/italic family so ``<b>``/``<i>`` markup in Paragraphs resolves
    to the matching face instead of a faux-bolded regular.
    """
    global _registered
    if _registered:
        return
    for name, filename in _FACES:
        pdfmetrics.registerFont(TTFont(name, str(_FONT_DIR / filename)))
    registerFontFamily(
        FONT_REGULAR,
        normal=FONT_REGULAR,
        bold=FONT_BOLD,
        italic=FONT_ITALIC,
        boldItalic=FONT_BOLD_ITALIC,
    )
    _registered = True
