"""Transaction contracts for experiment administration commands."""

from __future__ import annotations

import inspect
import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.experiments.application import experiment_administration
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_administration import (
    end_experiment,
    set_sandbox,
    update_focal_learners,
)
from app.domains.experiments.domain.types import ExperimentLifecycleStatus


class _ExperimentAdministration:
    def __init__(self, *, fail_stage: bool = False) -> None:
        self.experiment = SimpleNamespace(
            experiment_id="EXP-1",
            teacher_workspace_id=uuid.uuid4(),
            plan_version_id="PLAN-1",
            focal_learner_ids=["OLD"],
            lifecycle_status=ExperimentLifecycleStatus.ACTIVE,
            ended_at=None,
            ended_by=None,
            is_sandbox=False,
        )
        self.workspace = SimpleNamespace(term_class_subject=SimpleNamespace(class_id=uuid.uuid4()))
        self.learners = [
            SimpleNamespace(student_id="S-1"),
            SimpleNamespace(student_id="S-2"),
        ]
        self.diagnostics = {
            learner.student_id: SimpleNamespace(student_id=learner.student_id)
            for learner in self.learners
        }
        self.staged: list[Any] = []
        self.events: list[str] = []
        self.fail_stage = fail_stage

    async def get_experiment(self, experiment_id: str) -> Any:
        return self.experiment if experiment_id == "EXP-1" else None

    async def get_workspace(self, workspace_id: uuid.UUID) -> Any:
        return self.workspace

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[Any]:
        return self.learners

    async def latest_diagnostic_per_student(
        self,
        *,
        student_ids: list[str],
        plan_version_id: str,
    ) -> dict[str, Any]:
        self.events.append("validated_candidates")
        return self.diagnostics

    async def stage_experiment(self, experiment: Any) -> Any:
        self.events.append("staged")
        self.staged.append(experiment)
        if self.fail_stage:
            raise RuntimeError("experiment stage failed")
        return experiment


class _LessonConclusions:
    def __init__(self) -> None:
        self.requested: list[set[str]] = []

    async def conclude_where_no_experiment_is_active(self, plan_version_ids: Any) -> None:
        self.requested.append(set(plan_version_ids))


class _ExperimentAdministrationStore:
    def __init__(self, *, fail_stage: bool = False) -> None:
        self.experiments = _ExperimentAdministration(fail_stage=fail_stage)
        self.experiment_context = self.experiments
        self.lesson_conclusions = _LessonConclusions()
        self.commits = 0
        self.rollbacks = 0
        experiment = self.experiments.experiment
        self._original_state = (
            list(experiment.focal_learner_ids),
            experiment.lifecycle_status,
            experiment.ended_at,
            experiment.ended_by,
            experiment.is_sandbox,
        )

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1
        experiment = self.experiments.experiment
        (
            focal_learner_ids,
            experiment.lifecycle_status,
            experiment.ended_at,
            experiment.ended_by,
            experiment.is_sandbox,
        ) = self._original_state
        experiment.focal_learner_ids = list(focal_learner_ids)


async def _focal_candidates(
    repository: _ExperimentAdministration,
    *,
    experiment: Any,
) -> list[Any]:
    repository.events.append("validated_candidates")
    return [
        SimpleNamespace(learner=learner, diagnostic=repository.diagnostics[learner.student_id])
        for learner in repository.learners
    ]


def test_experiment_administration_commands_receive_no_raw_session() -> None:
    assert "db" not in inspect.signature(end_experiment).parameters
    assert "db" not in inspect.signature(set_sandbox).parameters
    assert "db" not in inspect.signature(update_focal_learners).parameters


@pytest.mark.asyncio
async def test_end_experiment_stages_lifecycle_fields_and_commits_once() -> None:
    store = _ExperimentAdministrationStore()

    experiment = await end_experiment(
        store,  # type: ignore[arg-type]
        experiment_id="EXP-1",
        ended_by="researcher",
    )

    assert experiment.lifecycle_status == ExperimentLifecycleStatus.ENDED
    assert experiment.ended_at is not None
    assert experiment.ended_by == "researcher"
    assert store.experiments.staged == [experiment]
    assert store.lesson_conclusions.requested == [{"PLAN-1"}]
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_set_sandbox_stages_flag_and_commits_once() -> None:
    store = _ExperimentAdministrationStore()

    experiment = await set_sandbox(
        store,  # type: ignore[arg-type]
        experiment_id="EXP-1",
        is_sandbox=True,
    )

    assert experiment.is_sandbox is True
    assert store.experiments.staged == [experiment]
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_update_focal_learners_validates_before_staging_and_commits_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = _ExperimentAdministrationStore()
    monkeypatch.setattr(
        experiment_administration,
        "list_focal_learner_candidates",
        _focal_candidates,
    )

    experiment = await update_focal_learners(
        store,  # type: ignore[arg-type]
        experiment_id="EXP-1",
        learner_ids=["S-2", "S-1", "S-2"],
    )

    assert experiment.focal_learner_ids == ["S-2", "S-1"]
    assert store.experiments.events == ["validated_candidates", "staged"]
    assert store.experiments.staged == [experiment]
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_update_focal_learners_stages_nothing_when_candidate_validation_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = _ExperimentAdministrationStore()
    monkeypatch.setattr(
        experiment_administration,
        "list_focal_learner_candidates",
        _focal_candidates,
    )

    with pytest.raises(
        ExperimentApplicationError,
        match="focal_learner_not_in_workspace_class",
    ):
        await update_focal_learners(
            store,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            learner_ids=["S-1", "NOT-IN-CLASS"],
        )

    assert store.experiments.staged == []
    assert store.experiments.experiment.focal_learner_ids == ["OLD"]
    assert store.commits == 0
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_experiment_administration_rolls_back_mutation_when_staging_fails() -> None:
    store = _ExperimentAdministrationStore(fail_stage=True)

    with pytest.raises(RuntimeError, match="experiment stage failed"):
        await end_experiment(
            store,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            ended_by="researcher",
        )

    experiment = store.experiments.experiment
    assert experiment.lifecycle_status == ExperimentLifecycleStatus.ACTIVE
    assert experiment.ended_at is None
    assert experiment.ended_by is None
    assert store.commits == 0
    assert store.rollbacks == 1
