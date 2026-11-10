"""Persistence capabilities for experiment plan-binding commands."""

from __future__ import annotations

from typing import Protocol

from app.domains.experiments.domain.records import (
    ExperimentPlanBindingRecord,
    LessonPlanBindingRecord,
    PlanVersionBindingRecord,
)


class ExperimentAuthoringWrites(Protocol):
    """Reads and staged write needed to bind an experiment plan version."""

    async def get_experiment(
        self,
        experiment_id: str,
    ) -> ExperimentPlanBindingRecord | None: ...

    async def get_plan_version_plan(
        self,
        *,
        plan_version_id: str,
    ) -> tuple[PlanVersionBindingRecord, LessonPlanBindingRecord] | None: ...

    async def stage_plan_binding(
        self,
        experiment: ExperimentPlanBindingRecord,
    ) -> ExperimentPlanBindingRecord: ...


class ExperimentAuthoringStore(Protocol):
    """Transaction owner for binding an accepted plan version to an experiment."""

    @property
    def experiment_authoring(self) -> ExperimentAuthoringWrites: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
