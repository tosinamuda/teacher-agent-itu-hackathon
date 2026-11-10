from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.tutor.application.service import TutorApplicationError, TutorApplicationService
from app.domains.tutor.schemas import TutorQueryRequest, TutorQueryResponse
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/tutor", tags=["tutor"])


def _raise_http_error(error: TutorApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post("/query", response_model=TutorQueryResponse)
async def query_tutor(
    payload: TutorQueryRequest,
    _actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> TutorQueryResponse:
    service = TutorApplicationService()
    try:
        return await service.answer_question(
            db=db,
            artefact_id=payload.artefact_id,
            step_id=payload.step_id,
            question=payload.question,
        )
    except TutorApplicationError as error:
        _raise_http_error(error)
