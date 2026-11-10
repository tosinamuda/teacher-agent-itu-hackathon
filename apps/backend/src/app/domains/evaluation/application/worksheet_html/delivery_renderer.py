"""WeasyPrint renderer for the lesson-plan delivery audit.

The third pack in this package, and the only one a researcher rather than a rater
marks up: it reports which of C1's keys reached which generation call, why each
miss happened, and — where the missing key was ``student_tasks`` — the
task-shaped lines in the teacher's note, each with a box to tick against the
source page.

Takes a plain ``detail`` mapping like its siblings, so the audit that computes
delivery stays outside this domain and nothing here depends on the experiment
harness. ``scripts.prompt_snapshots.delivery_pack`` builds the mapping.

Public entry points: :func:`render_delivery_audit_pdf` and
:func:`render_delivery_audit_html`.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from app.config import CONFIG
from app.domains.evaluation.application.worksheet_html.renderer import (
    _jinja_environment,
    _stylesheet,
)
from app.shared.native_libs import ensure_native_lib_path

_PACKAGE_DIR = Path(__file__).resolve().parent
_TEMPLATE_NAME = "delivery_audit.html.j2"
_STYLESHEET_NAME = "delivery_audit.css"


def render_delivery_audit_html(detail: Mapping[str, object]) -> str:
    """Render the audit HTML only — the shape the PDF is made from."""
    context: dict[str, Any] = {
        "institution_name": CONFIG.institution_name.upper(),
        "study_title": CONFIG.study_title,
        "stylesheet": _stylesheet() + "\n" + _stylesheet(_STYLESHEET_NAME),
        "pack_code": detail.get("pack_code") or "delivery-audit",
        "key_heads": detail.get("key_heads") or (),
        "summary": detail.get("summary"),
        "lessons": detail.get("lessons") or (),
    }
    return cast(str, _jinja_environment().get_template(_TEMPLATE_NAME).render(**context))


def render_delivery_audit_pdf(detail: Mapping[str, object]) -> bytes:
    """Render the lesson-plan delivery audit to PDF bytes via WeasyPrint."""
    ensure_native_lib_path()
    from weasyprint import HTML  # imported lazily so the native-lib path is set first

    html = render_delivery_audit_html(detail)
    return cast(bytes, HTML(string=html, base_url=str(_PACKAGE_DIR)).write_pdf())
