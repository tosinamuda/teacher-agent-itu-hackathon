"""The background work the app has to do, and the runners doing it.

A job is a row added in the same transaction as the change that asks for it, so work is
queued exactly when that change commits, and only then. The API process's runner claims
jobs from here and runs each in a process of its own.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, MICROSECOND_DATETIME, UUID
from app.shared.time import utc_now


class JobState(str, Enum):
    """QUEUED until a runner claims it, RUNNING while one holds it, then one of the ends."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


#: The states a job can still leave.
UNFINISHED = (JobState.QUEUED, JobState.RUNNING)


class Job(Base):
    """One piece of background work.

    ``active_subject`` carries the subject while the job is unfinished and is NULLed when it
    ends. MySQL allows repeated NULLs in a unique index, so this says "at most one unfinished
    job of a kind per subject" without a partial index, which MySQL does not have.
    """

    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("active_subject", "kind", name="uq_jobs_active_subject"),
        # A claim walks one of these in order and locks only the first row it can take;
        # without them it scans, and InnoDB locks every row a locking read examines.
        Index("ix_jobs_state_created_at", "state", "created_at"),
        Index("ix_jobs_state_lease_expires_at", "state", "lease_expires_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    kind: Mapped[str] = mapped_column(String(128), index=True)
    args: Mapped[list] = mapped_column(JSON)
    # What the job acts on, such as an execution id: how the ops panel finds and cancels it.
    subject: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    active_subject: Mapped[str | None] = mapped_column(String(128), nullable=True)
    state: Mapped[str] = mapped_column(String(16), default=JobState.QUEUED)
    attempts: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False
    )
    runner: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # A RUNNING job whose lease has passed is taken to have died with its process.
    lease_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    # What the handler returned, such as the id of what it made: how its caller finds it.
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # The auth id of whoever asked for the job: who may follow it.
    requested_by: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(MICROSECOND_DATETIME, default=utc_now)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class JobRunner(Base):
    """A process running jobs, as last seen: what the ops panel reads for liveness."""

    __tablename__ = "job_runners"

    runner: Mapped[str] = mapped_column(String(128), primary_key=True)
    slots: Mapped[int] = mapped_column(Integer)
    running: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
