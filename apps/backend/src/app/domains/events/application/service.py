from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.infrastructure.repository import EventRepository
from app.domains.events.models.events import Event
from app.domains.events.schemas.events import EventIn
from app.shared.ids import PublicIdPrefix, new_public_id


@dataclass(frozen=True)
class EventApplicationError(Exception):
    status_code: int
    detail: str


class EventApplicationService:
    def __init__(self, repository: EventRepository | None = None) -> None:
        self.repository = repository or EventRepository()

    async def ingest_event(
        self,
        *,
        db: AsyncSession,
        payload: EventIn,
    ) -> str:
        event_id = payload.event_id or new_public_id(PublicIdPrefix.EVENT)
        event_timestamp = payload.event_timestamp or datetime.now(timezone.utc)

        existing_event = await self.repository.get_event(db, event_id)
        if existing_event is not None:
            raise EventApplicationError(409, "event_id already exists")

        event = Event(
            event_id=event_id,
            student_id=payload.student_id,
            artefact_id=payload.artefact_id,
            event_type=payload.event_type,
            payload=payload.payload,
            event_timestamp=event_timestamp,
        )
        try:
            await self.repository.save_event(db, event)
        except IntegrityError as exc:
            # Concurrent caller inserted the same event_id between our check and
            # insert — the unique index caught it; surface the intended 409.
            await db.rollback()
            raise EventApplicationError(409, "event_id already exists") from exc
        return event_id
