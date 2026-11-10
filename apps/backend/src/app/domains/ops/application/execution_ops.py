"""Experiment-execution control for the admin ops panel: list, re-dispatch, cancel.

This is the domain-aware half of the panel: a stranded ``queued`` execution is the thing
an admin actually needs to recover. The ``execution_id`` ties the two together — it is the
subject of the job that runs the execution.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.domain.types import ExecutionStatus
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.infra.jobs.kinds import RUN_CONDITIONED_EXECUTION
from app.infra.jobs.queue import JobQueue
from app.shared.time import as_utc

# Past these an execution is done: cancel is then an idempotent no-op, not a clobber.
_TERMINAL_STATUSES = frozenset({ExecutionStatus.SUCCEEDED, ExecutionStatus.FAILED})


def _row(
    execution: ExperimentExecution, experiment_id: str, experiment_code: str
) -> dict[str, Any]:
    status = execution.status
    return {
        "execution_id": execution.execution_id,
        "experiment_id": experiment_id,
        "experiment_code": experiment_code,
        "hypothesis": execution.hypothesis,
        "status": status.value if hasattr(status, "value") else str(status),
        "attempt_number": execution.attempt_number,
        "error_category": execution.error_category,
        "error_message": execution.error_message,
        "created_at": as_utc(execution.created_at).isoformat() if execution.created_at else None,
        "updated_at": as_utc(execution.updated_at).isoformat() if execution.updated_at else None,
    }


async def recent_executions(
    db: AsyncSession, *, limit: int = 50, status: str | None = None
) -> list[dict[str, Any]]:
    """Most-recent executions joined to their experiment, newest first."""
    stmt = (
        select(ExperimentExecution, Experiment.experiment_id, Experiment.experiment_code)
        .join(Experiment, Experiment.id == ExperimentExecution.experiment_db_id)
        .order_by(ExperimentExecution.created_at.desc())
        .limit(limit)
    )
    if status:
        stmt = stmt.where(ExperimentExecution.status == status)
    rows = (await db.execute(stmt)).all()
    return [_row(execution, exp_id, exp_code) for execution, exp_id, exp_code in rows]


async def redispatch(db: AsyncSession, execution_id: str) -> dict[str, Any]:
    """Re-queue an execution (recovers a stranded queued / failed / crashed-running one).

    Locks the execution ``FOR UPDATE`` first so it can't race the job running it: cancels
    that job, clears the prior attempt's partial output (idempotent re-run), flips to QUEUED
    and queues a fresh job, all in one commit. A job still finishing the old attempt finds
    the status is no longer RUNNING at its terminal write and discards its result, so this
    safely recovers even a genuinely-running (or crashed-running) one.
    """
    repo = ExperimentRepository(db)
    execution = await repo.get_execution_for_update(execution_id)
    if execution is None:
        return {"ok": False, "detail": "execution_not_found"}
    jobs = JobQueue(db)
    await jobs.cancel(execution_id)
    await repo.clear_execution_generation(execution.id)
    execution.status = ExecutionStatus.QUEUED
    execution.error_message = None
    execution.error_category = None
    jobs.add(RUN_CONDITIONED_EXECUTION, execution_id, subject=execution_id)
    await db.commit()
    return {"ok": True, "execution_id": execution_id, "status": ExecutionStatus.QUEUED.value}


async def cancel(db: AsyncSession, execution_id: str) -> dict[str, Any]:
    """Cancel the job running the execution (if any) and mark the execution failed/cancelled.

    Locks the execution ``FOR UPDATE`` and only transitions from a NON-terminal status,
    so a cancel arriving as the job finishes is neither silently lost nor a clobber of
    the job's terminal write — whichever takes the lock first wins deterministically,
    and an already-terminal execution is an idempotent no-op.

    Also clears any output the run already COMMITTED (the generation commits condition runs
    incrementally), so a cancelled execution carries no leftover/orphaned rows — the same
    discard the job's finalize performs, done here under the same lock.
    """
    repo = ExperimentRepository(db)
    execution = await repo.get_execution_for_update(execution_id)
    if execution is None:
        return {"ok": False, "detail": "execution_not_found"}
    status = execution.status
    if status in _TERMINAL_STATUSES:
        return {
            "ok": True,
            "execution_id": execution_id,
            "status": status.value if hasattr(status, "value") else str(status),
            "cancelled_job_ids": [],
        }
    cancelled = await JobQueue(db).cancel(execution_id)
    # Discard anything the (possibly still-running) job already committed for this run,
    # under the lock — downstream reads condition runs with no status filter, and a committed
    # SUCCEEDED H1 run would otherwise re-freeze H1 (409 h1_conditions_frozen). Runs the job
    # commits AFTER this are cleared by its own finalize (it sees status != RUNNING).
    await repo.clear_execution_generation(execution.id)
    execution.status = ExecutionStatus.FAILED
    execution.error_category = "cancelled"
    execution.error_message = "Cancelled by admin from the ops panel."
    await db.commit()
    return {
        "ok": True,
        "execution_id": execution_id,
        "status": ExecutionStatus.FAILED.value,
        "cancelled_job_ids": cancelled,
    }
