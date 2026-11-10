from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.domain.term_weeks import current_week_number, week_starts_on
from app.domains.teaching.infrastructure.sequence_repository import (
    TeachingSequenceRepository,
    TermDates,
)
from app.domains.teaching.models import LessonPeriod, SchemeOfWork
from app.domains.teaching.schemas import (
    LessonPeriodCreateRequest,
    LessonPeriodResponse,
    LessonPeriodUpdateRequest,
    SchemeOfWorkResponse,
    SchemeOfWorkUpdateRequest,
    TermClassSubjectResponse,
)


@dataclass(frozen=True)
class TeachingSequenceApplicationError(Exception):
    status_code: int
    detail: str


def _lesson_period_response(lesson_period: LessonPeriod) -> LessonPeriodResponse:
    return LessonPeriodResponse(
        id=lesson_period.id,
        scheme_of_work_id=lesson_period.scheme_of_work_id,
        period_number=lesson_period.period_number,
        title=lesson_period.title,
        subtopic_id=lesson_period.subtopic_id,
        subtopic_title=lesson_period.subtopic.title if lesson_period.subtopic else None,
    )


def _scheme_of_work_response(
    week: SchemeOfWork, term: TermDates | None = None
) -> SchemeOfWorkResponse:
    return SchemeOfWorkResponse(
        id=week.id,
        starts_on=week_starts_on(term.starts_on, week.week_number) if term else None,
        term_class_subject_id=week.term_class_subject_id,
        week_number=week.week_number,
        title=week.title,
        objectives=week.objectives,
        lesson_periods=[_lesson_period_response(lp) for lp in week.lesson_periods],
    )


def _term_class_subject_response(
    tcs: TermClassSubject, term: TermDates | None, today: date
) -> TermClassSubjectResponse:
    return TermClassSubjectResponse(
        id=tcs.id,
        course_id=tcs.course_id,
        term=tcs.term,
        year=tcs.year,
        created_at=tcs.created_at,
        weeks=[_scheme_of_work_response(week, term) for week in tcs.weeks],
        current_week_number=(
            current_week_number(term.starts_on, term.ends_on, today) if term else None
        ),
    )


class TeachingSequenceApplicationService:
    def __init__(self, repository: TeachingSequenceRepository | None = None) -> None:
        self.repository = repository or TeachingSequenceRepository()

    async def get_term_class_subject_by_id(
        self,
        *,
        db: AsyncSession,
        term_class_subject_id: uuid.UUID,
    ) -> TermClassSubjectResponse:
        term_class_subject = await self.repository.get_term_class_subject(db, term_class_subject_id)
        if term_class_subject is None:
            raise TeachingSequenceApplicationError(404, "term_class_subject_not_found")
        dates = await self.repository.term_dates(
            db, term_class_subject.term, term_class_subject.year
        )
        return _term_class_subject_response(term_class_subject, dates, date.today())

    async def get_term_class_subject_for_course(
        self,
        *,
        db: AsyncSession,
        course_id: uuid.UUID,
        term: str | None,
    ) -> TermClassSubjectResponse:
        term_class_subject = await self.repository.get_latest_term_class_subject_for_course(
            db,
            course_id,
            term=term,
        )
        if term_class_subject is None:
            raise TeachingSequenceApplicationError(404, "term_class_subject_not_found")
        dates = await self.repository.term_dates(
            db, term_class_subject.term, term_class_subject.year
        )
        return _term_class_subject_response(term_class_subject, dates, date.today())

    async def get_scheme_of_work_week(
        self,
        *,
        db: AsyncSession,
        week_id: uuid.UUID,
    ) -> SchemeOfWorkResponse:
        week = await self.repository.get_scheme_of_work_week(db, week_id)
        if week is None:
            raise TeachingSequenceApplicationError(404, "week_not_found")
        return _scheme_of_work_response(week)

    async def update_scheme_of_work_week(
        self,
        *,
        db: AsyncSession,
        week_id: uuid.UUID,
        payload: SchemeOfWorkUpdateRequest,
    ) -> SchemeOfWorkResponse:
        week = await self.repository.get_scheme_of_work_week(db, week_id)
        if week is None:
            raise TeachingSequenceApplicationError(404, "week_not_found")

        if payload.title is not None:
            week.title = payload.title
        if payload.objectives is not None:
            week.objectives = payload.objectives
        return _scheme_of_work_response(await self.repository.update_scheme_of_work_week(db, week))

    async def create_lesson_period(
        self,
        *,
        db: AsyncSession,
        week_id: uuid.UUID,
        payload: LessonPeriodCreateRequest,
    ) -> LessonPeriodResponse:
        week = await self.repository.get_scheme_of_work_week(db, week_id)
        if week is None:
            raise TeachingSequenceApplicationError(404, "week_not_found")

        lesson_period = LessonPeriod(
            scheme_of_work_id=week.id,
            period_number=payload.period_number,
            subtopic_id=payload.subtopic_id,
        )
        return _lesson_period_response(
            await self.repository.create_lesson_period(db, lesson_period)
        )

    async def update_lesson_period(
        self,
        *,
        db: AsyncSession,
        lesson_period_id: uuid.UUID,
        payload: LessonPeriodUpdateRequest,
    ) -> LessonPeriodResponse:
        lesson_period = await self.repository.get_lesson_period(db, lesson_period_id)
        if lesson_period is None:
            raise TeachingSequenceApplicationError(404, "lesson_period_not_found")

        if payload.subtopic_id is not None:
            lesson_period.subtopic_id = payload.subtopic_id
        if payload.period_number is not None:
            lesson_period.period_number = payload.period_number
        return _lesson_period_response(
            await self.repository.update_lesson_period(db, lesson_period)
        )

    async def delete_lesson_period(
        self,
        *,
        db: AsyncSession,
        lesson_period_id: uuid.UUID,
    ) -> None:
        lesson_period = await self.repository.get_lesson_period(db, lesson_period_id)
        if lesson_period is None:
            raise TeachingSequenceApplicationError(404, "lesson_period_not_found")
        await self.repository.delete_lesson_period(db, lesson_period)
