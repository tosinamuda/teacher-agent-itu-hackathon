"""Teaching-sequence models for schemes, periods, and delivery."""

from __future__ import annotations

import uuid
from datetime import date as calendar_date
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.db.enums import status_enum
from app.domains.teaching.domain.types import LessonDeliveryStatus
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.curriculum.models.curriculum import CurriculumSubtopic
    from app.domains.school.models.subject_offerings import TermClassSubject


class SchemeOfWork(Base):
    """A week's entry in the teaching sequence."""

    __tablename__ = "scheme_of_work"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term_class_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("term_class_subjects.id"),
        index=True,
    )
    week_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255))
    objectives: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    term_class_subject: Mapped[TermClassSubject] = relationship(
        "TermClassSubject",
        back_populates="weeks",
    )
    lesson_periods: Mapped[list[LessonPeriod]] = relationship(
        "LessonPeriod",
        back_populates="scheme_of_work",
        order_by="LessonPeriod.period_number",
    )


class LessonPeriod(Base):
    """One lesson period slot within a scheme-of-work week."""

    __tablename__ = "lesson_periods"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_of_work_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheme_of_work.id"),
        index=True,
    )
    period_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subtopic_id: Mapped[str | None] = mapped_column(
        String(200),
        ForeignKey("curriculum_subtopics.subtopic_id"),
        nullable=True,
    )

    scheme_of_work: Mapped[SchemeOfWork] = relationship(
        "SchemeOfWork",
        back_populates="lesson_periods",
    )
    subtopic: Mapped[CurriculumSubtopic | None] = relationship(
        "CurriculumSubtopic",
        lazy="joined",
    )


class LessonDelivery(Base):
    """Recorded lesson delivery for a lesson period.

    P5.2 Phase 4 / audit §2.4: the table previously carried duplicate columns
    from an incomplete rename — ``workspace_id`` and ``teacher_workspace_id``
    both FK'd to ``teacher_workspaces.id``; ``syllabus_day_id`` and
    ``lesson_period_id`` both FK'd to ``lesson_periods.id``; ``date`` shadowed
    ``delivered_on``. The new names (``teacher_workspace_id``,
    ``lesson_period_id``, ``delivered_on``) survive; the old shadows are
    dropped. Promoted to ``NOT NULL`` where the semantics call for it
    (workspace + lesson_period must be present; ``delivered_on`` stays
    nullable — a planned delivery has no actual date until it happens).
    """

    __tablename__ = "lesson_deliveries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    teacher_workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teacher_workspaces.id", name="fk_lesson_deliveries_teacher_workspace_id"),
        index=True,
    )
    lesson_period_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_periods.id", name="fk_lesson_deliveries_lesson_period_id"),
        index=True,
    )
    plan_version_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id", name="fk_lesson_deliveries_plan_version_id"),
        nullable=True,
    )
    status: Mapped[LessonDeliveryStatus] = mapped_column(
        status_enum(LessonDeliveryStatus, name="lesson_delivery_status"),
        default=LessonDeliveryStatus.PLANNED,
        server_default=text("'planned'"),
    )
    delivered_on: Mapped[calendar_date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
