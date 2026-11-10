"""Expert-content textbook persistence models."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.db.enums import status_enum
from app.db.mixins import TimestampMixin
from app.domains.expert_content.domain.types import (
    TextbookRecordLinkStatus,
    TextbookSeedRunStatus,
)
from app.shared.time import utc_now


class TextbookPacket(TimestampMixin, Base):
    __tablename__ = "textbook_packets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    packet_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    source_response_path: Mapped[str] = mapped_column(Text)
    source_packet_manifest: Mapped[str | None] = mapped_column(Text, nullable=True)
    record_count: Mapped[int] = mapped_column(Integer)


class TextbookRecord(TimestampMixin, Base):
    __tablename__ = "textbook_records"
    __table_args__ = (
        # link_status is now enforced by the ``textbook_record_link_status`` PG
        # enum on the column itself — no CHECK needed.
        CheckConstraint(
            "visibility_default IS NULL OR visibility_default IN ('visible', 'hidden', 'none')",
            name="ck_textbook_records_visibility_default",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    packet_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("textbook_packets.packet_id", ondelete="CASCADE"),
        index=True,
    )
    record_type: Mapped[str] = mapped_column(String(64), index=True)
    parent_block_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    chapter_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    chapter_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    heading_path: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    source_html_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_anchor_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_type_guess: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    retrieval_text: Mapped[str] = mapped_column(Text)
    visibility_default: Mapped[str | None] = mapped_column(String(32), nullable=True)
    asset_refs: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    llm_review_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    llm_review_notes: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    primary_subtopic_id: Mapped[str] = mapped_column(
        String(200),
        ForeignKey("curriculum_subtopics.subtopic_id", ondelete="RESTRICT"),
        index=True,
    )
    link_status: Mapped[TextbookRecordLinkStatus] = mapped_column(
        status_enum(TextbookRecordLinkStatus, name="textbook_record_link_status"),
    )
    link_notes: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)


class TextbookRecordSubtopic(Base):
    __tablename__ = "textbook_record_subtopics"
    __table_args__ = (
        UniqueConstraint(
            "record_id",
            "subtopic_id",
            name="uq_textbook_record_subtopics_record_subtopic",
        ),
        Index(
            "ix_textbook_record_subtopics_subtopic_primary",
            "subtopic_id",
            "is_primary",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("textbook_records.record_id", ondelete="CASCADE"),
        index=True,
    )
    subtopic_id: Mapped[str] = mapped_column(
        String(200),
        ForeignKey("curriculum_subtopics.subtopic_id", ondelete="RESTRICT"),
        index=True,
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class TextbookSeedRun(Base):
    __tablename__ = "textbook_seed_runs"
    # status is now enforced by the ``textbook_seed_run_status`` enum on the
    # column itself — no CHECK needed.

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seed_name: Mapped[str] = mapped_column(String(128))
    source_manifest_path: Mapped[str] = mapped_column(Text)
    source_record_count: Mapped[int] = mapped_column(Integer)
    inserted_packet_count: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    inserted_record_count: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    inserted_link_count: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    status: Mapped[TextbookSeedRunStatus] = mapped_column(
        status_enum(TextbookSeedRunStatus, name="textbook_seed_run_status"),
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
