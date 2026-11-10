from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.curriculum.infrastructure.repository import CurriculumRepository
from app.domains.curriculum.models.curriculum import (
    ClassSession,
    CurriculumSubtopic,
    CurriculumTopic,
)


class CurriculumApplicationService:
    def __init__(
        self,
        repository: CurriculumRepository | None = None,
    ) -> None:
        self.repository = repository or CurriculumRepository()

    async def list_topics(
        self,
        *,
        db: AsyncSession,
        subject: str | None,
        track: str | None,
        grade: str | None,
        term: str | None,
        week: int | None,
        limit: int,
    ) -> list[CurriculumTopic]:
        return await self.repository.list_topics(
            db,
            subject=subject,
            track=track,
            grade=grade,
            term=term,
            week=week,
            limit=limit,
        )

    async def list_sessions(
        self,
        *,
        db: AsyncSession,
        subject: str | None,
        track: str | None,
        grade: str | None,
        term: str | None,
        week: int | None,
        limit: int,
    ) -> list[tuple[ClassSession, CurriculumSubtopic]]:
        return await self.repository.list_sessions(
            db,
            subject=subject,
            track=track,
            grade=grade,
            term=term,
            week=week,
            limit=limit,
        )
