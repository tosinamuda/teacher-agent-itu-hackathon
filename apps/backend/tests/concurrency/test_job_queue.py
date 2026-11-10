"""Jobs are queued with the caller's commit, claimed once, and run again when cut short.

These run against the real database: the unique index and ``SKIP LOCKED`` live there.
"""

from __future__ import annotations

import asyncio
from datetime import timedelta

import pytest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.infra.jobs.claims import JobClaims
from app.infra.jobs.kinds import DURABLE_RUNS, RUN_CONDITIONED_EXECUTION, SYNTHETIC_RATE
from app.infra.jobs.models import Job, JobRunner, JobState
from app.infra.jobs.queue import JobAlreadyQueuedError, JobQueue
from app.shared.time import utc_now

pytestmark = pytest.mark.asyncio

_KIND = RUN_CONDITIONED_EXECUTION


def _claims(session_factory, runner: str = "host:1") -> JobClaims:
    return JobClaims(session_factory, runner=runner, lease_seconds=120)


async def _queue(session_factory, *subjects: str, kind: str = _KIND) -> None:
    async with session_factory() as session:
        for subject in subjects:
            JobQueue(session).add(kind, subject, subject=subject)
        await session.commit()


async def _job(session_factory, subject: str) -> Job:
    async with session_factory() as session:
        return (await session.execute(select(Job).where(Job.subject == subject))).scalar_one()


async def _lapse(session_factory, subject: str) -> None:
    async with session_factory() as session:
        await session.execute(
            update(Job)
            .where(Job.subject == subject)
            .values(lease_expires_at=utc_now() - timedelta(seconds=1))
        )
        await session.commit()


async def test_a_job_exists_only_once_its_transaction_commits(session_factory, count_rows) -> None:
    async with session_factory() as session:
        JobQueue(session).add(_KIND, "EXE-1", subject="EXE-1")
        await session.rollback()

    assert await count_rows(Job) == 0


async def test_one_unfinished_job_of_a_kind_per_subject(session_factory) -> None:
    await _queue(session_factory, "EXE-1")

    async with session_factory() as session:
        JobQueue(session).add(_KIND, "EXE-1", subject="EXE-1")
        with pytest.raises(IntegrityError):
            await session.commit()


async def test_submitting_a_second_unfinished_job_says_so(session_factory) -> None:
    await _queue(session_factory, "EXE-1")

    async with session_factory() as session:
        with pytest.raises(JobAlreadyQueuedError):
            await JobQueue(session).submit(_KIND, "EXE-1", subject="EXE-1")


async def test_another_kind_and_a_finished_job_leave_the_subject_free(
    session_factory, count_rows
) -> None:
    await _queue(session_factory, "EXE-1")
    async with session_factory() as session:
        await JobQueue(session).cancel("EXE-1")
        await session.commit()

    await _queue(session_factory, "EXE-1")
    await _queue(session_factory, "EXE-1", kind=SYNTHETIC_RATE)

    assert await count_rows(Job, subject="EXE-1") == 3


async def test_cancelling_ends_only_the_subject_s_unfinished_jobs(session_factory) -> None:
    await _queue(session_factory, "EXE-1", "EXE-2")

    async with session_factory() as session:
        assert len(await JobQueue(session).cancel("EXE-1")) == 1
        await session.commit()

    assert (await _job(session_factory, "EXE-1")).state == JobState.CANCELLED
    assert (await _job(session_factory, "EXE-2")).state == JobState.QUEUED


async def test_a_claim_takes_the_oldest_job_and_holds_it(session_factory) -> None:
    await _queue(session_factory, "EXE-1")
    await _queue(session_factory, "EXE-2")

    claimed = await _claims(session_factory).claim()

    assert claimed is not None
    assert (claimed.args, claimed.attempt, claimed.rerun) == (["EXE-1"], 1, False)
    held = await _job(session_factory, "EXE-1")
    assert (held.state, held.runner, held.attempts) == (JobState.RUNNING, "host:1", 1)
    assert held.lease_expires_at is not None


