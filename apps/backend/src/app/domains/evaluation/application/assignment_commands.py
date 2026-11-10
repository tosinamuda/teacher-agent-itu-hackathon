"""Atomic H1, H2, audit, and experiment-bundle assignment commands."""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

from app.domains.evaluation.application.assignment_ports import AssignmentStore
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.domain.records import AssignmentRecord, RaterIdentity
from app.domains.experiments.application.evaluation_scope import EvaluationExperimentScope
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.time import utc_now

HYPOTHESIS_H1 = "H1"
HYPOTHESIS_H2 = "H2"
HYPOTHESIS_AUDIT = "audit"

_H1_CAP = 3
_H2_CAP = 3
_AUDIT_CAP = 2
_AUDIT_ADJUDICATOR_CAP = 1

_ResultT = TypeVar("_ResultT")


class AssignmentConflictError(Exception):
    """A concurrent insert won an assignment unique key."""


@dataclass(frozen=True)
class AssignmentBundleResult:
    h1: int
    h2: int
    audit: int


async def assign_h1(
    store: AssignmentStore,
    *,
    experiment_id: str,
    rater_id: str,
    lesson_period_id: uuid.UUID,
    assigned_by: str | None,
) -> AssignmentRecord:
    async def _operation() -> AssignmentRecord:
        experiment, rater = await _experiment_and_rater(store, experiment_id, rater_id)
        if experiment.lesson_period_id != lesson_period_id:
            if not await store.assignment_scopes.lesson_period_exists(
                lesson_period_id=lesson_period_id
            ):
                raise EvaluationApplicationError(404, "lesson_period_not_found")
            raise EvaluationApplicationError(409, "lesson_does_not_belong_to_experiment")
        await store.assignment_scopes.lock_evaluation_scope(experiment_db_id=experiment.id)
        return await _stage_scope(
            store,
            experiment=experiment,
            rater=rater,
            hypothesis=HYPOTHESIS_H1,
            scope_id=str(lesson_period_id),
            cap=_H1_CAP,
            cap_message="max 3 raters per lesson for H1",
            assigned_by=assigned_by,
        )

    return await _commit_command(store, _operation)


async def assign_h2(
    store: AssignmentStore,
    *,
    experiment_id: str,
    rater_id: str,
    focal_case_id: str,
    assigned_by: str | None,
) -> AssignmentRecord:
    async def _operation() -> AssignmentRecord:
        experiment, rater = await _experiment_and_rater(store, experiment_id, rater_id)
        if not await store.assignment_scopes.focal_case_belongs_to_experiment(
            experiment_db_id=experiment.id,
            focal_case_id=focal_case_id,
        ):
            raise EvaluationApplicationError(404, "focal_case_not_found_for_experiment")
        await store.assignment_scopes.lock_evaluation_scope(experiment_db_id=experiment.id)
        return await _stage_scope(
            store,
            experiment=experiment,
            rater=rater,
            hypothesis=HYPOTHESIS_H2,
            scope_id=focal_case_id,
            cap=_H2_CAP,
            cap_message="max 3 raters per focal case for H2",
            assigned_by=assigned_by,
        )

    return await _commit_command(store, _operation)


async def assign_audit(
    store: AssignmentStore,
    *,
    audit_item_id: str,
    rater_id: str,
    is_adjudicator: bool,
    assigned_by: str | None,
) -> AssignmentRecord:
    async def _operation() -> AssignmentRecord:
        execution_id = await store.assignments.audit_assignment_target(audit_item_id=audit_item_id)
        if execution_id is None:
            raise EvaluationApplicationError(404, "audit_item_not_found")
        experiment = await store.assignment_scopes.evaluation_scope_for_execution(
            execution_id=execution_id
        )
        if experiment is None:
            raise EvaluationApplicationError(409, "audit_item_experiment_missing")
        rater = await _rater(store, rater_id)
        await store.assignment_scopes.lock_evaluation_scope(experiment_db_id=experiment.id)
        return await _stage_scope(
            store,
            experiment=experiment,
            rater=rater,
            hypothesis=HYPOTHESIS_AUDIT,
            scope_id=audit_item_id,
            cap=_AUDIT_ADJUDICATOR_CAP if is_adjudicator else _AUDIT_CAP,
            cap_message=(
                "audit items already have an adjudicator"
                if is_adjudicator
                else "audit items have exactly 2 non-adjudicator raters"
            ),
            assigned_by=assigned_by,
            is_adjudicator=is_adjudicator,
            count_filter="adjudicator" if is_adjudicator else "primary",
        )

    return await _commit_command(store, _operation)


