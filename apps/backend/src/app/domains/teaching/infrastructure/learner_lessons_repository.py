"""A learner's lessons that have a plan, with where their revision note stands."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.teaching.domain.learner_lessons import LessonNote, PlannedLesson
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace


class LearnerLessonsRepository:
    async def lessons_of(
        self, db: AsyncSession, workspace_id: uuid.UUID, student_id: str
    ) -> list[PlannedLesson]:
        """Every lesson of the workspace's subject that has a plan, in the order taught.

        Each carries the learner's newest revision note for it, unless it was rejected.
        """
        lessons = await self._planned(db, workspace_id)
        notes = await self._notes(db, workspace_id, student_id)
        return [PlannedLesson(lesson, title, notes.get(lesson)) for lesson, title in lessons]

    async def _planned(
        self, db: AsyncSession, workspace_id: uuid.UUID
    ) -> list[tuple[uuid.UUID, str]]:
        rows = (
            await db.execute(
                select(LessonPeriod.id, LessonPlan.title)
                .join(LessonPlan, LessonPlan.lesson_period_id == LessonPeriod.id)
                .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
                .join(
                    TeacherWorkspace,
                    TeacherWorkspace.term_class_subject_id == SchemeOfWork.term_class_subject_id,
                )
                .where(TeacherWorkspace.id == workspace_id)
                .order_by(SchemeOfWork.week_number, LessonPeriod.period_number, LessonPlan.plan_id)
            )
        ).all()
        # A lesson can have several plans; it is one lesson, named by its first plan.
        titles: dict[uuid.UUID, str] = {}
        for lesson, title in rows:
            titles.setdefault(lesson, title)
        return list(titles.items())

    async def _notes(
        self, db: AsyncSession, workspace_id: uuid.UUID, student_id: str
    ) -> dict[uuid.UUID, LessonNote]:
        rows = (
            await db.execute(
                select(LessonPeriod.id, Artefact.artefact_id, Artefact.review_status)
                .select_from(Artefact)
                .join(PlanVersion, PlanVersion.version_id == Artefact.plan_version_id)
                .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
                .join(LessonPeriod, LessonPeriod.id == LessonPlan.lesson_period_id)
                .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
                .join(
                    TeacherWorkspace,
                    TeacherWorkspace.term_class_subject_id == SchemeOfWork.term_class_subject_id,
                )
                .where(
                    TeacherWorkspace.id == workspace_id,
                    Artefact.student_id == student_id,
                    Artefact.scope == ArtefactScope.LEARNER_LEVEL.value,
                    Artefact.review_status != ArtefactReviewStatus.REJECTED,
                )
                .order_by(Artefact.created_at)
            )
        ).all()
        # Oldest first, so the newest note for a lesson is the one left.
        return {lesson: LessonNote(artefact_id, status) for lesson, artefact_id, status in rows}
