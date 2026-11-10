"""The runner runs each job in a process of its own, and recovers what that process cannot.

End to end: a real runner spawning real processes against the real database. Each test's
handler writes to a file, which is how the test sees what happened inside the process.
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import time
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from sqlalchemy import select

from app.config import JobsConfig
from app.infra.jobs.claims import JobClaims
from app.infra.jobs.kinds import KINDS, JobKind
from app.infra.jobs.models import Job, JobState
from app.infra.jobs.queue import JobQueue
from app.infra.jobs.runner import Runner
from tests.job_runner_process import KILLED_KIND

pytestmark = pytest.mark.asyncio

#: Short enough that a test sees a lapse, a heartbeat or a time limit within seconds.
_FAST = JobsConfig(
    slots=2, poll_seconds=0.2, lease_seconds=6, heartbeat_seconds=1, time_limit_seconds=60
)
#: A spawned process imports the app before it runs anything; allow for that.
_PATIENCE_SECONDS = 60.0


@pytest.fixture
def kind(monkeypatch) -> Callable[..., str]:
    """Register a test handler as a job kind, for the runner that hands it to its process."""

    def _register(handler: str, *, runs: int = 1, told_of_rerun: bool = False) -> str:
        name = f"tests.{handler}"
        monkeypatch.setitem(
            KINDS, name, JobKind(f"tests.job_handlers:{handler}", runs, told_of_rerun)
        )
        return name

    return _register


@asynccontextmanager
async def _running(session_factory, config: JobsConfig = _FAST) -> AsyncIterator[Runner]:
    runner = Runner(
        JobClaims(session_factory, runner="test:1", lease_seconds=config.lease_seconds), config
    )
    task = asyncio.create_task(runner.run())
    try:
        yield runner
    finally:
        runner.stop()
        await task


async def _queue(session_factory, kind: str, trace: Path) -> None:
    async with session_factory() as session:
        await JobQueue(session).submit(kind, str(trace), subject=trace.name)


async def _job(session_factory) -> Job:
    async with session_factory() as session:
        return (await session.execute(select(Job))).scalar_one()


async def _until(session_factory, done: Callable[[Job], bool]) -> Job:
    deadline = time.monotonic() + _PATIENCE_SECONDS
    while time.monotonic() < deadline:
        job = await _job(session_factory)
        if done(job):
            return job
        await asyncio.sleep(0.2)
    raise AssertionError(f"job never got there: {job.state}, {job.last_error}")


def _runs(trace: Path) -> list[str]:
    return trace.read_text().splitlines() if trace.exists() else []


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


async def _gone(pid: int) -> None:
    """Wait for a job's process to end: it checks for its runner and its claim every beat."""
    deadline = time.monotonic() + 10
    while _alive(pid) and time.monotonic() < deadline:
        await asyncio.sleep(0.2)
    assert not _alive(pid), f"the job's process {pid} kept running"


async def test_a_job_runs_in_its_own_process_and_records_success(
    session_factory, kind, tmp_path
) -> None:
    trace = tmp_path / "record"
    await _queue(session_factory, kind("record"), trace)

    async with _running(session_factory):
        job = await _until(session_factory, lambda job: job.state == JobState.SUCCEEDED)

    assert _runs(trace) == ["ran"]
    assert (job.attempts, job.active_subject, job.last_error) == (1, None, None)
    assert job.result == {"trace": str(trace)}


async def test_a_handler_that_raises_fails_its_job_and_is_not_run_again(
    session_factory, kind, tmp_path
) -> None:
    trace = tmp_path / "raise"
    await _queue(session_factory, kind("raise_error", runs=3), trace)

    async with _running(session_factory):
        job = await _until(session_factory, lambda job: job.state == JobState.FAILED)

    assert _runs(trace) == ["ran"]
    assert job.last_error == "ValueError: the handler failed"


