"""Legacy evaluation-prefixed event summary route."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.events.application.summary import EventSummaryReader, event_summary
from app.domains.events.infrastructure.summary_reader import SqlAlchemyEventSummaryReader
from app.shared.auth import Actor
from app.shared.authz import requires
from app.shared.json_types import JsonObject

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


def event_summary_reader(db: AsyncSession = Depends(get_db)) -> EventSummaryReader:
    return SqlAlchemyEventSummaryReader(db)


@router.get("/summary")
async def evaluation_summary(
    artefact_id: str | None = None,
    events: EventSummaryReader = Depends(event_summary_reader),
    _actor: Actor = Depends(requires(obj="experiment:*", act="read")),
) -> JsonObject:
    return await event_summary(events, artefact_id=artefact_id)
