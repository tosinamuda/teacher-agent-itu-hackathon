"""AO-level textbook linkage persistence models.

Stores the manual atomic-objective -> textbook-record linkage (roles, step
blueprints, reused assessments) so the lesson-plan pipeline can ground on
expert-validated links instead of BM25 retrieval.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
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
    AoTextbookLinkageSeedRunStatus,
    AoTextbookLinkageStatus,
)
from app.shared.time import utc_now


class AoTextbookLinkage(TimestampMixin, Base):
    __tablename__ = "ao_textbook_linkages"
    __table_args__ = (
        # status is now enforced by the ``ao_textbook_linkage_status`` enum.
        UniqueConstraint("subtopic_id", name="uq_ao_textbook_linkages_subtopic_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subtopic_id: Mapped[str] = mapped_column(
        String(200),
        ForeignKey("curriculum_subtopics.subtopic_id", ondelete="RESTRICT"),
    )
    subtopic_title: Mapped[str] = mapped_column(Text)
    status: Mapped[AoTextbookLinkageStatus] = mapped_column(
        status_enum(AoTextbookLinkageStatus, name="ao_textbook_linkage_status"),
    )
    status_reasons: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    review_categories: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    shared_foundation_record_ids: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    source_set: Mapped[str] = mapped_column(String(64))


class AoTextbookObjectiveLink(Base):
    __tablename__ = "ao_textbook_objective_links"
    __table_args__ = (
        UniqueConstraint(
            "subtopic_id",
            "ao_id",
            name="uq_ao_textbook_objective_links_subtopic_ao",
        ),
        Index("ix_ao_textbook_objective_links_subtopic_id", "subtopic_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subtopic_id: Mapped[str] = mapped_column(
        String(200),
        ForeignKey("ao_textbook_linkages.subtopic_id", ondelete="CASCADE"),
    )
    ao_id: Mapped[str] = mapped_column(String(200))
    ao_order: Mapped[int] = mapped_column(Integer)
    curriculum_objective_id: Mapped[str] = mapped_column(String(200))
    curriculum_objective_text: Mapped[str] = mapped_column(Text)
    objective_text: Mapped[str] = mapped_column(Text)
    bloom_verb: Mapped[str] = mapped_column(String(64))
    bloom_level: Mapped[str] = mapped_column(String(32))
    evidence_classification: Mapped[str | None] = mapped_column(String(32), nullable=True)
    step_blueprint: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    practice_record_ids: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    assessment: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class AoTextbookRecordLink(Base):
    __tablename__ = "ao_textbook_record_links"
    __table_args__ = (
        CheckConstraint(
            "role IN ('foundation', 'instruction', 'worked_example', 'exercise')",
            name="ck_ao_textbook_record_links_role",
        ),
        CheckConstraint(
            "method IN ('rule_type', 'rule_heading', 'judgment')",
            name="ck_ao_textbook_record_links_method",
        ),
        UniqueConstraint(
            "subtopic_id",
            "ao_id",
            "record_id",
            name="uq_ao_textbook_record_links_subtopic_ao_record",
        ),
        ForeignKeyConstraint(
            ["subtopic_id", "ao_id"],
            [
                "ao_textbook_objective_links.subtopic_id",
                "ao_textbook_objective_links.ao_id",
            ],
            ondelete="CASCADE",
        ),
        Index("ix_ao_textbook_record_links_subtopic_ao", "subtopic_id", "ao_id"),
        Index("ix_ao_textbook_record_links_record_id", "record_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subtopic_id: Mapped[str] = mapped_column(String(200))
    ao_id: Mapped[str] = mapped_column(String(200))
    record_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("textbook_records.record_id", ondelete="RESTRICT"),
    )
    role: Mapped[str] = mapped_column(String(32))
    method: Mapped[str] = mapped_column(String(32))
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    link_order: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class AoTextbookLinkageSeedRun(Base):
    __tablename__ = "ao_textbook_linkage_seed_runs"
    # status is now enforced by the ``ao_textbook_linkage_seed_run_status`` enum.

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seed_name: Mapped[str] = mapped_column(String(128))
    source_dir: Mapped[str] = mapped_column(Text)
    source_row_count: Mapped[int] = mapped_column(Integer)
    inserted_linkage_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )
    inserted_objective_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )
    inserted_record_link_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )
    skipped_row_count: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    status: Mapped[AoTextbookLinkageSeedRunStatus] = mapped_column(
        status_enum(AoTextbookLinkageSeedRunStatus, name="ao_textbook_linkage_seed_run_status"),
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
