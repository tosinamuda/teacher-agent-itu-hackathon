"""Teaching-sequence routes."""

from __future__ import annotations

import uuid
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.teaching.application.sequence_service import (
    TeachingSequenceApplicationError,
    TeachingSequenceApplicationService,
)
from app.domains.teaching.schemas import (
    LessonPeriodCreateRequest,
    LessonPeriodResponse,
    LessonPeriodUpdateRequest,
    SchemeOfWorkResponse,
    SchemeOfWorkUpdateRequest,
    TermClassSubjectResponse,
)
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(tags=["teaching"])


def _raise_http_error(error: TeachingSequenceApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get(
    "/term-class-subjects/by-id/{term_class_subject_id}",
    response_model=TermClassSubjectResponse,
)
async def get_term_class_subject_by_id(
    term_class_subject_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> TermClassSubjectResponse:
    service = TeachingSequenceApplicationService()
    try:
        term_class_subject = await service.get_term_class_subject_by_id(
            db=db,
            term_class_subject_id=term_class_subject_id,
        )
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return term_class_subject


@router.get("/term-class-subjects/{course_id}", response_model=TermClassSubjectResponse)
async def get_term_class_subject_for_course(
    course_id: uuid.UUID,
    term: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> TermClassSubjectResponse:
    service = TeachingSequenceApplicationService()
    try:
        term_class_subject = await service.get_term_class_subject_for_course(
            db=db,
            course_id=course_id,
            term=term,
        )
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return term_class_subject


@router.get("/scheme-of-work/{week_id}", response_model=SchemeOfWorkResponse)
async def get_scheme_of_work_week(
    week_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> SchemeOfWorkResponse:
    service = TeachingSequenceApplicationService()
    try:
        week = await service.get_scheme_of_work_week(db=db, week_id=week_id)
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return week


@router.put("/scheme-of-work/{week_id}", response_model=SchemeOfWorkResponse)
async def update_scheme_of_work_week(
    week_id: uuid.UUID,
    payload: SchemeOfWorkUpdateRequest,
    _actor: Actor = Depends(requires(obj="workspace:*", act="update")),
    db: AsyncSession = Depends(get_db),
) -> SchemeOfWorkResponse:
    service = TeachingSequenceApplicationService()
    try:
        week = await service.update_scheme_of_work_week(
            db=db,
            week_id=week_id,
            payload=payload,
        )
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return week


@router.post("/scheme-of-work/{week_id}/lesson-periods", response_model=LessonPeriodResponse)
async def create_lesson_period(
    week_id: uuid.UUID,
    payload: LessonPeriodCreateRequest,
    _actor: Actor = Depends(requires(obj="workspace:*", act="update")),
    db: AsyncSession = Depends(get_db),
) -> LessonPeriodResponse:
    service = TeachingSequenceApplicationService()
    try:
        lesson_period = await service.create_lesson_period(
            db=db,
            week_id=week_id,
            payload=payload,
        )
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return lesson_period


@router.put("/lesson-periods/{lesson_period_id}", response_model=LessonPeriodResponse)
async def update_lesson_period(
    lesson_period_id: uuid.UUID,
    payload: LessonPeriodUpdateRequest,
    _actor: Actor = Depends(requires(obj="workspace:*", act="update")),
    db: AsyncSession = Depends(get_db),
) -> LessonPeriodResponse:
    service = TeachingSequenceApplicationService()
    try:
        lesson_period = await service.update_lesson_period(
            db=db,
            lesson_period_id=lesson_period_id,
            payload=payload,
        )
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return lesson_period


@router.delete("/lesson-periods/{lesson_period_id}")
async def delete_lesson_period(
    lesson_period_id: uuid.UUID,
    _actor: Actor = Depends(requires(obj="workspace:*", act="update")),
    db: AsyncSession = Depends(get_db),
) -> dict[str, bool]:
    service = TeachingSequenceApplicationService()
    try:
        await service.delete_lesson_period(db=db, lesson_period_id=lesson_period_id)
    except TeachingSequenceApplicationError as error:
        _raise_http_error(error)
    return {"success": True}
