"""The slides that put the evaluation's questions to the class: no answer shown, no rehearsal."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from app.domains.content_engine.rules.slide_deck.config import EVALUATION_STEP
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.problem_numbers import holds, number_count
from app.shared.json_types import JsonObject, JsonValue

#: A problem has at least two numbers; one number alone is too common to tell problems apart.
_MIN_NUMBERS = 2
_RESULT = re.compile(r"≈|\\approx|\b(?:answer|approx\w*)\b", re.IGNORECASE)


def _points(slide: JsonObject) -> list[str]:
    entries: JsonValue | None = slide.get("points")
    return [
        str(entry["point"]).strip()
        for entry in (entries if isinstance(entries, list) else [])
        if isinstance(entry, dict) and isinstance(entry.get("point"), str)
    ]


def slides_of(part: JsonObject) -> list[tuple[JsonObject, list[str]]]:
    """Each slide of a part with its points, in order."""
    return [(slide, _points(slide)) for slide in _slides(part)]


def _slides(part: JsonObject) -> list[JsonObject]:
    slides: JsonValue | None = part.get("slides")
    return (
        [slide for slide in slides if isinstance(slide, dict)] if isinstance(slides, list) else []
    )


def _states_result(point: str) -> bool:
    return bool(_RESULT.search(point)) and any(c.isdigit() for c in point) and "?" not in point


def _stated(slide: JsonObject) -> str:
    """What a slide's points say, as the one text its numbers are read from."""
    return " ".join(_points(slide))


def _answers_given(part: JsonObject) -> list[str]:
    return [
        f"{EVALUATION_STEP}: slide {number}: {point[:60]!r} gives the answer; put it in the "
        "speaker notes and show only the question"
        for number, slide in enumerate(_slides(part), start=1)
        for point in _points(slide)
        if _states_result(point)
    ]


def _own_problem(points: list[str], own: Sequence[str]) -> bool:
    """Whether a slide starts from a problem the note itself puts in this step."""
    return bool(points) and any(holds(points[0], problem) for problem in own)


def _rehearsals(draft: Deck, problems: list[str], own: Mapping[str, Sequence[str]]) -> list[str]:
    return [
        f"{unit.unit_id}: slide {number} puts a problem the {EVALUATION_STEP} asks, so the class "
        "would meet it twice; delete the slide, or use another question of the note for this step"
        for unit, part in draft.written()
        if unit.unit_id != EVALUATION_STEP
        for number, slide in enumerate(_slides(part), start=1)
        if any(holds(_stated(slide), problem) for problem in problems)
        and not _own_problem(_points(slide), own.get(unit.unit_id, ()))
    ]


def evaluation_slide_issues(
    draft: Deck, own: Mapping[str, Sequence[str]] | None = None
) -> list[str]:
    """Faults of the evaluation's slides, and of slides that rehearse its problems.

    ``own`` holds the problems the note itself works or asks in each step: a slide that starts
    from one follows the note, so it is not a rehearsal.
    """
    evaluation = [part for unit, part in draft.written() if unit.unit_id == EVALUATION_STEP]
    problems = [
        stated
        for part in evaluation
        for slide in _slides(part)
        if number_count(stated := _stated(slide)) >= _MIN_NUMBERS
    ]
    answers = [fault for part in evaluation for fault in _answers_given(part)]
    return [*answers, *_rehearsals(draft, problems, own or {})]
