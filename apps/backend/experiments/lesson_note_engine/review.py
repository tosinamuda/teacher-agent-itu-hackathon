"""Blind the two arms' notes for review: each step's pair in a random order, the key apart."""

from __future__ import annotations

import random

from app.shared.json_types import JsonObject

ARMS = ("current", "engine")


def blinded(lessons: list[JsonObject], seed: int) -> tuple[list[JsonObject], JsonObject]:
    """The review items and the key that says which arm wrote each item's first note."""
    order = random.Random(seed)
    items: list[JsonObject] = []
    key: JsonObject = {}
    for lesson in lessons:
        notes = lesson["notes"]
        for step in lesson["steps"]:
            first, second = order.sample(list(ARMS), k=2)
            item_id = f"{lesson['plan_version_id']}:{step['step_id']}"
            items.append(
                {
                    "item_id": item_id,
                    "lesson": lesson["title"],
                    "step": step["title"],
                    "note_1": notes[first][step["step_id"]],
                    "note_2": notes[second][step["step_id"]],
                }
            )
            key[item_id] = {"note_1": first, "note_2": second}
    return items, key
