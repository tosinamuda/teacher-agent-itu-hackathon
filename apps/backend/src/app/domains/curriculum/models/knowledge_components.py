"""Knowledge component model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID
from app.shared.time import utc_now


class KnowledgeComponent(Base):
    __tablename__ = "knowledge_components"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kc_code: Mapped[str] = mapped_column(String(64), unique=True)
    subtopic_id: Mapped[str] = mapped_column(
        String(200),
        ForeignKey("curriculum_subtopics.subtopic_id"),
    )
    description: Mapped[str] = mapped_column(Text)
    bloom_level: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        server_default=text("now()"),
    )
