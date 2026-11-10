"""Persistence roles participating in investigation commands."""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable, Sequence
from typing import Protocol, TypeVar

from app.domains.experiments.application.lesson_conclusions import LessonConclusions

InvestigationRecord = TypeVar("InvestigationRecord")
InvestigationExperimentRecord = TypeVar("InvestigationExperimentRecord")


class InvestigationWrites(Protocol[InvestigationRecord, InvestigationExperimentRecord]):
    """Reads and staged writes needed by investigation commands."""

    async def next_investigation_code_sequence(self) -> int: ...

    async def stage_investigation(
        self,
        investigation: InvestigationRecord,
    ) -> InvestigationRecord: ...

    async def get_investigation(
        self,
        investigation_id: str,
    ) -> InvestigationRecord | None: ...

    async def list_experiments_for_investigation(
        self,
        investigation_db_id: uuid.UUID,
    ) -> Sequence[InvestigationExperimentRecord]: ...

    async def stage_experiments(
        self,
        experiments: Sequence[InvestigationExperimentRecord],
    ) -> None: ...


class InvestigationStore(Protocol[InvestigationRecord, InvestigationExperimentRecord]):
    """One atomic investigation command over a session-bound adapter."""

    @property
    def investigations(
        self,
    ) -> InvestigationWrites[InvestigationRecord, InvestigationExperimentRecord]: ...

    @property
    def lesson_conclusions(self) -> LessonConclusions: ...

    async def commit_unique_investigation(
        self,
        build: Callable[[], Awaitable[InvestigationRecord]],
    ) -> InvestigationRecord: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
