"""Following a job: the page that asked for a generation reads how it is going."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.jobs.api.schemas import JobStatus
from app.domains.jobs.application.following import followed, latest
from app.shared.auth import ROLE_ANONYMOUS, Actor, get_actor

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _signed_in(actor: Actor = Depends(get_actor)) -> Actor:
    if actor.role == ROLE_ANONYMOUS:
        raise HTTPException(status_code=403, detail="sign_in_to_follow_a_job")
    return actor


@router.get("", response_model=JobStatus | None)
async def latest_job(
    kind: str,
    subject: str,
    actor: Actor = Depends(_signed_in),
    db: AsyncSession = Depends(get_db),
) -> JobStatus | None:
    """The newest job of ``kind`` for ``subject`` the caller asked for, or null."""
    job = await latest(db, actor, kind=kind, subject=subject)
    return JobStatus(**asdict(job)) if job is not None else None


@router.get("/{job_id}", response_model=JobStatus)
async def get_job(
    job_id: str,
    actor: Actor = Depends(_signed_in),
    db: AsyncSession = Depends(get_db),
) -> JobStatus:
    job = await followed(db, actor, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job_not_found")
    return JobStatus(**asdict(job))
