"""Exit ticket item model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now


class ExitTicketItem(Base):
    __tablename__ = "exit_ticket_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subtopic_id: Mapped[str] = mapped_column(
        String(200), ForeignKey("curriculum_subtopics.subtopic_id")
    )
    knowledge_component_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("knowledge_components.id"), nullable=True
    )
    plan_version_id: Mapped[str] = mapped_column(String(64), ForeignKey("plan_versions.version_id"))
    # Objective this item assesses (drives objective-indexed scoring).
    lesson_objective_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    stem: Mapped[str] = mapped_column(Text)
    correct_option: Mapped[str] = mapped_column(String(16))
    options: Mapped[dict] = mapped_column(JSON)
    # Per-distractor misconception map {option_key: misconception_code}: selecting
    # a tagged distractor reveals that misconception.
    option_misconceptions: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
