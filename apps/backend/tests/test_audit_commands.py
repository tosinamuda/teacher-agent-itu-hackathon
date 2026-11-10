"""Unit-of-work contracts for source-audit commands."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.evaluation.application import audit_commands
from app.domains.evaluation.application.audit_commands import (
    AuditBuildDependencies,
    AuditRatingConflictError,
    AuditRatingSubmission,
    build_audit_items,
    submit_audit_rating,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.domain.records import (
    AuditItemRecord,
    AuditRatingRecord,
    RaterIdentity,
)
from app.domains.evaluation.domain.types import AuditItemStatus
from app.shared.time import utc_now


@dataclass
class _AuditStore:
    item: AuditItemRecord
    rater: RaterIdentity
    assigned: bool = True
    existing_rating: AuditRatingRecord | None = None
    staged_ratings: list[AuditRatingRecord] = field(default_factory=list)
    staged_items: list[AuditItemRecord] = field(default_factory=list)
    existing_execution_ids: set[uuid.UUID] = field(default_factory=set)
    commits: int = 0
    rollbacks: int = 0
    conflict: bool = False

    @property
    def audit_ratings(self) -> _AuditStore:
        return self

    @property
    def audit_builds(self) -> _AuditStore:
        return self

    async def audit_item_record(self, *, audit_item_id: str) -> AuditItemRecord | None:
        return self.item if audit_item_id == self.item.audit_item_id else None

    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None:
        return self.rater if rater_id == self.rater.rater_id else None

    async def audit_item_is_assigned(self, *, audit_item_id: str, rater_db_id: uuid.UUID) -> bool:
        return self.assigned

    async def audit_rating_record(
        self, *, audit_item_db_id: uuid.UUID, rater_db_id: uuid.UUID
    ) -> AuditRatingRecord | None:
        return self.existing_rating

    async def stage_audit_rating(self, rating: AuditRatingRecord) -> AuditRatingRecord:
        if self.conflict:
            raise AuditRatingConflictError
        self.staged_ratings.append(rating)
        return rating

    async def count_audit_items_for_execution(self, *, execution_db_id: uuid.UUID) -> int:
        return int(execution_db_id in self.existing_execution_ids)

    async def stage_audit_items(
        self, items: tuple[AuditItemRecord, ...]
    ) -> tuple[AuditItemRecord, ...]:
        self.staged_items.extend(items)
        return items

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1


def _records() -> tuple[AuditItemRecord, RaterIdentity]:
    now = utc_now()
    item = AuditItemRecord(
        id=uuid.UUID(int=1),
        audit_item_id="SGA-1",
        execution_db_id=uuid.UUID(int=2),
        condition_run_id="RUN-1",
        condition_code="C2",
        lesson_id="LPV-1",
        lesson_objective_id=None,
        objective_text=None,
        generated_excerpt="generated",
        source_ref=None,
        source_record_id=None,
        source_excerpt=None,
        figure_url=None,
        figure_caption=None,
        scope_boundary=None,
        status=AuditItemStatus.READY,
        created_at=now,
        updated_at=now,
    )
    rater = RaterIdentity(
        id=uuid.UUID(int=3),
        rater_id="EVR-1",
        display_name="Rater",
        user_id=None,
        created_at=now,
        updated_at=now,
    )
    return item, rater


def _submission(*, source_relevance: int = 2) -> AuditRatingSubmission:
    return AuditRatingSubmission(
        source_relevance=source_relevance,
        support_sufficiency=2,
        faithfulness=1,
        scope_correctness=2,
        notes=None,
    )


@pytest.mark.asyncio
async def test_audit_rating_validates_then_stages_and_commits_once() -> None:
    store = _AuditStore(*_records())
    result = await submit_audit_rating(
        store,
        audit_item_id="SGA-1",
        rater_id="EVR-1",
        submission=_submission(),
    )
    assert result["source_grounding_score"] == 1.75
    assert len(store.staged_ratings) == 1
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_invalid_audit_rating_writes_nothing() -> None:
    store = _AuditStore(*_records())
    with pytest.raises(EvaluationApplicationError, match="audit_source_relevance_out_of_range"):
        await submit_audit_rating(
            store,
            audit_item_id="SGA-1",
            rater_id="EVR-1",
            submission=_submission(source_relevance=3),
        )
    assert store.staged_ratings == []
    assert store.commits == 0


@pytest.mark.asyncio
async def test_audit_rating_conflict_rolls_back() -> None:
    store = _AuditStore(*_records(), conflict=True)
    with pytest.raises(EvaluationApplicationError, match="audit_rating_already_submitted"):
        await submit_audit_rating(
            store,
            audit_item_id="SGA-1",
            rater_id="EVR-1",
            submission=_submission(),
        )
    assert store.commits == 0
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_audit_build_uses_one_transaction_per_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    item, rater = _records()
    first = uuid.UUID(int=10)
    second = uuid.UUID(int=11)
    store = _AuditStore(item, rater, existing_execution_ids={second})
    experiments = SimpleNamespace(
        get_experiment=_async_return(SimpleNamespace(id=uuid.UUID(int=20))),
        list_executions_for_experiment=_async_return(
            [
                SimpleNamespace(id=first, execution_id="EXE-1"),
                SimpleNamespace(id=second, execution_id="EXE-2"),
            ]
        ),
        lock_execution_by_public_id=_async_return(None),
    )
    context = SimpleNamespace(
        get_experiment_context=_async_return(
            SimpleNamespace(plan_version=SimpleNamespace(session_plan={}, version_id="LPV-1"))
        )
    )

    async def _items(*_args: Any, execution_id: uuid.UUID, **_kwargs: Any):
        return ((item.__class__(**{**item.__dict__, "execution_db_id": execution_id}),), 0)

    monkeypatch.setattr(audit_commands, "_audit_items_for_execution", _items)
    result = await build_audit_items(
        AuditBuildDependencies(
            store=store,
            experiments=experiments,
            experiment_context=context,
            artefacts=SimpleNamespace(),
            textbook=SimpleNamespace(),
        ),
        experiment_id="EXP-1",
    )
    assert (result.created, result.skipped_executions) == (1, 1)
    assert store.commits == 2
    assert store.rollbacks == 0
    assert [row.execution_db_id for row in store.staged_items] == [first]


def _async_return(value: Any):
    async def _call(*_args: Any, **_kwargs: Any) -> Any:
        return value

    return _call
