"""School-domain subject offering model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import UUID
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.school.models.structure import Class, Course
    from app.domains.teaching.models.syllabus import SchemeOfWork


class TermClassSubject(Base):
    """Subject offered in a class for a specific term."""

    __tablename__ = "term_class_subjects"
    # One offering per (class, course, term, year): the provisioning get-or-create key.
    __table_args__ = (
        UniqueConstraint(
            "class_id", "course_id", "term", "year", name="uq_tcs_class_course_term_year"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses_curriculum.id"),
        index=True,
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id"),
        index=True,
    )
    term: Mapped[str] = mapped_column(String(32))
    year: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )

    weeks: Mapped[list[SchemeOfWork]] = relationship(
        "SchemeOfWork",
        back_populates="term_class_subject",
        order_by="SchemeOfWork.week_number",
    )
    course: Mapped[Course] = relationship("Course", back_populates="term_class_subjects")
    classroom: Mapped[Class] = relationship("Class", back_populates="term_class_subjects")


__all__ = ["TermClassSubject"]
