from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domains.school.models.core import AcademicYear, Term
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.models import LessonPeriod, SchemeOfWork


@dataclass(frozen=True)
class TermDates:
    starts_on: date
    ends_on: date


class TeachingSequenceRepository:
    async def term_dates(
        self, db: AsyncSession, term_name: str, year_name: str
    ) -> TermDates | None:
        """The named term's dates in the named academic year; None when unset."""
        row = (
            await db.execute(
                select(Term.start_date, Term.end_date)
                .join(AcademicYear, AcademicYear.id == Term.academic_year_id)
                .where(Term.name == term_name, AcademicYear.name == year_name)
            )
        ).first()
        return None if row is None else TermDates(row.start_date, row.end_date)

    async def get_term_class_subject(
        self,
        db: AsyncSession,
        term_class_subject_id: uuid.UUID,
    ) -> TermClassSubject | None:
        stmt = (
            select(TermClassSubject)
            .where(TermClassSubject.id == term_class_subject_id)
            .options(
                joinedload(TermClassSubject.weeks)
                .joinedload(SchemeOfWork.lesson_periods)
                .joinedload(LessonPeriod.subtopic)
            )
        )
        result = await db.execute(stmt)
        return result.scalars().unique().first()

    async def get_latest_term_class_subject_for_course(
        self,
        db: AsyncSession,
        course_id: uuid.UUID,
        *,
        term: str | None,
    ) -> TermClassSubject | None:
        stmt = (
            select(TermClassSubject)
            .where(TermClassSubject.course_id == course_id)
            .options(
                joinedload(TermClassSubject.weeks)
                .joinedload(SchemeOfWork.lesson_periods)
                .joinedload(LessonPeriod.subtopic)
            )
            .order_by(TermClassSubject.created_at.desc())
            .limit(1)
        )
        if term:
            stmt = stmt.where(TermClassSubject.term == term)
        result = await db.execute(stmt)
        return result.scalars().unique().first()

    async def get_scheme_of_work_week(
        self,
        db: AsyncSession,
        week_id: uuid.UUID,
    ) -> SchemeOfWork | None:
        result = await db.execute(
            select(SchemeOfWork)
            .where(SchemeOfWork.id == week_id)
            .options(joinedload(SchemeOfWork.lesson_periods))
        )
        return result.scalars().unique().first()

    async def update_scheme_of_work_week(
        self,
        db: AsyncSession,
        week: SchemeOfWork,
    ) -> SchemeOfWork:
        db.add(week)
        await db.commit()
        await db.refresh(week)
        return week

    async def get_lesson_period(
        self,
        db: AsyncSession,
        lesson_period_id: uuid.UUID,
    ) -> LessonPeriod | None:
        result = await db.execute(select(LessonPeriod).where(LessonPeriod.id == lesson_period_id))
        return result.scalars().first()

    async def create_lesson_period(
        self,
        db: AsyncSession,
        lesson_period: LessonPeriod,
    ) -> LessonPeriod:
        db.add(lesson_period)
        await db.commit()
        await db.refresh(lesson_period)
        return lesson_period

    async def update_lesson_period(
        self,
        db: AsyncSession,
        lesson_period: LessonPeriod,
    ) -> LessonPeriod:
        db.add(lesson_period)
        await db.commit()
        await db.refresh(lesson_period)
        return lesson_period

    async def delete_lesson_period(
        self,
        db: AsyncSession,
        lesson_period: LessonPeriod,
    ) -> None:
        await db.delete(lesson_period)
        await db.commit()
