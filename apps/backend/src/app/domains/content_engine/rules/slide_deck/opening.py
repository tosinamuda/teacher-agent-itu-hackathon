"""The introduction opens with the question the note puts to the class."""

from __future__ import annotations

from collections.abc import Mapping

from app.domains.content_engine.rules.slide_deck.config import INTRO_STEP
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.question_coverage import (
    note_questions,
    puts,
)
from app.domains.content_engine.rules.slide_deck.questions import slides_of

_SHOWN = 70


def unopened_lesson(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """The introduction, when its first slide does not put the note's first question."""
    faults: list[str] = []
    for unit, part in draft.written():
        questions = note_questions(note.get(unit.unit_id, "")) if unit.unit_id == INTRO_STEP else []
        slides = slides_of(part)
        if questions and slides and not puts(questions[0], slides[0][1]):
            faults.append(
                f"{unit.unit_id}: the first slide must put the note's first question to the "
                f"class, {questions[0][:_SHOWN]!r}, worded as the note words it; open with it "
                "and put the aim and the other slides after it"
            )
    return faults
