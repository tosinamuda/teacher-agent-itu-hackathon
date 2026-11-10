"""Guard on ``LaunchExecution``:

- Only ONE generation per experiment+hypothesis may be in flight at a time —
  a second launch while one is queued/running/created is rejected (409).
- H1's C0–C3 conditions are FROZEN once they succeed: the ablation is fixed
  for reproducibility, and only C4 re-iterates via the teacher gate. So a new
  H1 launch after a succeeded H1 run is rejected (409). H2 is not frozen.

Both rejections must fire BEFORE anything is committed or published, so these
tests need no worker and no database.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.execution_launch import (
    LaunchExecution,
    LaunchExecutionInput,
)
from app.domains.experiments.domain import ExecutionStatus, Hypothesis
from app.infra.jobs.kinds import RUN_CONDITIONED_EXECUTION
from tests.launch_collaborators import FakeLaunchStore


def _execution(status: ExecutionStatus, hypothesis: Hypothesis = Hypothesis.H1) -> Any:
    return SimpleNamespace(id=uuid.uuid4(), status=status, hypothesis=hypothesis.value)


async def _start(store: FakeLaunchStore, hypothesis: Hypothesis) -> Any:
    launch = LaunchExecution(store)  # type: ignore[arg-type]
    return await launch(
        LaunchExecutionInput(
            experiment_id="EXP-test",
            hypothesis=hypothesis,
            runtime_snapshot=None,
        )
    )


@pytest.mark.asyncio
async def test_rejects_second_generation_while_one_is_in_flight() -> None:
    store = FakeLaunchStore([_execution(ExecutionStatus.RUNNING)])
    with pytest.raises(ExperimentApplicationError) as exc:
        await _start(store, Hypothesis.H1)
    assert exc.value.status_code == 409
    assert exc.value.detail == "generation_already_in_progress"
    assert store.events == []


@pytest.mark.asyncio
async def test_rejects_h1_regeneration_after_success() -> None:
    store = FakeLaunchStore([_execution(ExecutionStatus.SUCCEEDED)])
    with pytest.raises(ExperimentApplicationError) as exc:
        await _start(store, Hypothesis.H1)
    assert exc.value.status_code == 409
    assert exc.value.detail == "h1_conditions_frozen"
    assert store.events == []


@pytest.mark.asyncio
async def test_queued_in_flight_also_blocks() -> None:
    store = FakeLaunchStore([_execution(ExecutionStatus.QUEUED)])
    with pytest.raises(ExperimentApplicationError) as exc:
        await _start(store, Hypothesis.H1)
    assert exc.value.detail == "generation_already_in_progress"


@pytest.mark.asyncio
async def test_failed_h1_does_not_freeze() -> None:
    """A *failed* H1 run must not freeze — retry has to get past the guard."""
    store = FakeLaunchStore([_execution(ExecutionStatus.FAILED)])

    execution = await _start(store, Hypothesis.H1)

    assert execution.status == ExecutionStatus.QUEUED


@pytest.mark.asyncio
async def test_queued_and_its_job_commit_together_exactly_once() -> None:
    """A committed QUEUED execution always has the job that runs it beside it."""
    store = FakeLaunchStore()

    result = await _start(store, Hypothesis.H1)

    assert store.events == ["stage", "stage_job", "commit"]
    assert result.status == ExecutionStatus.QUEUED
    assert store.jobs_added == [
        (RUN_CONDITIONED_EXECUTION, (result.execution_id,), result.execution_id)
    ]


@pytest.mark.asyncio
async def test_attempt_conflict_rolls_back_and_commits_nothing() -> None:
    store = FakeLaunchStore(conflict=True)

    with pytest.raises(ExperimentApplicationError) as exc:
        await _start(store, Hypothesis.H2)

    assert exc.value.status_code == 409
    assert exc.value.detail == "generation_already_in_progress"
    assert store.events == ["stage", "rollback"]


@pytest.mark.asyncio
async def test_the_launched_job_names_who_started_it_so_they_can_follow_it() -> None:
    store = FakeLaunchStore()
    launch = LaunchExecution(store)  # type: ignore[arg-type]

    await launch(
        LaunchExecutionInput(
            experiment_id="EXP-test",
            hypothesis=Hypothesis.H1,
            runtime_snapshot=None,
            requested_by="code|teacher-1",
        )
    )

    assert [kind for kind, _args, _subject in store.jobs_added] == [RUN_CONDITIONED_EXECUTION]
    assert store.requesters == ["code|teacher-1"]
