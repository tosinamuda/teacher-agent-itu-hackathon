"""Slides and decks built by hand, for the tests of the checks that read them."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.deck import Deck
from app.shared.json_types import JsonObject

NOTES = "Ask the class, wait for answers, and note anyone who forgets to round."


def slide(*points: str, title: str = "A slide") -> JsonObject:
    return {
        "title": title,
        "points": [{"point": point} for point in points],
        "speaker_notes": NOTES,
    }


def deck(**steps: list[JsonObject]) -> Deck:
    return Deck.of(
        [{"unit_id": step, "part": {"slides": slides}} for step, slides in steps.items()]
    )
