"""Pydantic contracts for the generation log API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from app.shared.schema_base import UtcDatetime

if TYPE_CHECKING:
    from app.domains.generation_log.models.generation_event import GenerationEvent


class LoggedEvent(BaseModel):
    """One recorded LM call, with the request/response captured."""

    id: str
    seq: int
    kind: str
    model: str
    correlation_id: str | None
    context: dict
    request: dict
    response: dict
    duration_ms: float | None
    token_usage: dict | None
    created_at: UtcDatetime

    @classmethod
    def from_model(cls, event: GenerationEvent) -> LoggedEvent:
        """Build the API contract from a persisted GenerationEvent row."""
        return cls(
            id=str(event.id),
            seq=event.seq,
            kind=event.kind,
            model=event.model,
            correlation_id=event.correlation_id,
            context=event.context or {},
            request=event.request or {},
            response=event.response or {},
            duration_ms=event.duration_ms,
            token_usage=event.token_usage,
            created_at=event.created_at,
        )
