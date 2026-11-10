"""A worked example's slide shows every line of the note's working, in the note's numbers."""

from __future__ import annotations

from collections.abc import Iterator, Mapping

from app.domains.content_engine.rules.slide_deck.config import EVALUATION_STEP, LIMITS
from app.domains.content_engine.rules.slide_deck.coverage import words_of
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.note_examples import worked_examples
from app.domains.content_engine.rules.slide_deck.problem_numbers import holds, number_count
from app.domains.content_engine.rules.slide_deck.questions import slides_of
from app.shared.latex_plain import plain_maths

_SHOWN = 70
_REASON = " — "
#: A point carries the note's reason when it keeps this share of the reason's words.
_REASON_KEPT = 0.7
_MIN_REASON_WORDS = 2
#: A slide that is not a worked example holds this many points at most.
_TEACHING_POINTS = LIMITS["teaching_points"]


def _line_of(line: str) -> str:
    """A line of the note's working as written, without the reason that follows its dash."""
    return line.split(_REASON, 1)[0]


def _working_of(line: str) -> str:
    return plain_maths(_line_of(line))


def worked_lines(note: str) -> list[tuple[str, list[str]]]:
    """The problem of each worked example in a step's note with the lines of its working."""
    return [(example.problem, example.lines) for example in worked_examples(note)]


def _reason_of(line: str) -> str:
    return line.split(_REASON, 1)[1] if _REASON in line else ""


def worked_slides(
    draft: Deck, note: Mapping[str, str]
) -> Iterator[tuple[str, str, int, list[str], list[str]]]:
    """Each worked example that has a slide: step, problem, slide number, its points, its lines."""
    for unit, part in draft.written():
        if unit.unit_id == EVALUATION_STEP:
            continue
        slides = slides_of(part)
        for problem, lines in worked_lines(note.get(unit.unit_id, "")):
            if not number_count(problem):
                continue
            for number, (_, points) in enumerate(slides, start=1):
                if points and holds(points[0], problem):
                    yield unit.unit_id, problem, number, points, lines
                    break


def missing_working(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each line of a note's worked example, with numbers, that its slide leaves out."""
    return [
        f"{step}: slide {number} works the example {problem[:_SHOWN]!r} but "
        f"leaves out the note's line {_working_of(line)!r}; show every line of the "
        "note's working, in order"
        for step, problem, number, points, lines in worked_slides(draft, note)
        for line in lines
        if number_count(_line_of(line))
        and not any(holds(point, _line_of(line)) for point in points[1:])
    ]


def _gives_reason(point: str, line: str) -> bool:
    reason = words_of(_reason_of(line))
    if _REASON in point:
        return True
    return len(reason) >= _MIN_REASON_WORDS and (
        len(reason & words_of(point)) >= _REASON_KEPT * len(reason)
    )


def reasons_on_slides(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each working point that carries the note's reason for the line, which is for the notes."""
    return [
        f"{step}: slide {number} writes the reason after the line {_working_of(line)!r}; a "
        "working point is the line alone, in the note's numbers, and its reason goes in the "
        "speaker notes"
        for step, _, number, points, lines in worked_slides(draft, note)
        for line in lines
        if number_count(_line_of(line))
        and _reason_of(line)
        and any(holds(point, _line_of(line)) and _gives_reason(point, line) for point in points[1:])
    ]


def crowded_slides(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each slide that is not a worked example and has more points than a class can hold."""
    worked = {(step, number) for step, _, number, _, _ in worked_slides(draft, note)}
    return [
        f"{unit.unit_id}: slide {number} has {len(points)} points; a slide that teaches a rule "
        f"or an idea holds at most {_TEACHING_POINTS}: put the rest on the next slide, so each "
        "is shown large"
        for unit, part in draft.written()
        if unit.unit_id != EVALUATION_STEP
        for number, (_, points) in enumerate(slides_of(part), start=1)
        if len(points) > _TEACHING_POINTS and (unit.unit_id, number) not in worked
    ]
