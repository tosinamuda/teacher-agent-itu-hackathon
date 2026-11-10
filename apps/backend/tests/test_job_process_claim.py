"""A job's process renews its claim from its start, before it prepares to run the handler."""

from __future__ import annotations

import os
import threading
import uuid

import pytest

from app.config import JobsConfig
from app.infra.jobs import process
from app.infra.jobs.claims import ClaimedJob
from app.infra.jobs.kinds import JobKind


def test_the_claim_is_renewed_while_the_process_is_still_preparing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    renewing = threading.Event()

    def watching(*_: object) -> None:
        renewing.set()

    def preparing() -> None:
        assert renewing.wait(timeout=5), "the claim thread had not started"
        raise RuntimeError("prepared")

    monkeypatch.setattr(process, "_keep_claim", watching)
    monkeypatch.setattr(process, "_prepare_process", preparing)
    claimed = ClaimedJob(uuid.uuid4(), "J-1", "tests.kind", [], 1)
    config = JobsConfig(slots=1, poll_seconds=0.2, lease_seconds=6, heartbeat_seconds=1)

    with pytest.raises(RuntimeError, match="prepared"):
        process.run_job(
            claimed, JobKind("tests.job_handlers:hang_telling_pid"), config, os.getpid()
        )
