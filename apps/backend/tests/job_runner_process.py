"""A runner in a process of its own, for a test to kill: ``python -m tests.job_runner_process``.

It runs the one test kind the kill test queues, against the database the test's environment
names, until it is killed.
"""

from __future__ import annotations

import asyncio

import app.db.metadata  # noqa: F401  (registers every ORM model; mappers need them all)
from app.config import JobsConfig
from app.db.session import AsyncSessionLocal
from app.infra.jobs.claims import JobClaims
from app.infra.jobs.kinds import KINDS, JobKind
from app.infra.jobs.runner import Runner

KILLED_KIND = "tests.hang_telling_pid"
CONFIG = JobsConfig(
    slots=1, poll_seconds=0.2, lease_seconds=4, heartbeat_seconds=1, time_limit_seconds=60
)


async def _main() -> None:
    KINDS[KILLED_KIND] = JobKind("tests.job_handlers:hang_telling_pid", runs=2)
    claims = JobClaims(AsyncSessionLocal, runner="doomed:1", lease_seconds=CONFIG.lease_seconds)
    await Runner(claims, CONFIG).run()


if __name__ == "__main__":
    asyncio.run(_main())
