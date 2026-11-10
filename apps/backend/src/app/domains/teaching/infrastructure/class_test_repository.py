"""A class's learners, each with their latest class-test submission for the workspace's subject."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
    PlanVersionObjective,
)
from app.domains.assessments.models.exit_ticket import ExitTicketSubmission
from app.domains.learners.models.learner import LearnerProfile
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import TeacherWorkspace
from app.domains.teaching.models.syllabus import LessonPeriod, SchemeOfWork
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class LatestTest:
    lesson_title: str
    results: JsonObject
    taken_at: datetime


@dataclass(frozen=True)
class ClassLearnerRow:
    student_id: str
    full_name: str
    latest_test: LatestTest | None


@dataclass(frozen=True)
class LearnerTest:
    plan_version_id: str
    lesson_period_id: uuid.UUID
    lesson_title: str
    results: JsonObject
    taken_at: datetime
    #: Who entered the results for the learner, when the learner did not answer themselves.
    entered_by: str | None = None


@dataclass(frozen=True)
class LearnerResults:
    full_name: str
    tests: list[LearnerTest]
    """Newest first."""
    objective_texts: dict[tuple[str, str], str]
    """The wording of each objective, by (plan version, objective id)."""


class ClassTestRepository:
    async def results_for_learner(
        self, db: AsyncSession, workspace_id: uuid.UUID, student_id: str
    ) -> LearnerResults | None:
        """The learner's class tests for the workspace's subject.

        None when the workspace does not exist or the learner is not in its class.
        """
        offering = await self._offering_of(db, workspace_id)
        if offering is None:
            return None
        learner = (
            await db.execute(
                select(LearnerProfile.full_name).where(
                    LearnerProfile.student_id == student_id,
                    LearnerProfile.class_id == offering.class_id,
                )
            )
        ).scalar_one_or_none()
        if learner is None:
            return None
        rows = (
            await db.execute(
                select(
                    ExitTicketSubmission.plan_version_id,
                    ExitTicketSubmission.results,
                    ExitTicketSubmission.created_at,
                    LessonPlan.title,
                    LessonPeriod.id,
                    ExitTicketSubmission.entered_by,
                )
                .join(PlanVersion, PlanVersion.version_id == ExitTicketSubmission.plan_version_id)
                .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
                .join(LessonPeriod, LessonPeriod.id == LessonPlan.lesson_period_id)
                .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
                .where(
                    SchemeOfWork.term_class_subject_id == offering.id,
                    ExitTicketSubmission.student_id == student_id,
                )
                .order_by(ExitTicketSubmission.created_at.desc())
            )
        ).all()
        tests = [
            LearnerTest(version, period, title, results, taken, entered_by)
            for version, results, taken, title, period, entered_by in rows
        ]
        texts = await self._objective_texts(db, [test.plan_version_id for test in tests])
        return LearnerResults(learner, tests, texts)

    async def _objective_texts(
        self, db: AsyncSession, plan_version_ids: list[str]
    ) -> dict[tuple[str, str], str]:
        if not plan_version_ids:
            return {}
        rows = (
            await db.execute(
                select(
                    PlanVersionObjective.plan_version_id,
                    PlanVersionObjective.lesson_objective_id,
                    PlanVersionObjective.objective_text,
                ).where(PlanVersionObjective.plan_version_id.in_(plan_version_ids))
            )
        ).all()
        return {(version, objective): text for version, objective, text in rows}

    async def _offering_of(
        self, db: AsyncSession, workspace_id: uuid.UUID
    ) -> TermClassSubject | None:
        return (
            await db.execute(
                select(TermClassSubject)
                .join(
                    TeacherWorkspace,
                    TeacherWorkspace.term_class_subject_id == TermClassSubject.id,
                )
                .where(TeacherWorkspace.id == workspace_id)
            )
        ).scalar_one_or_none()

    async def learners_with_latest_test(
        self,
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lesson_period_id: uuid.UUID | None = None,
    ) -> list[ClassLearnerRow] | None:
        """Every learner of the workspace's class, with their latest class test.

        The test is the latest for the subject, or for one lesson when `lesson_period_id` is given.
        None when the workspace does not exist, or the lesson is not one of its subject's.
        """
        offering = await self._offering_of(db, workspace_id)
        if offering is None:
            return None
        if lesson_period_id is not None and not await self._is_lesson_of(
            db, offering.id, lesson_period_id
        ):
            return None

        learners = (
            await db.execute(
                select(LearnerProfile.student_id, LearnerProfile.full_name)
                .where(LearnerProfile.class_id == offering.class_id)
                .order_by(LearnerProfile.full_name)
            )
        ).all()
        latest = await self._latest_test_per_learner(
            db, offering.id, [student_id for student_id, _ in learners], lesson_period_id
        )
        return [
            ClassLearnerRow(student_id, full_name, latest.get(student_id))
            for student_id, full_name in learners
        ]

    async def _is_lesson_of(
        self, db: AsyncSession, offering_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> bool:
        found = await db.execute(
            select(LessonPeriod.id)
            .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
            .where(
                LessonPeriod.id == lesson_period_id,
                SchemeOfWork.term_class_subject_id == offering_id,
            )
        )
        return found.scalar_one_or_none() is not None

    async def _latest_test_per_learner(
        self,
        db: AsyncSession,
        offering_id: uuid.UUID,
        student_ids: list[str],
        lesson_period_id: uuid.UUID | None,
    ) -> dict[str, LatestTest]:
        if not student_ids:
            return {}
        newest_first = func.row_number().over(
            partition_by=ExitTicketSubmission.student_id,
            order_by=ExitTicketSubmission.created_at.desc(),
        )
        in_lesson = [LessonPeriod.id == lesson_period_id] if lesson_period_id else []
        ranked = (
            select(
                ExitTicketSubmission.student_id.label("student_id"),
                ExitTicketSubmission.results.label("results"),
                ExitTicketSubmission.created_at.label("taken_at"),
                LessonPlan.title.label("lesson_title"),
                newest_first.label("rank"),
            )
            .join(PlanVersion, PlanVersion.version_id == ExitTicketSubmission.plan_version_id)
            .join(LessonPlan, LessonPlan.plan_id == PlanVersion.plan_id)
            .join(LessonPeriod, LessonPeriod.id == LessonPlan.lesson_period_id)
            .join(SchemeOfWork, SchemeOfWork.id == LessonPeriod.scheme_of_work_id)
            .where(
                SchemeOfWork.term_class_subject_id == offering_id,
                ExitTicketSubmission.student_id.in_(student_ids),
                *in_lesson,
            )
            .subquery()
        )
        rows = (
            await db.execute(
                select(
                    ranked.c.student_id,
                    ranked.c.results,
                    ranked.c.taken_at,
                    ranked.c.lesson_title,
                ).where(ranked.c.rank == 1)
            )
        ).all()
        return {
            row.student_id: LatestTest(row.lesson_title, row.results, row.taken_at) for row in rows
        }
