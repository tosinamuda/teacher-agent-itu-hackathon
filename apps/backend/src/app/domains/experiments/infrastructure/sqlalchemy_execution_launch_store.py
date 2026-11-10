"""SQLAlchemy-backed unit of work for starting one generation."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.application.launch_policy import (
    ConditionFreezeReader,
    PlanApprovalReader,
)
from app.domains.experiments.application.launch_ports import (
    LaunchExecutions,
    LaunchExperiments,
    LaunchJobs,
)
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.infra.jobs.queue import JobQueue


class SqlAlchemyExecutionLaunchStore:
    """One request-bound session exposed through the launch role capabilities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = ExperimentRepository(session)

    @property
    def experiments(self) -> LaunchExperiments:
        return self._repository

    @property
    def plan_approvals(self) -> PlanApprovalReader:
        return self._repository

    @property
    def condition_freezes(self) -> ConditionFreezeReader:
        return self._repository

    @property
    def executions(self) -> LaunchExecutions:
        return self._repository

    @property
    def jobs(self) -> LaunchJobs:
        return JobQueue(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
