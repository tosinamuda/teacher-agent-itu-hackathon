"""The process a job runs in, from start to recorded outcome.

Each job gets a fresh interpreter (``spawn``): nothing is inherited from the API process —
no database sockets, no event loop, no LLM client state — and the runner can stop exactly
this job by stopping this process.

From its start, a thread renews the job's claim, so preparing the process cannot outlast the
lease. The process exits on its own when its claim is gone (the job was cancelled, or another
runner took it after a lapse) or when the runner that started it has died, so no job outlives
the runner responsible for it.
"""

from __future__ import annotations

import importlib
import logging
import os
import threading
import time
from collections.abc import Awaitable, Callable
from datetime import timedelta

from sqlalchemy import Update, update

from app.config import CONFIG, JobsConfig
from app.db.session import sync_engine
from app.infra.jobs.claims import ClaimedJob
from app.infra.jobs.kinds import JobKind
from app.infra.jobs.models import Job, JobState
from app.infra.worker_async import run_in_worker
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

logger = logging.getLogger(__name__)

#: How often the claim thread checks that the runner is still there.
_WATCH_SECONDS = 2.0


def run_job(claimed: ClaimedJob, kind: JobKind, config: JobsConfig, runner_pid: int) -> None:
    """Run one job and record how it ended; the runner reads an exit without one as a crash.

    The runner hands over the kind and its timings, so this process runs what the runner
    resolved rather than looking anything up again.
    """
    watch = threading.Thread(target=_keep_claim, args=(claimed, config, runner_pid), daemon=True)
    watch.start()
    _prepare_process()
    try:
        handler = _handler(kind.handler)
        rerun = {"redelivered": claimed.rerun} if kind.told_of_rerun else {}
        result = run_in_worker(handler(*claimed.args, **rerun))
    except Exception as error:
        logger.exception("job %s (%s) failed", claimed.job_id, claimed.kind)
        _record(claimed, JobState.FAILED, error=_described(error))
        return
    _record(claimed, JobState.SUCCEEDED, result=result)


def _described(error: Exception) -> str:
    """What a caller reads: a domain error's own detail code, or the exception as it was."""
    detail = getattr(error, "detail", None)
    return (detail if isinstance(detail, str) else f"{type(error).__name__}: {error}")[:4000]


def _prepare_process() -> None:
    """What every job needs before its handler is imported: logging, LLM calls recorded."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    from app.infra.litellm_worker import disable_litellm_telemetry, reset_litellm_logging_worker

    disable_litellm_telemetry()
    reset_litellm_logging_worker()

    import dspy

    import app.db.metadata  # noqa: F401  (registers every ORM model; mappers need them all)
    from app.domains.generation_log.application import GenerationLogRecorder
    from app.infra.dspy_lm import build_dspy_lm

    callbacks = [GenerationLogRecorder()] if CONFIG.log_model_calls else []
    dspy.configure(lm=build_dspy_lm(), callbacks=callbacks)


def _handler(path: str) -> Callable[..., Awaitable[JsonObject | None]]:
    module, function = path.split(":")
    handler: Callable[..., Awaitable[JsonObject | None]] = getattr(
        importlib.import_module(module), function
    )
    return handler


def _keep_claim(claimed: ClaimedJob, config: JobsConfig, runner_pid: int) -> None:
    """Renew the claim every heartbeat; end the process once it is no longer this job's."""
    last = time.monotonic()
    while True:
        time.sleep(min(_WATCH_SECONDS, config.heartbeat_seconds))
        if os.getppid() != runner_pid:
            logger.error("job %s: its runner is gone; stopping", claimed.job_id)
            os._exit(1)
        if time.monotonic() - last < config.heartbeat_seconds:
            continue
        last = time.monotonic()
        if not _renew(claimed, config.lease_seconds):
            logger.warning("job %s: no longer held by this run; stopping", claimed.job_id)
            os._exit(0)


def _owned(claimed: ClaimedJob) -> Update:
    return update(Job).where(
        Job.id == claimed.id,
        Job.state == JobState.RUNNING,
        Job.attempts == claimed.attempt,
    )


def _renew(claimed: ClaimedJob, lease_seconds: int) -> bool:
    lease = utc_now() + timedelta(seconds=lease_seconds)
    with sync_engine.begin() as connection:
        renewed = connection.execute(_owned(claimed).values(lease_expires_at=lease))
    return renewed.rowcount == 1


def _record(
    claimed: ClaimedJob,
    state: JobState,
    *,
    error: str | None = None,
    result: JsonObject | None = None,
) -> None:
    with sync_engine.begin() as connection:
        connection.execute(
            _owned(claimed).values(
                state=state,
                last_error=error,
                result=result,
                active_subject=None,
                lease_expires_at=None,
                finished_at=utc_now(),
            )
        )
