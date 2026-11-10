from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.db.enums import status_enum
from app.domains.artefacts.core.domain.types import ArtefactPlanStatus, ArtefactReviewStatus

ARTEFACT_TYPE_DB_COLUMN_NAME = "artefact_kind"


class ArtefactPlan(Base):
    __tablename__ = "artefact_plans"
    __table_args__ = (
        # Hot read path: ArtefactRepository.get_latest_plan filters by
        # (artefact_type, scope, plan_version_id) and ORDER BY created_at DESC.
        # DB column is artefact_kind (Python attribute is artefact_type).
        # See migration 20260607_index_audit_round1_fk_and_composites.
        Index(
            "ix_artefact_plans_kind_scope_plan_version_created_at",
            "artefact_kind",
            "scope",
            "plan_version_id",
            text("created_at DESC"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artefact_plan_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    artefact_type: Mapped[str] = mapped_column(
        ARTEFACT_TYPE_DB_COLUMN_NAME,
        String(64),
        index=True,
    )
    scope: Mapped[str] = mapped_column(String(32), index=True)
    plan_version_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("plan_versions.version_id"), index=True
    )
    student_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id", name="fk_artefact_plans_student_id"),
        index=True,
        nullable=True,
    )
    parent_artefact_plan_id: Mapped[str | None] = mapped_column(
        String(64), index=True, nullable=True
    )
    experiment_condition_run_id: Mapped[str | None] = mapped_column(
        String(64),
        index=True,
        nullable=True,
    )
    payload: Mapped[dict] = mapped_column(JSON)
    learner_state_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[ArtefactPlanStatus] = mapped_column(
        status_enum(ArtefactPlanStatus, name="artefact_plan_status"),
        default=ArtefactPlanStatus.DRAFT,
        server_default=text("'draft'"),
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class Artefact(Base):
    __tablename__ = "artefacts"
    __table_args__ = (
        # Hot read path: list_pending_learner_artefacts. Filters by
        # (artefact_kind, scope, plan_version_id) and ORDER BY created_at DESC.
        # DB column is artefact_kind (Python attribute is artefact_type). See
        # migration 20260607_index_audit_round1_fk_and_composites.
        Index(
            "ix_artefacts_kind_scope_plan_version_created_at",
            "artefact_kind",
            "scope",
            "plan_version_id",
            text("created_at DESC"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artefact_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    artefact_type: Mapped[str] = mapped_column(
        ARTEFACT_TYPE_DB_COLUMN_NAME,
        String(64),
        index=True,
    )
    scope: Mapped[str] = mapped_column(String(32), index=True)
    source_artefact_plan_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    parent_artefact_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    experiment_condition_run_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey(
            "experiment_condition_runs.experiment_condition_run_id",
            name="fk_artefacts_experiment_condition_run_id",
        ),
        index=True,
        nullable=True,
    )
    # The run that produced this artefact (the single run<->artefact link).
    # Purpose: teach SQLAlchemy's unit of work the insert dependency so the run
    # row is inserted before this artefact's FK references it — no manual flush
    # needed. The target class is referenced by name (resolved via the mapper
    # registry) so this module takes no hard import on the experiments domain.
    # `lazy="raise"` makes it write-/ordering-only: any accidental lazy load
    # (e.g. across a closed async session) errors loudly instead of N+1-ing.
    condition_run = relationship(
        "ExperimentConditionRun",
        primaryjoin=(
            "Artefact.experiment_condition_run_id "
            "== ExperimentConditionRun.experiment_condition_run_id"
        ),
        foreign_keys="Artefact.experiment_condition_run_id",
        lazy="raise",
    )
    plan_version_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("plan_versions.version_id"), index=True
    )
    student_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id", name="fk_artefacts_student_id"),
        index=True,
        nullable=True,
    )
    manifest: Mapped[dict] = mapped_column(JSON)
    artefact_refs: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Optimistic-concurrency token for the teacher review gate. Bumped on every
    # content/status mutation (an in-place revise, and each approve), so an approve
    # that carries the version the teacher reviewed can be rejected (409) if the
    # row changed underneath them — the lock prevents a torn write, this prevents a
    # blind approve of a manifest the teacher never saw / a silently-undone approval.
    version: Mapped[int] = mapped_column(
        Integer, default=1, server_default=text("1"), nullable=False
    )
    # Teacher approval gate for auto-generated learner packs: a per-student pack is
    # "pending" until a teacher approves it, and only approved packs are shown to
    # the student. Defaults to "approved" so existing/non-student artefacts stay
    # visible.
    review_status: Mapped[ArtefactReviewStatus] = mapped_column(
        status_enum(ArtefactReviewStatus, name="artefact_review_status"),
        default=ArtefactReviewStatus.APPROVED,
        server_default=text("'approved'"),
        index=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    #: Why the teacher rejected a pending version or withdrew an approved one.
    review_reason: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class ContentSpecificationRecord(Base):
    """One revision of one kind's specification. Revisions are added, never edited."""

    __tablename__ = "content_specifications"
    __table_args__ = (
        UniqueConstraint("kind", "revision", name="uq_content_specifications_kind_revision"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kind: Mapped[str] = mapped_column(String(64), index=True)
    revision: Mapped[int] = mapped_column(Integer)
    material: Mapped[str] = mapped_column(Text)
    audience: Mapped[str] = mapped_column(Text)
    levels: Mapped[list] = mapped_column(JSON)
    structure: Mapped[list] = mapped_column(JSON)
    requirements: Mapped[list] = mapped_column(JSON)
    adaptable: Mapped[list] = mapped_column(JSON)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    parts: Mapped[list | None] = mapped_column(JSON, nullable=True)
    lesson_parts: Mapped[list | None] = mapped_column(JSON, nullable=True)
    skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    mcp: Mapped[list | None] = mapped_column(JSON, nullable=True)
    #: The plugin whose generator this spec belongs to. NULL for the type's own specs, which
    #: are the only ones a kind's "current" revision is taken from.
    generator: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )


class ContentApproval(Base):
    """One teacher approval of one version of a content item. Approvals are added, never edited."""

    __tablename__ = "content_approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    approval_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    artefact_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("artefacts.artefact_id", name="fk_content_approvals_artefact_id"),
        index=True,
    )
    #: The version the teacher saw and approved.
    approved_version: Mapped[int] = mapped_column(Integer)
    approved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), server_default=text("now()")
    )
