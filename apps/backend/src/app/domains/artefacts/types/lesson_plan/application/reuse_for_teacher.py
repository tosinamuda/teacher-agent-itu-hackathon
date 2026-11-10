"""Reuse an existing plan as a lesson's plan, for the teacher who asks."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.errors import (
    PlanNotOwnedByTeacherError,
    SessionNotFoundError,
)
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owns_lesson_period,
)
from app.domains.artefacts.types.lesson_plan.application.plan_reuse import ReusedPlan
from app.domains.artefacts.types.lesson_plan.application.service import (
    LessonPlanApplicationService,
)
from app.shared.auth import ROLE_TEACHER, Actor
from app.shared.json_types import JsonObject


async def _owns(db: AsyncSession, actor: Actor, lesson_period_id: uuid.UUID) -> bool:
    """A teacher owns the lessons of their own classes; any other caller is allowed."""
    if actor.role != ROLE_TEACHER or actor.teacher_id is None:
        return True
    return await teacher_owns_lesson_period(
        db, teacher_id=actor.teacher_id, lesson_period_id=lesson_period_id
    )


async def reuse_plan_for_lesson(
    db: AsyncSession,
    service: LessonPlanApplicationService,
    actor: Actor,
    *,
    session_id: str,
    source_plan_version_id: str | None,
    session_plan: JsonObject | None,
    curriculum_choices: dict[str, str],
) -> ReusedPlan:
    """Save an existing plan as the lesson's draft plan, or say which choices are left.

    A teacher may reuse the plans of lessons they teach, and put one only on a lesson they teach.
    """
    try:
        lesson = uuid.UUID(session_id)
    except ValueError:
        raise SessionNotFoundError(session_id) from None
    if not await _owns(db, actor, lesson):
        raise PlanNotOwnedByTeacherError
    source, imported_from = session_plan or {}, None
    if source_plan_version_id is not None:
        found = await service.reusable_source(source_plan_version_id)
        if not await _owns(db, actor, found.lesson_period_id):
            raise PlanNotOwnedByTeacherError
        source, imported_from = found.session_plan, found.version_id
    teacher_id = str(actor.teacher_id) if actor.teacher_id else None
    return await service.reuse_plan(
        session_id=session_id,
        source=source,
        chosen=curriculum_choices,
        teacher_id=teacher_id,
        imported_from=imported_from,
    )
