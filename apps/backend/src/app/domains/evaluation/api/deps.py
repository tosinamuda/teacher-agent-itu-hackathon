"""Composition root for the evaluation HTTP surface.

Evaluation reads the experiments it evaluates, so this module — and only this
module — names both domains: it builds each application service over the same
per-request, session-bound experiment repository. Routes ask for a finished
service, so the transport layer never reaches into the experiments domain
itself (``lint-imports``: "evaluation transport+persistence do not
DIRECTLY import experiments").
"""

from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.evaluation.application.assignment_ports import AssignmentStore
from app.domains.evaluation.application.assignment_presenter import AssignmentViewPresenter
from app.domains.evaluation.application.assignment_queries import (
    AssignmentViewReader,
    MyQueueReader,
    RaterListReader,
)
from app.domains.evaluation.application.audit_commands import AuditBuildDependencies
from app.domains.evaluation.application.audit_ports import (
    AuditRatingStore,
)
from app.domains.evaluation.application.audit_presenter import AuditPresenter
from app.domains.evaluation.application.audit_queries import (
    AuditDetailReader,
    AuditExportReader,
    AuditQueueReader,
)
from app.domains.evaluation.application.blinding_queries import (
    BlindingKeyExperiments,
    BlindingKeyProjector,
)
from app.domains.evaluation.application.dataset_queries import DatasetProjector
from app.domains.evaluation.application.experiment_statistics import (
    ExperimentStatisticsDependencies,
)
from app.domains.evaluation.application.identity_ports import RaterIdentityReader
from app.domains.evaluation.application.investigation_rollup import (
    InvestigationRollupDependencies,
)
from app.domains.evaluation.application.packet_ports import (
    H1PacketDetailDependencies,
    H2PacketDetailDependencies,
    PacketQueueDependencies,
)
from app.domains.evaluation.application.peer_ports import (
    LearnerNamesPort,
    PackArtefactsPort,
    TextbookExcerptReader,
)
from app.domains.evaluation.application.rating_commands import RatingCommandDependencies
from app.domains.evaluation.application.rating_import_service import (
    RatingImportApplicationService,
)
from app.domains.evaluation.application.ratings_summary import (
    RatingsSummaryDependencies,
)
from app.domains.evaluation.application.study_ratings import StudyRatingsReader
from app.domains.evaluation.infrastructure.pack_artefacts import SqlAlchemyPackArtefacts
from app.domains.evaluation.infrastructure.repository import EvaluationRepository
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
    SqlAlchemyEvaluationStore,
)
from app.domains.evaluation.infrastructure.study_ratings import SqlAlchemyStudyRatings
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
)
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.expert_content.infrastructure.textbook_excerpt_reader import (
    SqlAlchemyTextbookExcerptReader,
)
from app.domains.learners.infrastructure.repository import LearnerRepository
from app.shared.auth import Actor, get_actor
from app.shared.authz import enforce


def experiment_repository(db: AsyncSession = Depends(get_db)) -> ExperimentRepository:
    """The experiment repository every evaluation service reads through."""
    return ExperimentRepository(db)


