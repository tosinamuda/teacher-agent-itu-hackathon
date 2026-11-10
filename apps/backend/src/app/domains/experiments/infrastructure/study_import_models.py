"""Which published release, read by which importer, the study in the database came from."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID
from app.shared.time import utc_now


class StudyImport(Base):
    """One imported study: its pinned datasets and the digest of the code that imported it.

    A host whose record matches what the code pins holds the study as published; one whose
    record differs is brought up to date by importing it again.
    """

    __tablename__ = "study_imports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id: Mapped[str] = mapped_column(String(64), unique=True)
    #: Each dataset's Hub commit and the SHA-256 of its PROVENANCE.json.
    release: Mapped[dict[str, dict[str, str]]] = mapped_column(JSON)
    #: The SHA-256 of the importer's source, so a corrected importer is seen to differ.
    importer: Mapped[str] = mapped_column(String(64))
    imported_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
