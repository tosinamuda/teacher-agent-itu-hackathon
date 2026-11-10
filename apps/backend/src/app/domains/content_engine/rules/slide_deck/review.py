"""What a step's slides need to be shown to a class; a slide that falls short goes back."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from app.domains.content_engine.rules.slide_deck.aim import unstated_aim
from app.domains.content_engine.rules.slide_deck.config import LIMITS
from app.domains.content_engine.rules.slide_deck.coverage import (
    uncovered_examples,
    unreadable_examples,
    worked_problems,
)
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.evaluation_drawings import (
    revealing_drawings,
)
from app.domains.content_engine.rules.slide_deck.number_lines import number_line_issues
from app.domains.content_engine.rules.slide_deck.opening import unopened_lesson
from app.domains.content_engine.rules.slide_deck.pictures import unpictured_rounding
from app.domains.content_engine.rules.slide_deck.placeholders import placeholder_drawings
from app.domains.content_engine.rules.slide_deck.question_coverage import (
    note_questions,
    uncovered_questions,
)
from app.domains.content_engine.rules.slide_deck.questions import evaluation_slide_issues
from app.domains.content_engine.rules.slide_deck.repeats import (
    repeated_drawings,
    repeated_measures,
    repeated_slides,
)
from app.domains.content_engine.rules.slide_deck.wording import wording_faults
from app.domains.content_engine.rules.slide_deck.working import (
    crowded_slides,
    missing_working,
    reasons_on_slides,
)
from app.shared.json_types import JsonObject, JsonValue

MAX_SLIDES = LIMITS["max_slides"]
MAX_POINTS = LIMITS["max_points"]
MAX_POINT_WORDS = LIMITS["max_point_words"]
#: A slide's first point may state a problem or a question in full.
MAX_FIRST_POINT_WORDS = LIMITS["max_first_point_words"]
MAX_TITLE_WORDS = LIMITS["max_title_words"]
#: A slide with a drawing keeps its words few, so the drawing and the words both read large.
MAX_POINTS_WITH_DRAWING = LIMITS["max_points_with_drawing"]
MIN_NOTES_CHARS = LIMITS["min_notes_chars"]

_MATHS = re.compile(r"\$[^$]*\$")
_COMMAND = re.compile(r"\\[A-Za-z,;:!]")
_ONLY_WORDS_IN_MATHS = re.compile(r"^\$\\text\{[^{}$]*\}\$$")
#: The frame the aim is worded in: fixed wording, so it is not part of the point's length.
_AIM_FRAME = re.compile(r"^\s*by the end,?\s+(?:i|we) can\b", re.IGNORECASE)


def _words(text: str) -> int:
    """A formula counts as one word, because the class reads it as one."""
    return len(_MATHS.sub("x", text).split())


def _records(value: JsonValue | None) -> list[JsonObject]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _text(value: JsonValue | None) -> str:
    return str(value).strip() if value is not None else ""


def _point_faults(where: str, points: list[str]) -> list[str]:
    faults: list[str] = []
    for index, point in enumerate(points):
        if _ONLY_WORDS_IN_MATHS.match(point):
            faults.append(
                f"{where}: {point!r} is only words inside $ signs; write it as plain text"
            )
        limit = MAX_FIRST_POINT_WORDS if index == 0 else MAX_POINT_WORDS
        length = _words(_AIM_FRAME.sub("", point))
        if length > limit:
            long = f"a point of {length} words runs past {limit}"
            faults.append(f"{where}: {long}: {point[:60]!r}")
    return faults


def _drawing_faults(where: str, slide: JsonObject, points: list[str]) -> list[str]:
    if not _text(slide.get("figure")):
        return [f"{where} shows nothing: give it points or a drawing"] if not any(points) else []
    if len(points) > MAX_POINTS_WITH_DRAWING:
        return [
            f"{where} has a drawing and {len(points)} points; keep at most "
            f"{MAX_POINTS_WITH_DRAWING} with a drawing: give the drawing a slide of its own, "
            "with one point that says what it shows"
        ]
    return []


def _slide_faults(number: int, slide: JsonObject) -> list[str]:
    where = f"slide {number}"
    faults: list[str] = []
    title = _text(slide.get("title"))
    if _words(title) > MAX_TITLE_WORDS:
        faults.append(f"{where}: the title runs past {MAX_TITLE_WORDS} words; say it in a few")
    points = [_text(p.get("point")) for p in _records(slide.get("points"))]
    if len(points) > MAX_POINTS:
        faults.append(f"{where} has {len(points)} points; keep at most {MAX_POINTS}")
    faults += _point_faults(where, points)
    for shown in (*points, _text(slide.get("speaker_notes"))):
        if _COMMAND.search(_MATHS.sub("", shown)):
            faults.append(
                f"{where}: {shown[:50]!r} has a LaTeX command outside $ signs; put the "
                "mathematics between $ signs, or write the word"
            )
    faults += _drawing_faults(where, slide, points)
    if len(_text(slide.get("speaker_notes"))) < MIN_NOTES_CHARS:
        faults.append(f"{where} needs speaker notes: what the teacher says and asks while it is up")
    return [*faults, *wording_faults(where, slide)]


def slide_deck_issues(
    draft: Deck, own_problems: Mapping[str, Sequence[str]] | None = None
) -> list[str]:
    """Every fault in the slides written so far, each naming its step and slide."""
    issues: list[str] = []
    for unit, part in draft.written():
        slides = _records(part.get("slides"))
        if not slides:
            issues.append(f"{unit.unit_id}: write at least one slide")
        elif len(slides) > MAX_SLIDES:
            issues.append(
                f"{unit.unit_id}: {len(slides)} slides; keep a step to {MAX_SLIDES} at most"
            )
        for number, slide in enumerate(slides, start=1):
            issues += [f"{unit.unit_id}: {fault}" for fault in _slide_faults(number, slide)]
    return [
        *issues,
        *evaluation_slide_issues(draft, own_problems),
        *repeated_slides(draft),
        *repeated_drawings(draft),
        *placeholder_drawings(draft),
        *repeated_measures(draft),
        *number_line_issues(draft),
    ]


def _own_problems(note: Mapping[str, str]) -> dict[str, list[str]]:
    """The problems the note itself works or asks in each step."""
    return {step: [*worked_problems(text), *note_questions(text)] for step, text in note.items()}


def _sections(payload: Mapping[str, object]) -> list[Mapping[str, object]]:
    draft = payload.get("draft")
    sections = draft.get("sections") if isinstance(draft, dict) else None
    return [s for s in (sections if isinstance(sections, list) else []) if isinstance(s, dict)]


def _note(source: Mapping[str, object]) -> dict[str, str]:
    note = source.get("note")
    return {str(k): str(v) for k, v in note.items()} if isinstance(note, dict) else {}


def _objectives(source: Mapping[str, object]) -> list[str]:
    objectives = source.get("objectives")
    return [str(o) for o in objectives] if isinstance(objectives, list) else []


def review(payload: Mapping[str, object]) -> list[str]:
    """The deck's faults, and what the plan and the approved note have that it leaves out.

    ``payload`` holds the ``draft`` (its ``sections``) and the ``source``: the approved ``note``
    of each step and the lesson's ``objectives``; a draft without a source is checked alone.
    """
    deck = Deck.of(_sections(payload))
    source = payload.get("source")
    if not isinstance(source, dict):
        return slide_deck_issues(deck)
    note, objectives = _note(source), _objectives(source)
    return [
        *slide_deck_issues(deck, _own_problems(note)),
        *unopened_lesson(deck, note),
        *unstated_aim(deck, objectives),
        *unreadable_examples(deck, note),
        *uncovered_examples(deck, note),
        *missing_working(deck, note),
        *reasons_on_slides(deck, note),
        *crowded_slides(deck, note),
        *uncovered_questions(deck, note),
        *revealing_drawings(deck, note),
        *unpictured_rounding(deck, note),
    ]
