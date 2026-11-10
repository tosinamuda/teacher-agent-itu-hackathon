"""Transaction contracts for binding authored experiment plans."""

from __future__ import annotations

import inspect
import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_authoring import (
    bind_experiment_plan_version,
)


class _ExperimentAuthoring:
    def __init__(self, *, fail_stage: bool = False) -> None:
        self.lesson_period_id = uuid.uuid4()
        self.experiment = SimpleNamespace(
            experiment_id="EXP-1",
            lesson_period_id=self.lesson_period_id,
            plan_version_id="LPV-OLD",
        )
        self.plans = {
            "LPV-OLD": (
                SimpleNamespace(version_id="LPV-OLD", plan_id="LP-1"),
                SimpleNamespace(plan_id="LP-1", lesson_period_id=self.lesson_period_id),
            ),
            "LPV-NEW": (
                SimpleNamespace(version_id="LPV-NEW", plan_id="LP-1"),
                SimpleNamespace(plan_id="LP-1", lesson_period_id=self.lesson_period_id),
            ),
            "LPV-OTHER-PLAN": (
                SimpleNamespace(version_id="LPV-OTHER-PLAN", plan_id="LP-2"),
                SimpleNamespace(plan_id="LP-2", lesson_period_id=self.lesson_period_id),
            ),
            "LPV-OTHER-LESSON": (
                SimpleNamespace(version_id="LPV-OTHER-LESSON", plan_id="LP-3"),
                SimpleNamespace(plan_id="LP-3", lesson_period_id=uuid.uuid4()),
            ),
        }
        self.events: list[str] = []
        self.staged: list[Any] = []
        self.fail_stage = fail_stage

    async def get_experiment(self, experiment_id: str) -> Any:
        self.events.append("experiment_loaded")
        return self.experiment if experiment_id == "EXP-1" else None

    async def get_plan_version_plan(self, *, plan_version_id: str) -> Any:
        self.events.append("plan_validated")
        return self.plans.get(plan_version_id)

    async def stage_plan_binding(self, experiment: Any) -> Any:
        self.events.append("binding_staged")
        self.staged.append(experiment)
        if self.fail_stage:
            raise RuntimeError("binding stage failed")
        return experiment


class _ExperimentAuthoringStore:
    def __init__(self, *, fail_stage: bool = False) -> None:
        self.experiment_authoring = _ExperimentAuthoring(fail_stage=fail_stage)
        self.commits = 0
        self.rollbacks = 0
        self._original_plan_version_id = self.experiment_authoring.experiment.plan_version_id

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1
        self.experiment_authoring.experiment.plan_version_id = self._original_plan_version_id


def test_plan_binding_command_receives_no_raw_session() -> None:
    assert "db" not in inspect.signature(bind_experiment_plan_version).parameters


@pytest.mark.asyncio
async def test_plan_binding_validates_before_staging_and_commits_once() -> None:
    store = _ExperimentAuthoringStore()

    experiment = await bind_experiment_plan_version(
        store,  # type: ignore[arg-type]
        experiment_id="EXP-1",
        plan_version_id="LPV-NEW",
    )

    assert experiment.plan_version_id == "LPV-NEW"
    assert store.experiment_authoring.events == [
        "experiment_loaded",
        "plan_validated",
        "binding_staged",
    ]
    assert store.experiment_authoring.staged == [experiment]
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_plan_binding_rejects_an_unknown_version_before_staging() -> None:
    store = _ExperimentAuthoringStore()

    with pytest.raises(ExperimentApplicationError) as raised:
        await bind_experiment_plan_version(
            store,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            plan_version_id="LPV-MISSING",
        )

    assert raised.value.status_code == 404
    assert raised.value.detail == "plan_version_not_found"
    assert store.experiment_authoring.staged == []
    assert store.experiment_authoring.experiment.plan_version_id == "LPV-OLD"
    assert store.commits == 0
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_plan_binding_rejects_another_lesson_before_staging() -> None:
    store = _ExperimentAuthoringStore()

    with pytest.raises(ExperimentApplicationError) as raised:
        await bind_experiment_plan_version(
            store,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            plan_version_id="LPV-OTHER-LESSON",
        )

    assert raised.value.detail == "plan_version_belongs_to_other_lesson"
    assert store.experiment_authoring.staged == []
    assert store.experiment_authoring.experiment.plan_version_id == "LPV-OLD"


@pytest.mark.asyncio
async def test_revised_binding_rejects_another_plan_before_staging() -> None:
    store = _ExperimentAuthoringStore()

    with pytest.raises(ExperimentApplicationError) as raised:
        await bind_experiment_plan_version(
            store,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            plan_version_id="LPV-OTHER-PLAN",
            expected_plan_id="LP-1",
            target_not_found_detail="accepted_version_not_found",
        )

    assert raised.value.detail == "accepted_version_belongs_to_other_plan"
    assert store.experiment_authoring.staged == []
    assert store.experiment_authoring.experiment.plan_version_id == "LPV-OLD"


@pytest.mark.asyncio
async def test_plan_binding_rolls_back_mutation_when_staging_fails() -> None:
    store = _ExperimentAuthoringStore(fail_stage=True)

    with pytest.raises(RuntimeError, match="binding stage failed"):
        await bind_experiment_plan_version(
            store,  # type: ignore[arg-type]
            experiment_id="EXP-1",
            plan_version_id="LPV-NEW",
        )

    assert store.experiment_authoring.experiment.plan_version_id == "LPV-OLD"
    assert store.commits == 0
    assert store.rollbacks == 1


def test_every_plan_binding_path_uses_the_named_command() -> None:
    source = Path("src/app/domains/experiments/application/service.py").read_text(encoding="utf-8")

    assert source.count("bind_experiment_plan_version(") == 3
    assert "set_experiment_plan_version" not in source
