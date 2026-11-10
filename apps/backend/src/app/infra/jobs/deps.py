"""The job queue, bound to the request's session."""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.infra.jobs.queue import JobQueue


def job_queue(db: AsyncSession = Depends(get_db)) -> JobQueue:
    """Jobs queued with whatever else the request commits."""
    return JobQueue(db)
