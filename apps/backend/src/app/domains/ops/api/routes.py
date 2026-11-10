"""Admin ops panel API: job-queue health + execution recovery.

All routes are gated on ``ops:*`` — held by ``admin`` (and the global-wildcard
``researcher``). Reads use ``act="read"``; state-changing actions use
``act="manage"`` so a read-only ops viewer can be granted later without the
ability to cancel or re-dispatch.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.ops.api.schemas import (
    ExecutionRow,
    JobRow,
    OpsActionResponse,
    OpsHealthResponse,
)
from app.domains.ops.application import execution_ops, job_ops
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/health", response_model=OpsHealthResponse)
async def ops_health(
    db: AsyncSession = Depends(get_db),
    _: Actor = Depends(requires(obj="ops:*", act="read")),
) -> OpsHealthResponse:
    return OpsHealthResponse.model_validate(await job_ops.job_health(db))


@router.get("/jobs", response_model=list[JobRow])
async def ops_jobs(
    state: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    _: Actor = Depends(requires(obj="ops:*", act="read")),
) -> list[JobRow]:
    rows = await job_ops.recent_jobs(db, state=state, limit=limit)
    return [JobRow.model_validate(row) for row in rows]


@router.post("/jobs/{job_id}/cancel", response_model=OpsActionResponse)
async def ops_cancel_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    _: Actor = Depends(requires(obj="ops:*", act="manage")),
) -> OpsActionResponse:
    return OpsActionResponse.model_validate(await job_ops.cancel_job(db, job_id))


@router.get("/executions", response_model=list[ExecutionRow])
async def ops_executions(
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    _: Actor = Depends(requires(obj="ops:*", act="read")),
) -> list[ExecutionRow]:
    rows = await execution_ops.recent_executions(db, limit=limit, status=status)
    return [ExecutionRow.model_validate(r) for r in rows]


@router.post("/executions/{execution_id}/redispatch", response_model=OpsActionResponse)
async def ops_redispatch(
    execution_id: str,
    db: AsyncSession = Depends(get_db),
    _: Actor = Depends(requires(obj="ops:*", act="manage")),
) -> OpsActionResponse:
    return OpsActionResponse.model_validate(await execution_ops.redispatch(db, execution_id))


@router.post("/executions/{execution_id}/cancel", response_model=OpsActionResponse)
async def ops_cancel(
    execution_id: str,
    db: AsyncSession = Depends(get_db),
    _: Actor = Depends(requires(obj="ops:*", act="manage")),
) -> OpsActionResponse:
    return OpsActionResponse.model_validate(await execution_ops.cancel(db, execution_id))
