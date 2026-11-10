"""The loop in the API process that runs queued jobs, each in a process of its own.

Every beat it looks at the jobs it is running — a finished process is given back if it
recorded nothing, one past the time limit is stopped — then claims more while it has free
slots. Stopping it stops its jobs and gives them back to be run again at once.
"""

from __future__ import annotations

import asyncio
import logging
import multiprocessing
import os
import time
from dataclasses import dataclass
from multiprocessing.process import BaseProcess

from app.config import JobsConfig
from app.infra.jobs.claims import ClaimedJob, JobClaims
from app.infra.jobs.kinds import KINDS
from app.infra.jobs.process import run_job

logger = logging.getLogger(__name__)

#: How often the runner records that it is alive.
_SEEN_EVERY_SECONDS = 10.0
#: How long a stopped job's process is given to exit before it is killed.
_STOP_GRACE_SECONDS = 5.0


@dataclass
class _Running:
    claimed: ClaimedJob
    process: BaseProcess
    started: float
    stopped_for: str | None = None


class Runner:
    """Runs up to ``slots`` jobs at once until stopped."""

    def __init__(self, claims: JobClaims, config: JobsConfig) -> None:
        self._claims = claims
        self._config = config
        self._running: dict[str, _Running] = {}
        self._stopping = asyncio.Event()
        self._spawn = multiprocessing.get_context("spawn")
        self._last_seen = 0.0

    def stop(self) -> None:
        self._stopping.set()

    async def run(self) -> None:
        logger.info("job runner started: %d slots", self._config.slots)
        while not self._stopping.is_set():
            try:
                await self._beat()
            except Exception:  # noqa: BLE001 - a failed beat must not end the loop
                logger.exception("job runner: beat failed")
            try:
                await asyncio.wait_for(self._stopping.wait(), self._config.poll_seconds)
            except TimeoutError:
                pass
        await self._stop_all()

    async def _beat(self) -> None:
        await self._supervise()
        while len(self._running) < self._config.slots and not self._stopping.is_set():
            claimed = await self._claims.claim()
            if claimed is None:
                break
            await self._start(claimed)
        if time.monotonic() - self._last_seen >= _SEEN_EVERY_SECONDS:
            await self._claims.seen(slots=self._config.slots, running=len(self._running))
            self._last_seen = time.monotonic()

    async def _start(self, claimed: ClaimedJob) -> None:
        process = self._spawn.Process(
            target=run_job,
            args=(claimed, KINDS[claimed.kind], self._config, os.getpid()),
            name=f"job {claimed.job_id}",
        )
        await asyncio.to_thread(process.start)
        self._running[claimed.job_id] = _Running(claimed, process, time.monotonic())
        logger.info("job %s (%s) run %d started", claimed.job_id, claimed.kind, claimed.attempt)

    async def _supervise(self) -> None:
        for job_id, running in list(self._running.items()):
            if running.process.is_alive():
                self._enforce_time_limit(running)
                continue
            del self._running[job_id]
            exit_code = running.process.exitcode
            running.process.close()
            reason = running.stopped_for or f"its process exited with code {exit_code}"
            await self._claims.give_back(running.claimed, reason)

    def _enforce_time_limit(self, running: _Running) -> None:
        limit = self._config.time_limit_seconds
        if running.stopped_for is None and time.monotonic() - running.started > limit:
            running.stopped_for = f"it ran past the {limit}s time limit"
            logger.error("job %s: %s; stopping it", running.claimed.job_id, running.stopped_for)
            running.process.kill()

    async def _stop_all(self) -> None:
        """Stop every running job and give it back, so a restart runs it again at once."""
        for running in self._running.values():
            running.stopped_for = "the runner stopped"
            running.process.terminate()
        for running in self._running.values():
            await asyncio.to_thread(running.process.join, _STOP_GRACE_SECONDS)
            if running.process.is_alive():
                running.process.kill()
                await asyncio.to_thread(running.process.join)
        await self._supervise()
        logger.info("job runner stopped")
