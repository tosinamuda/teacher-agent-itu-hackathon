"""A drawing in the evaluation shows only the numbers its question states."""

from __future__ import annotations

from collections.abc import Mapping

from app.domains.content_engine.rules.slide_deck.config import EVALUATION_STEP
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.number_lines import label_numbers
from app.domains.content_engine.rules.slide_deck.problem_numbers import holds
from app.domains.content_engine.rules.slide_deck.question_coverage import note_questions
from app.domains.content_engine.rules.slide_deck.questions import slides_of


def revealing_drawings(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each drawing of the evaluation that prints a number its questions do not state."""
    issues: list[str] = []
    for unit, part in draft.written():
        if unit.unit_id != EVALUATION_STEP:
            continue
        asked = " ".join(note_questions(note.get(unit.unit_id, "")))
        for number, (slide, _) in enumerate(slides_of(part), start=1):
            unstated = [
                n for n in label_numbers(str(slide.get("figure") or "")) if not holds(asked, n)
            ]
            if unstated:
                issues.append(
                    f"{unit.unit_id}: slide {number}: the drawing shows {', '.join(unstated)}, "
                    "which no question states, so it gives away the working; delete the slide"
                )
    return issues
