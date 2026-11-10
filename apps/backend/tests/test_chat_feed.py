"""A chat's events: kept in order for a page to replay, and shown live to whoever is watching."""

from __future__ import annotations

import asyncio

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed, StoredEvent
from app.domains.artefact_revision.application.chat_stream import frame, stream
from app.domains.artefact_revision.models.revision import ChatEvent, RevisionThread
from tests.chat_support import feed_over

pytestmark = pytest.mark.asyncio

THREAD = "RVT-feed-1"


async def _thread(db: AsyncSession) -> None:
    db.add(
        RevisionThread(revision_thread_id=THREAD, artefact_type="engine", subject_id="C-1", slot=0)
    )
    await db.flush()


class _Page:
    """A page that reads frames until told it has gone."""

    def __init__(self) -> None:
        self.gone = False

    async def disconnected(self) -> bool:
        return self.gone


async def _read(feed: ChatFeed, page: _Page, after: int = 0, **kw: object) -> list[str]:
    frames: list[str] = []
    async for each in stream(feed, THREAD, after, page.disconnected, **kw):  # type: ignore[arg-type]
        frames.append(each)
    return frames


async def test_kept_events_come_back_in_order_after_the_one_a_page_last_saw(
    db: AsyncSession,
) -> None:
    await _thread(db)
    feed = feed_over(db)
    first = await feed.record(THREAD, "user_message", {"text": "Simpler."})
    await feed.record(THREAD, "agent_text", {"text": "Simplified."})
    await feed.record(THREAD, "turn_done", {"summary": "Simplified."})

    everything = await feed.since(THREAD, 0)
    later = await feed.since(THREAD, first.seq or 0)

    assert [e.kind for e in everything] == ["user_message", "agent_text", "turn_done"]
    assert [e.kind for e in later] == ["agent_text", "turn_done"]
    assert everything[0].seq is not None and everything[0].seq < everything[1].seq  # type: ignore[operator]


async def test_the_stream_replays_what_was_kept_then_shows_what_happens_next(
    db: AsyncSession,
) -> None:
    await _thread(db)
    feed, page = feed_over(db), _Page()
    await feed.record(THREAD, "user_message", {"text": "Simpler."})
    reading = asyncio.create_task(_read(feed, page, poll=0.05))
    await asyncio.sleep(0.1)

    feed.show(THREAD, "partial", {"part_id": "p1", "text": "Simpl"})
    done = await feed.record(THREAD, "turn_done", {"summary": "Done."})
    await asyncio.sleep(0.2)
    page.gone = True
    frames = await asyncio.wait_for(reading, timeout=3)

    assert frames[0].startswith("id: ") and "event: user_message" in frames[0]
    assert any("event: partial" in f and not f.startswith("id:") for f in frames)
    assert any(f.startswith(f"id: {done.seq}\n") and "event: turn_done" in f for f in frames)


async def test_a_page_that_comes_back_is_sent_only_what_it_missed(db: AsyncSession) -> None:
    await _thread(db)
    feed, page = feed_over(db), _Page()
    seen = await feed.record(THREAD, "user_message", {"text": "One."})
    await feed.record(THREAD, "turn_done", {"summary": "Two."})
    reading = asyncio.create_task(_read(feed, page, after=seen.seq or 0, poll=0.05))
    await asyncio.sleep(0.15)
    page.gone = True
    frames = await asyncio.wait_for(reading, timeout=3)

    assert len([f for f in frames if "event:" in f]) == 1 and "turn_done" in frames[0]


async def test_a_quiet_stream_sends_a_keep_alive_line_and_a_chat_with_no_events_sends_its_turns(
    db: AsyncSession,
) -> None:
    await _thread(db)
    feed, page = feed_over(db), _Page()
    earlier = [StoredEvent(None, "user_message", {"text": "Older."})]
    reading = asyncio.create_task(_read(feed, page, earlier=earlier, poll=0.02, beat=0.05))
    await asyncio.sleep(0.2)
    page.gone = True
    frames = await asyncio.wait_for(reading, timeout=3)

    assert "event: user_message" in frames[0] and not frames[0].startswith("id:")
    assert ": keep-alive\n\n" in frames


async def test_an_event_kept_by_another_process_is_found_by_reading(db: AsyncSession) -> None:
    await _thread(db)
    feed, page = feed_over(db), _Page()
    reading = asyncio.create_task(_read(feed, page, poll=0.05))
    await asyncio.sleep(0.1)

    thread_db_id = await db.scalar(
        select(RevisionThread.id).where(RevisionThread.revision_thread_id == THREAD)
    )
    db.add(ChatEvent(thread_db_id=thread_db_id, kind="agent_text", data={"text": "From afar."}))
    await db.flush()
    await asyncio.sleep(0.2)
    page.gone = True
    frames = await asyncio.wait_for(reading, timeout=3)

    assert any("From afar." in f for f in frames)


async def test_a_frame_has_an_id_only_when_the_event_was_kept() -> None:
    assert frame(StoredEvent(7, "turn_done", {"a": 1})) == (
        'id: 7\nevent: turn_done\ndata: {"a": 1}\n\n'
    )
    assert frame(StoredEvent(None, "partial", {"a": 1})) == 'event: partial\ndata: {"a": 1}\n\n'
