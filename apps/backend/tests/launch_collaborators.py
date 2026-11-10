"""One in-memory unit of work standing in for the execution launch store.

Every capability and both transaction calls land on the same recorder, so a test can
assert what launch staged and committed, and in which order.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

from sqlalchemy.exc import IntegrityError

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.experiments.domain import Hypothesis


class FakeLaunchStore:
    """Approved plan, a fixed prior-execution list, and a recorded transaction."""

    def __init__(self, executions: list[Any] | None = None, *, conflict: bool = False) -> None:
        self._executions = executions or []
        self._conflict = conflict
        self.experiment_db_id = uuid.uuid4()
        self.events: list[str] = []
        self.staged: list[Any] = []
        self.jobs_added: list[tuple[str, tuple[Any, ...], str | None]] = []
        self.requesters: list[str | None] = []

    @property
    def experiments(self) -> FakeLaunchStore:
        return self

    @property
    def plan_approvals(self) -> FakeLaunchStore:
        return self

    @property
    def condition_freezes(self) -> FakeLaunchStore:
        return self

    @property
    def executions(self) -> FakeLaunchStore:
        return self

    @property
    def jobs(self) -> FakeLaunchStore:
        return self

    async def get_experiment(self, experiment_id: str) -> Any:
        del experiment_id
        return SimpleNamespace(id=self.experiment_db_id, plan_version_id="LPV-test")

    async def get_plan_version(self, plan_version_id: str) -> Any:
        del plan_version_id
        return SimpleNamespace(status=PlanVersionStatus.APPROVED, session_plan={})

    async def list_executions_for_experiment(self, experiment_db_id: uuid.UUID) -> list[Any]:
        del experiment_db_id
        return self._executions

    async def list_condition_runs_for_executions(self, execution_db_ids: Any) -> list[Any]:
        del execution_db_ids
        return []

    async def next_attempt_number(
        self, *, experiment_db_id: uuid.UUID, hypothesis: Hypothesis
    ) -> int:
        del experiment_db_id, hypothesis
        return 1

    async def stage_execution(self, execution: Any) -> Any:
        self.staged.append(execution)
        self.events.append("stage")
        if self._conflict:
            raise IntegrityError("INSERT", {}, RuntimeError("duplicate attempt"))
        return execution

    def add(
        self, kind: str, *args: Any, subject: str | None = None, requested_by: str | None = None
    ) -> str:
        self.jobs_added.append((kind, args, subject))
        self.requesters.append(requested_by)
        self.events.append("stage_job")
        return f"JOB-{len(self.jobs_added)}"

    async def submit(
        self, kind: str, *args: Any, subject: str | None = None, requested_by: str | None = None
    ) -> str:
        job_id = self.add(kind, *args, subject=subject, requested_by=requested_by)
        self.events.append("commit")
        return job_id

    async def commit(self) -> None:
        self.events.append("commit")

    async def rollback(self) -> None:
        self.events.append("rollback")
