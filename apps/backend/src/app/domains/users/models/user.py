"""User-domain identity model.

A single ``users`` table carries every authenticated identity (researcher,
teacher, admin, rater, student). The ``role`` column distinguishes them; the
relationships hung off this class are sparse by role (e.g. only teacher users
have ``workspaces``).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.teaching.models.workspace import TeacherWorkspace


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    role: Mapped[str] = mapped_column(
        String(32), default="teacher", server_default=text("'teacher'")
    )
    preferences: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )

    # Sparse: only teacher-role users have workspaces. Other roles leave it empty.
    workspaces: Mapped[list[TeacherWorkspace]] = relationship(
        "TeacherWorkspace",
        back_populates="teacher",
    )
