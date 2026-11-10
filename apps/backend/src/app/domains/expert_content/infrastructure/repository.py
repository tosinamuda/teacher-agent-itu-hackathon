"""Persistence access for expert-content textbook records."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.expert_content.models.textbook import TextbookRecord


class TextbookRecordRepository:
    """Fetches textbook records by their public identifiers."""

    async def get_by_record_id(
        self,
        db: AsyncSession,
        record_id: str,
    ) -> TextbookRecord | None:
        result = await db.execute(
            select(TextbookRecord).where(TextbookRecord.record_id == record_id)
        )
        return result.scalar_one_or_none()
