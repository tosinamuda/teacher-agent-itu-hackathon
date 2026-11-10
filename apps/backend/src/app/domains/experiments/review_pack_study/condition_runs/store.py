"""Where an experiment's condition runs are kept, and who ends the write.

The unit of work that ends it lives in ``experiments/application/store.py``,
along with the two-transaction rule this write depends on.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from app.domains.experiments.application.store import ExperimentStoreFactory

from .records import CompletedConditionRun, FailedConditionRun


class ConditionRuns(Protocol):
    """The condition runs belonging to one experiment execution."""

    async def record(
        self,
        *,
        completed: Sequence[CompletedConditionRun],
        failed: Sequence[FailedConditionRun],
    ) -> None: ...


async def record_condition_runs(
    open_store: ExperimentStoreFactory,
    *,
    completed: Sequence[CompletedConditionRun],
    failed: Sequence[FailedConditionRun] = (),
) -> None:
    """Record one experiment's whole condition grid, or none of it."""
    async with open_store() as store:
        await store.condition_runs.record(completed=completed, failed=failed)
        await store.commit()
