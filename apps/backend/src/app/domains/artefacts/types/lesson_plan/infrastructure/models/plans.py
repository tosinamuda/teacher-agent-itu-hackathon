"""Lesson plan models."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.db.enums import status_enum
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.shared.time import utc_now


class LessonPlan(Base):
    __tablename__ = "lesson_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    lesson_period_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_periods.id", name="fk_lesson_plans_lesson_period_id"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(256))
    subject: Mapped[str] = mapped_column(String(128), index=True)
    track: Mapped[str] = mapped_column(String(64), index=True)
    grade: Mapped[str] = mapped_column(String(32), index=True)
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
    )


class PlanVersion(Base):
    __tablename__ = "plan_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    plan_id: Mapped[str] = mapped_column(String(64), ForeignKey("lesson_plans.plan_id"), index=True)
    source_type: Mapped[str] = mapped_column(String(32))
    parent_version_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    session_plan: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    run_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[PlanVersionStatus] = mapped_column(
        status_enum(PlanVersionStatus, name="plan_version_status"),
        default=PlanVersionStatus.DRAFT,
        server_default=text("'draft'"),
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # Set when the teacher discards a draft (rejected) or takes an approval back (withdrawn):
    # when, who, and the reason they gave.
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closed_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    closed_reason: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Set when the teacher releases the exit assessment to students. NULL until
    # then — students cannot fetch or submit an unreleased assessment.
    assessment_released_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    assessment_released_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # Set when the study this version was taught in has concluded. From then on the lesson's
    # record — this version, its content and the class's answers — is read-only.
    concluded_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
    )


class PlanVersionObjective(Base):
    """A single ``lesson_objective`` row derived from a plan_version's session_plan JSON.

    P5.6 promotes the per-plan-version ``lesson_plan_objectives`` array out of
    ``plan_versions.session_plan`` into a real table so ``exit_ticket_items
    .lesson_objective_id`` can be FK-enforced (composite FK on
    ``(plan_version_id, lesson_objective_id)``). The JSON stays as the LLM's
    natural output shape; this table is **derived** — kept in sync on every
    ``persist_plan_version`` / ``persist_revised_plan_version`` write.

    Future P5.6 Phase 2 will promote ``CurriculumSubtopic.performance_objectives``
    to its own table and FK ``curriculum_objective_id`` here to it.
    """

    __tablename__ = "plan_version_objectives"
    __table_args__ = (
        UniqueConstraint(
            "plan_version_id",
            "lesson_objective_id",
            name="uq_plan_version_objectives_pv_lop",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            "plan_versions.version_id",
            name="fk_plan_version_objectives_plan_version_id",
        ),
        index=True,
    )
    lesson_objective_id: Mapped[str] = mapped_column(String(64), index=True)
    objective_text: Mapped[str] = mapped_column(Text)
    objective_order: Mapped[int] = mapped_column(Integer)
    kc_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    kc_focus: Mapped[str | None] = mapped_column(Text, nullable=True)
    curriculum_objective_id: Mapped[str | None] = mapped_column(
        String(200),
        ForeignKey(
            "curriculum_performance_objectives.curriculum_objective_id",
            name="fk_plan_version_objectives_curriculum_objective_id",
        ),
        nullable=True,
        index=True,
    )
    curriculum_objective_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        server_default=text("now()"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        server_default=text("now()"),
    )
