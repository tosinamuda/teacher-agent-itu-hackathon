"""The rules that allow or refuse a new conditioned generation.

Each rule raises the ``ExperimentApplicationError`` the API returns; a caller
that passes them all may create an execution row.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.domain import ConditionRunStatus, ExecutionStatus
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.shared.session_plan_view import SessionPlanView

# Statuses that mean a generation is still running — a second launch is rejected
# while any execution for the same experiment+hypothesis is in one of these.
IN_FLIGHT_STATUSES: frozenset[ExecutionStatus] = frozenset(
    {ExecutionStatus.CREATED, ExecutionStatus.QUEUED, ExecutionStatus.RUNNING}
)


class PlanApprovalReader(Protocol):
    async def get_plan_version(self, plan_version_id: str) -> LaunchPlanRecord | None: ...


class LaunchPlanRecord(Protocol):
    @property
    def status(self) -> PlanVersionStatus: ...

    @property
    def session_plan(self) -> object: ...


class ConditionFreezeReader(Protocol):
    async def list_condition_runs_for_executions(
        self, execution_db_ids: Sequence[UUID]
    ) -> list[ExperimentConditionRun]: ...


async def ensure_plan_is_approved(
    reader: PlanApprovalReader,
    experiment: Experiment,
) -> None:
    """Refuse a generation whose lesson plan is unauthored, absent, unapproved or empty."""
    if experiment.plan_version_id is None:
        raise ExperimentApplicationError(409, "experiment_plan_not_authored")
    plan_version = await reader.get_plan_version(experiment.plan_version_id)
    if plan_version is None:
        raise ExperimentApplicationError(404, "plan_version_not_found")
    if plan_version.status != PlanVersionStatus.APPROVED:
        raise ExperimentApplicationError(409, "plan_version_not_approved")
    try:
        SessionPlanView.model_validate(plan_version.session_plan)
    except ValidationError as exc:
        raise ExperimentApplicationError(409, "plan_version_session_plan_missing") from exc


def ensure_no_generation_in_flight(executions: list[ExperimentExecution]) -> None:
    """Refuse a launch while one generation for the same experiment+hypothesis runs."""
    if any(execution.status in IN_FLIGHT_STATUSES for execution in executions):
        raise ExperimentApplicationError(409, "generation_already_in_progress")


async def ensure_h1_conditions_unfrozen(
    reader: ConditionFreezeReader,
    prior: list[ExperimentExecution],
) -> None:
    """Refuse a fresh H1 generation once any H1 condition has succeeded.

    The C0–C3 ablation is fixed for reproducibility, and only C4 re-iterates via
    the teacher gate. A partially succeeded run freezes its succeeded conditions
    too — those are recovered by the per-condition retry, never by a fresh full
    generation that would re-roll them.
    """
    if any(execution.status == ExecutionStatus.SUCCEEDED for execution in prior):
        raise ExperimentApplicationError(409, "h1_conditions_frozen")
    if not prior:
        return
    runs = await reader.list_condition_runs_for_executions([execution.id for execution in prior])
    if any(run.status == ConditionRunStatus.SUCCEEDED for run in runs):
        raise ExperimentApplicationError(409, "h1_conditions_frozen")