async def test_two_runners_claiming_at_once_never_take_the_same_job(session_factory) -> None:
    await _queue(session_factory, *(f"EXE-{i}" for i in range(20)))

    claimed = await asyncio.gather(
        *(_claims(session_factory, f"host:{i}").claim() for i in range(24))
    )

    taken = [job.job_id for job in claimed if job is not None]
    assert len(taken) == len(set(taken)) == 20


async def test_a_held_job_is_not_claimed_again(session_factory) -> None:
    await _queue(session_factory, "EXE-1")
    await _claims(session_factory).claim()

    assert await _claims(session_factory, "host:2").claim() is None


async def test_a_job_whose_claim_lapsed_is_claimed_again_as_a_rerun(session_factory) -> None:
    await _queue(session_factory, "EXE-1")
    await _claims(session_factory).claim()
    await _lapse(session_factory, "EXE-1")

    claimed = await _claims(session_factory, "host:2").claim()

    assert claimed is not None and (claimed.attempt, claimed.rerun) == (2, True)
    job = await _job(session_factory, "EXE-1")
    assert (job.runner, job.last_error) == ("host:2", "run 1 stopped renewing its claim")


async def test_a_run_cut_short_is_given_back_to_run_again(session_factory) -> None:
    await _queue(session_factory, "EXE-1")
    claimed = await _claims(session_factory).claim()

    await _claims(session_factory).give_back(claimed, "its process exited with code -9")

    job = await _job(session_factory, "EXE-1")
    assert (job.state, job.runner, job.last_error) == (
        JobState.QUEUED,
        None,
        "its process exited with code -9",
    )
    assert (await _claims(session_factory).claim()).rerun


async def test_a_job_cut_short_on_every_run_fails_at_its_bound(session_factory) -> None:
    await _queue(session_factory, "EXE-1")
    for _ in range(DURABLE_RUNS):
        claimed = await _claims(session_factory).claim()
        await _claims(session_factory).give_back(claimed, "its process exited with code -9")

    job = await _job(session_factory, "EXE-1")
    assert job.state == JobState.FAILED
    assert job.active_subject is None
    assert job.last_error.endswith(f"stopped after {DURABLE_RUNS} interrupted run(s)")


async def test_a_best_effort_job_gets_one_run(session_factory) -> None:
    await _queue(session_factory, "EXP-1", kind=SYNTHETIC_RATE)
    claimed = await _claims(session_factory).claim()

    await _claims(session_factory).give_back(claimed, "its process exited with code 1")

    assert (await _job(session_factory, "EXP-1")).state == JobState.FAILED


async def test_giving_back_leaves_a_job_its_run_no_longer_holds(session_factory) -> None:
    """A job cancelled, or claimed again after a lapse, belongs to someone else now."""
    await _queue(session_factory, "EXE-1")
    first = await _claims(session_factory).claim()
    await _lapse(session_factory, "EXE-1")
    await _claims(session_factory, "host:2").claim()

    await _claims(session_factory).give_back(first, "its process exited with code 1")

    job = await _job(session_factory, "EXE-1")
    assert (job.state, job.attempts, job.runner) == (JobState.RUNNING, 2, "host:2")


async def test_a_job_of_no_known_kind_fails_rather_than_blocking_the_queue(
    session_factory,
) -> None:
    async with session_factory() as session:
        JobQueue(session).add(_KIND, "EXE-1", subject="EXE-1")
        await session.flush()
        await session.execute(update(Job).values(kind="experiments.retired_kind"))
        await session.commit()
    await _queue(session_factory, "EXE-2")

    claimed = await _claims(session_factory).claim()

    assert claimed is not None and claimed.args == ["EXE-2"]
    assert (await _job(session_factory, "EXE-1")).state == JobState.FAILED


async def test_a_runner_is_recorded_as_seen(session_factory) -> None:
    claims = _claims(session_factory)
    await claims.seen(slots=4, running=1)
    await claims.seen(slots=4, running=3)

    async with session_factory() as session:
        runners = list((await session.execute(select(JobRunner))).scalars())
    assert [(runner.runner, runner.running) for runner in runners] == [("host:1", 3)]
