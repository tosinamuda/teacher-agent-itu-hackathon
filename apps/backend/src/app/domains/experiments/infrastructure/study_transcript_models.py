"""How the study's lessons became data: each transcript the published release carries.

A lesson's teacher pages were photographed, transcribed verbatim, and cleaned, each change
logged with the source that licenses it; each learner's marked script was transcribed with
the teacher's marks. The photographs are the study's private record; the transcripts are
published, and kept here as published, with the pages each one came from.
"""

from __future__ import annotations

import uuid

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID


class StudyTranscript(Base):
    __tablename__ = "study_transcripts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id", name="fk_study_transcripts_plan_version_id"),
        index=True,
    )
    #: ``teacher_record`` (verbatim), ``teacher_cleaned``, ``cleaning_log`` or ``learner_script``.
    kind: Mapped[str] = mapped_column(String(32))
    #: The learner whose script it is, for a ``learner_script``.
    student_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    #: The photographed pages it was transcribed from, each ``{"file", "role"}``.
    pages: Mapped[list[dict[str, str]]] = mapped_column(JSON)
    #: The transcript's header, e.g. the teacher's total and comment on a script.
    header: Mapped[dict[str, object]] = mapped_column(JSON)
    body: Mapped[str] = mapped_column(Text)
    #: Where it sits in the release, and the SHA-256 the release records for it.
    source_path: Mapped[str] = mapped_column(String(255))
    sha256: Mapped[str] = mapped_column(String(64))
