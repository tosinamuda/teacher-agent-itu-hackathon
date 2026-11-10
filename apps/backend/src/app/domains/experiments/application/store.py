"""The experiments unit of work: who owns a transaction, and what it holds.

A repository defines queries and owns no lifetime; a store owns the session and
ends it. Each use case sees a role-specific property rather than the repository's
full surface, so unrelated worker operations are unavailable by construction.

H1 spans two stores deliberately. Its inputs are read and committed through the
first, which is released *before* generation because generation is minutes of
model calls and must not hold a transaction open; a second is opened afterwards
to record what was produced. Opening a store is therefore the transaction
boundary, and a reader who assumes one spans both will be wrong.
"""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.domains.experiments.application.condition_recovery import (
        FailedConditionRunRecovery,
    )
    from app.domains.experiments.application.execution_lifecycle import ExecutionLifecycle
    from app.domains.experiments.application.execution_progress import ExecutionProgressReader
    from app.domains.experiments.application.focal_case_records import FocalCaseWriter
    from app.domains.experiments.application.h1_execution import H1InputReader
    from app.domains.experiments.application.h2_execution import H2InputReader
    from app.domains.experiments.review_pack_study.condition_runs.store import ConditionRuns


class ExperimentStore(Protocol):
    """One open unit of work over an experiment's records."""

    @property
    def execution_lifecycle(self) -> ExecutionLifecycle: ...

    @property
    def h1_inputs(self) -> H1InputReader: ...

    @property
    def h2_inputs(self) -> H2InputReader: ...

    @property
    def focal_cases(self) -> FocalCaseWriter: ...

    @property
    def execution_progress(self) -> ExecutionProgressReader: ...

    @property
    def condition_runs(self) -> ConditionRuns: ...

    @property
    def condition_recovery(self) -> FailedConditionRunRecovery: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class ExperimentStoreFactory(Protocol):
    """Open a fresh unit of work; nothing is written unless someone commits."""

    def __call__(self) -> AbstractAsyncContextManager[ExperimentStore]: ...
