"""WeasyPrint renderer for the source-grounding audit pack.

A parallel, additive alternative to ``audit_pack_pdf.py`` (the reportlab path). It
builds the same self-contained pack — instructions + the 0/1/2 scale legend, then
one card per audit item (lesson objective, generated excerpt, cited source id +
snippet, scope boundary, and a 4-criteria 0/1/2 grid + comment column) — from a
Jinja2 HTML template + the shared print CSS, and renders it to PDF with WeasyPrint.

Why this exists: like the H1 worksheet, the audit pack's generated excerpts are
LLM-authored markdown. WeasyPrint renders real HTML with the full Unicode-capable
Computer Modern TTFs, so the excerpt markdown (``**bold**``, ``*italic*``, lists,
…) renders natively and exotic glyphs survive unchanged — no ``■`` missing-glyph
boxes and no hand-rolled regex emphasis. Selection markers are CSS shapes
(circle = single-select 0/1/2 score cells), not font glyphs.

Public entry point: :func:`render_source_audit_pack_html_pdf`.

Native libraries (pango/cairo/gdk-pixbuf/fontconfig/harfbuzz) are required by
WeasyPrint — see this package's README. The macOS dyld shim lives in
``app.shared.native_libs``.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import cast

from app.config import CONFIG, STATIC_DIR
from app.domains.evaluation.application.source_record_format import friendly_source_record_id
from app.domains.evaluation.application.worksheet_html.renderer import (
    _jinja_environment,
    _render_markdown,
    _sequence,
    _stylesheet,
    _text_or_dash,
    _text_or_none,
)
from app.shared.native_libs import ensure_native_lib_path

_TEMPLATE_NAME = "audit_pack.html.j2"

# Local cache of bundled textbook figures (see ``app.server`` — the same dir is
# mounted at ``/static/figures/`` for the SPA). Mirrors the frontend
# ``localFigureSrc`` helper: when the URL host belongs to one of the bundled
# textbook CDNs and the basename is cached on disk, rewrite to a ``file://`` URL
# so WeasyPrint loads from disk instead of fetching over HTTPS (slow / fragile
# in CI + offline). Non-matching URLs pass through; WeasyPrint's default URL
# fetcher then handles them.
_TEXTBOOK_CDN_HOSTS = re.compile(r"electricbookworks\.github\.io|siyavula")
_FIGURE_CACHE_DIR = STATIC_DIR / "figures"


def render_source_audit_pack_html_pdf(detail: Mapping[str, object]) -> bytes:
    """Render the source-grounding audit pack to PDF bytes via WeasyPrint.

    Accepts the same ``detail`` mapping as ``render_source_audit_pack_pdf`` in the
    reportlab renderer (see ``AuditPresenter.export_source_audit_pack``):
    a ``textbook_name`` string and an ``items`` list. Returns a complete PDF
    document as bytes.
    """
    ensure_native_lib_path()
    from weasyprint import HTML  # imported lazily so the native-lib path is set first

    html = _render_html(detail)

    package_dir = Path(__file__).resolve().parent
    return cast(bytes, HTML(string=html, base_url=str(package_dir)).write_pdf())


def render_source_audit_pack_html(detail: Mapping[str, object]) -> str:
    """Render the audit-pack HTML only (no PDF) — useful for debugging/tests."""
    return _render_html(detail)


def _render_html(detail: Mapping[str, object]) -> str:
    textbook_name = _text_or_none(detail.get("textbook_name")) or "the source textbook"
    items = [
        _item(index, cast(Mapping[str, object], item))
        for index, item in enumerate(_sequence(detail.get("items")), start=1)
        if isinstance(item, Mapping)
    ]
    context = {
        "institution_name": CONFIG.institution_name.upper(),
        "study_title": CONFIG.study_title,
        "pack_code": "Source-Grounding Audit Pack",
        "textbook_name": textbook_name,
        "items": items,
        "criteria": _criteria(),
        "stylesheet": _stylesheet(),
    }
    template = _jinja_environment().get_template(_TEMPLATE_NAME)
    return cast(str, template.render(**context))


def _item(index: int, item: Mapping[str, object]) -> dict[str, object]:
    audit_id = _text_or_none(item.get("audit_item_id")) or f"SG-{index}"
    objective = (
        _text_or_none(item.get("objective_text"))
        or _text_or_none(item.get("lesson_objective_id"))
        or "—"
    )
    snippet = (
        _text_or_none(item.get("source_excerpt"))
        or "Source snippet unavailable — consult the textbook."
    )
    figure_url = _text_or_none(item.get("figure_url"))
    return {
        "index": index,
        # ``condition_code`` (C2/C3/C4) is intentionally not surfaced — raters
        # judge source grounding against the excerpt itself, not which
        # experimental condition produced it.
        "source_ref": _text_or_dash(item.get("source_ref")),
        # Render the textbook block id as a rater-friendly "Chapter X — Block Y"
        # label; the raw ``chXX-bYY`` stays on the wire for analysis paths.
        "source_id": friendly_source_record_id(_text_or_none(item.get("source_record_id"))) or "—",
        "audit_id": audit_id,
        "objective": objective,
        # Strip inline ``REF-N`` markers from the excerpt — the rater anchors
        # against the cited-source label in the right cell, so the inline
        # markers add noise without help. Editorial ``(Source: REF-N for X)``
        # annotations are stripped unconditionally in ``_render_markdown``.
        "excerpt_html": _render_markdown(
            _text_or_none(item.get("generated_excerpt")) or "", strip_citations=True
        ),
        # Render the snippet through the same markdown converter as the excerpt
        # so list markers / bold / italics / paragraph breaks the source carries
        # are readable side-by-side, not lumped into one paragraph.
        "snippet_html": _render_markdown(snippet, strip_citations=False),
        # Figure fields are None when the cited record is text-only; the
        # template guards on ``figure_url`` so no broken ``<img>`` is emitted.
        "figure_url": _resolve_figure_src(figure_url) if figure_url else None,
        "figure_caption": _text_or_none(item.get("figure_caption")),
        "scope": _text_or_dash(item.get("scope_boundary")),
    }


def _resolve_figure_src(url: str) -> str:
    """Rewrite a bundled-textbook CDN URL to the local on-disk cache when present.

    Mirrors the frontend ``localFigureSrc`` (``src/shared/components/renderer/
    VisualBlock.tsx``): if the URL host belongs to one of the bundled textbook
    CDNs (electricbookworks / siyavula) and the basename exists under
    ``app/static/figures/``, return a ``file://`` URL pointing at the
    cached file so WeasyPrint can load it from disk (fast, offline-safe). All
    other URLs pass through unchanged and WeasyPrint's default URL fetcher
    handles them. Falls back to the original URL on any path-shaped surprise so
    we never substitute a broken local path.
    """
    if not _TEXTBOOK_CDN_HOSTS.search(url):
        return url
    basename = url.rsplit("/", 1)[-1].split("?", 1)[0]
    if not basename:
        return url
    candidate = _FIGURE_CACHE_DIR / basename
    if not candidate.is_file():
        return url
    return candidate.as_uri()


def _criteria() -> list[dict[str, str]]:
    """Return the four 0/1/2 audit criteria, in protocol order, from service.py.

    Sourced from ``SOURCE_AUDIT_CRITERIA`` (the canonical definition shared with the
    digital audit form and the reportlab pack) so all three stay in lockstep. The
    import is local to break the import cycle: ``service`` imports this renderer for
    the active download path, while ``SOURCE_AUDIT_CRITERIA`` lives in ``service``.
    """
    from app.domains.evaluation.application.constants import SOURCE_AUDIT_CRITERIA

    return [
        {
            "label": _text_or_dash(criterion.get("label")),
            "description": _text_or_dash(criterion.get("description")),
        }
        for criterion in SOURCE_AUDIT_CRITERIA
    ]
