"""WeasyPrint renderer for the H2 personalised-reading-note review worksheet.

A net-new offline worksheet for the H2 (personalised) rater track — the H2 twin of
the H1 ``renderer.py``. H1 has a long-standing offline PDF; H2 did not, so this
module builds one from a Jinja2 HTML template + the shared print CSS and renders it
to PDF with WeasyPrint.

What the H2 worksheet contains (Final Evaluation Protocol §4):

- **Cover** — institution band; the title "Revision-Note Review Worksheet for
  Expert Rater"; a welcome paragraph framing the BLINDED task (two anonymous
  candidate versions of a revision note for one focal learner — judge each
  candidate's fit-to-learner *without* losing the lesson goal; which candidate is
  the class version vs the personalised one is never revealed); the lesson
  reference (topic + objectives + scope); and the learner-state card (one row per
  objective: band / confidence / difficulty / misconception + evidence).
- **The candidate versions, section-aligned, rated inline** — one column per
  blinded candidate ("Candidate A/B", per-rater randomised order; see
  ``candidate_blinding``). If a candidate has no section for an objective it is
  shown as missing so the rater can penalise the lesson-goal score. Immediately
  AFTER each section's comparison comes that section's own "Rate this section"
  block: a per-section misconception call-out (so the rater knows whether to score
  Misconception help or mark N/A), then ONE rating strip per candidate — each
  carrying the five H2 dimensions (Learner suitability, Scaffolding, Challenge,
  Misconception support [N/A + 1-5], Objective preservation) as single-select
  circle rows and a Comment line. The rating header (Revision note ID / Date /
  Rater) and the dimension key / how-to-score reference are shown once, near the
  top, before the first section — there is no consolidated rating form at the end.

Why HTML/WeasyPrint (same rationale as H1): LLM-authored reading-note prose
(``**bold**``, ``*italic*``, lists, exotic glyphs) renders natively via
python-markdown and the Computer Modern TTFs — no ``■`` missing-glyph boxes, no
hand-rolled regex emphasis. Selection markers are CSS shapes (circle =
single-select), not font glyphs.

This module reuses H1's renderer helpers wholesale — the Jinja2 environment, the shared
stylesheet, the markdown converter, and the text/sequence helpers — so the look matches the
H1 worksheet exactly. There is no H1 "major-issue flag" panel here (H1 only). No
"packet"/"pack" wording is shown to the rater — everything is a "revision note".

Public entry point: :func:`render_h2_worksheet_html_pdf`.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import cast

from app.config import CONFIG
from app.domains.evaluation.application.worksheet_html.renderer import (
    _as_mapping,
    _jinja_environment,
    _sequence,
    _step,
    _string_list,
    _stylesheet,
    _text_or_dash,
    _text_or_none,
)
from app.domains.learner_state.domain.models import humanise_misconception_code
from app.shared.native_libs import ensure_native_lib_path

_PACKAGE_DIR = Path(__file__).resolve().parent
_TEMPLATE_NAME = "h2_worksheet.html.j2"

# The five H2 dimensions get compact column headers on the inline "Rate this
# section" strip; map the canonical criterion_id to a short header so the landscape
# strip stays legible. Teacher-friendly column headers — the technical research
# dimension names are not shown to raters (they stay in the dataset).
_DIMENSION_COLUMN_HEADERS: dict[str, str] = {
    "learner_state_suitability": "Fit for this learner",
    "scaffolding_appropriateness": "Teaching support",
    "challenge_calibration": "Challenge level",
    "misconception_support": "Misconception help",
    "objective_preservation": "Keeps the lesson goal",
}
# Misconception support is the one dimension that may be N/A (no recorded
# misconception), so its score row offers an extra N/A marker before 1-5.
_MISCONCEPTION_DIMENSION_ID = "misconception_support"

# Rater-friendly labels for the learner-state signal enums (band/confidence/
# difficulty are stored lower-case literals). The thesis taxonomy
# (remediate / reinforce / extend) is hidden from raters; they see the
# suggested study direction in plain English.
_BAND_LABELS: dict[str, str] = {
    "remediate": "Needs more practice",
    "reinforce": "On track",
    "extend": "Ready for extension",
}
_SIGNAL_LABELS: dict[str, str] = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
}


def render_h2_worksheet_html_pdf(detail: Mapping[str, object]) -> bytes:
    """Render the H2 personalised-reading-note worksheet to PDF bytes via WeasyPrint.

    Accepts the ``detail`` mapping produced by
    ``_PacketDetailProjection._build_h2_packet_detail`` (the same BLINDED
    payload the H2 detail endpoint returns): ``packet_code``,
    ``lesson_title``/``subtitle``, ``objectives``, ``focal_learner`` (the
    learner-state card), ``candidates`` (anonymous, randomised per-rater order,
    each with its pack manifest), ``sections`` (per-candidate steps keyed by
    candidate id), and ``rubric`` (the five H2 dimensions, already carrying
    ``display_label``). Returns a complete PDF document as bytes.
    """
    ensure_native_lib_path()
    from weasyprint import HTML  # imported lazily so the native-lib path is set first

    html = _render_html(detail)
    return cast(bytes, HTML(string=html, base_url=str(_PACKAGE_DIR)).write_pdf())


def render_h2_worksheet_html(detail: Mapping[str, object]) -> str:
    """Render the H2 worksheet HTML only (no PDF) — useful for debugging/tests."""
    return _render_html(detail)


def _render_html(detail: Mapping[str, object]) -> str:
    candidates = _candidates(detail.get("candidates"))
    # Lesson metadata is identical across candidates (same lesson), so the first
    # candidate's manifest is a safe, role-free source for the reference fields.
    lesson_manifest = (
        _as_mapping(_as_mapping(candidates[0].get("pack")).get("manifest")) if candidates else {}
    )
    focal_learner = _as_mapping(detail.get("focal_learner"))

    rubric = _rubric(detail.get("rubric"))
    # Map each lesson_objective_id ("lop01") to its 1-based ordinal so the rater
    # sees "Objective 1", never the internal id. The cover objectives list defines
    # the canonical order; sections/learner-state are labelled against it.
    objective_ordinals = _objective_ordinals(detail.get("objectives"))
    # Per-objective recorded misconception, keyed by lesson_objective_id. Threaded
    # into each section so its inline rating block can call out the misconception
    # (or say none is recorded) — the rater then knows whether to score
    # "Misconception help" or mark it N/A.
    misconceptions_by_objective = _misconceptions_by_objective(focal_learner)
    context = {
        "institution_name": CONFIG.institution_name.upper(),
        "study_title": CONFIG.study_title,
        "packet_code": _text_or_dash(detail.get("packet_code")) or "H2",
        "lesson_title": _text_or_none(detail.get("lesson_title")),
        "lesson_subtitle": _text_or_none(detail.get("lesson_subtitle")),
        "subtopic": _text_or_dash(lesson_manifest.get("subtopic")),
        "grade": _text_or_dash(lesson_manifest.get("grade")),
        "subject": _text_or_dash(lesson_manifest.get("subject")),
        "week": _text_or_dash(lesson_manifest.get("week")),
        "welcome_note": _welcome_note(),
        "lesson_reference": _lesson_reference(lesson_manifest),
        "objectives": _objectives(detail.get("objectives")),
        "learner_state": _learner_state(focal_learner, objective_ordinals),
        "candidates": [{"label": candidate.get("label")} for candidate in candidates],
        "sections": _sections(
            detail.get("sections"),
            candidates,
            objective_ordinals,
            misconceptions_by_objective,
        ),
        "rubric": rubric,
        "stylesheet": _stylesheet(),
    }
    template = _jinja_environment().get_template(_TEMPLATE_NAME)
    return cast(str, template.render(**context))


def _candidates(value: object) -> list[Mapping[str, object]]:
    """The blinded candidate descriptors, ordered by ``display_order``."""
    rows = [
        cast("Mapping[str, object]", entry)
        for entry in _sequence(value)
        if isinstance(entry, Mapping)
    ]
    return sorted(rows, key=lambda row: int(cast(int, row.get("display_order") or 0)))


# --- Context builders -------------------------------------------------------


def _welcome_note() -> str:
    """Return the cover task framing — blinded: judge each candidate's fit-to-learner.

    Must not reveal which candidate is the class version and which is personalised
    (Protocol §4 blinding). Still maps to the H2 rubric: fit-to-learner (suitability
    + scaffolding + challenge), the misconception cue, and objective preservation
    within the same scope.
    """
    return (
        "You will see two candidate versions of a student revision note, prepared "
        "for one learner. The learner-state card below shows what this learner "
        "needs, objective by objective. For each section, read both candidate "
        "versions and judge how suitable each candidate is for this learner — and "
        "whether each still teaches the same objectives and stays within the same "
        "scope. Score every candidate independently; you are not asked to pick a "
        "winner or guess how either version was made."
    )


def _lesson_reference(base_manifest: Mapping[str, object]) -> list[dict[str, object]]:
    """Ordered key/value rows for the lesson-reference table (Protocol §4.1).

    Topic + scope come from the base-pack manifest (the standard the personalised
    version is judged against); the per-objective list is rendered separately below.
    """
    return [
        _scalar_row("Subject", base_manifest.get("subject")),
        _scalar_row("Grade", base_manifest.get("grade")),
        _scalar_row("Term", base_manifest.get("term")),
        _scalar_row("Week", base_manifest.get("week")),
        _scalar_row("Topic", base_manifest.get("topic")),
        _scalar_row("Subtopic", base_manifest.get("subtopic")),
        _scalar_row("Theme", base_manifest.get("theme")),
        _list_row("Misconceptions in scope", base_manifest.get("misconceptions")),
    ]


def _scalar_row(label: str, value: object) -> dict[str, object]:
    return {"label": label, "value": _text_or_dash(value), "list_items": None}


def _list_row(label: str, value: object) -> dict[str, object]:
    return {"label": label, "value": None, "list_items": _string_list(value)}


def _objectives(value: object) -> list[str]:
    texts: list[str] = []
    for entry in _sequence(value):
        if isinstance(entry, Mapping):
            objective = cast(Mapping[str, object], entry)
            text = _text_or_none(objective.get("objective_text"))
            texts.append(text or "—")
    return texts


def _objective_ordinals(value: object) -> dict[str, int]:
    """Map each ``lesson_objective_id`` to its 1-based position in the lesson.

    The cover objectives list is the canonical ordering, so we number from it. The
    raw id ("lop01") is internal and must never reach the rater; it is replaced by
    "Objective N" everywhere via :func:`_objective_label`.
    """
    ordinals: dict[str, int] = {}
    position = 0
    for entry in _sequence(value):
        if not isinstance(entry, Mapping):
            continue
        position += 1
        objective_id = _text_or_none(cast(Mapping[str, object], entry).get("lesson_objective_id"))
        if objective_id is not None and objective_id not in ordinals:
            ordinals[objective_id] = position
    return ordinals


def _objective_label(objective_id: str | None, ordinals: Mapping[str, int]) -> str | None:
    """Human label for an objective id: "Objective N", or ``None`` if unmatched.

    Returning ``None`` (rather than echoing the raw id) lets callers fall back
    gracefully — e.g. to just the section number — so "lop01" never reaches a rater.
    """
    if objective_id is None:
        return None
    ordinal = ordinals.get(objective_id)
    if ordinal is None:
        return None
    return f"Objective {ordinal}"


def _learner_state(
    focal_learner: Mapping[str, object], objective_ordinals: Mapping[str, int]
) -> dict[str, object]:
    """Build the learner-state card payload for the cover (Protocol §4.3).

    One row per objective: the human "Objective N" label (the raw id is internal
    and dropped), band (Remediate/Reinforce/Extend), confidence, perceived
    difficulty, and any recorded misconception + evidence. Falls back to a row
    counter when an objective id has no ordinal so the card still renders.
    """
    rows: list[dict[str, object]] = []
    for index, entry in enumerate(_sequence(focal_learner.get("objective_states")), start=1):
        if not isinstance(entry, Mapping):
            continue
        state = cast(Mapping[str, object], entry)
        label = _objective_label(
            _text_or_none(state.get("lesson_objective_id")), objective_ordinals
        )
        rows.append(
            {
                "objective_label": label or f"Objective {index}",
                "objective_text": _text_or_dash(state.get("objective_text")),
                "band": _band_label(state.get("band")),
                "confidence": _signal_label(state.get("confidence")),
                "difficulty": _signal_label(state.get("perceived_difficulty")),
                "misconception": _misconception_text(state),
            }
        )
    return {
        "focal_case_type": _focal_case_label(focal_learner.get("focal_case_type")),
        "session_note": _session_survey_note(focal_learner),
        "rows": rows,
    }


def _session_survey_note(focal_learner: Mapping[str, object]) -> str | None:
    """One line for the session-level survey: "Interest 4/5 · End-of-lesson feeling 2/5"."""
    raw = focal_learner.get("session_survey")
    if not isinstance(raw, Mapping):
        return None
    survey = cast("Mapping[str, object]", raw)
    parts: list[str] = []
    interest = survey.get("interest")
    affect = survey.get("affect")
    if isinstance(interest, int):
        parts.append(f"Interest {interest}/5")
    if isinstance(affect, int):
        parts.append(f"End-of-lesson feeling {affect}/5")
    return " · ".join(parts) if parts else None


def _band_label(value: object) -> str:
    text = _text_or_none(value)
    if text is None:
        return "—"
    return _BAND_LABELS.get(text.lower(), text)


def _signal_label(value: object) -> str:
    text = _text_or_none(value)
    if text is None:
        return "—"
    return _SIGNAL_LABELS.get(text.lower(), text)


def _focal_case_label(value: object) -> str | None:
    text = _text_or_none(value)
    if text is None:
        return None
    return _BAND_LABELS.get(text.lower(), text.replace("_", " "))


def _misconception_evidence(state: Mapping[str, object]) -> str | None:
    """Return the combined misconception + evidence string for one objective, or ``None``.

    Returns ``None`` when the objective has no recorded misconception (no
    description and no code) so callers can branch on "recorded vs none" — the
    learner-state card shows "None recorded", the per-section call-out tells the
    rater to mark Misconception help as N/A.
    """
    description = _text_or_none(state.get("misconception_description"))
    code = _text_or_none(state.get("misconception_code"))
    if not description and not code:
        return None
    if not description and code:
        description = humanise_misconception_code(code)
    evidence = _string_list(state.get("evidence_refs"))
    parts: list[str] = [cast(str, description)]
    if evidence:
        parts.append("Evidence: " + ", ".join(evidence))
    return " — ".join(parts)


def _misconception_text(state: Mapping[str, object]) -> str:
    """Return the combined misconception + evidence cell for the learner-state card."""
    return _misconception_evidence(state) or "None recorded"


def _misconceptions_by_objective(
    focal_learner: Mapping[str, object],
) -> dict[str, str]:
    """Map each ``lesson_objective_id`` to its recorded misconception evidence string.

    Built from the focal learner's objective states. Objectives with no recorded
    misconception are omitted, so a section whose objective is absent from this map
    has no misconception to call out (rate Misconception help as N/A).
    """
    by_objective: dict[str, str] = {}
    for entry in _sequence(focal_learner.get("objective_states")):
        if not isinstance(entry, Mapping):
            continue
        state = cast(Mapping[str, object], entry)
        objective_id = _text_or_none(state.get("lesson_objective_id"))
        if objective_id is None:
            continue
        evidence = _misconception_evidence(state)
        if evidence is not None:
            by_objective[objective_id] = evidence
    return by_objective


def _sections(
    value: object,
    candidates: list[Mapping[str, object]],
    objective_ordinals: Mapping[str, int],
    misconceptions_by_objective: Mapping[str, str],
) -> list[dict[str, object]]:
    """One section row per section, with one rendered column per blinded candidate.

    Each section's ``columns`` follow the candidates' randomised display order: a
    column carries the candidate's rendered blocks, or ``missing: True`` when that
    candidate has no section for the objective (shown so the rater can penalise the
    lesson-goal score) — without revealing which condition dropped it.

    Each section also gets a human ``objective_label`` ("Objective N", or ``None``
    when the section's objective id has no ordinal) so the rater never sees the raw
    internal id, and a ``misconception`` string looked up by the section's
    ``lesson_objective_id`` (``None`` when the objective has no recorded
    misconception). The inline rating block uses it to call out the misconception so
    the rater knows whether to score Misconception help or mark it N/A.
    """
    candidate_ids = [_text_or_none(candidate.get("candidate_id")) for candidate in candidates]
    sections: list[dict[str, object]] = []
    for index, entry in enumerate(_sequence(value), start=1):
        if not isinstance(entry, Mapping):
            continue
        section = cast("Mapping[str, object]", entry)
        steps_by_candidate = _as_mapping(section.get("candidate_steps"))
        columns: list[dict[str, object]] = []
        for candidate_id in candidate_ids:
            raw_step = steps_by_candidate.get(candidate_id) if candidate_id else None
            if isinstance(raw_step, Mapping):
                columns.append({"missing": False, "blocks": _step(_as_mapping(raw_step))["blocks"]})
            else:
                columns.append({"missing": True, "blocks": []})
        objective_id = _text_or_none(section.get("lesson_objective_id"))
        objective_label = _objective_label(objective_id, objective_ordinals)
        misconception = (
            misconceptions_by_objective.get(objective_id) if objective_id is not None else None
        )
        sections.append(
            {
                "index": index,
                "section_id": _text_or_dash(section.get("section_id")),
                "title": _text_or_none(section.get("title")) or f"Section {index}",
                "objective_label": objective_label,
                "objective_text": _text_or_none(section.get("objective_text")),
                "columns": columns,
                "misconception": misconception,
            }
        )
    return sections


def _rubric(value: object) -> list[dict[str, object]]:
    """Rubric rows for the inline per-section rating strips + the dimension key.

    Each row carries the teacher-friendly ``display_label`` (the bold lead), the
    canonical technical ``label`` (kept small for the dataset/thesis link), a short
    column ``header`` for the inline strip, and ``allow_na`` (only misconception
    support may be N/A).
    """
    rows: list[dict[str, object]] = []
    for entry in _sequence(value):
        if not isinstance(entry, Mapping):
            continue
        criterion = cast(Mapping[str, object], entry)
        criterion_id = _text_or_none(criterion.get("criterion_id")) or ""
        label = _text_or_dash(criterion.get("label"))
        display_label = _text_or_none(criterion.get("display_label")) or label
        header = _DIMENSION_COLUMN_HEADERS.get(criterion_id, display_label)
        rows.append(
            {
                "criterion_id": criterion_id,
                "header": header,
                "display_label": display_label,
                "label": label,
                "description": _text_or_dash(criterion.get("description")),
                "allow_na": criterion_id == _MISCONCEPTION_DIMENSION_ID,
            }
        )
    return rows
