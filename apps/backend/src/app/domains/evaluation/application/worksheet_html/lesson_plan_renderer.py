"""WeasyPrint renderer for a NERDC lesson (session) plan → PDF.

Reuses this package's shared rendering primitives — markdown→HTML with math,
per-block rendering, the Jinja environment, the font-bound base stylesheet, and
the macOS native-lib shim — so the researcher's lesson-plan export matches the
pack/audit PDFs. No duplication of that machinery; this module only adds the
plan-specific context builders + its own template.

Public entry point: :func:`render_lesson_plan_pdf`.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from app.config import CONFIG
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import activities_of
from app.domains.evaluation.application.worksheet_html.renderer import (
    _PACKAGE_DIR,
    _block,
    _jinja_environment,
    _render_markdown,
    _sequence,
    _string_list,
    _text_or_dash,
    _text_or_none,
)
from app.shared.native_libs import ensure_native_lib_path

_TEMPLATE_NAME = "lesson_plan.html.j2"


def render_lesson_plan_pdf(session_plan: Mapping[str, object], *, plan_label: str) -> bytes:
    """Render a session plan to PDF bytes via WeasyPrint."""
    ensure_native_lib_path()
    from weasyprint import HTML  # lazy import so the native-lib path is set first

    html = render_lesson_plan_html(session_plan, plan_label=plan_label)
    return cast(bytes, HTML(string=html, base_url=str(_PACKAGE_DIR)).write_pdf())


def render_lesson_plan_html(session_plan: Mapping[str, object], *, plan_label: str) -> str:
    """Render the lesson-plan HTML only (no PDF) — useful for tests/debugging."""
    context = _context(session_plan, plan_label=plan_label)
    template = _jinja_environment().get_template(_TEMPLATE_NAME)
    return cast(str, template.render(**context))


# --- context builders -------------------------------------------------------


def _context(plan: Mapping[str, object], *, plan_label: str) -> dict[str, Any]:
    title = _text_or_none(plan.get("title")) or _text_or_dash(plan.get("subtopic"))
    return {
        "stylesheet": _stylesheet_with_plan_styles(),
        "institution_name": CONFIG.institution_name.upper(),
        "study_title": CONFIG.study_title,
        "plan_label": plan_label,
        "title": title,
        "meta_rows": _meta_rows(plan),
        "curriculum_objectives": _objective_texts(plan.get("curriculum_objectives")),
        "lesson_objectives": _objective_texts(plan.get("lesson_plan_objectives")),
        "entry_behaviour": _string_list(plan.get("entry_behaviour")),
        "instructional_materials": _string_list(plan.get("instructional_materials")),
        "references": _string_list(plan.get("references")),
        "steps": [
            _step(cast(Mapping[str, object], step))
            for step in _sequence(plan.get("steps"))
            if isinstance(step, Mapping)
        ],
    }


def _stylesheet_with_plan_styles() -> str:
    """Reuse the worksheet base stylesheet (fonts + typography) + plan layout."""
    from app.domains.evaluation.application.worksheet_html.renderer import _stylesheet

    return _stylesheet() + _PLAN_CSS


def _meta_rows(plan: Mapping[str, object]) -> list[dict[str, str]]:
    return [
        {"label": "Subject", "value": _text_or_dash(plan.get("subject"))},
        {"label": "Grade", "value": _text_or_dash(plan.get("grade"))},
        {"label": "Term", "value": _text_or_dash(plan.get("term"))},
        {"label": "Week", "value": _text_or_dash(plan.get("week"))},
        {"label": "Topic", "value": _text_or_dash(plan.get("topic"))},
        {"label": "Subtopic", "value": _text_or_dash(plan.get("subtopic"))},
        {"label": "Theme", "value": _text_or_dash(plan.get("theme"))},
    ]


def _objective_texts(value: object) -> list[str]:
    """Objective texts from either ``{objective_text|text}`` mappings or bare strings."""
    texts: list[str] = []
    for entry in _sequence(value):
        if isinstance(entry, Mapping):
            entry_map = cast(Mapping[str, object], entry)
            text = _text_or_none(entry_map.get("objective_text")) or _text_or_none(
                entry_map.get("text")
            )
        else:
            text = _text_or_none(entry)
        if text:
            texts.append(text)
    return texts


def _step(step: Mapping[str, object]) -> dict[str, Any]:
    title = _text_or_none(step.get("title")) or _text_or_none(step.get("step_id")) or "Step"
    content = _text_or_none(step.get("content"))
    minutes = step.get("estimated_minutes")
    return {
        "title": title,
        "kind": _text_or_none(step.get("step_kind")),
        "minutes": f"{minutes} min" if isinstance(minutes, int) else None,
        # Lesson-plan prose is teacher-authored, not a revision note, so keep any
        # citations rather than stripping them.
        "content_html": _render_markdown(content, strip_citations=False) if content else None,
        "teacher_activities": activities_of(step, "teacher"),
        "student_activities": activities_of(step, "student"),
        "blocks": [
            rendered
            for block in _sequence(step.get("blocks"))
            if isinstance(block, Mapping)
            for rendered in (_block(cast(Mapping[str, object], block)),)
            if rendered is not None
        ],
    }


# Plan-specific layout, appended after the reused worksheet base stylesheet
# (which supplies the @font-face declarations + base body typography).
_PLAN_CSS = """
.plan-cover { margin-bottom: 1.2rem; }
.plan-institution { font-size: 8pt; letter-spacing: 0.18em; color: #6b6b6b; margin: 0; }
.plan-study-title { font-size: 9pt; color: #8a8a8a; margin: 0.1rem 0 0; }
.plan-eyebrow { font-size: 8pt; letter-spacing: 0.16em; color: #9a5a3a; margin: 0.9rem 0 0.2rem; }
.plan-title { font-size: 17pt; font-weight: 700; margin: 0 0 0.2rem; }
.plan-label { font-size: 8pt; color: #9a9a9a; font-family: monospace; }
.plan-meta { width: 100%; border-collapse: collapse; margin: 0.6rem 0 1rem; }
.plan-meta td { padding: 2px 8px 2px 0; vertical-align: top; font-size: 9.5pt; }
.plan-meta td.k { color: #6b6b6b; width: 7rem; white-space: nowrap; }
.plan-section-title { font-size: 8pt; letter-spacing: 0.14em; color: #6b6b6b;
  margin: 1rem 0 0.3rem; text-transform: uppercase; }
.plan-list { margin: 0 0 0.6rem 1.1rem; padding: 0; }
.plan-list li { margin: 0.1rem 0; font-size: 10pt; }
.plan-step { border: 1px solid #e3e0da; border-radius: 4px; padding: 0.7rem 0.9rem;
  margin: 0.6rem 0; break-inside: avoid; }
.plan-step-head { display: flex; justify-content: space-between; align-items: baseline;
  gap: 0.6rem; margin-bottom: 0.3rem; }
.plan-step-title { font-size: 11pt; font-weight: 700; margin: 0; }
.plan-step-meta { font-size: 8pt; color: #9a9a9a; white-space: nowrap; }
.plan-step-content { font-size: 10pt; }
.plan-activities { margin-top: 0.4rem; }
.plan-activities .lab { font-size: 8pt; letter-spacing: 0.1em; color: #6b6b6b; }
.plan-block { margin-top: 0.5rem; padding-left: 0.6rem; border-left: 2px solid #eee; }
.plan-block .lab { font-size: 8pt; letter-spacing: 0.08em; color: #9a5a3a; }
"""
