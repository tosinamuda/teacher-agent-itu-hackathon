from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.models.events import Event


class EventRepository:
    async def get_event(self, db: AsyncSession, event_id: str) -> Event | None:
        result = await db.execute(select(Event).filter(Event.event_id == event_id))
        return result.scalars().first()

    async def save_event(self, db: AsyncSession, event: Event) -> Event:
        db.add(event)
        await db.commit()
        return event
