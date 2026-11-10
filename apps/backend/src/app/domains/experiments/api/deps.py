"""Composition root for the experiments HTTP surface.

One repository per request, bound to the session FastAPI already opened. Routes
inject it rather than constructing one, so nothing below the route decides for
itself which session it runs in.
"""

from collections.abc import Awaitable, Callable
from functools import partial

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.evaluation.api.deps import experiment_statistics_dependencies
from app.domains.evaluation.application.experiment_statistics import (
    ExperimentStatisticsDependencies,
    experiment_statistics,
)
from app.domains.evaluation.application.result_schemas import ExperimentStatistics
from app.domains.experiments.application.authorization import ExperimentAccessReader
from app.domains.experiments.application.execution_launch import LaunchExecution
from app.domains.experiments.application.experiment_administration_store import (
    ExperimentAdministrationStore,
)
from app.domains.experiments.application.experiment_authoring_store import (
    ExperimentAuthoringStore,
)
from app.domains.experiments.application.experiment_context_service import (
    ExperimentWorkspaceCatalogueReader,
)
from app.domains.experiments.application.experiment_plan_reuse import ExperimentPlanReuse
from app.domains.experiments.application.experiment_story_service import (
    ExperimentStoryApplicationService,
)
from app.domains.experiments.application.experiment_views import (
    ExperimentExecutionViewQuery,
    ExperimentExecutionViewReader,
    ExperimentListQuery,
    ExperimentViewQuery,
    SyntheticStudentContextQuery,
)
from app.domains.experiments.application.investigation_service import InvestigationQueryReader
from app.domains.experiments.application.investigation_store import InvestigationStore
from app.domains.experiments.application.launch_ports import (
    ExecutionLaunchStore,
)
from app.domains.experiments.application.lookups import ExecutionIdentityReader
from app.domains.experiments.application.packet_export_store import PacketExportStore
from app.domains.experiments.application.service import ExperimentApplicationQueries
from app.domains.experiments.application.study_record import StudyRecordQuery
from app.domains.experiments.application.workflow_query import ExperimentWorkflowQuery
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.experiments.infrastructure.sqlalchemy_execution_launch_store import (
    SqlAlchemyExecutionLaunchStore,
)
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)
from app.domains.experiments.infrastructure.study_record import SqlAlchemyStudyRecord


def experiment_repository(db: AsyncSession = Depends(get_db)) -> ExperimentRepository:
    """The repository every experiments route reads and writes through."""
    return ExperimentRepository(db)


def experiment_access_reader(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentAccessReader:
    """Expose only experiment authorization reads to HTTP handlers."""
    return repository


def experiment_workspace_catalogue_reader(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentWorkspaceCatalogueReader:
    """Expose only workspace and lesson option reads to catalogue handlers."""
    return repository


def investigation_query_reader(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> InvestigationQueryReader:
    """Expose only investigation list/detail reads to HTTP handlers."""
    return repository


def experiment_view_query(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentViewQuery:
    """Compose the experiment header/detail read model from narrow roles."""
    return ExperimentViewQuery(repository, repository, repository)


def experiment_list_query(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentListQuery:
    """Compose the batched dashboard-list query from its four read roles."""
    return ExperimentListQuery(repository, repository, repository, repository)


def experiment_execution_view_query(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentExecutionViewQuery:
    """Compose the execution-detail read model."""
    return ExperimentExecutionViewQuery(repository)


def synthetic_student_context_query(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> SyntheticStudentContextQuery:
    """Compose the synthetic-student launch precondition query."""
    return SyntheticStudentContextQuery(repository, repository)


def experiment_application_queries(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentApplicationQueries:
    """Expose setup-command reads without giving routes the concrete adapter."""
    return repository


def execution_launch_store(
    db: AsyncSession = Depends(get_db),
) -> ExecutionLaunchStore:
    """The one transaction a launch reads its preconditions in and commits QUEUED to."""
    return SqlAlchemyExecutionLaunchStore(db)


def launch_execution(
    store: ExecutionLaunchStore = Depends(execution_launch_store),
) -> LaunchExecution:
    """The finished launch operation; HTTP, worker and CLI all receive this."""
    return LaunchExecution(store)


def experiment_execution_view_reader(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentExecutionViewReader:
    return repository


def experiment_story_query(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentStoryApplicationService:
    return ExperimentStoryApplicationService(repository, repository)


def execution_identity_reader(
    repository: ExperimentRepository = Depends(experiment_repository),
) -> ExecutionIdentityReader:
    return repository


def packet_export_store(db: AsyncSession = Depends(get_db)) -> PacketExportStore:
    """Bind one request's packet-export transaction to its database session."""
    return SqlAlchemyExperimentStore(db)


def investigation_store(db: AsyncSession = Depends(get_db)) -> InvestigationStore:
    """Bind one request's investigation command to its database session."""
    return SqlAlchemyExperimentStore(db)


def experiment_administration_store(
    db: AsyncSession = Depends(get_db),
) -> ExperimentAdministrationStore:
    """Bind one experiment administration command to its request session."""
    return SqlAlchemyExperimentStore(db)


def experiment_authoring_store(
    db: AsyncSession = Depends(get_db),
) -> ExperimentAuthoringStore:
    """Bind one experiment plan-binding command to its request session."""
    return SqlAlchemyExperimentStore(db)


def experiment_plan_reuse(
    db: AsyncSession = Depends(get_db),
    queries: ExperimentApplicationQueries = Depends(experiment_application_queries),
    store: ExperimentAuthoringStore = Depends(experiment_authoring_store),
) -> ExperimentPlanReuse:
    """Reuse an existing plan as an experiment's plan, in the request's transaction."""
    return ExperimentPlanReuse(db, queries, store)


def statistics_query(
    dependencies: ExperimentStatisticsDependencies = Depends(experiment_statistics_dependencies),
) -> Callable[[str], Awaitable[ExperimentStatistics]]:
    return partial(experiment_statistics, dependencies)


def experiment_workflow_query(
    access: ExperimentAccessReader = Depends(experiment_access_reader),
    experiment_view: ExperimentViewQuery = Depends(experiment_view_query),
    statistics: Callable[[str], Awaitable[ExperimentStatistics]] = Depends(statistics_query),
) -> ExperimentWorkflowQuery:
    """The workflow snapshot, which reads an experiment's detail and its ratings.

    The one place the experiments surface names evaluation: the snapshot spans
    both, so the composition happens here rather than inside the use case.
    """
    return ExperimentWorkflowQuery(access, experiment_view.build_detail, statistics)


def study_record_query(
    db: AsyncSession = Depends(get_db),
    repository: ExperimentRepository = Depends(experiment_repository),
) -> StudyRecordQuery:
    """An experiment's record: provenance, rater schedule and the study's ratings."""
    return StudyRecordQuery(repository, SqlAlchemyStudyRecord(db))
