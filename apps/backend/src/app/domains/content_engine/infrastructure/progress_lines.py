"""What an agent has done in its latest run, from the progress channel its tap writes."""

from __future__ import annotations

from collections.abc import Sequence

from app.shared.json_types import JsonObject

#: The most events of an agent's work one read returns.
MAX_LINES = 300


def lines_after(
    events: Sequence[tuple[int, JsonObject]], after: int
) -> list[tuple[int, JsonObject]]:
    """The events of the latest run past ``after``: a run begins at its ``start`` event."""
    starts = [index for index, (_, event) in enumerate(events) if event.get("kind") == "start"]
    current = events[starts[-1] :] if starts else []
    return [(event_id, event) for event_id, event in current if event_id > after][-MAX_LINES:]


def data_of(event: JsonObject) -> JsonObject:
    """What a progress event carries: the chat event's data."""
    data = event.get("data")
    return data if isinstance(data, dict) else {}
