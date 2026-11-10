"""Bound read adapter for textbook excerpts used by audit construction."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.expert_content.models.textbook import TextbookRecord


class SqlAlchemyTextbookExcerptReader:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def excerpt_for_record(self, *, record_id: str) -> str | None:
        result = await self._session.execute(
            select(TextbookRecord).where(TextbookRecord.record_id == record_id)
        )
        record = result.scalars().first()
        if record is None:
            return None
        if record.content_text and record.content_text.strip():
            return record.content_text
        stitched = "\n\n".join(
            part for part in (record.prompt_text, record.answer_text) if part and part.strip()
        )
        return stitched or (record.retrieval_text or None)
