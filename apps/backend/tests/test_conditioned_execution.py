"""What the worker guarantees about an execution that ends badly.

The terminal write is the one write that must not be lost: a row left RUNNING
looks like work in progress, so nothing retries it and no one is told. These
drive ``conduct_conditioned_execution`` with its collaborators replaced — the
seams are module-level today (`docs/refactor-backlog.md` §1).
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.experiments.application import conditioned_execution as worker
from app.domains.experiments.application import execution_progress
from app.domains.experiments.domain.types import (
    ConditionCode,
    ExecutionErrorCategory,
    ExecutionStatus,
    Hypothesis,
)
from app.domains.experiments.review_pack_study.h1.outcomes import (
    AllConditionsGenerated,
    ConditionFailure,
    SomeConditionsFailed,
)

_EXECUTION_ID = "EXE-1"


class _Repository:
    """The one read the worker makes through the store, for the progress channel."""

    async def get_experiment_by_db_id(self, _db_id: Any) -> SimpleNamespace:
        return SimpleNamespace(experiment_id="EXP-1")


class _Store:
    """A unit of work that records nothing but its own identity."""

    def __init__(self) -> None:
        self.execution_progress = _Repository()

    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None


class _Context:
    """One attempt's collaborators, over one (fake) unit of work."""

    def __init__(self) -> None:
        self.store = _Store()
        self.excerpts = object()


class _Worker:
    """The worker's collaborators, replaced and recorded."""

    def __init__(self) -> None:
        self.contexts: list[_Context] = []
        self.finalized: list[tuple[_Store, ExecutionStatus, str | None, Any]] = []
        self.events: list[dict[str, Any]] = []

    @asynccontextmanager
    async def open_context(self) -> AsyncGenerator[_Context]:
        context = _Context()
        self.contexts.append(context)
        yield context

    async def finalize(
        self,
        store: Any,
        execution_id: str,
        *,
        status: ExecutionStatus,
        error: str | None = None,
        error_category: Any = None,
    ) -> None:
        assert execution_id == _EXECUTION_ID
        self.finalized.append((store, status, error, error_category))

    def publish(self, _experiment_id: str, event: dict[str, Any]) -> None:
        self.events.append(event)

    @property
    def terminal_events(self) -> list[dict[str, Any]]:
        return [event for event in self.events if event["type"] in {"done", "error"}]

    @property
    def run_store(self) -> _Store:
        return self.contexts[0].store

    @property
    def terminal_store(self) -> _Store:
        return self.contexts[1].store


@pytest.fixture
def worker_double(monkeypatch: pytest.MonkeyPatch) -> _Worker:
    double = _Worker()
    execution = SimpleNamespace(
        id=uuid.uuid4(),
        execution_id=_EXECUTION_ID,
        experiment_db_id=uuid.uuid4(),
        hypothesis=Hypothesis.H1.value,
    )

    async def _claim(_store: Any, _execution_id: str, *, redelivered: bool) -> SimpleNamespace:
        del redelivered
        return execution

    monkeypatch.setattr(worker, "open_execution_context", double.open_context)
    monkeypatch.setattr(worker, "claim_execution", _claim)
    monkeypatch.setattr(worker, "finalize_execution", double.finalize)
    monkeypatch.setattr(execution_progress, "publish_synthetic_progress", double.publish)
    # Building the real runner opens a language model; the use case is replaced below.
    monkeypatch.setattr(worker, "build_h1_experiment", lambda: None)
    return double


def _h1_returns(monkeypatch: pytest.MonkeyPatch, outcome: object) -> None:
    async def _run(**_kwargs: Any) -> object:
        return outcome

    monkeypatch.setattr(worker, "run_h1_execution", _run)


def _h1_raises(monkeypatch: pytest.MonkeyPatch, error: BaseException) -> None:
    async def _run(**_kwargs: Any) -> object:
        raise error

    monkeypatch.setattr(worker, "run_h1_execution", _run)


@pytest.mark.asyncio
async def test_a_successful_run_ends_in_exactly_one_done_event(
    monkeypatch: pytest.MonkeyPatch,
    worker_double: _Worker,
) -> None:
    _h1_returns(
        monkeypatch,
        AllConditionsGenerated(completed_conditions=(ConditionCode.C0, ConditionCode.C1)),
    )

    await worker.conduct_conditioned_execution(_EXECUTION_ID)

    assert [event["type"] for event in worker_double.terminal_events] == ["done"]
    assert worker_double.terminal_events[0]["message"] == "2 study pack(s) generated"
    assert [status for _, status, _, _ in worker_double.finalized] == [ExecutionStatus.SUCCEEDED]


@pytest.mark.asyncio
async def test_a_successful_run_is_also_finalized_through_a_fresh_unit_of_work(
    monkeypatch: pytest.MonkeyPatch,
    worker_double: _Worker,
) -> None:
    """The attempt's own store sat idle across generation; the terminal write never uses it."""
    _h1_returns(monkeypatch, AllConditionsGenerated(completed_conditions=(ConditionCode.C0,)))

    await worker.conduct_conditioned_execution(_EXECUTION_ID)

    finalized_on, _, _, _ = worker_double.finalized[0]
    assert finalized_on is worker_double.terminal_store
    assert finalized_on is not worker_double.run_store


@pytest.mark.asyncio
async def test_a_partial_run_reports_error_and_never_also_done(
    monkeypatch: pytest.MonkeyPatch,
    worker_double: _Worker,
) -> None:
    """A watcher gets one terminal event, so it never has to guess which one won."""
    _h1_returns(
        monkeypatch,
        SomeConditionsFailed(
            completed_conditions=(ConditionCode.C0,),
            failed_conditions=(
                ConditionFailure(condition_code=ConditionCode.C2, message="LLM timeout"),
            ),
        ),
    )

    await worker.conduct_conditioned_execution(_EXECUTION_ID)

    assert [event["type"] for event in worker_double.terminal_events] == ["error"]
    _, status, error, category = worker_double.finalized[0]
    assert status == ExecutionStatus.FAILED
    assert error == "conditions failed to generate: C2"
    assert category == ExecutionErrorCategory.GENERATION


@pytest.mark.asyncio
async def test_a_failed_run_is_finalized_through_a_fresh_unit_of_work(
    monkeypatch: pytest.MonkeyPatch,
    worker_double: _Worker,
) -> None:
    """Whatever failed may have poisoned the store, and this write cannot be lost."""
    _h1_raises(monkeypatch, RuntimeError("the model went away"))

    await worker.conduct_conditioned_execution(_EXECUTION_ID)

    finalized_on, status, error, category = worker_double.finalized[0]
    assert finalized_on is worker_double.terminal_store
    assert finalized_on is not worker_double.run_store
    assert status == ExecutionStatus.FAILED
    assert error == "the model went away"
    assert category == ExecutionErrorCategory.GENERATION


@pytest.mark.asyncio
async def test_cancellation_is_recorded_before_it_unwinds(
    monkeypatch: pytest.MonkeyPatch,
    worker_double: _Worker,
) -> None:
    """Shutdown cancels the task; the row must not be left claimed and silent."""
    _h1_raises(monkeypatch, asyncio.CancelledError())

    with pytest.raises(asyncio.CancelledError):
        await worker.conduct_conditioned_execution(_EXECUTION_ID)

    _, status, _, category = worker_double.finalized[0]
    assert status == ExecutionStatus.FAILED
    assert category == ExecutionErrorCategory.CANCELLED
    assert [event["type"] for event in worker_double.terminal_events] == ["error"]
