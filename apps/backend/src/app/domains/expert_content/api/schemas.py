"""HTTP contract shapes for the expert-content API."""

from __future__ import annotations

from pydantic import BaseModel


class TextbookRecordResponse(BaseModel):
    """A single source textbook chunk, for the "click a reference to read it" view."""

    record_id: str
    record_type: str
    chapter_id: str | None = None
    chapter_title: str | None = None
    heading: str | None = None
    content: str
    source_html_path: str | None = None
    source_anchor_id: str | None = None
