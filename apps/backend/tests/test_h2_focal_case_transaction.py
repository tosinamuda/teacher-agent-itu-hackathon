"""Transaction contracts for preparing H2 focal-case inputs."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.application import h2_execution
from app.domains.experiments.infrastructure.models import (
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.experiments.review_pack_study.h2.experiment import H2Experiment


class _RecordingSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.flushes = 0
        self.refreshed: list[object] = []
        self.commits = 0

    def add(self, value: object) -> None:
        self.added.append(value)

    async def flush(self) -> None:
        self.flushes += 1

    async def refresh(self, value: object) -> None:
        self.refreshed.append(value)

    async def commit(self) -> None:
        self.commits += 1


class _FakeStore:
    def __init__(self) -> None:
        preparation = SimpleNamespace(staged=[])
        self.h2_inputs = preparation
        self.focal_cases = preparation
        self.commits = 0
        self.rollbacks = 0
        self.persisted: list[str] = []

    async def commit(self) -> None:
        self.commits += 1
        self.persisted.extend(self.focal_cases.staged)
        self.focal_cases.staged.clear()

    async def rollback(self) -> None:
        self.rollbacks += 1
        self.focal_cases.staged.clear()


def _isolate_h2_input_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _inputs(**_kwargs: Any) -> object:
        return SimpleNamespace(experiment=object())

    async def _base_pack(**_kwargs: Any) -> object:
        return object()

    async def _learners(**_kwargs: Any) -> tuple[str, ...]:
        return ("student-1", "student-2")

    monkeypatch.setattr(h2_execution, "validated_h2_inputs", _inputs)
    monkeypatch.setattr(h2_execution, "approved_h2_base", _base_pack)
    monkeypatch.setattr(h2_execution, "select_focal_learners", _learners)


@pytest.mark.asyncio
async def test_save_focal_case_stages_and_flushes_without_committing() -> None:
    session = _RecordingSession()
    repository = ExperimentRepository(cast(AsyncSession, session))
    focal_case = cast(ExperimentFocalCase, object())

    result = await repository.save_focal_case(focal_case)

    assert result is focal_case
    assert session.added == [focal_case]
    assert session.flushes == 1
    assert session.refreshed == [focal_case]
    assert session.commits == 0


@pytest.mark.asyncio
async def test_h2_commits_once_after_every_focal_case_is_staged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_h2_input_reads(monkeypatch)
    store = _FakeStore()

    async def _record(*, experiments: Any, learners: tuple[str, ...], **_kwargs: Any) -> tuple:
        experiments.staged.extend(learners)
        return ()

    async def _load(**_kwargs: Any) -> object:
        assert store.commits == 0
        assert store.focal_cases.staged == ["student-1", "student-2"]
        return SimpleNamespace(learners=())

    class _Runner:
        async def run(self, *, experiment: object) -> str:
            del experiment
            assert store.commits == 1
            assert store.persisted == ["student-1", "student-2"]
            return "completed"

    monkeypatch.setattr(h2_execution, "record_focal_cases", _record)
    monkeypatch.setattr(h2_execution, "load_h2_experiment", _load)

    result = await h2_execution.run_h2_execution(
        store=store,  # type: ignore[arg-type]
        excerpts=object(),  # type: ignore[arg-type]
        execution=cast(ExperimentExecution, object()),
        runner=cast(H2Experiment, _Runner()),
    )

    assert result == "completed"
    assert store.commits == 1
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_h2_rolls_back_every_staged_focal_case_when_one_learner_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_h2_input_reads(monkeypatch)
    store = _FakeStore()

    async def _record(*, experiments: Any, **_kwargs: Any) -> tuple:
        experiments.staged.append("student-1")
        experiments.staged.append("student-2")
        raise RuntimeError("student-2 snapshot failed")

    monkeypatch.setattr(h2_execution, "record_focal_cases", _record)

    with pytest.raises(RuntimeError, match="student-2 snapshot failed"):
        await h2_execution.run_h2_execution(
            store=store,  # type: ignore[arg-type]
            excerpts=object(),  # type: ignore[arg-type]
            execution=cast(ExperimentExecution, object()),
            runner=cast(H2Experiment, object()),
        )

    assert store.commits == 0
    assert store.rollbacks == 1
    assert store.focal_cases.staged == []


@pytest.mark.asyncio
async def test_h2_rolls_back_staged_focal_cases_when_input_assembly_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _isolate_h2_input_reads(monkeypatch)
    store = _FakeStore()

    async def _record(*, experiments: Any, learners: tuple[str, ...], **_kwargs: Any) -> tuple:
        experiments.staged.extend(learners)
        return ()

    async def _load(**_kwargs: Any) -> object:
        raise RuntimeError("lesson source missing")

    monkeypatch.setattr(h2_execution, "record_focal_cases", _record)
    monkeypatch.setattr(h2_execution, "load_h2_experiment", _load)

    with pytest.raises(RuntimeError, match="lesson source missing"):
        await h2_execution.run_h2_execution(
            store=store,  # type: ignore[arg-type]
            excerpts=object(),  # type: ignore[arg-type]
            execution=cast(ExperimentExecution, object()),
            runner=cast(H2Experiment, object()),
        )

    assert store.commits == 0
    assert store.rollbacks == 1
    assert store.focal_cases.staged == []
