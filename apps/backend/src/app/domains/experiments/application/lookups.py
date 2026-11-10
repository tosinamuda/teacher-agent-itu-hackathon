"""Repository + 404 lookup helpers shared between the experiments services.

Each helper pairs a repo call with the typed ``ExperimentApplicationError(404)``
the API expects when the row is absent. Centralised so the not-found policy
(error code + detail string) lives in one place — both the main
``ExperimentApplicationService`` and the ``ExperimentContextApplicationService``
delegate to these rather than carrying duplicate inline guards.
"""

from __future__ import annotations

import uuid
from typing import Protocol
from uuid import UUID

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.domain import Hypothesis
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.domains.teaching.models import LessonPeriod, TeacherWorkspace


class WorkspaceReader(Protocol):
    async def get_workspace(self, workspace_id: UUID) -> TeacherWorkspace | None: ...


class LessonPeriodReader(Protocol):
    async def get_lesson_period(self, lesson_period_id: UUID) -> LessonPeriod | None: ...


class ExperimentIdentityReader(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...


class ExecutionIdentityReader(Protocol):
    async def get_execution(self, execution_id: str) -> ExperimentExecution | None: ...


class ExperimentExecutionHistoryReader(Protocol):
    async def list_executions_for_experiment(
        self, experiment_db_id: UUID
    ) -> list[ExperimentExecution]: ...


class PlanVersionPlanReader(Protocol):
    async def get_plan_version_plan(
        self, *, plan_version_id: str
    ) -> tuple[PlanVersion, LessonPlan] | None: ...


def safe_uuid(value: str | None) -> uuid.UUID | None:
    """Parse a string as UUID, returning ``None`` on any malformed input."""
    if value is None:
        return None
    try:
        return uuid.UUID(value)
    except ValueError:
        return None


async def experiment_or_error(
    repository: ExperimentIdentityReader,
    experiment_id: str,
) -> Experiment:
    """Fetch an experiment by public id; raise 404 if absent."""
    experiment = await repository.get_experiment(experiment_id)
    if experiment is None:
        raise ExperimentApplicationError(404, "experiment_not_found")
    return experiment


async def execution_or_error(
    repository: ExecutionIdentityReader,
    execution_id: str,
) -> ExperimentExecution:
    """Fetch an execution by public id; raise 404 if absent."""
    execution = await repository.get_execution(execution_id)
    if execution is None:
        raise ExperimentApplicationError(404, "execution_not_found")
    return execution


async def executions_for_hypothesis(
    repository: ExperimentExecutionHistoryReader,
    experiment_db_id: UUID,
    hypothesis: Hypothesis,
) -> list[ExperimentExecution]:
    """List one experiment's executions for a single hypothesis, latest first."""
    return [
        execution
        for execution in await repository.list_executions_for_experiment(experiment_db_id)
        if execution.hypothesis == hypothesis.value
    ]


async def workspace_or_error(
    repository: WorkspaceReader,
    workspace_id: UUID,
) -> TeacherWorkspace:
    """Fetch a teacher workspace by id; raise 404 if absent."""
    workspace = await repository.get_workspace(workspace_id)
    if workspace is None:
        raise ExperimentApplicationError(404, "teacher_workspace_not_found")
    return workspace


async def plan_version_record_or_error(
    repository: PlanVersionPlanReader,
    plan_version_id: str,
) -> tuple[PlanVersion, LessonPlan]:
    """Fetch the (plan_version, lesson_plan) record by id; raise 404 if absent."""
    record = await repository.get_plan_version_plan(plan_version_id=plan_version_id)
    if record is None:
        raise ExperimentApplicationError(404, "plan_version_not_found")
    return record


async def resolve_lesson_period(
    repository: LessonPeriodReader,
    lesson_period_id: uuid.UUID,
) -> LessonPeriod | None:
    """Fetch the lesson_period row for the given id (``None`` if absent)."""
    return await repository.get_lesson_period(lesson_period_id)
