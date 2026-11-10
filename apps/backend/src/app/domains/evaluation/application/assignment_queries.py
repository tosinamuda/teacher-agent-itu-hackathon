"""Named read-only assignment and rater-queue queries."""

from __future__ import annotations

from typing import Protocol

from app.domains.evaluation.application.assignment_presenter import (
    ExperimentAssignments,
    MyQueue,
)
from app.domains.evaluation.domain.records import RaterIdentity


class AssignmentViewReader(Protocol):
    async def experiment_assignments(self, *, experiment_id: str) -> ExperimentAssignments: ...


class RaterListReader(Protocol):
    async def list_raters(self) -> list[RaterIdentity]: ...


class MyQueueReader(Protocol):
    async def my_queue(self, *, rater: RaterIdentity) -> MyQueue: ...


async def experiment_assignment_view(
    reader: AssignmentViewReader,
    *,
    experiment_id: str,
) -> ExperimentAssignments:
    return await reader.experiment_assignments(experiment_id=experiment_id)


async def list_raters(reader: RaterListReader) -> list[RaterIdentity]:
    return await reader.list_raters()


async def my_assignment_queue(reader: MyQueueReader, *, rater: RaterIdentity) -> MyQueue:
    return await reader.my_queue(rater=rater)
