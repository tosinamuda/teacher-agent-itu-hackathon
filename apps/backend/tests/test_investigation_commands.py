"""Transaction contracts for investigation commands."""

from __future__ import annotations

import inspect
import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.experiments.application.investigation_service import (
    create_investigation,
    end_investigation,
)
from app.domains.experiments.domain.types import (
    ExperimentLifecycleStatus,
    InvestigationStatus,
)


class _Investigations:
    def __init__(self, *, fail_experiment_stage: bool = False) -> None:
        self.sequence = 1
        self.investigation = SimpleNamespace(
            id=uuid.uuid4(),
            investigation_id="INV-1",
            status=InvestigationStatus.ACTIVE,
            ended_at=None,
            ended_by=None,
        )
        self.experiments = [
            SimpleNamespace(
                plan_version_id="PLAN-ACTIVE",
                lifecycle_status=ExperimentLifecycleStatus.ACTIVE,
                ended_at=None,
                ended_by=None,
            ),
            SimpleNamespace(
                plan_version_id="PLAN-ENDED-EARLIER",
                lifecycle_status=ExperimentLifecycleStatus.ENDED,
                ended_at="already-ended",
                ended_by="other",
            ),
        ]
        self.staged_investigations: list[Any] = []
        self.staged_experiment_batches: list[list[Any]] = []
        self.fail_experiment_stage = fail_experiment_stage

    async def next_investigation_code_sequence(self) -> int:
        return self.sequence

    async def stage_investigation(self, investigation: Any) -> Any:
        self.staged_investigations.append(investigation)
        return investigation

    async def get_investigation(self, investigation_id: str) -> Any:
        return self.investigation if investigation_id == "INV-1" else None

    async def list_experiments_for_investigation(self, investigation_db_id: uuid.UUID) -> list[Any]:
        return self.experiments

    async def stage_experiments(self, experiments: list[Any]) -> None:
        self.staged_experiment_batches.append(experiments)
        if self.fail_experiment_stage:
            raise RuntimeError("experiment stage failed")


class _LessonConclusions:
    def __init__(self) -> None:
        self.requested: list[set[str]] = []

    async def conclude_where_no_experiment_is_active(self, plan_version_ids: Any) -> None:
        self.requested.append(set(plan_version_ids))


class _InvestigationStore:
    def __init__(self, *, fail_experiment_stage: bool = False) -> None:
        self.investigations = _Investigations(fail_experiment_stage=fail_experiment_stage)
        self.lesson_conclusions = _LessonConclusions()
        self.commits = 0
        self.rollbacks = 0
        self._original_investigation = self._investigation_state()
        self._original_experiments = self._experiment_states()

    def _investigation_state(self) -> tuple[Any, Any, Any]:
        investigation = self.investigations.investigation
        return investigation.status, investigation.ended_at, investigation.ended_by

    def _experiment_states(self) -> list[tuple[Any, Any, Any]]:
        return [
            (experiment.lifecycle_status, experiment.ended_at, experiment.ended_by)
            for experiment in self.investigations.experiments
        ]

    async def commit_unique_investigation(self, build: Any) -> Any:
        investigation = await build()
        self.commits += 1
        return investigation

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1
        investigation = self.investigations.investigation
        investigation.status, investigation.ended_at, investigation.ended_by = (
            self._original_investigation
        )
        for experiment, state in zip(
            self.investigations.experiments,
            self._original_experiments,
            strict=True,
        ):
            experiment.lifecycle_status, experiment.ended_at, experiment.ended_by = state


def test_investigation_commands_receive_no_raw_session() -> None:
    assert "db" not in inspect.signature(create_investigation).parameters
    assert "db" not in inspect.signature(end_investigation).parameters


@pytest.mark.asyncio
async def test_creating_investigation_delegates_unique_code_commit_to_store() -> None:
    store = _InvestigationStore()

    result = await create_investigation(
        store,  # type: ignore[arg-type]
        title="  Trial study  ",
        description="  comparison  ",
    )

    assert result.investigation_code == "INV-0001"
    assert result.title == "Trial study"
    assert result.description == "comparison"
    assert store.investigations.staged_investigations == [result]
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_ending_investigation_stages_complete_cascade_then_commits_once() -> None:
    store = _InvestigationStore()

    result = await end_investigation(
        store,  # type: ignore[arg-type]
        investigation_id="INV-1",
        ended_by="researcher",
    )

    assert result.status == InvestigationStatus.ENDED
    assert store.commits == 1
    assert store.rollbacks == 0
    assert store.investigations.staged_investigations == [result]
    staged_experiments = store.investigations.staged_experiment_batches[0]
    assert staged_experiments == [store.investigations.experiments[0]]
    assert staged_experiments[0].lifecycle_status == ExperimentLifecycleStatus.ENDED
    assert staged_experiments[0].ended_by == "researcher"
    assert store.investigations.experiments[1].ended_at == "already-ended"
    assert store.lesson_conclusions.requested == [{"PLAN-ACTIVE"}]


@pytest.mark.asyncio
async def test_ending_investigation_rolls_back_every_mutation_on_failure() -> None:
    store = _InvestigationStore(fail_experiment_stage=True)

    with pytest.raises(RuntimeError, match="experiment stage failed"):
        await end_investigation(
            store,  # type: ignore[arg-type]
            investigation_id="INV-1",
            ended_by="researcher",
        )

    assert store.commits == 0
    assert store.rollbacks == 1
    assert store.investigations.investigation.status == InvestigationStatus.ACTIVE
    assert store.investigations.experiments[0].lifecycle_status == ExperimentLifecycleStatus.ACTIVE
