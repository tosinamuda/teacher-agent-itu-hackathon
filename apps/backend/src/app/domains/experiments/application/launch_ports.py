"""Role capabilities for the one transaction a generation launch commits.

Launch reads an experiment's identity and history, checks the plan and freeze rules
against them, and stages one execution. That is a single unit of work, so the store
below is named for what the launch commits rather than for the experiments domain.
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from app.domains.experiments.application.launch_policy import (
    ConditionFreezeReader,
    PlanApprovalReader,
)
from app.domains.experiments.domain import Hypothesis
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.shared.json_types import JsonValue


class LaunchExperiments(Protocol):
    """Experiment identity and attempt history, read together by launch and retry."""

    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: UUID
    ) -> list[ExperimentExecution]: ...


class LaunchExecutions(Protocol):
    """The two writes that stage one uniquely numbered attempt."""

    async def next_attempt_number(
        self, *, experiment_db_id: UUID, hypothesis: Hypothesis
    ) -> int: ...

    async def stage_execution(self, execution: ExperimentExecution) -> ExperimentExecution: ...


class LaunchJobs(Protocol):
    """Queue a generation: with the launch's transaction, or as a transaction of its own."""

    def add(
        self,
        kind: str,
        *args: JsonValue,
        subject: str | None = None,
        requested_by: str | None = None,
    ) -> str: ...

    async def submit(
        self,
        kind: str,
        *args: JsonValue,
        subject: str | None = None,
        requested_by: str | None = None,
    ) -> str: ...


class ExecutionLaunchStore(Protocol):
    """One open transaction for starting a generation."""

    @property
    def experiments(self) -> LaunchExperiments: ...

    @property
    def plan_approvals(self) -> PlanApprovalReader: ...

    @property
    def condition_freezes(self) -> ConditionFreezeReader: ...

    @property
    def executions(self) -> LaunchExecutions: ...

    @property
    def jobs(self) -> LaunchJobs: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
