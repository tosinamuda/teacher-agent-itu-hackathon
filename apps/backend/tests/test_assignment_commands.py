"""Unit-of-work contracts for evaluation assignment commands."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

import pytest

from app.domains.evaluation.application.assignment_commands import (
    HYPOTHESIS_AUDIT,
    HYPOTHESIS_H1,
    HYPOTHESIS_H2,
    assign_audit,
    assign_experiment_bundle,
    assign_h1,
    assign_h2,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.domain.records import AssignmentRecord, RaterIdentity
from app.domains.experiments.application.evaluation_scope import (
    EvaluationBundleScope,
    EvaluationExperimentScope,
    EvaluationFocalCaseScope,
)
from app.shared.time import utc_now


@dataclass
class _AssignmentStore:
    experiment: EvaluationExperimentScope
    raters: dict[str, RaterIdentity]
    focal_case_ids: tuple[str, ...] = ("EFC-1",)
    audit_item_ids: tuple[str, ...] = ("SGA-1",)
    execution_ids: tuple[uuid.UUID, ...] = (uuid.UUID(int=42),)
    committed: list[AssignmentRecord] = field(default_factory=list)
    pending: list[AssignmentRecord] = field(default_factory=list)
    commits: int = 0
    rollbacks: int = 0
    locks: int = 0

    @property
    def assignments(self) -> _AssignmentStore:
        return self

    @property
    def assignment_scopes(self) -> _AssignmentStore:
        return self

    async def evaluation_scope(self, *, experiment_id: str) -> EvaluationExperimentScope | None:
        return self.experiment if experiment_id == self.experiment.experiment_id else None

    async def evaluation_scope_for_execution(
        self, *, execution_id: uuid.UUID
    ) -> EvaluationExperimentScope | None:
        return self.experiment if execution_id in self.execution_ids else None

    async def lock_evaluation_scope(self, *, experiment_db_id: uuid.UUID) -> None:
        assert experiment_db_id == self.experiment.id
        self.locks += 1

    async def lesson_period_exists(self, *, lesson_period_id: uuid.UUID) -> bool:
        return False

    async def focal_case_belongs_to_experiment(
        self, *, experiment_db_id: uuid.UUID, focal_case_id: str
    ) -> bool:
        return experiment_db_id == self.experiment.id and focal_case_id in self.focal_case_ids

    async def evaluation_bundle_scope(self, *, experiment_id: str) -> EvaluationBundleScope | None:
        if experiment_id != self.experiment.experiment_id:
            return None
        return EvaluationBundleScope(
            experiment=self.experiment,
            execution_ids=self.execution_ids,
            focal_cases=tuple(
                EvaluationFocalCaseScope(
                    focal_case_id=focal_id,
                    student_id=f"student-{index}",
                    focal_case_type="target",
                )
                for index, focal_id in enumerate(self.focal_case_ids)
            ),
        )

    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None:
        return self.raters.get(rater_id)

    async def assignment_record(
        self,
        *,
        experiment_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
    ) -> AssignmentRecord | None:
        return next(
            (
                row
                for row in [*self.committed, *self.pending]
                if row.experiment_db_id == experiment_db_id
                and row.rater_db_id == rater_db_id
                and row.hypothesis == hypothesis
                and row.scope_id == scope_id
            ),
            None,
        )

    async def assignment_count(
        self,
        *,
        experiment_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
        exclude_adjudicators: bool = False,
        adjudicators_only: bool = False,
    ) -> int:
        return sum(
            row.experiment_db_id == experiment_db_id
            and row.hypothesis == hypothesis
            and row.scope_id == scope_id
            and (not exclude_adjudicators or not row.is_adjudicator)
            and (not adjudicators_only or row.is_adjudicator)
            for row in [*self.committed, *self.pending]
        )

    async def stage_assignment_record(self, assignment: AssignmentRecord) -> AssignmentRecord:
        self.pending.append(assignment)
        return assignment

    async def audit_assignment_target(self, *, audit_item_id: str) -> uuid.UUID | None:
        return self.execution_ids[0] if audit_item_id in self.audit_item_ids else None

    async def audit_item_ids_for_executions(
        self, *, execution_ids: tuple[uuid.UUID, ...]
    ) -> tuple[str, ...]:
        return self.audit_item_ids if execution_ids == self.execution_ids else ()

    async def commit(self) -> None:
        self.committed.extend(self.pending)
        self.pending.clear()
        self.commits += 1

    async def rollback(self) -> None:
        self.pending.clear()
        self.rollbacks += 1


def _rater(index: int) -> RaterIdentity:
    now = utc_now()
    return RaterIdentity(
        id=uuid.UUID(int=100 + index),
        rater_id=f"EVR-{index}",
        display_name=f"Rater {index}",
        user_id=None,
        created_at=now,
        updated_at=now,
    )


def _store(*, focal_case_ids: tuple[str, ...] = ("EFC-1",)) -> _AssignmentStore:
    raters = {_rater(index).rater_id: _rater(index) for index in range(1, 6)}
    return _AssignmentStore(
        experiment=EvaluationExperimentScope(
            id=uuid.UUID(int=1),
            experiment_id="EXP-1",
            lesson_period_id=uuid.UUID(int=99),
        ),
        raters=raters,
        focal_case_ids=focal_case_ids,
    )


def _committed_assignment(
    store: _AssignmentStore,
    *,
    rater_index: int,
    hypothesis: str,
    scope_id: str,
    is_adjudicator: bool = False,
) -> None:
    store.committed.append(
        AssignmentRecord(
            id=uuid.uuid4(),
            assignment_id=f"RAS-{len(store.committed) + 1}",
            experiment_db_id=store.experiment.id,
            rater_db_id=store.raters[f"EVR-{rater_index}"].id,
            hypothesis=hypothesis,
            scope_id=scope_id,
            is_adjudicator=is_adjudicator,
            assigned_by="researcher",
            created_at=utc_now(),
        )
    )


@pytest.mark.asyncio
async def test_h1_stages_and_commits_exactly_once() -> None:
    store = _store()
    result = await assign_h1(
        store,
        experiment_id="EXP-1",
        rater_id="EVR-1",
        lesson_period_id=uuid.UUID(int=99),
        assigned_by="researcher",
    )
    assert result.hypothesis == HYPOTHESIS_H1
    assert len(store.committed) == 1
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_h1_is_idempotent_and_still_finishes_its_transaction() -> None:
    store = _store()
    first = await assign_h1(
        store,
        experiment_id="EXP-1",
        rater_id="EVR-1",
        lesson_period_id=uuid.UUID(int=99),
        assigned_by="researcher",
    )
    second = await assign_h1(
        store,
        experiment_id="EXP-1",
        rater_id="EVR-1",
        lesson_period_id=uuid.UUID(int=99),
        assigned_by="researcher",
    )
    assert first.assignment_id == second.assignment_id
    assert len(store.committed) == 1
    assert store.commits == 2


@pytest.mark.asyncio
async def test_h1_cap_rolls_back_without_staging() -> None:
    store = _store()
    scope_id = str(uuid.UUID(int=99))
    for index in range(1, 4):
        _committed_assignment(store, rater_index=index, hypothesis=HYPOTHESIS_H1, scope_id=scope_id)
    with pytest.raises(EvaluationApplicationError, match="max 3 raters"):
        await assign_h1(
            store,
            experiment_id="EXP-1",
            rater_id="EVR-4",
            lesson_period_id=uuid.UUID(int=99),
            assigned_by="researcher",
        )
    assert len(store.committed) == 3
    assert store.commits == 0
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_h2_cap_is_scoped_to_one_focal_case() -> None:
    store = _store()
    for index in range(1, 4):
        _committed_assignment(store, rater_index=index, hypothesis=HYPOTHESIS_H2, scope_id="EFC-1")
    with pytest.raises(EvaluationApplicationError, match="max 3 raters"):
        await assign_h2(
            store,
            experiment_id="EXP-1",
            rater_id="EVR-4",
            focal_case_id="EFC-1",
            assigned_by="researcher",
        )
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_audit_primary_and_adjudicator_caps_are_independent() -> None:
    store = _store()
    _committed_assignment(store, rater_index=1, hypothesis=HYPOTHESIS_AUDIT, scope_id="SGA-1")
    _committed_assignment(store, rater_index=2, hypothesis=HYPOTHESIS_AUDIT, scope_id="SGA-1")
    adjudicator = await assign_audit(
        store,
        audit_item_id="SGA-1",
        rater_id="EVR-3",
        is_adjudicator=True,
        assigned_by="researcher",
    )
    assert adjudicator.is_adjudicator is True
    with pytest.raises(EvaluationApplicationError, match="adjudicator"):
        await assign_audit(
            store,
            audit_item_id="SGA-1",
            rater_id="EVR-4",
            is_adjudicator=True,
            assigned_by="researcher",
        )
    assert store.commits == 1
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_bundle_locks_once_and_commits_all_assignments_once() -> None:
    store = _store(focal_case_ids=("EFC-1", "EFC-2"))
    result = await assign_experiment_bundle(
        store,
        experiment_id="EXP-1",
        rater_id="EVR-1",
        include_audit=True,
        assigned_by="researcher",
    )
    assert (result.h1, result.h2, result.audit) == (1, 2, 1)
    assert [row.hypothesis for row in store.committed] == [
        HYPOTHESIS_H1,
        HYPOTHESIS_H2,
        HYPOTHESIS_H2,
        HYPOTHESIS_AUDIT,
    ]
    assert store.locks == 1
    assert store.commits == 1


@pytest.mark.asyncio
async def test_bundle_cap_failure_rolls_back_every_staged_assignment() -> None:
    store = _store(focal_case_ids=("EFC-1", "EFC-2"))
    for index in range(1, 4):
        _committed_assignment(store, rater_index=index, hypothesis=HYPOTHESIS_H2, scope_id="EFC-2")
    baseline = list(store.committed)
    with pytest.raises(EvaluationApplicationError, match="max 3 raters"):
        await assign_experiment_bundle(
            store,
            experiment_id="EXP-1",
            rater_id="EVR-4",
            include_audit=True,
            assigned_by="researcher",
        )
    assert store.committed == baseline
    assert store.pending == []
    assert store.commits == 0
    assert store.rollbacks == 1
