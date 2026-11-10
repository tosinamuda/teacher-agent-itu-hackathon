"""Resolve lesson-plan reference citations to the real textbook passages.

Plan references are citation strings ending in a record id, e.g.
``"Chapter 2: Highest common factor and lowest common multiple (ch02-b029)"``.
Until 2026-06-11 the study-pack pipeline passed that STRING as the "evidence
excerpt" — so the model was told to ground claims in a chapter title. The
actual passage lives in ``textbook_records``; this resolver fetches it so
``SourceEvidenceItem.excerpt`` can carry real content.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.expert_content.models.textbook import TextbookRecord

_RECORD_ID_SUFFIX = re.compile(r"\(([\w-]+)\)\s*$")


def reference_record_id(reference: str) -> str | None:
    """The trailing ``(record-id)`` of a citation string, if present."""
    match = _RECORD_ID_SUFFIX.search(reference or "")
    return match.group(1) if match else None


class SqlAlchemyExcerpts:
    """``ExcerptsPort`` over one session; the caller owns the transaction."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def excerpts_for(self, references: Sequence[str]) -> dict[str, str]:
        return await resolve_reference_excerpts(self._db, list(references))


async def resolve_reference_excerpts(db: AsyncSession, references: list[str]) -> dict[str, str]:
    """record_id -> the record's passage text, for every resolvable reference.

    ``prompt_text`` is the LM-ready rendering of a record; falls back to
    ``content_text`` / ``retrieval_text``. References whose id has no record
    simply don't appear in the map (callers keep the citation string).
    """
    record_ids = {
        record_id for record_id in (reference_record_id(ref) for ref in references) if record_id
    }
    if not record_ids:
        return {}
    rows = (
        await db.execute(select(TextbookRecord).where(TextbookRecord.record_id.in_(record_ids)))
    ).scalars()
    excerpts: dict[str, str] = {}
    for record in rows:
        text = (record.prompt_text or record.content_text or record.retrieval_text or "").strip()
        if text:
            excerpts[record.record_id] = text
    return excerpts
