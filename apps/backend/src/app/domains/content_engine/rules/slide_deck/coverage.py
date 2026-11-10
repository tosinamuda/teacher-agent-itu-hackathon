"""A step's slides show every worked example of the approved note, each from its problem."""

from __future__ import annotations

import re
from collections.abc import Mapping

from app.domains.content_engine.rules.slide_deck.config import EVALUATION_STEP
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.note_examples import (
    has_unreadable_examples,
    worked_examples,
)
from app.domains.content_engine.rules.slide_deck.problem_numbers import holds, number_count
from app.domains.content_engine.rules.slide_deck.questions import slides_of
from app.shared.json_types import JsonObject

_SHOWN = 70
_WORDS = re.compile(r"[a-z']+")
#: How much of the note's wording a first point keeps for the problem to read as stated in full.
_IN_FULL = 0.8


def worked_problems(note: str) -> list[str]:
    """The problem of each worked example in one step's note, in order."""
    return [example.problem for example in worked_examples(note)]


def words_of(text: str) -> set[str]:
    return set(_WORDS.findall(text.casefold().replace("\u2019", "'")))


def _starts_with(points: list[str], problem: str) -> bool:
    return bool(points) and holds(points[0], problem)


def _in_full(points: list[str], problem: str) -> bool:
    """Whether the first point keeps the note's own words, not a shortened label of them."""
    wanted = words_of(problem)
    return bool(wanted) and len(wanted & words_of(points[0])) >= _IN_FULL * len(wanted)


def _shows(slide: JsonObject, points: list[str], problem: str) -> bool:
    return holds(" ".join([str(slide.get("title", "")), *points]), problem)


def _fault(step: str, problem: str, slides: list[tuple[JsonObject, list[str]]]) -> list[str]:
    if not number_count(problem):
        return []
    starting = [
        (n, points)
        for n, (_, points) in enumerate(slides, start=1)
        if _starts_with(points, problem)
    ]
    if any(_in_full(points, problem) for _, points in starting):
        return []
    shown = problem[:_SHOWN]
    if starting:
        return [
            f"{step}: slide {starting[0][0]} starts the example {shown!r} with a shortened "
            "problem; write the note's question in full as its first point"
        ]
    for number, (slide, points) in enumerate(slides, start=1):
        if _shows(slide, points, problem):
            return [
                f"{step}: slide {number} works the example {shown!r} but does not start from "
                "its problem; make its first point the note's question, written in full, "
                "then the working"
            ]
    return [
        f"{step}: the note's worked example {shown!r} has no slide; give it one slide whose "
        "first point is the note's question, written in full, and whose next points are the "
        "working"
    ]


def uncovered_examples(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each worked example of the note that its step's slides do not show from its problem."""
    return [
        fault
        for unit, part in draft.written()
        if unit.unit_id != EVALUATION_STEP
        for problem in worked_problems(note.get(unit.unit_id, ""))
        for fault in _fault(unit.unit_id, problem, slides_of(part))
    ]


def unreadable_examples(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each step whose note works examples in a form the checks cannot read."""
    return [
        f"{unit.unit_id}: the note works examples in a form these checks cannot read, so the "
        "slides cannot be checked against them; the lesson note needs rewriting before this "
        "step's slides can be checked"
        for unit, _ in draft.written()
        if unit.unit_id != EVALUATION_STEP and has_unreadable_examples(note.get(unit.unit_id, ""))
    ]