async def assign_experiment_bundle(
    store: AssignmentStore,
    *,
    experiment_id: str,
    rater_id: str,
    include_audit: bool,
    assigned_by: str | None,
) -> AssignmentBundleResult:
    async def _operation() -> AssignmentBundleResult:
        bundle = await store.assignment_scopes.evaluation_bundle_scope(experiment_id=experiment_id)
        if bundle is None:
            raise EvaluationApplicationError(404, "experiment_not_found")
        rater = await _rater(store, rater_id)
        experiment = bundle.experiment
        await store.assignment_scopes.lock_evaluation_scope(experiment_db_id=experiment.id)
        h1 = 0
        if experiment.lesson_period_id is not None:
            await _stage_scope(
                store,
                experiment=experiment,
                rater=rater,
                hypothesis=HYPOTHESIS_H1,
                scope_id=str(experiment.lesson_period_id),
                cap=_H1_CAP,
                cap_message="max 3 raters per lesson for H1",
                assigned_by=assigned_by,
            )
            h1 = 1
        for focal_case_id in bundle.focal_case_ids:
            await _stage_scope(
                store,
                experiment=experiment,
                rater=rater,
                hypothesis=HYPOTHESIS_H2,
                scope_id=focal_case_id,
                cap=_H2_CAP,
                cap_message="max 3 raters per focal case for H2",
                assigned_by=assigned_by,
            )
        audit_ids = (
            await store.assignments.audit_item_ids_for_executions(
                execution_ids=bundle.execution_ids
            )
            if include_audit
            else ()
        )
        for audit_item_id in audit_ids:
            await _stage_scope(
                store,
                experiment=experiment,
                rater=rater,
                hypothesis=HYPOTHESIS_AUDIT,
                scope_id=audit_item_id,
                cap=_AUDIT_CAP,
                cap_message="audit items have exactly 2 non-adjudicator raters",
                assigned_by=assigned_by,
                count_filter="primary",
            )
        return AssignmentBundleResult(h1=h1, h2=len(bundle.focal_case_ids), audit=len(audit_ids))

    return await _commit_command(store, _operation)


async def _stage_scope(
    store: AssignmentStore,
    *,
    experiment: EvaluationExperimentScope,
    rater: RaterIdentity,
    hypothesis: str,
    scope_id: str,
    cap: int,
    cap_message: str,
    assigned_by: str | None,
    is_adjudicator: bool = False,
    count_filter: str | None = None,
) -> AssignmentRecord:
    existing = await store.assignments.assignment_record(
        experiment_db_id=experiment.id,
        rater_db_id=rater.id,
        hypothesis=hypothesis,
        scope_id=scope_id,
    )
    if existing is not None:
        return existing
    current = await store.assignments.assignment_count(
        experiment_db_id=experiment.id,
        hypothesis=hypothesis,
        scope_id=scope_id,
        exclude_adjudicators=count_filter == "primary",
        adjudicators_only=count_filter == "adjudicator",
    )
    if current >= cap:
        raise EvaluationApplicationError(409, cap_message)
    try:
        return await store.assignments.stage_assignment_record(
            AssignmentRecord(
                id=uuid.uuid4(),
                assignment_id=new_public_id(PublicIdPrefix.RATER_ASSIGNMENT),
                experiment_db_id=experiment.id,
                rater_db_id=rater.id,
                hypothesis=hypothesis,
                scope_id=scope_id,
                is_adjudicator=is_adjudicator,
                assigned_by=assigned_by,
                created_at=utc_now(),
            )
        )
    except AssignmentConflictError as exc:
        raise EvaluationApplicationError(409, "assignment_already_created") from exc


async def _experiment_and_rater(
    store: AssignmentStore,
    experiment_id: str,
    rater_id: str,
) -> tuple[EvaluationExperimentScope, RaterIdentity]:
    experiment = await store.assignment_scopes.evaluation_scope(experiment_id=experiment_id)
    if experiment is None:
        raise EvaluationApplicationError(404, "experiment_not_found")
    return experiment, await _rater(store, rater_id)


async def _rater(store: AssignmentStore, rater_id: str) -> RaterIdentity:
    rater = await store.assignments.rater_identity(rater_id=rater_id)
    if rater is None:
        raise EvaluationApplicationError(404, "rater_not_found")
    return rater


async def _commit_command(
    store: AssignmentStore,
    operation: Callable[[], Awaitable[_ResultT]],
) -> _ResultT:
    try:
        result = await operation()
        await store.commit()
        return result
    except Exception:
        await store.rollback()
        raise
