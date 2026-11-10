from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.db.enums import status_enum
from app.domains.evaluation.domain.types import AuditItemStatus
from app.shared.experiment_enums import PacketStatus
from app.shared.time import utc_now


class EvaluationRater(Base):
    __tablename__ = "evaluation_raters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rater_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    # Login link: a human rater binds 1:1 to a ``User`` row with role='rater'.
    # Synthetic judges leave this NULL — they have no human identity.
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=True,
        index=True,
    )
    #: ``app`` for a rater the app can assign; ``study_record`` for a rater of an imported
    #: study, who rated on its documents and is never assigned in the app.
    origin: Mapped[str] = mapped_column(String(16), default="app", server_default=text("'app'"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class EvaluationRating(Base):
    __tablename__ = "evaluation_ratings"
    __table_args__ = (
        UniqueConstraint(
            "evaluation_packet_db_id",
            "rater_db_id",
            name="uq_evaluation_ratings_packet_rater",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    evaluation_packet_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_packets.id"),
        index=True,
    )
    rater_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_raters.id"),
        index=True,
    )
    hypothesis: Mapped[str] = mapped_column(String(8), index=True)
    overall_score: Mapped[float] = mapped_column(Float)
    rubric_scores: Mapped[dict] = mapped_column(JSON)
    section_scores: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    diagnostic_scores: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    archived_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class EvaluationAuditItem(Base):
    """One source-grounding audit item: a generated excerpt paired with the cited.

    textbook source snippet + lesson objective, for C2-C4 conditions only. Audit
    raters check whether the source actually supports the generated content.
    """

    __tablename__ = "evaluation_audit_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_item_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    execution_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiment_executions.id"),
        index=True,
    )
    condition_run_id: Mapped[str] = mapped_column(String(64), index=True)
    condition_code: Mapped[str] = mapped_column(String(8), index=True)
    lesson_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    lesson_objective_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    objective_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_excerpt: Mapped[str] = mapped_column(Text)
    source_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_record_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    # When the cited source is a textbook figure (a VisualBlock in the pack
    # manifest), carry the figure's url + caption so the audit pack can render
    # the figure beside the source snippet — raters cannot judge whether the
    # cited figure supports the generated content if they can only read its
    # caption. NULL for text-only sources; the renderer falls back to the
    # snippet-only layout in that case.
    figure_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    figure_caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    scope_boundary: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[AuditItemStatus] = mapped_column(
        status_enum(AuditItemStatus, name="audit_item_status"),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class EvaluationAuditRating(Base):
    """One audit rater's 0/1/2 scores for a source-grounding audit item."""

    __tablename__ = "evaluation_audit_ratings"
    __table_args__ = (
        UniqueConstraint(
            "audit_item_db_id",
            "rater_db_id",
            name="uq_evaluation_audit_ratings_item_rater",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    audit_item_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_audit_items.id"),
        index=True,
    )
    rater_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluation_raters.id"),
        index=True,
    )
    source_relevance: Mapped[int] = mapped_column(SmallInteger)
    support_sufficiency: Mapped[int] = mapped_column(SmallInteger)
    faithfulness: Mapped[int] = mapped_column(SmallInteger)
    scope_correctness: Mapped[int] = mapped_column(SmallInteger)
    source_grounding_score: Mapped[float] = mapped_column(Float)
    notes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class EvaluationPacket(Base):
    """A blinded unit of evaluation work: one packet a rater scores.

    Produced by the experiments pipeline (it carries an FK to the experiment
    execution that generated it) but owned by the evaluation domain, since a
    packet only exists to be rated. The ``experiment_executions`` FK is a
    string reference across the domain boundary — no Python import of the
    experiments models is needed to declare it.
    """

    __tablename__ = "evaluation_packets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_packet_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    execution_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiment_executions.id"),
        index=True,
    )
    packet_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    hypothesis: Mapped[str] = mapped_column(String(8), index=True)
    status: Mapped[PacketStatus] = mapped_column(
        status_enum(PacketStatus, name="packet_status"),
        index=True,
    )
    primary_condition_run_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            "experiment_condition_runs.experiment_condition_run_id",
            name="fk_evaluation_packets_primary_condition_run_id",
        ),
        index=True,
    )
    experiment_focal_case_id: Mapped[str | None] = mapped_column(
        String(64),
        index=True,
        nullable=True,
    )
    export_refs: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    condition_run_ids: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class RaterAssignment(Base):
    """Binds a rater to a unit of work in an experiment (Phase H).

    One row = "this rater rates this scope". ``hypothesis`` + ``scope_id`` say
    what's being rated:

    - ``H1`` → scope_id is a ``lesson_period_id`` (UUID string). The rater
      rates all C0–C3 packets for that lesson.
    - ``H2`` → scope_id is an ``experiment_focal_case_id`` (public id). The
      rater rates both P0 and P1 for that focal learner.
    - ``audit`` → scope_id is an ``audit_item_id`` (public id). Two
      non-adjudicator rows per audit item; ``is_adjudicator=True`` marks the
      tiebreaker added when scores diverge.

    Distribution caps (max 3 per lesson for H1, max 3 per focal case for H2,
    max 2 non-adjudicators per audit item) are enforced by
    Assignment commands — this table only carries the FK + uniqueness.
    """

    __tablename__ = "rater_assignments"
    __table_args__ = (
        UniqueConstraint(
            "experiment_db_id",
            "rater_db_id",
            "hypothesis",
            "scope_id",
            name="uq_rater_assignments_unique",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    assignment_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    experiment_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("experiments.id"), index=True
    )
    rater_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evaluation_raters.id"), index=True
    )
    hypothesis: Mapped[str] = mapped_column(String(16), index=True)
    scope_id: Mapped[str] = mapped_column(String(64), index=True)
    is_adjudicator: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    assigned_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
