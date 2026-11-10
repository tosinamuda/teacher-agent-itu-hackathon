"""Learner management routes."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.learners.application import LearnerApplicationError, LearnerApplicationService
from app.domains.learners.application.identity import student_id_of
from app.domains.learners.schemas import (
    LearnerCreateRequest,
    LearnerResponse,
    LearnerUpdateRequest,
    PaginatedLearnerResponse,
)
from app.shared.auth import ROLE_STUDENT, Actor, get_actor
from app.shared.authz import enforce, requires

if TYPE_CHECKING:
    # Type-annotation-only — see ``api ↛ models`` rule.
    from app.domains.learners.models.learner import LearnerProfile

router = APIRouter(tags=["learners"])


def _raise_http_error(error: LearnerApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


def _learner_response(
    learner: LearnerProfile,
    *,
    class_name: str | None = None,
) -> LearnerResponse:
    return LearnerResponse(
        student_id=learner.student_id,
        code=learner.code,
        full_name=learner.full_name,
        grade=learner.grade,
        track=learner.track,
        class_id=learner.class_id,
        class_name=class_name,
        field_of_study=learner.field_of_study,
        trade_subject=learner.trade_subject,
        field_core_subjects=learner.field_core_subjects,
        language_level=learner.language_level,
        pace_preference=learner.pace_preference,
        time_budget_minutes=learner.time_budget_minutes,
        created_at=learner.created_at,
    )


@router.post("/learners", response_model=LearnerResponse)
async def create_learner(
    payload: LearnerCreateRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="learner:*", act="create")),
) -> LearnerResponse:
    service = LearnerApplicationService()
    try:
        learner = await service.create_learner(db=db, payload=payload)
    except LearnerApplicationError as error:
        _raise_http_error(error)
    return _learner_response(learner)


@router.get("/learners", response_model=PaginatedLearnerResponse)
async def list_learners(
    grade: str | None = None,
    track: str | None = None,
    class_id: str | None = None,
    field_of_study: str | None = None,
    page: int = 1,
    page_size: int = 10,
    _actor: Actor = Depends(requires(obj="learner:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> PaginatedLearnerResponse:
    service = LearnerApplicationService()
    try:
        rows, total = await service.list_learners(
            db=db,
            grade=grade,
            track=track,
            class_id=class_id,
            field_of_study=field_of_study,
            page=page,
            page_size=page_size,
        )
    except LearnerApplicationError as error:
        # e.g. a malformed ?class_id= → 422 (was an unhandled 500 before).
        _raise_http_error(error)
    return PaginatedLearnerResponse(
        data=[_learner_response(learner, class_name=class_name) for learner, class_name in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/learners/{learner_id}", response_model=LearnerResponse)
async def get_learner(
    learner_id: str,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> LearnerResponse:
    """A learner's profile: a learner reads their own, a teacher, admin or researcher any."""
    if actor.role == ROLE_STUDENT:
        if learner_id != await student_id_of(actor, db):
            raise HTTPException(status_code=403, detail="You can only see your own profile.")
    else:
        await enforce(actor, obj="learner:*", act="read", db=db)
    service = LearnerApplicationService()
    try:
        learner, class_name = await service.get_learner(db=db, learner_id=learner_id)
    except LearnerApplicationError as error:
        _raise_http_error(error)
    return _learner_response(learner, class_name=class_name)


@router.put("/learners/{learner_id}", response_model=LearnerResponse)
async def update_learner(
    learner_id: str,
    payload: LearnerUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="learner:*", act="update")),
) -> LearnerResponse:
    service = LearnerApplicationService()
    try:
        learner = await service.update_learner(
            db=db,
            learner_id=learner_id,
            payload=payload,
        )
    except LearnerApplicationError as error:
        _raise_http_error(error)
    return _learner_response(learner)
