"""Event-summary query owned by the events domain."""

from __future__ import annotations

from collections import Counter
from typing import Protocol

from app.shared.json_types import JsonObject


class EventSummaryReader(Protocol):
    async def event_types(self, *, artefact_id: str | None) -> list[str]: ...


async def event_summary(
    reader: EventSummaryReader,
    *,
    artefact_id: str | None,
) -> JsonObject:
    event_types = await reader.event_types(artefact_id=artefact_id)
    return {
        "artefact_id": artefact_id,
        "total_events": len(event_types),
        "by_type": dict(Counter(event_types)),
    }
