"""Event ingestion routes."""

from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.events.application.service import EventApplicationError, EventApplicationService
from app.domains.events.schemas.events import EventIn, EventOut

router = APIRouter(prefix="/events", tags=["events"])


def _raise_http_error(error: EventApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post("", response_model=EventOut)
async def ingest_event(
    payload: EventIn,
    db: AsyncSession = Depends(get_db),
) -> EventOut:
    service = EventApplicationService()
    try:
        event_id = await service.ingest_event(db=db, payload=payload)
    except EventApplicationError as error:
        _raise_http_error(error)
    return EventOut(event_id=event_id, status="ok")
