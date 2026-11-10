"""Attachment model: an uploaded provenance image (a photo of the original).

Bytes live on disk under the uploads dir at ``stored_path``; this row is the
opaque handle (its UUID is the public id) so downloads go through an auth-gated
route, never a guessable filesystem path.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID
from app.shared.time import utc_now


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # What the image documents, e.g. 'student_answer_sheet' or 'lesson_plan_document'.
    kind: Mapped[str] = mapped_column(String(64))
    content_type: Mapped[str] = mapped_column(String(128))
    byte_size: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64))
    # Path relative to the uploads dir (never returned to clients).
    stored_path: Mapped[str] = mapped_column(String(512))
    caption: Mapped[str | None] = mapped_column(String(512), nullable=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
