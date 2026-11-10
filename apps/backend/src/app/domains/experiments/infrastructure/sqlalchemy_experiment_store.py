"""Open short-lived SQLAlchemy units of work for one condition-run batch.

The composition root for the experiments store is the one experiment module
that names the product-owned artefact writer. The experiment adapter itself
supplies only condition-run persistence.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.retry import commit_with_unique_retry
from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.post_class_review_pack.infrastructure.condition_run_artefact import (  # noqa: E501
    SqlAlchemyReviewPackArtefactWriter,
)
from app.domains.experiments.application.store import ExperimentStoreFactory
from app.domains.experiments.infrastructure.lesson_conclusions import SqlAlchemyLessonConclusions
from app.domains.experiments.infrastructure.models import Investigation
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.experiments.infrastructure.sqlalchemy_condition_runs import (
    SqlAlchemyConditionRuns,
)


class SqlAlchemyExperimentStore:
    """One SQLAlchemy session, exposed as an experiment unit of work."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._experiments = ExperimentRepository(session)
        self._condition_runs = SqlAlchemyConditionRuns(
            session,
            SqlAlchemyReviewPackArtefactWriter(session),
        )

    # HTTP command roles
    @property
    def experiments(self) -> ExperimentRepository:
        return self._experiments

    @property
    def experiment_context(self) -> ExperimentRepository:
        return self._experiments

    @property
    def experiment_authoring(self) -> ExperimentRepository:
        return self._experiments

    @property
    def packet_exports(self) -> ExperimentRepository:
        return self._experiments

    @property
    def investigations(self) -> ExperimentRepository:
        return self._experiments

    @property
    def lesson_conclusions(self) -> SqlAlchemyLessonConclusions:
        return SqlAlchemyLessonConclusions(self._session)

    # Conditioned-execution worker roles
    @property
    def execution_lifecycle(self) -> ExperimentRepository:
        return self._experiments

    @property
    def h1_inputs(self) -> ExperimentRepository:
        return self._experiments

    @property
    def h2_inputs(self) -> ExperimentRepository:
        return self._experiments

    @property
    def focal_cases(self) -> ExperimentRepository:
        return self._experiments

    @property
    def execution_progress(self) -> ExperimentRepository:
        return self._experiments

    @property
    def condition_runs(self) -> SqlAlchemyConditionRuns:
        return self._condition_runs

    @property
    def condition_recovery(self) -> SqlAlchemyConditionRuns:
        return self._condition_runs

    async def commit(self) -> None:
        await self._session.commit()

    async def commit_unique_investigation(
        self,
        build: Callable[[], Awaitable[Investigation]],
    ) -> Investigation:
        return await commit_with_unique_retry(
            self._session,
            build,
            conflict_token="investigation_code",
        )

    async def rollback(self) -> None:
        await self._session.rollback()


@asynccontextmanager
async def open_experiment_store(
    sessions: Callable[[], AsyncSession] = AsyncSessionLocal,
) -> AsyncGenerator[SqlAlchemyExperimentStore]:
    """Open one session for a batch: roll back on error, and never auto-commit."""
    async with sessions() as session:
        store = SqlAlchemyExperimentStore(session)
        try:
            yield store
        except BaseException:
            await store.rollback()
            raise


_conforms: ExperimentStoreFactory = open_experiment_store