async def test_a_refusal_keeps_its_own_reason_for_the_page_that_asked(
    session_factory, kind, tmp_path
) -> None:
    trace = tmp_path / "refuse"
    await _queue(session_factory, kind("refuse", runs=3), trace)

    async with _running(session_factory):
        job = await _until(session_factory, lambda job: job.state == JobState.FAILED)

    assert (_runs(trace), job.last_error) == (["ran"], "approve_the_lesson_note_first")


async def test_a_process_that_dies_is_run_again_until_its_bound(
    session_factory, kind, tmp_path
) -> None:
    trace = tmp_path / "die"
    await _queue(session_factory, kind("die", runs=2), trace)

    async with _running(session_factory):
        job = await _until(session_factory, lambda job: job.state == JobState.FAILED)

    assert _runs(trace) == ["ran", "ran"]
    assert job.last_error == ("its process exited with code 3; stopped after 2 interrupted run(s)")


async def test_a_rerun_is_told_it_follows_a_run_cut_short(session_factory, kind, tmp_path) -> None:
    trace = tmp_path / "rerun"
    name = kind("record_rerun", runs=2, told_of_rerun=True)
    await _queue(session_factory, name, trace)
    async with session_factory() as session:
        job = (await session.execute(select(Job))).scalar_one()
        job.attempts = 1  # as if a first run had been cut short
        await session.commit()

    async with _running(session_factory):
        await _until(session_factory, lambda job: job.state == JobState.SUCCEEDED)

    assert _runs(trace) == ["rerun=True"]


async def test_a_job_past_its_time_limit_is_stopped(session_factory, kind, tmp_path) -> None:
    trace = tmp_path / "hang"
    await _queue(session_factory, kind("hang"), trace)
    config = _FAST.model_copy(update={"time_limit_seconds": 2})

    async with _running(session_factory, config):
        job = await _until(session_factory, lambda job: job.state == JobState.FAILED)

    assert job.last_error.startswith("it ran past the 2s time limit")


async def test_a_cancelled_job_s_process_stops_itself(session_factory, kind, tmp_path) -> None:
    trace = tmp_path / "cancel"
    await _queue(session_factory, kind("hang_telling_pid"), trace)

    async with _running(session_factory):
        await _until(session_factory, lambda _job: bool(_runs(trace)))
        process = int(_runs(trace)[0].removeprefix("pid="))
        async with session_factory() as session:
            await JobQueue(session).cancel(trace.name)
            await session.commit()
        await _gone(process)

    assert (await _job(session_factory)).state == JobState.CANCELLED


async def test_stopping_the_runner_gives_its_jobs_back_to_run_again(
    session_factory, kind, tmp_path
) -> None:
    trace = tmp_path / "stop"
    await _queue(session_factory, kind("hang", runs=2), trace)

    async with _running(session_factory):
        await _until(session_factory, lambda _job: _runs(trace) == ["ran"])

    job = await _job(session_factory)
    assert (job.state, job.last_error, job.runner) == (
        JobState.QUEUED,
        "the runner stopped",
        None,
    )


async def test_a_killed_runner_s_job_stops_and_is_run_again_by_another(
    session_factory, kind, tmp_path
) -> None:
    """``kill -9`` of the API process: its job's process ends itself, and the job lives on."""
    trace = tmp_path / "killed"
    kind("hang_telling_pid", runs=2)
    await _queue(session_factory, KILLED_KIND, trace)
    doomed = subprocess.Popen([sys.executable, "-m", "tests.job_runner_process"])
    try:
        job = await _until(session_factory, lambda _job: bool(_runs(trace)))
        orphan = int(_runs(trace)[0].removeprefix("pid="))
        doomed.kill()
        doomed.wait()
        await _gone(orphan)
    finally:
        doomed.kill()

    async with _running(session_factory):
        job = await _until(session_factory, lambda job: job.attempts == 2)

    assert (job.state, job.runner) == (JobState.RUNNING, "test:1")
    assert job.last_error == "run 1 stopped renewing its claim"
