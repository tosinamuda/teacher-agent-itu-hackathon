"""Launch conditioned generation: a whole experiment, or one failed condition.

Both entrypoints read the same shape — check the launch is allowed, then queue
the job that does the work. What the worker then runs lives in
``conditioned_execution``; per-condition retries live in ``condition_retry``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from app.domains.experiments.application.create_execution import create_execution
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.launch_policy import (
    ensure_h1_conditions_unfrozen,
    ensure_no_generation_in_flight,
    ensure_plan_is_approved,
)
from app.domains.experiments.application.launch_ports import ExecutionLaunchStore
from app.domains.experiments.application.lookups import (
    executions_for_hypothesis,
    experiment_or_error,
)
from app.domains.experiments.domain import ExecutionStatus, Hypothesis
from app.domains.experiments.infrastructure.models import ExperimentExecution
from app.infra.jobs.kinds import RETRY_CONDITION_RUN, RUN_CONDITIONED_EXECUTION
from app.infra.jobs.queue import JobAlreadyQueuedError
from app.shared.json_types import JsonObject
from app.shared.time import utc_now


@dataclass(frozen=True)
class LaunchExecutionInput:
    """What any transport must supply to start one generation."""

    experiment_id: str
    hypothesis: Hypothesis
    runtime_snapshot: JsonObject | None
    #: Who started it, so they may follow its job.
    requested_by: str | None = None


@dataclass(frozen=True)
class LaunchExecutionOutput:
    """The attempt a launch created, with nothing a database session is needed to read."""

    id: uuid.UUID
    execution_id: str
    hypothesis: Hypothesis
    attempt_number: int
    status: ExecutionStatus
    runtime_snapshot: JsonObject | None
    error_message: str | None
    error_category: str | None
    created_at: datetime
    updated_at: datetime


class LaunchExecution:
    """Start one generation: H1's C0-C3, or H2's P0/P1 per focal learner.

    The QUEUED execution and the job that runs it are staged together and committed once,
    so a committed launch always has its job, and no launch leaves one behind.
    """

    def __init__(self, store: ExecutionLaunchStore) -> None:
        self._store = store

    async def __call__(self, request: LaunchExecutionInput) -> LaunchExecutionOutput:
        store = self._store
        experiment = await experiment_or_error(store.experiments, request.experiment_id)
        await ensure_plan_is_approved(store.plan_approvals, experiment)

        prior = await executions_for_hypothesis(
            store.experiments, experiment.id, request.hypothesis
        )
        ensure_no_generation_in_flight(prior)
        if request.hypothesis is Hypothesis.H1:
            await ensure_h1_conditions_unfrozen(store.condition_freezes, prior)

        execution = await create_execution(
            store,
            experiment_db_id=experiment.id,
            hypothesis=request.hypothesis,
            runtime_snapshot=request.runtime_snapshot,
        )
        execution.status = ExecutionStatus.QUEUED
        execution.updated_at = utc_now()
        store.jobs.add(
            RUN_CONDITIONED_EXECUTION,
            execution.execution_id,
            subject=execution.execution_id,
            requested_by=request.requested_by,
        )
        await store.commit()
        return _to_output(execution)


def _to_output(execution: ExperimentExecution) -> LaunchExecutionOutput:
    """Copy the staged row's fields out, so no caller holds the row itself."""
    return LaunchExecutionOutput(
        id=execution.id,
        execution_id=execution.execution_id,
        hypothesis=Hypothesis(execution.hypothesis),
        attempt_number=execution.attempt_number,
        status=execution.status,
        runtime_snapshot=execution.runtime_snapshot,
        error_message=execution.error_message,
        error_category=execution.error_category,
        created_at=execution.created_at,
        updated_at=execution.updated_at,
    )


async def retry_condition(
    store: ExecutionLaunchStore,
    *,
    experiment_id: str,
    condition_code: str,
) -> ExperimentExecution:
    """Relaunch one FAILED condition on the experiment's latest H1 execution.

    Only that condition regenerates — the job refuses to touch a frozen, succeeded one.
    """
    experiment = await experiment_or_error(store.experiments, experiment_id)
    h1_executions = await executions_for_hypothesis(store.experiments, experiment.id, Hypothesis.H1)
    if not h1_executions:
        raise ExperimentApplicationError(404, "no_h1_execution")

    execution = h1_executions[0]
    ensure_no_generation_in_flight([execution])
    try:
        await store.jobs.submit(
            RETRY_CONDITION_RUN,
            execution.execution_id,
            condition_code,
            subject=f"{execution.execution_id}:{condition_code}",
        )
    except JobAlreadyQueuedError as error:
        raise ExperimentApplicationError(409, "condition_retry_already_queued") from error
    return execution
