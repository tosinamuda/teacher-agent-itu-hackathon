from __future__ import annotations

from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.curriculum.models.curriculum import (
    ClassSession,
    CurriculumSubtopic,
    CurriculumTopic,
)


class CurriculumRepository:
    async def list_topics(
        self,
        db: AsyncSession,
        *,
        subject: str | None,
        track: str | None,
        grade: str | None,
        term: str | None,
        week: int | None,
        limit: int,
    ) -> list[CurriculumTopic]:
        stmt = select(CurriculumTopic)
        if subject:
            stmt = stmt.filter(CurriculumTopic.subject == subject)
        if track:
            stmt = stmt.filter(CurriculumTopic.track == track)
        if grade:
            stmt = stmt.filter(CurriculumTopic.grade == grade)
        if term:
            stmt = stmt.filter(CurriculumTopic.term == term)
        if week:
            stmt = stmt.filter(CurriculumTopic.week == week)
        stmt = stmt.order_by(CurriculumTopic.week.asc()).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def list_sessions(
        self,
        db: AsyncSession,
        *,
        subject: str | None,
        track: str | None,
        grade: str | None,
        term: str | None,
        week: int | None,
        limit: int,
    ) -> list[tuple[ClassSession, CurriculumSubtopic]]:
        stmt = select(ClassSession, CurriculumSubtopic).join(
            CurriculumSubtopic, ClassSession.subtopic_id == CurriculumSubtopic.subtopic_id
        )
        if subject:
            stmt = stmt.filter(ClassSession.subject == subject)
        if track:
            stmt = stmt.filter(ClassSession.track == track)
        if grade:
            stmt = stmt.filter(ClassSession.grade == grade)
        if term:
            stmt = stmt.filter(ClassSession.term == term)
        if week:
            stmt = stmt.filter(ClassSession.week == week)
        stmt = stmt.order_by(ClassSession.week.asc(), ClassSession.day_index.asc()).limit(limit)
        result = await db.execute(stmt)
        return cast(list[tuple[ClassSession, CurriculumSubtopic]], list(result.all()))
