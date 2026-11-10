"""Structural school models (schools, classes, courses)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import UUID
from app.domains.school.models.core import GradeLevel, Subject
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.school.models.subject_offerings import TermClassSubject


class School(Base):
    """Institution boundary for classes and researcher filtering."""

    __tablename__ = "schools"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    default_academic_year: Mapped[str | None] = mapped_column(String(32), nullable=True)
    current_term: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class Class(Base):
    """A specific group/arm of students (e.g., SS1A)."""

    __tablename__ = "classes"
    # One class per (school, name): provisioning is get-or-create by this key, so
    # concurrent setup must not mint two "JSS1" rows for the same school.
    __table_args__ = (UniqueConstraint("school_id", "name", name="uq_classes_school_name"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(32), index=True)  # "SS1A"
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("schools.id"), index=True
    )
    grade_level_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("grade_levels.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )

    # Relationships
    school: Mapped[School] = relationship("School")
    grade_level: Mapped[GradeLevel] = relationship("GradeLevel")
    term_class_subjects: Mapped[list[TermClassSubject]] = relationship(
        "TermClassSubject",
        back_populates="classroom",
    )


class Course(Base):
    """The distinct curriculum unit: Subject + Grade Level.

    Example: "SS1 Mathematics".
    """

    __tablename__ = "courses_curriculum"  # Renamed to avoid alias conflict during migration
    # One course per (subject, grade): get-or-create key for provisioning.
    __table_args__ = (
        UniqueConstraint("subject_id", "grade_level_id", name="uq_courses_subject_grade"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128))  # "SS1 Mathematics"
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subjects.id"), index=True
    )
    grade_level_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("grade_levels.id"), index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )

    # Relationships
    subject: Mapped[Subject] = relationship("Subject")
    grade_level: Mapped[GradeLevel] = relationship("GradeLevel")
    term_class_subjects: Mapped[list[TermClassSubject]] = relationship(
        "TermClassSubject", back_populates="course"
    )
