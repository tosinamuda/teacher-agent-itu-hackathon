"""Guard on ``retry_condition``, the launch side of a per-condition retry.

The retry targets the experiment's LATEST H1 execution, refuses to queue while
that execution is still in flight, and 404s when the experiment has never run H1.
Nothing is written but the job, so a fake job queue is the whole seam.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.execution_launch import retry_condition
from app.domains.experiments.domain import ExecutionStatus, Hypothesis
from app.infra.jobs.kinds import RETRY_CONDITION_RUN
from app.infra.jobs.queue import JobAlreadyQueuedError


class _FakeRepo:
    """Returns a fixed execution list for the experiment, and records the jobs queued."""

    def __init__(self, executions: list[Any], *, queued_already: bool = False) -> None:
        self._executions = executions
        self._queued_already = queued_already
        self.submitted: list[tuple[str, tuple[Any, ...], str | None]] = []

    @property
    def experiments(self) -> _FakeRepo:
        return self

    @property
    def jobs(self) -> _FakeRepo:
        return self

    async def get_experiment(self, experiment_id: str) -> Any:
        return SimpleNamespace(id=uuid.uuid4())

    async def list_executions_for_experiment(self, experiment_db_id: uuid.UUID) -> list[Any]:
        return self._executions

    async def submit(
        self, kind: str, *args: Any, subject: str | None = None, requested_by: str | None = None
    ) -> str:
        if self._queued_already:
            raise JobAlreadyQueuedError(kind, subject)
        self.submitted.append((kind, args, subject))
        return "JOB-1"


def _execution(
    execution_id: str,
    status: ExecutionStatus,
    hypothesis: Hypothesis = Hypothesis.H1,
) -> Any:
    return SimpleNamespace(execution_id=execution_id, status=status, hypothesis=hypothesis.value)


async def _retry(repo: _FakeRepo, enqueued: list[tuple[str, str]]) -> Any:
    try:
        return await retry_condition(
            repo,  # type: ignore[arg-type]
            experiment_id="EXP-test",
            condition_code="C1",
        )
    finally:
        enqueued.extend((args[0], args[1]) for _kind, args, _subject in repo.submitted)


@pytest.mark.asyncio
async def test_enqueues_the_condition_on_the_latest_h1_execution() -> None:
    repo = _FakeRepo(
        [
            _execution("EXE-latest", ExecutionStatus.FAILED),
            _execution("EXE-older", ExecutionStatus.FAILED),
        ]
    )
    enqueued: list[tuple[str, str]] = []

    execution = await _retry(repo, enqueued)

    assert enqueued == [("EXE-latest", "C1")]
    assert execution.execution_id == "EXE-latest"


@pytest.mark.asyncio
async def test_h2_executions_are_not_retry_targets() -> None:
    repo = _FakeRepo([_execution("EXE-h2", ExecutionStatus.FAILED, Hypothesis.H2)])
    enqueued: list[tuple[str, str]] = []

    with pytest.raises(ExperimentApplicationError) as exc:
        await _retry(repo, enqueued)

    assert exc.value.status_code == 404
    assert exc.value.detail == "no_h1_execution"
    assert enqueued == []


@pytest.mark.asyncio
async def test_refuses_while_the_latest_h1_execution_is_in_flight() -> None:
    repo = _FakeRepo([_execution("EXE-latest", ExecutionStatus.RUNNING)])
    enqueued: list[tuple[str, str]] = []

    with pytest.raises(ExperimentApplicationError) as exc:
        await _retry(repo, enqueued)

    assert exc.value.status_code == 409
    assert exc.value.detail == "generation_already_in_progress"
    assert enqueued == []


@pytest.mark.asyncio
async def test_the_retry_job_acts_on_the_execution_s_condition() -> None:
    repo = _FakeRepo([_execution("EXE-latest", ExecutionStatus.FAILED)])

    await _retry(repo, [])

    assert repo.submitted == [(RETRY_CONDITION_RUN, ("EXE-latest", "C1"), "EXE-latest:C1")]


@pytest.mark.asyncio
async def test_a_retry_already_queued_for_the_condition_is_a_conflict() -> None:
    repo = _FakeRepo([_execution("EXE-latest", ExecutionStatus.FAILED)], queued_already=True)

    with pytest.raises(ExperimentApplicationError) as exc:
        await _retry(repo, [])

    assert (exc.value.status_code, exc.value.detail) == (409, "condition_retry_already_queued")
