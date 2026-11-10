"""A step whose worked examples round a number draws it on a number line."""

from __future__ import annotations

import re
from collections.abc import Mapping

from app.domains.content_engine.rules.slide_deck.config import EVALUATION_STEP
from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.note_examples import worked_text
from app.domains.content_engine.rules.slide_deck.number_lines import marks_to_write
from app.domains.content_engine.rules.slide_deck.questions import slides_of
from app.shared.latex_plain import plain_maths
from app.shared.rounding_text import ROUNDING_SIGNS, ROUNDING_WORDS

_ROUNDED = re.compile(r"(\d+\.\d+)\s*[^\d≈]{0,12}≈\s*\d")
_ROUNDS = re.compile(f"{ROUNDING_SIGNS}|{ROUNDING_WORDS}", re.IGNORECASE)


def _how(section: str) -> str:
    """The marks that draw the first decimal a worked example rounds, when it has one."""
    found = _ROUNDED.search(plain_maths(section))
    if found is None:
        return ""
    value = found.group(1)
    return f"; for {value} write \\foreach \\x/\\label in {marks_to_write(float(value))}"


def unpictured_rounding(draft: Deck, note: Mapping[str, str]) -> list[str]:
    """Each step whose note rounds in a worked example and whose slides draw nothing."""
    return [
        f"{unit.unit_id}: the note rounds a number, which is a value placed on a scale; draw "
        "it on a slide of a rounding example: a number line with the number marked between "
        f"the two whole numbers it lies between (see references/drawings.md){_how(section)}"
        for unit, part in draft.written()
        if unit.unit_id != EVALUATION_STEP
        and _ROUNDS.search(section := worked_text(note.get(unit.unit_id, "")))
        and not any(str(slide.get("figure") or "").strip() for slide, _ in slides_of(part))
    ]
