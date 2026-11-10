"""Assessment response persistence model."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID
from app.shared.time import utc_now


class StudentItemResponse(Base):
    __tablename__ = "student_item_responses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("exit_ticket_items.id"),
        index=True,
    )
    student_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id"),
        index=True,
    )
    lesson_delivery_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_deliveries.id"),
        nullable=True,
        index=True,
    )
    choice: Mapped[str] = mapped_column(String(16))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    score: Mapped[float] = mapped_column(Float)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        server_default=text("now()"),
    )


__all__ = ["StudentItemResponse"]
