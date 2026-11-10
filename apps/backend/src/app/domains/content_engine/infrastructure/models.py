"""Drafts of content being written part by part, whatever its type."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID


class ContentDraftRecord(Base):
    """One draft: what it is made from, its units, and the checked part of each unit so far."""

    __tablename__ = "content_drafts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    draft_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    type: Mapped[str] = mapped_column(String(64))
    kind: Mapped[str] = mapped_column(String(64))
    spec_revision: Mapped[int] = mapped_column(Integer)
    #: What it is made from: a plan version, or else a lesson period.
    plan_version_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    #: A document the draft is written from, such as a teacher's own plan.
    source: Mapped[str] = mapped_column(Text, default="")
    unit: Mapped[str] = mapped_column(String(32))
    #: The units in order: ``[{"unit_id", "label", "unit"}]``.
    units: Mapped[list] = mapped_column(JSON)
    #: The checked part of each filled unit, by unit ID.
    parts: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(16))
    #: The content it revises, or what it was saved as once submitted.
    saved_as: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_by: Mapped[str] = mapped_column(String(128))
    #: The teacher whose work it is.
    author: Mapped[str | None] = mapped_column(String(64), nullable=True)
    student_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
    )
