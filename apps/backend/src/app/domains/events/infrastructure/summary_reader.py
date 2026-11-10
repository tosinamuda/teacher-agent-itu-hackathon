"""SQLAlchemy event-summary reader."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.models.events import Event


class SqlAlchemyEventSummaryReader:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def event_types(self, *, artefact_id: str | None) -> list[str]:
        statement = select(Event.event_type)
        if artefact_id is not None:
            statement = statement.where(Event.artefact_id == artefact_id)
        return list((await self._session.execute(statement)).scalars().all())