async def evaluation_store(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> AsyncGenerator[SqlAlchemyEvaluationStore, None]:
    """One evaluation unit of work over the request's session.

    Use cases commit their successful transactions explicitly. Any exception
    escaping the request rolls back staged work before the session closes.
    """
    store = SqlAlchemyEvaluationStore(db, assignment_scopes=experiments)
    try:
        yield store
    except BaseException:
        await store.rollback()
        raise


def rater_identity_reader(
    db: AsyncSession = Depends(get_db),
) -> RaterIdentityReader:
    return EvaluationRepository(db)


def assignment_store(
    store: SqlAlchemyEvaluationStore = Depends(evaluation_store),
) -> AssignmentStore:
    return store


async def rater_session_actor(
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> Actor:
    """Authorize rater-session creation while preserving its explicit 401."""
    if actor.teacher_id is None:
        raise HTTPException(status_code=401, detail="not_authenticated")
    await enforce(actor, obj="rater_session:*", act="create", db=db)
    return actor


def pack_artefacts(db: AsyncSession = Depends(get_db)) -> PackArtefactsPort:
    """The generated packs a rater packet points at."""
    return SqlAlchemyPackArtefacts(db)


class _BoundLearnerNames:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = LearnerRepository()

    async def list_names_by_student_ids(self, student_ids: set[str]) -> dict[str, str | None]:
        return await self._repository.list_names_by_student_ids(self._session, student_ids)


def learner_names(db: AsyncSession = Depends(get_db)) -> LearnerNamesPort:
    """The learner names an assignment lane displays."""
    return _BoundLearnerNames(db)


def experiment_context(
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentContextApplicationService:
    """The lesson/workspace context a packet is presented against."""
    return ExperimentContextApplicationService(experiments)


def packet_queue_dependencies(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
    context: ExperimentContextApplicationService = Depends(experiment_context),
    artefacts: PackArtefactsPort = Depends(pack_artefacts),
) -> PacketQueueDependencies:
    return PacketQueueDependencies(
        data=EvaluationRepository(db),
        experiments=experiments,
        context=context,
        artefacts=artefacts,
    )


def h1_packet_detail_dependencies(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
    context: ExperimentContextApplicationService = Depends(experiment_context),
    artefacts: PackArtefactsPort = Depends(pack_artefacts),
) -> H1PacketDetailDependencies:
    return H1PacketDetailDependencies(
        data=EvaluationRepository(db),
        experiments=experiments,
        context=context,
        artefacts=artefacts,
    )


def h2_packet_detail_dependencies(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
    context: ExperimentContextApplicationService = Depends(experiment_context),
    artefacts: PackArtefactsPort = Depends(pack_artefacts),
) -> H2PacketDetailDependencies:
    return H2PacketDetailDependencies(
        data=EvaluationRepository(db),
        experiments=experiments,
        context=context,
        artefacts=artefacts,
    )


def rating_command_dependencies(
    store: SqlAlchemyEvaluationStore = Depends(evaluation_store),
    experiments: ExperimentRepository = Depends(experiment_repository),
    context: ExperimentContextApplicationService = Depends(experiment_context),
    artefacts: PackArtefactsPort = Depends(pack_artefacts),
) -> RatingCommandDependencies:
    return RatingCommandDependencies(
        store=store,
        experiments=experiments,
        experiment_context=context,
        artefacts=artefacts,
    )


def textbook_excerpts(db: AsyncSession = Depends(get_db)) -> TextbookExcerptReader:
    return SqlAlchemyTextbookExcerptReader(db)


def audit_presenter(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> AuditPresenter:
    """The source-grounding audit lane."""
    return AuditPresenter(
        EvaluationRepository(db),
        experiment_repository=experiments,
    )


def audit_queue_reader(
    presenter: AuditPresenter = Depends(audit_presenter),
) -> AuditQueueReader:
    return presenter


def audit_detail_reader(
    presenter: AuditPresenter = Depends(audit_presenter),
) -> AuditDetailReader:
    return presenter


def audit_export_reader(
    presenter: AuditPresenter = Depends(audit_presenter),
) -> AuditExportReader:
    return presenter


def audit_rating_store(
    store: SqlAlchemyEvaluationStore = Depends(evaluation_store),
) -> AuditRatingStore:
    return store


def audit_build_dependencies(
    store: SqlAlchemyEvaluationStore = Depends(evaluation_store),
    experiments: ExperimentRepository = Depends(experiment_repository),
    context: ExperimentContextApplicationService = Depends(experiment_context),
    artefacts: PackArtefactsPort = Depends(pack_artefacts),
    textbook: TextbookExcerptReader = Depends(textbook_excerpts),
) -> AuditBuildDependencies:
    return AuditBuildDependencies(
        store=store,
        experiments=experiments,
        experiment_context=context,
        artefacts=artefacts,
        textbook=textbook,
    )


def ratings_summary_dependencies(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> RatingsSummaryDependencies:
    return RatingsSummaryDependencies(
        ratings=EvaluationRepository(db),
        experiments=experiments,
    )


def experiment_statistics_dependencies(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> ExperimentStatisticsDependencies:
    return ExperimentStatisticsDependencies(
        data=EvaluationRepository(db),
        experiments=experiments,
    )


def investigation_rollup_dependencies(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> InvestigationRollupDependencies:
    return InvestigationRollupDependencies(
        ratings=EvaluationRepository(db),
        experiments=experiments,
    )


def dataset_reader(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
) -> DatasetProjector:
    """The analysis-dataset export."""
    return DatasetProjector(EvaluationRepository(db), experiment_repository=experiments)


def assignment_view_presenter(
    db: AsyncSession = Depends(get_db),
    experiments: ExperimentRepository = Depends(experiment_repository),
    learners: LearnerNamesPort = Depends(learner_names),
) -> AssignmentViewPresenter:
    """Who rates what: the assignment lanes and each rater's own queue."""
    return AssignmentViewPresenter(
        EvaluationRepository(db),
        assignment_scopes=experiments,
        learner_repository=learners,
    )


def assignment_view_reader(
    presenter: AssignmentViewPresenter = Depends(assignment_view_presenter),
) -> AssignmentViewReader:
    return presenter


def rater_list_reader(
    presenter: AssignmentViewPresenter = Depends(assignment_view_presenter),
) -> RaterListReader:
    return presenter


def my_queue_reader(
    presenter: AssignmentViewPresenter = Depends(assignment_view_presenter),
) -> MyQueueReader:
    return presenter


def rating_import_service(
    store: SqlAlchemyEvaluationStore = Depends(evaluation_store),
) -> RatingImportApplicationService:
    """Offline rating sheets, replayed into the store."""
    return RatingImportApplicationService(store)


def blinding_reader(
    db: AsyncSession = Depends(get_db),
    experiments: BlindingKeyExperiments = Depends(experiment_repository),
) -> BlindingKeyProjector:
    """Server-side de-anonymisation of the blinded candidate order."""
    return BlindingKeyProjector(EvaluationRepository(db), experiment_repository=experiments)


def study_ratings_reader() -> StudyRatingsReader:
    """The study's recorded ratings; they need no experiment repository."""
    return SqlAlchemyStudyRatings()
