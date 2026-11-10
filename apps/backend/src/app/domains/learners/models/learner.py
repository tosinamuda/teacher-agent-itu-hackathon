"""Learner profile model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now


class LearnerProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    code: Mapped[str | None] = mapped_column(String(64), unique=True, index=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(128))
    grade: Mapped[str] = mapped_column(String(32), index=True)
    track: Mapped[str] = mapped_column(String(64), index=True)
    class_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classes.id"), nullable=True, index=True
    )
    field_of_study: Mapped[str | None] = mapped_column(String(32), nullable=True)
    trade_subject: Mapped[str | None] = mapped_column(String(128), nullable=True)
    field_core_subjects: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    language_level: Mapped[str | None] = mapped_column(String(32), nullable=True)
    pace_preference: Mapped[str | None] = mapped_column(String(32), nullable=True)
    time_budget_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Login link: a human student binds 1:1 to a ``User`` row with role='student'.
    # Pure research-data identities (no ``code``) leave this NULL.
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


__all__ = ["LearnerProfile"]
