"""Persistence for the student-pack generation job (the async-generation lifecycle).

A ``StudentPackGeneration`` row tracks one *attempt* to generate a learner's
post-class review pack. It is the student-pack analogue of ``ExperimentExecution``:
it makes the queued/running/failed state of a background generation visible (so a
failed generation is distinguishable from a never-run one, and the teacher UI can
show "generating…" / "failed → retry"), and its ``(student, lesson, attempt)``
unique key + in-flight guard stop two concurrent dispatches from both generating.

It is deliberately separate from the produced ``Artefact``: a generation can fail
before any pack exists, and — under "keep versions" semantics — each successful
attempt produces a NEW pack row, so the job (the attempt) and the artefact (its
output) are one-to-(zero-or-one).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import UUID
from app.db.enums import status_enum
from app.domains.artefacts.types.post_class_review_pack.domain.types import (
    StudentPackGenerationStatus,
)
from app.shared.time import utc_now


class StudentPackGeneration(Base):
    __tablename__ = "student_pack_generations"
    __table_args__ = (
        # One row per (student, lesson, attempt): attempt_number is MAX()+1, so two
        # concurrent dispatches must not mint two rows at the same attempt — the loser
        # trips this and converges to the winner (no double-generation).
        UniqueConstraint(
            "student_id",
            "plan_version_id",
            "attempt_number",
            name="uq_student_pack_generation_attempt",
        ),
        # Hot read: latest status per (plan_version, student) for the teacher queue.
        Index(
            "ix_student_pack_generations_plan_student_created",
            "plan_version_id",
            "student_id",
            text("created_at DESC"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    student_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id", name="fk_student_pack_generations_student_id"),
        index=True,
    )
    plan_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id", name="fk_student_pack_generations_plan_version_id"),
        index=True,
    )
    attempt_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[StudentPackGenerationStatus] = mapped_column(
        status_enum(StudentPackGenerationStatus, name="student_pack_generation_status"),
        index=True,
    )
    # Times a job has claimed this generation. A run cut short (a crash, a deploy) is run
    # again; bounding the claim count stops a generation that always dies from looping.
    delivery_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False
    )
    # The pack version this attempt produced (set on success). Plain public id, not an
    # FK: the artefact is created + committed inside generation, then stamped here at
    # finalize — a loose reference keeps the job decoupled from artefact insert ordering.
    produced_artefact_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Structured failure category set by the worker (inputs_missing / generation),
    # so the UI reads it instead of pattern-matching error_message. Null unless FAILED.
    error_category: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, server_default=text("now()")
    )
