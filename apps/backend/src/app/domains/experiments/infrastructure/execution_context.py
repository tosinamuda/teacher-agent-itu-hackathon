"""What one worker attempt runs against: its unit of work, and the sources it reads.

The composition root for conditioned generation. An attempt needs two
collaborators over the same session — the experiments unit of work, and the
textbook passages its lesson cites — so they are bound together and released
together. Above this module nothing names a session, a repository, or an
adapter; below it nothing decides when a transaction ends.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.domains.experiments.application.condition_recovery import FailedConditionRunRecovery
from app.domains.experiments.application.store import ExperimentStore
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)
from app.domains.expert_content.application.excerpt_resolver import SqlAlchemyExcerpts
from app.domains.expert_content.application.excerpts_port import ExcerptsPort


@dataclass(frozen=True)
class ExecutionContext:
    """The collaborators one execution is conducted through."""

    store: ExperimentStore
    excerpts: ExcerptsPort


@dataclass(frozen=True)
class ConditionRetryContext:
    """The collaborators one condition retry is conducted through."""

    store: ExperimentStore
    excerpts: ExcerptsPort
    condition_runs: FailedConditionRunRecovery


def bind_execution_context(session: AsyncSession) -> ExecutionContext:
    """Bind an attempt's collaborators to a session someone else owns."""
    return ExecutionContext(
        store=SqlAlchemyExperimentStore(session),
        excerpts=SqlAlchemyExcerpts(session),
    )


def bind_condition_retry_context(session: AsyncSession) -> ConditionRetryContext:
    """Bind a retry's collaborators, recovery included, to one session."""
    store = SqlAlchemyExperimentStore(session)
    return ConditionRetryContext(
        store=store,
        excerpts=SqlAlchemyExcerpts(session),
        condition_runs=store.condition_recovery,
    )


@asynccontextmanager
async def open_execution_context(
    sessions: Callable[[], AsyncSession] = AsyncSessionLocal,
) -> AsyncGenerator[ExecutionContext]:
    """Open one attempt's collaborators: roll back on error, and never auto-commit."""
    async with sessions() as session:
        context = bind_execution_context(session)
        try:
            yield context
        except BaseException:
            await context.store.rollback()
            raise


@asynccontextmanager
async def open_condition_retry_context(
    sessions: Callable[[], AsyncSession] = AsyncSessionLocal,
) -> AsyncGenerator[ConditionRetryContext]:
    """Open one retry's collaborators: roll back on error, and never auto-commit."""
    async with sessions() as session:
        context = bind_condition_retry_context(session)
        try:
            yield context
        except BaseException:
            await context.store.rollback()
            raise
