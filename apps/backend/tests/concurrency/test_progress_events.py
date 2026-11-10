"""Live progress crosses from a job's process to the API through one table.

Against the real database: the publisher writes on its own connection, as a job's process
does, and a watcher reads what is new on its channel.
"""

from __future__ import annotations

import time
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import update

from app.db.session import engine
from app.infra import progress
from app.infra.progress import ProgressEvent
from app.main import app
from app.shared.time import utc_now


async def _settle(session_factory) -> None:
    """Age every event past the moment a watcher waits for it to commit."""
    async with session_factory() as session:
        await session.execute(
            update(ProgressEvent).values(created_at=utc_now() - timedelta(seconds=5))
        )
        await session.commit()


@pytest.mark.asyncio
async def test_a_watcher_sees_only_what_is_reported_after_it_connects(session_factory) -> None:
    progress.publish("synthetic:EXP-1", {"phase": "before"})
    async with session_factory() as session:
        seen = await progress.latest(session, "synthetic:EXP-1")

    progress.publish("synthetic:EXP-1", {"phase": "rating", "done": 1})
    progress.publish("synthetic:EXP-2", {"phase": "elsewhere"})
    progress.publish("synthetic:EXP-1", {"phase": "rating", "done": 2})
    await _settle(session_factory)

    async with session_factory() as session:
        events = await progress.after(session, "synthetic:EXP-1", seen)
    assert [payload for _id, payload in events] == [
        {"phase": "rating", "done": 1},
        {"phase": "rating", "done": 2},
    ]


@pytest.mark.asyncio
async def test_an_event_just_written_waits_until_it_has_settled(session_factory) -> None:
    """A lower id may still be committing beside it; reading it now could skip that one."""
    progress.publish("synthetic:EXP-1", {"phase": "fresh"})

    async with session_factory() as session:
        assert await progress.after(session, "synthetic:EXP-1", 0) == []

    await _settle(session_factory)
    async with session_factory() as session:
        assert len(await progress.after(session, "synthetic:EXP-1", 0)) == 1


@pytest.mark.asyncio
async def test_events_older_than_a_day_are_forgotten(session_factory, count_rows) -> None:
    progress.publish("synthetic:EXP-1", {"phase": "old"})
    async with session_factory() as session:
        await session.execute(
            update(ProgressEvent).values(created_at=utc_now() - timedelta(days=2))
        )
        await session.commit()
    progress.publish("synthetic:EXP-1", {"phase": "new"})

    async with session_factory() as session:
        await progress.forget_old(session)

    assert await count_rows(ProgressEvent) == 1


@pytest.mark.asyncio
async def test_a_lost_progress_event_never_fails_the_work(monkeypatch) -> None:
    def _down(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise ConnectionError("database away")

    monkeypatch.setattr(progress.sync_engine, "begin", _down)

    progress.publish("synthetic:EXP-1", {"phase": "rating"})


def test_the_experiment_websocket_relays_what_a_job_reports(session_factory) -> None:
    """The route a researcher's page opens, fed by a publisher on another connection."""
    del session_factory  # the fixture empties the tables around the test
    try:
        with TestClient(app).websocket_connect("/experiments/EXP-1/synthetic/ws") as socket:
            time.sleep(1)  # the relay has read where the channel stood when it connected
            progress.publish("synthetic:EXP-1", {"flow": "generation", "type": "condition_done"})

            assert socket.receive_json() == {"flow": "generation", "type": "condition_done"}
    finally:
        # The relay pooled connections on the test client's own loop, which is closed now;
        # abandon them rather than let a later test check one out.
        engine.sync_engine.dispose(close=False)
