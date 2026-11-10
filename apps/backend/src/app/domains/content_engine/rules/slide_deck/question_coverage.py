"""A step's slides put every question of the approved note to the class."""

from __future__ import annotations

import re
from collections.abc import Mapping

from app.domains.content_engine.rules.slide_deck.coverage import words_of
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.problem_numbers import holds, number_count
from app.domains.content_engine.rules.slide_deck.questions import slides_of
from app.domains.content_engine.rules.slide_deck.titles import title_of

_FIELDS = ("questions_for_the_class", "classwork")
_QUESTION = re.compile(
    rf"\*\*{title_of('question')}\.\*\*\s*(.+?)\s*\*\*{title_of('expected_answer')}\.\*\*",
    re.DOTALL,
)
_SHOWN = 70
#: How much of a question's words one slide keeps for the question to be put as the note words it.
_KEPT = 0.7
#: A question with this many numbers is told from the others by them; one with fewer, by its words
#: as well as its numbers.
_NUMBERED = 2


def note_questions(note: str) -> list[str]:
    """Each question the note puts to the class in one step, in order."""
    sections = [
        match.group(1)
        for field in _FIELDS
        for match in re.finditer(
            rf"^####\s+{re.escape(title_of(field))}\s*$(.*?)(?=^####\s|\Z)",
            note,
            re.MULTILINE | re.DOTALL,
        )
    ]
    return [question for section in sections for question in _QUESTION.findall(section)]


def puts(question: str, points: list[str]) -> bool:
    """Whether one slide's points put the note's question, as the note words it."""
    text = " ".join(points)
    numbered = number_count(question)
    if numbered and not holds(text, question):
        return False
    wanted = words_of(question)
    return numbered >= _NUMBERED or len(wanted & words_of(text)) >= _KEPT * len(wanted)


def uncovered_questions(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each question of the note that no slide of its step puts to the class."""
    return [
        f"{unit.unit_id}: the note's question {question[:_SHOWN]!r} has no slide; put it to the "
        "class on a slide, worded as the note words it and with the numbers the note gives"
        for unit, part in draft.written()
        for question in note_questions(note.get(unit.unit_id, ""))
        if not any(puts(question, points) for _, points in slides_of(part))
    ]
