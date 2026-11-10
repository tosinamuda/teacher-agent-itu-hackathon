"""Clear what was made for a lesson, so the teacher can start it again from nothing."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.ops.application.lesson_reset import ResetPlan, plan_reset, reset_lesson
from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationError
from app.domains.teaching.infrastructure.study_results_repository import StudyResultsRepository


class LessonStartOver:
    """The lesson stays in its class's scheme of work; what was made for it goes.

    A lesson the study ran on is never cleared, so a teacher cannot remove it by mistake.
    """

    def __init__(self, repository: StudyResultsRepository | None = None) -> None:
        self._repository = repository or StudyResultsRepository()

    async def preview(
        self, db: AsyncSession, workspace_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> ResetPlan:
        await self._in_workspace(db, workspace_id, lesson_period_id)
        connection = await db.connection()
        return await connection.run_sync(lambda conn: plan_reset(conn, lesson_period_id.hex))

    async def clear(
        self, db: AsyncSession, workspace_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> dict[str, int]:
        await self._in_workspace(db, workspace_id, lesson_period_id)
        connection = await db.connection()
        try:
            removed = await connection.run_sync(
                lambda conn: reset_lesson(conn, lesson_period_id.hex)
            )
        except ValueError as error:
            raise TeachingSequenceApplicationError(409, str(error)) from error
        await db.commit()
        return removed

    async def _in_workspace(
        self, db: AsyncSession, workspace_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> None:
        if not await self._repository.lesson_in_workspace(db, workspace_id, lesson_period_id):
            raise TeachingSequenceApplicationError(404, "workspace_or_lesson_not_found")
