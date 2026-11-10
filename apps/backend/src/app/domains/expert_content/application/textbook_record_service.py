"""Owns the textbook-record read view: existence check + projection to public response.

Source textbook records are stored with multiple content fields (``content_text``,
``prompt_text``/``answer_text`` for exercises, ``retrieval_text`` as fallback) and
a structured ``heading_path``. The public view collapses those into a single
``content`` string and a single ``heading`` trail — that projection is a domain
decision (it encodes how a clickable lesson-plan reference reads to a learner),
not a transport detail, so it lives in the application layer.
"""

from __future__ import annotations

from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.expert_content.api.schemas import TextbookRecordResponse
from app.domains.expert_content.application.errors import ExpertContentApplicationError
from app.domains.expert_content.infrastructure.repository import TextbookRecordRepository
from app.domains.expert_content.models.textbook import TextbookRecord
from app.shared.json_types import JsonObject


def _label_or_title(item: JsonObject) -> str:
    return str(item.get("label") or item.get("title") or "").strip()


def _heading(heading_path: object) -> str | None:
    """Flatten a record's heading_path (list/dict of labels) into a readable trail."""
    if isinstance(heading_path, list):
        parts = [
            _label_or_title(cast(JsonObject, item)) if isinstance(item, dict) else str(item).strip()
            for item in heading_path
        ]
        trail = " › ".join(part for part in parts if part)
        return trail or None
    if isinstance(heading_path, dict):
        heading_obj = cast(JsonObject, heading_path)
        label = heading_obj.get("label") or heading_obj.get("title")
        return str(label).strip() if label else None
    return None


def _content(record: TextbookRecord) -> str:
    """Prefer human content; for exercises stitch the prompt + answer; else retrieval text."""
    if record.content_text and record.content_text.strip():
        return record.content_text
    parts = [record.prompt_text, record.answer_text]
    stitched = "\n\n".join(part for part in parts if part and part.strip())
    if stitched:
        return stitched
    return record.retrieval_text or ""


class TextbookRecordApplicationService:
    """Read-view service: validate the record exists, project it to the public response."""

    def __init__(self, repository: TextbookRecordRepository | None = None) -> None:
        self.repository = repository or TextbookRecordRepository()

    async def get_record_response(
        self,
        *,
        db: AsyncSession,
        record_id: str,
    ) -> TextbookRecordResponse:
        record = await self.repository.get_by_record_id(db, record_id)
        if record is None:
            raise ExpertContentApplicationError(404, "textbook_record_not_found")
        return TextbookRecordResponse(
            record_id=record.record_id,
            record_type=record.record_type,
            chapter_id=record.chapter_id,
            chapter_title=record.chapter_title,
            heading=_heading(record.heading_path),
            content=_content(record),
            source_html_path=record.source_html_path,
            source_anchor_id=record.source_anchor_id,
        )
