"""Read-only assignment views for the admin picker and rater queue."""

from __future__ import annotations

from dataclasses import dataclass

from app.domains.evaluation.application.assignment_ports import (
    AssignmentViewData,
    ExperimentAssignmentScopes,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.peer_ports import LearnerNamesPort
from app.domains.evaluation.domain.records import RaterIdentity
from app.domains.evaluation.infrastructure.models import RaterAssignment

HYPOTHESIS_H1 = "H1"
HYPOTHESIS_H2 = "H2"
HYPOTHESIS_AUDIT = "audit"

_H1_MAX_RATERS_PER_LESSON = 3
_H2_MAX_RATERS_PER_FOCAL_CASE = 3
_AUDIT_MAX_RATERS_PER_ITEM = 2
_AUDIT_MAX_ADJUDICATORS_PER_ITEM = 1


@dataclass(frozen=True)
class MyQueueLine:
    """One assignment as the rater sees it in their queue."""

    assignment_id: str
    hypothesis: str
    scope_id: str
    is_adjudicator: bool


@dataclass(frozen=True)
class MyQueue:
    """An actor-rater's assignments grouped by hypothesis (drives the rater landing)."""

    rater_id: str
    h1: list[MyQueueLine]
    h2: list[MyQueueLine]
    audit: list[MyQueueLine]


@dataclass(frozen=True)
class AssignedRater:
    """One rater holding one slot."""

    assignment_id: str
    rater_id: str
    display_name: str
    is_adjudicator: bool


@dataclass(frozen=True)
class H1AssignmentSlot:
    lesson_period_id: str
    lesson_title: str | None
    raters: list[AssignedRater]
    capacity: int


@dataclass(frozen=True)
class H2AssignmentSlot:
    focal_case_id: str
    student_id: str
    student_full_name: str | None
    focal_case_type: str
    raters: list[AssignedRater]
    capacity: int


@dataclass(frozen=True)
class AuditAssignmentSlot:
    audit_item_id: str
    raters: list[AssignedRater]
    adjudicators: list[AssignedRater]
    capacity: int
    adjudicator_capacity: int


@dataclass(frozen=True)
class ExperimentAssignments:
    """Every assignment slot for one experiment + capacity hints, ready for the picker."""

    experiment_id: str
    h1: H1AssignmentSlot | None
    h2: list[H2AssignmentSlot]
    audit: list[AuditAssignmentSlot]


class AssignmentViewPresenter:
    """Assemble read-only assignment views from narrow collaborators."""

    def __init__(
        self,
        repository: AssignmentViewData,
        *,
        assignment_scopes: ExperimentAssignmentScopes,
        learner_repository: LearnerNamesPort,
    ) -> None:
        self.repository = repository
        self.assignment_scopes = assignment_scopes
        self.learner_repository = learner_repository

    # ---------- reads ----------

    async def experiment_assignments(self, *, experiment_id: str) -> ExperimentAssignments:
        """Every slot for one experiment, with raters and capacity counts.

        The H1 slot is single (one lesson per experiment). H2 slots come from
        every focal case across the experiment's executions; audit slots come
        from every audit item. Existing assignments are joined to each slot so
        the picker can render "Rater 1 / 2 / 3 of 3" inline.
        """
        bundle = await self.assignment_scopes.evaluation_bundle_scope(experiment_id=experiment_id)
        if bundle is None:
            raise EvaluationApplicationError(404, "experiment_not_found")
        experiment = bundle.experiment
        audit_items = await self.repository.list_audit_items_for_executions(
            execution_db_ids=list(bundle.execution_ids)
        )

        assignments = await self.repository.list_assignments_for_experiment(
            experiment_db_id=experiment.id
        )
        # Cheap rater hydration — pull all raters once, dict by id.
        raters_by_db_id = {
            rater.id: rater for rater in await self.repository.list_rater_identities()
        }

        def _hydrate(row: RaterAssignment) -> AssignedRater:
            rater = raters_by_db_id.get(row.rater_db_id)
            return AssignedRater(
                assignment_id=row.assignment_id,
                rater_id=rater.rater_id if rater else "",
                display_name=rater.display_name if rater else "(unknown)",
                is_adjudicator=row.is_adjudicator,
            )

        by_scope_h1: dict[str, list[AssignedRater]] = {}
        by_scope_h2: dict[str, list[AssignedRater]] = {}
        audit_primaries: dict[str, list[AssignedRater]] = {}
        audit_adjudicators: dict[str, list[AssignedRater]] = {}
        for row in assignments:
            hydrated = _hydrate(row)
            if row.hypothesis == HYPOTHESIS_H1:
                by_scope_h1.setdefault(row.scope_id, []).append(hydrated)
            elif row.hypothesis == HYPOTHESIS_H2:
                by_scope_h2.setdefault(row.scope_id, []).append(hydrated)
            elif row.hypothesis == HYPOTHESIS_AUDIT:
                bucket = audit_adjudicators if row.is_adjudicator else audit_primaries
                bucket.setdefault(row.scope_id, []).append(hydrated)

        h1_slot: H1AssignmentSlot | None = None
        if experiment.lesson_period_id is not None:
            lesson_period_id_str = str(experiment.lesson_period_id)
            lesson_title = await self.assignment_scopes.lesson_period_title(
                lesson_period_id=experiment.lesson_period_id
            )
            h1_slot = H1AssignmentSlot(
                lesson_period_id=lesson_period_id_str,
                lesson_title=lesson_title,
                raters=by_scope_h1.get(lesson_period_id_str, []),
                capacity=_H1_MAX_RATERS_PER_LESSON,
            )

        names_by_student_id = await self.learner_repository.list_names_by_student_ids(
            {case.student_id for case in bundle.focal_cases}
        )
        h2_slots = [
            H2AssignmentSlot(
                focal_case_id=case.focal_case_id,
                student_id=case.student_id,
                student_full_name=names_by_student_id.get(case.student_id),
                focal_case_type=case.focal_case_type,
                raters=by_scope_h2.get(case.focal_case_id, []),
                capacity=_H2_MAX_RATERS_PER_FOCAL_CASE,
            )
            for case in bundle.focal_cases
        ]

        audit_slots = [
            AuditAssignmentSlot(
                audit_item_id=item.audit_item_id,
                raters=audit_primaries.get(item.audit_item_id, []),
                adjudicators=audit_adjudicators.get(item.audit_item_id, []),
                capacity=_AUDIT_MAX_RATERS_PER_ITEM,
                adjudicator_capacity=_AUDIT_MAX_ADJUDICATORS_PER_ITEM,
            )
            for item in audit_items
        ]

        return ExperimentAssignments(
            experiment_id=experiment_id,
            h1=h1_slot,
            h2=h2_slots,
            audit=audit_slots,
        )

    async def list_raters(self) -> list[RaterIdentity]:
        """Every rater profile, alphabetically — drives the admin picker."""
        return await self.repository.list_rater_identities()

    async def my_queue(self, *, rater: RaterIdentity) -> MyQueue:
        """Group a rater's assignments by hypothesis (drives the rater landing)."""
        rows = await self.repository.list_assignments_for_rater(rater_db_id=rater.id)
        h1: list[MyQueueLine] = []
        h2: list[MyQueueLine] = []
        audit: list[MyQueueLine] = []
        for row in rows:
            line = MyQueueLine(
                assignment_id=row.assignment_id,
                hypothesis=row.hypothesis,
                scope_id=row.scope_id,
                is_adjudicator=row.is_adjudicator,
            )
            if row.hypothesis == HYPOTHESIS_H1:
                h1.append(line)
            elif row.hypothesis == HYPOTHESIS_H2:
                h2.append(line)
            elif row.hypothesis == HYPOTHESIS_AUDIT:
                audit.append(line)
        return MyQueue(rater_id=rater.rater_id, h1=h1, h2=h2, audit=audit)
