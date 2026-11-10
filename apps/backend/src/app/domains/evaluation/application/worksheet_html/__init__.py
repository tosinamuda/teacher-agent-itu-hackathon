"""WeasyPrint renderers for the expert rater packs (active PDF download path).

Parallel HTML/CSS -> PDF renderers that replace the reportlab modules
(``h1_worksheet_pdf.py``, ``audit_pack_pdf.py``) on the download path:

- :func:`render_h1_worksheet_html_pdf` — the H1 reading-note review worksheet.
- :func:`render_h2_worksheet_html_pdf` — the H2 personalised-reading-note worksheet.
- :func:`render_source_audit_pack_html_pdf` — the source-grounding audit pack.

Both are built from Jinja2 HTML templates + a shared print CSS and rendered with
WeasyPrint. The headline win over reportlab is native markdown + full Unicode:
LLM-authored prose (``**bold**``, ``*italic*``, lists, exotic glyphs) renders via
python-markdown and the Computer Modern TTFs, so there are no ``■`` missing-glyph
boxes and no hand-rolled regex emphasis. The reportlab modules are kept as a
fallback. WeasyPrint needs native libs (pango/cairo/gdk-pixbuf/fontconfig/
harfbuzz) — see this package's README.
"""

from __future__ import annotations

from app.domains.evaluation.application.worksheet_html.audit_renderer import (
    render_source_audit_pack_html_pdf,
)
from app.domains.evaluation.application.worksheet_html.h2_renderer import (
    render_h2_worksheet_html_pdf,
)
from app.domains.evaluation.application.worksheet_html.renderer import (
    render_h1_worksheet_html_pdf,
)

__all__ = [
    "render_h1_worksheet_html_pdf",
    "render_h2_worksheet_html_pdf",
    "render_source_audit_pack_html_pdf",
]
