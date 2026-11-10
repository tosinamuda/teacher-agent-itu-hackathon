"""Persistence capabilities for experiment administration commands."""

from __future__ import annotations

from typing import Protocol

from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextReader,
)
from app.domains.experiments.application.lesson_conclusions import LessonConclusions
from app.domains.experiments.domain.records import ExperimentAdministrationRecord


class ExperimentAdministrationWrites(Protocol):
    """Reads and staged write needed by experiment administration commands."""

    async def get_experiment(
        self,
        experiment_id: str,
    ) -> ExperimentAdministrationRecord | None: ...

    async def stage_experiment(
        self,
        experiment: ExperimentAdministrationRecord,
    ) -> ExperimentAdministrationRecord: ...


class ExperimentAdministrationStore(Protocol):
    """Transaction owner for experiment lifecycle and focal-learner changes."""

    @property
    def experiments(self) -> ExperimentAdministrationWrites: ...

    @property
    def experiment_context(self) -> ExperimentContextReader: ...

    @property
    def lesson_conclusions(self) -> LessonConclusions: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
