"""Teaching workspace model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.school.models.subject_offerings import TermClassSubject
    from app.domains.users.models.user import User


class TeacherWorkspace(Base):
    """Intersection of teacher identity and a class-term subject offering."""

    __tablename__ = "teacher_workspaces"
    # One workspace per (teacher, offering): get-or-create key for provisioning.
    __table_args__ = (
        UniqueConstraint("teacher_id", "term_class_subject_id", name="uq_workspace_teacher_tcs"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # FK to the user who teaches this workspace (User with role='teacher').
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True,
    )
    term_class_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("term_class_subjects.id"),
        index=True,
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )

    teacher: Mapped[User] = relationship("User", back_populates="workspaces")
    term_class_subject: Mapped[TermClassSubject] = relationship("TermClassSubject")
