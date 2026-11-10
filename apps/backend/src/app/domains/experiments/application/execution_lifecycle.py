"""Claim and finalize one conditioned experiment worker attempt.

Both writes run under the execution's row lock, which is what serializes them
against the ops panel and against another delivery of the same task. Each takes
a store rather than sharing one: ``finalize_execution`` must be given a unit of
work that is not already carrying the failure it is recording, and nothing in a
signature can say that for the caller.
"""

import logging
import uuid
from typing import Protocol

from app.domains.experiments.application.store import ExperimentStore
from app.domains.experiments.domain.types import ExecutionErrorCategory, ExecutionStatus
from app.domains.experiments.infrastructure.models import ExperimentExecution
from app.shared.worker_delivery import MAX_TASK_DELIVERIES

logger = logging.getLogger(__name__)

_TERMINAL_STATUSES = (ExecutionStatus.SUCCEEDED, ExecutionStatus.FAILED)


class ExecutionLifecycle(Protocol):
    """Locked execution reads and writes used by worker claim/finalize/retry."""

    async def get_execution(self, execution_id: str) -> ExperimentExecution | None: ...

    async def get_execution_for_update(self, execution_id: str) -> ExperimentExecution | None: ...

    async def clear_execution_generation(self, execution_db_id: uuid.UUID) -> None: ...

    async def mark_execution_running(
        self, execution_db_id: uuid.UUID, *, deliveries: int
    ) -> None: ...

    async def mark_execution_poisoned(
        self, execution_db_id: uuid.UUID, *, deliveries: int, error: str
    ) -> None: ...

    async def record_terminal_status(
        self,
        execution_db_id: uuid.UUID,
        *,
        status: ExecutionStatus,
        error: str | None,
        error_category: ExecutionErrorCategory | None,
    ) -> None: ...


async def claim_execution(
    store: ExperimentStore,
    execution_id: str,
    *,
    redelivered: bool,
) -> ExperimentExecution | None:
    """Claim a runnable execution and clear output from its previous attempt.

    A RUNNING row is only claimable by a rerun of its job, because only then is the
    previous attempt certainly gone: a job is run again only once its process has exited,
    or its claim has lapsed — and a job's process stops itself when its claim is gone or
    its runner has died. A first run finding RUNNING is a duplicate instead, and running
    it would clear the output of the attempt that is still generating.
    """
    lifecycle = store.execution_lifecycle
    execution = await lifecycle.get_execution_for_update(execution_id)
    if execution is None:
        logger.warning("conditioned execution not found: %s", execution_id)
        return None
    if execution.status in _TERMINAL_STATUSES:
        logger.info("execution %s already %s; skipping run", execution_id, execution.status)
        return None
    if execution.status == ExecutionStatus.RUNNING and not redelivered:
        logger.warning("execution %s is already running; skipping duplicate dispatch", execution_id)
        return None

    # Read-modify-write, safe only because this holds the row FOR UPDATE.
    deliveries = (execution.delivery_count or 0) + 1
    if deliveries > MAX_TASK_DELIVERIES:
        await lifecycle.mark_execution_poisoned(
            execution.id,
            deliveries=deliveries,
            error=f"exceeded {MAX_TASK_DELIVERIES} deliveries (poison message)",
        )
        await store.commit()
        logger.error(
            "execution %s poison-bounded after %s deliveries; marked FAILED",
            execution_id,
            deliveries,
        )
        return None

    await lifecycle.clear_execution_generation(execution.id)
    await lifecycle.mark_execution_running(execution.id, deliveries=deliveries)
    await store.commit()
    return execution


async def finalize_execution(
    store: ExperimentStore,
    execution_id: str,
    *,
    status: ExecutionStatus,
    error: str | None = None,
    error_category: ExecutionErrorCategory | None = None,
) -> None:
    """Finalize the attempt if it still owns RUNNING; otherwise discard its output."""
    lifecycle = store.execution_lifecycle
    execution = await lifecycle.get_execution_for_update(execution_id)
    if execution is None:
        await store.rollback()
        logger.info("execution %s disappeared before finalization", execution_id)
        return
    if execution.status != ExecutionStatus.RUNNING:
        current_status = execution.status
        await lifecycle.clear_execution_generation(execution.id)
        await store.commit()
        logger.info(
            "execution %s no longer RUNNING (now %s); discarded generated output",
            execution_id,
            current_status,
        )
        return

    await lifecycle.record_terminal_status(
        execution.id,
        status=status,
        error=error,
        error_category=error_category,
    )
    await store.commit()
