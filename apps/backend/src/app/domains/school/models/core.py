"""Core school infrastructure models."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID
from app.shared.time import utc_now


class Subject(Base):
    """The pure domain of study (e.g., Mathematics)."""

    __tablename__ = "subjects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)  # Science, Arts, etc.
    is_trade: Mapped[bool] = mapped_column(Boolean, default=False)
    is_compulsory: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class GradeLevel(Base):
    """The academic level (e.g., SS1, JSS1)."""

    __tablename__ = "grade_levels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    # For sorting: 1 for JSS1, 6 for SS3
    sequence: Mapped[int] = mapped_column(Integer, unique=True)
    average_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class AcademicYear(Base):
    """Global school year (e.g., 2024/2025)."""

    __tablename__ = "academic_years"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)  # "2024/2025"
    start_date: Mapped[datetime] = mapped_column(Date)
    end_date: Mapped[datetime] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class Term(Base):
    """Academic Term (e.g., 1st Term)."""

    __tablename__ = "terms"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(32))  # "1st Term", "2nd Term"
    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("academic_years.id", name="fk_terms_academic_year_id"),
        index=True,
    )
    start_date: Mapped[datetime] = mapped_column(Date)
    end_date: Mapped[datetime] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
