"""WeasyPrint renderer for a post-class review pack (C0–C4 / P0–P1) → PDF.

The researcher-facing pack export reuses the SAME sheet as the rater worksheet
(``worksheet.html.j2``) in ``mode="pack"`` — the student revision note + the
research band/footer, minus the rater pages (instruction cover + rating sheet).
One template means the two never drift.

Public entry point: :func:`render_pack_pdf`.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from app.config import CONFIG
from app.domains.evaluation.application.worksheet_html.renderer import (
    _PACKAGE_DIR,
    _answer_key,
    _jinja_environment,
    _sequence,
    _step,
    _stylesheet,
    _text_or_dash,
)
from app.shared.native_libs import ensure_native_lib_path

_TEMPLATE_NAME = "worksheet.html.j2"


def render_pack_pdf(manifest: Mapping[str, object], *, pack_label: str) -> bytes:
    """Render a review-pack manifest to PDF bytes via WeasyPrint."""
    ensure_native_lib_path()
    from weasyprint import HTML  # lazy import so the native-lib path is set first

    html = render_pack_html(manifest, pack_label=pack_label)
    return cast(bytes, HTML(string=html, base_url=str(_PACKAGE_DIR)).write_pdf())


def render_pack_html(manifest: Mapping[str, object], *, pack_label: str) -> str:
    """Render the pack HTML only (no PDF) — the shared sheet in ``mode="pack"``."""
    context: dict[str, Any] = {
        "mode": "pack",
        "stylesheet": _stylesheet(),
        "institution_name": CONFIG.institution_name.upper(),
        "study_title": CONFIG.study_title,
        "pack_label": pack_label,
        # Footer-left for the researcher copy (the pack id lives in the band, not here).
        "footer_note": "Research Copy — Student Revision Note",
        "subtopic": _text_or_dash(manifest.get("subtopic")),
        "grade": _text_or_dash(manifest.get("grade")),
        "subject": _text_or_dash(manifest.get("subject")),
        "week": _text_or_dash(manifest.get("week")),
        # Built by the rater renderer, not rebuilt here: a second _step drifted from it
        # once already, and the practice blocks it kept emitting had lost their branch
        # in the shared template — the researcher copy printed no activities at all.
        "steps": [
            _step(cast(Mapping[str, object], step))
            for step in _sequence(manifest.get("steps"))
            if isinstance(step, Mapping)
        ],
        "answer_key": _answer_key(_sequence(manifest.get("steps"))),
    }
    template = _jinja_environment().get_template(_TEMPLATE_NAME)
    return cast(str, template.render(**context))
