"""Read access to source textbook records — backs the clickable lesson-plan references."""

from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.expert_content.api.schemas import TextbookRecordResponse
from app.domains.expert_content.application.errors import ExpertContentApplicationError
from app.domains.expert_content.application.textbook_record_service import (
    TextbookRecordApplicationService,
)
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/artefacts/textbook-records", tags=["expert-content"])


def _raise_http_error(error: ExpertContentApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get("/{record_id}", response_model=TextbookRecordResponse)
async def get_textbook_record(
    record_id: str,
    _actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> TextbookRecordResponse:
    """Return one source textbook record's content by its record id (e.g. ch02-b005)."""
    service = TextbookRecordApplicationService()
    try:
        return await service.get_record_response(db=db, record_id=record_id)
    except ExpertContentApplicationError as error:
        _raise_http_error(error)
