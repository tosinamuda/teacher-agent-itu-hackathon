"""Write a lesson plan from a teacher's document: paste its text or send the file."""

from __future__ import annotations

import hashlib
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owns_lesson_period,
)
from app.domains.content_engine.infrastructure.documents import (
    DocumentUnreadableError,
    document_text,
)
from app.domains.content_engine.infrastructure.experiments import experiment_lesson
from app.domains.content_engine.infrastructure.planning import LessonPlanning
from app.domains.jobs.api.schemas import JobAccepted
from app.infra.jobs.kinds import IMPORT_LESSON_PLAN
from app.infra.jobs.queue import JobQueue
from app.shared.auth import ROLE_TEACHER, Actor
from app.shared.authz import requires

router = APIRouter(prefix="/plan-imports", tags=["plan-imports"])


async def _lesson_the_actor_plans(actor: Actor, db: AsyncSession, session_id: str) -> None:
    if await LessonPlanning().lesson(db, session_id) is None:
        raise HTTPException(status_code=404, detail="lesson_not_found")
    if actor.role == ROLE_TEACHER and actor.teacher_id is not None:
        owns = await teacher_owns_lesson_period(
            db, teacher_id=actor.teacher_id, lesson_period_id=uuid.UUID(session_id)
        )
        if not owns:
            raise HTTPException(status_code=403, detail="not_your_class")


async def _document(text: str | None, file: UploadFile | None) -> str:
    if text and text.strip():
        return text.strip()
    if file is None:
        raise HTTPException(status_code=422, detail="send the document's text or its file")
    try:
        return document_text(file.filename or "", await file.read())
    except DocumentUnreadableError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


def import_subject(session_id: str, document: str) -> str:
    """What one import acts on: sending the same document again follows the same job."""
    digest = hashlib.sha256(document.encode("utf-8")).hexdigest()[:16]
    return f"{session_id}:plan-import:{digest}"


async def _experiment_on(db: AsyncSession, experiment_id: str, session_id: str) -> None:
    lesson = await experiment_lesson(db, experiment_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="experiment_not_found")
    if str(lesson) != session_id:
        raise HTTPException(status_code=409, detail="experiment_is_on_another_lesson")


@router.post("", response_model=JobAccepted, status_code=202)
async def import_plan(
    session_id: str = Form(..., min_length=1),
    text: str | None = Form(None),
    file: UploadFile | None = File(None),
    experiment_id: str | None = Form(None),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
    db: AsyncSession = Depends(get_db),
) -> JobAccepted:
    """Queue writing the lesson's plan from the document; follow the job it returns.

    The plan is saved as a draft for the teacher to review and approve, and becomes the named
    experiment's plan when there is one.
    """
    try:
        uuid.UUID(session_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail="lesson_not_found") from error
    await _lesson_the_actor_plans(actor, db, session_id)
    if experiment_id is not None:
        await _experiment_on(db, experiment_id, session_id)
    document = await _document(text, file)
    job_id = await JobQueue(db).ensure(
        IMPORT_LESSON_PLAN,
        session_id,
        document,
        str(actor.teacher_id) if actor.teacher_id is not None else None,
        experiment_id,
        subject=import_subject(session_id, document),
        requested_by=actor.auth_id,
    )
    return JobAccepted(job_id=job_id)
