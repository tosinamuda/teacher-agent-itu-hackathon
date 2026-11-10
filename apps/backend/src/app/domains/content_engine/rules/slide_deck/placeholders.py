"""A drawing the writer left unfinished: a placeholder is not a figure a class can be shown."""

from __future__ import annotations

import re

from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.domains.content_engine.rules.slide_deck.questions import slides_of

#: A TikZ comment that says the drawing is not all there: "omitted for brevity", "placeholder".
_UNFINISHED = re.compile(
    r"%[^\n]*(?:omitted|brevity|placeholder|to be (?:drawn|added|completed)|todo|\.\.\.|…)",
    re.IGNORECASE,
)


def placeholder_drawings(draft: Deck) -> list[str]:
    """Each slide whose drawing says in a comment that it is not finished."""
    return [
        f"{unit.unit_id}: slide {number} draws a placeholder, not the figure; draw the whole "
        "figure, or leave the drawing out and say it in words"
        for unit, part in draft.written()
        for number, (slide, _) in enumerate(slides_of(part), start=1)
        if _UNFINISHED.search(str(slide.get("figure") or ""))
    ]
