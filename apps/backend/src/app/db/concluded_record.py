"""Refuse any flush that would change the record of a lesson whose study has concluded.

A lesson's record is its plan versions and everything made from them: their content, its
approvals and ratings, the class test's questions and the class's answers, learners'
generation jobs, and the experiments run on it with their runs, raters and ratings. Once a
plan version is concluded none of it changes, whatever route or worker tries; the writes
allowed are the conclusion itself and ending its experiment.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from sqlalchemy import inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import instance_state

from app.domains.artefacts.core.infrastructure.models import Artefact, ContentApproval
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.assessments.models import (
    ExitTicketSubmission,
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.evaluation.infrastructure.models import (
    EvaluationAuditItem,
    EvaluationAuditRating,
    EvaluationPacket,
    EvaluationRating,
    RaterAssignment,
)
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)
from app.domains.experiments.infrastructure.models import (
    C4GovernanceDecision,
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.experiments.infrastructure.study_transcript_models import StudyTranscript
from app.shared.concluded import ConcludedLessonError

#: Rows that carry the plan version they belong to.
_BY_PLAN_VERSION = (
    Artefact,
    ExitTicketItem,
    ExitTicketSubmission,
    StudentPackGeneration,
    StudyClassworkQuestion,
    StudyClassworkScript,
    StudyClassworkAnswer,
    StudyTranscript,
)


#: Rows that carry the experiment they belong to.
_BY_EXPERIMENT = (RaterAssignment, ExperimentExecution, C4GovernanceDecision)
#: Rows that carry the execution they belong to.
_BY_EXECUTION = (ExperimentFocalCase, ExperimentConditionRun, EvaluationPacket, EvaluationAuditItem)
#: Ratings, by the column naming what they rate and the row that carries its execution.
#: A row that carries the execution its ratings rate.
_RatedOwner = type[EvaluationPacket] | type[EvaluationAuditItem]

_RATED_IN_AN_EXECUTION: dict[type, tuple[str, _RatedOwner]] = {
    EvaluationRating: ("evaluation_packet_db_id", EvaluationPacket),
    EvaluationAuditRating: ("audit_item_db_id", EvaluationAuditItem),
}
#: What ending an experiment writes; ending one is allowed, as concluding a version is.
_ENDING = {"lifecycle_status", "ended_at", "ended_by"}


def _changed(row: object) -> set[str]:
    return {attr.key for attr in instance_state(row).attrs if attr.history.has_changes()}


def _only_ending(experiment: Experiment) -> bool:
    return not inspect(experiment).pending and _changed(experiment) <= _ENDING


def _only_concluding(version: PlanVersion) -> bool:
    """The one change allowed: a version still open becoming concluded."""
    history = inspect(version).attrs.concluded_at.history
    return _changed(version) == {"concluded_at"} and history.deleted in ([None], [])


def _touched(session: Session) -> Iterable[object]:
    yield from session.new
    yield from session.dirty
    yield from session.deleted


def _concluded(session: Session, plan_version_ids: set[str], plan_ids: set[str]) -> bool:
    if not plan_version_ids and not plan_ids:
        return False
    with session.no_autoflush:
        query = select(PlanVersion.version_id).where(PlanVersion.concluded_at.is_not(None))
        by_version = query.where(PlanVersion.version_id.in_(plan_version_ids))
        by_plan = query.where(PlanVersion.plan_id.in_(plan_ids))
        return (
            session.execute(by_version.limit(1)).first() is not None
            or session.execute(by_plan.limit(1)).first() is not None
        )


def _experiments_versions(
    session: Session, experiment_ids: set[object], execution_ids: set[object]
) -> set[str]:
    """The plan versions the experiments, or the experiments of the executions, were run on."""
    if not experiment_ids and not execution_ids:
        return set()
    owning = select(ExperimentExecution.experiment_db_id).where(
        ExperimentExecution.id.in_(execution_ids)
    )
    with session.no_autoflush:
        found = session.execute(
            select(Experiment.plan_version_id).where(
                or_(Experiment.id.in_(experiment_ids), Experiment.id.in_(owning))
            )
        ).scalars()
        return {version for version in found if version}


def _rated_executions(session: Session, rated: dict[_RatedOwner, set[object]]) -> set[object]:
    """The executions whose packets or audit items the touched ratings rate."""
    found: set[object] = set()
    with session.no_autoflush:
        for owner, ids in rated.items():
            found |= set(
                session.execute(select(owner.execution_db_id).where(owner.id.in_(ids))).scalars()
            )
    return found


def _artefacts_versions(session: Session, artefact_ids: set[str]) -> set[str]:
    if not artefact_ids:
        return set()
    with session.no_autoflush:
        return set(
            session.execute(
                select(Artefact.plan_version_id).where(Artefact.artefact_id.in_(artefact_ids))
            ).scalars()
        )


def _rated_or_approved(row: object) -> set[str]:
    if isinstance(row, ContentApproval | StudyCriterionScore):
        return {row.artefact_id}
    if isinstance(row, StudyComparativeJudgement):
        return {row.artefact_a_id, row.artefact_b_id}
    if isinstance(row, StudyRatingDocument):
        return {row.artefact_a_id}
    return set()


@dataclass
class _Touched:
    """What a flush touches, by the kind of id that leads back to its plan version."""

    plan_version_ids: set[str] = field(default_factory=set)
    plan_ids: set[str] = field(default_factory=set)
    artefact_ids: set[str] = field(default_factory=set)
    experiment_ids: set[object] = field(default_factory=set)
    execution_ids: set[object] = field(default_factory=set)
    rated: dict[_RatedOwner, set[object]] = field(default_factory=dict)

    def add(self, row: object) -> None:
        if not (self._lesson_row(row) or self._experiment_row(row)):
            self.artefact_ids |= _rated_or_approved(row)

    def _lesson_row(self, row: object) -> bool:
        if isinstance(row, PlanVersion):
            if not _only_concluding(row):
                # A new version of a concluded plan is a change to that plan's record too.
                self.plan_version_ids.add(row.version_id)
                self.plan_ids.add(row.plan_id)
        elif isinstance(row, _BY_PLAN_VERSION):
            if row.plan_version_id:
                self.plan_version_ids.add(row.plan_version_id)
        elif isinstance(row, LessonPlan):
            self.plan_ids.add(row.plan_id)
        else:
            return False
        return True

    def _experiment_row(self, row: object) -> bool:
        if isinstance(row, Experiment):
            if row.plan_version_id and not _only_ending(row):
                self.plan_version_ids.add(row.plan_version_id)
        elif isinstance(row, _BY_EXPERIMENT):
            self.experiment_ids.add(row.experiment_db_id)
        elif isinstance(row, _BY_EXECUTION):
            self.execution_ids.add(row.execution_db_id)
        elif type(row) in _RATED_IN_AN_EXECUTION:
            column, owner = _RATED_IN_AN_EXECUTION[type(row)]
            self.rated.setdefault(owner, set()).add(getattr(row, column))
        else:
            return False
        return True


def refuse_changes_to_concluded_lessons(session: Session) -> None:
    touched = _Touched()
    for row in _touched(session):
        touched.add(row)
    plan_version_ids = touched.plan_version_ids
    plan_version_ids |= _artefacts_versions(session, touched.artefact_ids)
    execution_ids = touched.execution_ids | _rated_executions(session, touched.rated)
    plan_version_ids |= _experiments_versions(session, touched.experiment_ids, execution_ids)
    if _concluded(session, plan_version_ids, touched.plan_ids):
        raise ConcludedLessonError


async def is_concluded(db: AsyncSession, subject_id: str) -> bool:
    """Whether a plan, a plan version or an artefact belongs to a concluded lesson.

    Asked before work that spends — a model call — so a write the guard would refuse is
    never paid for first.
    """
    owning_version = select(Artefact.plan_version_id).where(Artefact.artefact_id == subject_id)
    found = await db.execute(
        select(PlanVersion.version_id)
        .where(PlanVersion.concluded_at.is_not(None))
        .where(
            or_(
                PlanVersion.version_id == subject_id,
                PlanVersion.plan_id == subject_id,
                PlanVersion.version_id.in_(owning_version),
            )
        )
        .limit(1)
    )
    return found.first() is not None
