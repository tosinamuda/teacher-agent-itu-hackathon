"""Who may author for a lesson."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.shared.auth import ROLE_TEACHER, Actor


async def assert_actor_owns_lesson(
    db: AsyncSession, *, actor: Actor, lesson_period_id: UUID
) -> None:
    """A teacher may only author for a class they teach; a manager bypasses."""
    if actor.role != ROLE_TEACHER or actor.teacher_id is None:
        return
    from app.domains.artefacts.types.lesson_plan.application.ownership import (
        teacher_owns_lesson_period,
    )

    owns = await teacher_owns_lesson_period(
        db, teacher_id=actor.teacher_id, lesson_period_id=lesson_period_id
    )
    if not owns:
        raise ExperimentApplicationError(
            403, "You can only author a plan for a class + subject you teach."
        )
