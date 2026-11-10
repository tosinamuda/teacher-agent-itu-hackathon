"""Open conversations: kept for the next message, closed when idle, crowded out, or at stop."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import pytest

from app.domains.content_engine.domain.turn import TurnStoppedError
from app.domains.content_engine.infrastructure.engine import Built, EngineIncompleteError
from app.domains.content_engine.infrastructure.live import (
    LiveConversations,
    Opener,
    Speaker,
    TooManyConversationsError,
)

pytestmark = pytest.mark.asyncio


class _Chat:
    """A conversation that answers with what it was told, and that can be made to fail."""

    def __init__(self, journal: list[str], name: str, delay: float = 0.0) -> None:
        self.journal = journal
        self.name = name
        self.delay = delay
        self.fail: Exception | None = None
        self.stoppable = True

    async def stop(self) -> None:
        self.journal.append(f"stop {self.name}")

    async def say(self, message: str, earlier: str = "", pointed: str = "") -> Built:
        self.journal.append(f"{self.name}: {message}" + (f" (after {earlier})" if earlier else ""))
        await asyncio.sleep(self.delay)
        if self.fail is not None:
            raise self.fail
        return Built("C-1", f"heard {message}", {})


class _Desk:
    """Opens `_Chat`s and records when each is opened and closed."""

    def __init__(self, delay: float = 0.0) -> None:
        self.journal: list[str] = []
        self.opened: list[_Chat] = []
        self.delay = delay

    def opener(self, name: str) -> Opener:
        @asynccontextmanager
        async def open_() -> AsyncIterator[Speaker]:
            chat = _Chat(self.journal, name, self.delay)
            self.opened.append(chat)
            self.journal.append(f"open {name}")
            try:
                yield chat
            finally:
                self.journal.append(f"close {name}")

        return open_


async def test_a_message_continues_the_open_conversation_and_carries_what_came_before() -> None:
    desk, live = _Desk(), LiveConversations()

    one = await live.say("t1", desk.opener("a"), "one", "turn 1")
    two = await live.say("t1", desk.opener("a"), "two")
    await live.close_all()

    assert (one.summary, two.summary) == ("heard one", "heard two")
    assert desk.journal == ["open a", "a: one (after turn 1)", "a: two", "close a"]


async def test_messages_to_one_conversation_are_taken_one_at_a_time_in_order() -> None:
    desk, live = _Desk(delay=0.02), LiveConversations()

    answers = await asyncio.gather(*(live.say("t1", desk.opener("a"), f"m{i}") for i in range(3)))
    await live.close_all()

    assert [a.summary for a in answers] == ["heard m0", "heard m1", "heard m2"]
    assert desk.journal[0] == "open a" and len(desk.opened) == 1


async def test_an_idle_conversation_closes_and_the_next_message_opens_another() -> None:
    desk, live = _Desk(), LiveConversations(idle_seconds=0.05)

    await live.say("t1", desk.opener("a"), "first")
    await asyncio.sleep(0.2)
    assert not live.is_open("t1")
    await live.say("t1", desk.opener("b"), "first")
    await live.close_all()

    assert desk.journal == ["open a", "a: first", "close a", "open b", "b: first", "close b"]


async def test_the_oldest_idle_one_makes_room_and_a_working_one_is_not_closed() -> None:
    desk, live = _Desk(), LiveConversations(limit=1)
    await live.say("t1", desk.opener("a"), "x")

    await live.say("t2", desk.opener("b"), "y")
    assert desk.journal == ["open a", "a: x", "close a", "open b", "b: y"]

    slow = _Desk(delay=0.3)
    busy = LiveConversations(limit=1)
    working = asyncio.create_task(busy.say("t1", slow.opener("a"), "x"))
    await asyncio.sleep(0.1)
    with pytest.raises(TooManyConversationsError):
        await busy.say("t2", slow.opener("b"), "y")
    await working
    await asyncio.gather(live.close_all(), busy.close_all())


async def test_a_message_that_can_be_retried_leaves_the_conversation_open() -> None:
    desk, live = _Desk(), LiveConversations()
    await live.say("t1", desk.opener("a"), "x")
    desk.opened[0].fail = EngineIncompleteError("left units without a part")

    with pytest.raises(EngineIncompleteError):
        await live.say("t1", desk.opener("a"), "again")
    desk.opened[0].fail = None
    await live.say("t1", desk.opener("a"), "once more")
    await live.close_all()

    assert len(desk.opened) == 1
    assert desk.journal[-2:] == ["a: once more", "close a"]


async def test_a_message_that_breaks_the_conversation_closes_it() -> None:
    desk, live = _Desk(), LiveConversations()
    await live.say("t1", desk.opener("a"), "x")
    desk.opened[0].fail = ConnectionError("the agent went away")

    with pytest.raises(ConnectionError):
        await live.say("t1", desk.opener("a"), "again")
    await asyncio.sleep(0.05)
    assert not live.is_open("t1")
    await live.say("t1", desk.opener("b"), "fresh")
    await live.close_all()

    assert len(desk.opened) == 2


async def test_a_conversation_that_cannot_be_opened_says_why() -> None:
    live = LiveConversations()

    @asynccontextmanager
    async def refuses() -> AsyncIterator[Speaker]:
        raise LookupError("no such content")
        yield  # pragma: no cover

    with pytest.raises(LookupError, match="no such content"):
        await live.say("t1", refuses, "x")
    assert not live.is_open("t1")


async def test_a_message_in_progress_can_be_stopped_and_the_conversation_goes_on() -> None:
    desk, live = _Desk(delay=5.0), LiveConversations()
    working = asyncio.create_task(live.say("t1", desk.opener("a"), "slow"))
    await asyncio.sleep(0.1)

    stopped = await live.stop("t1")
    with pytest.raises(TurnStoppedError):
        await working
    desk.opened[0].delay = 0.0
    after = await live.say("t1", desk.opener("a"), "again")
    await live.close_all()

    assert stopped is True and after.summary == "heard again"
    assert desk.journal == ["open a", "a: slow", "stop a", "a: again", "close a"]


async def test_messages_waiting_behind_the_one_stopped_are_dropped() -> None:
    desk, live = _Desk(delay=5.0), LiveConversations()
    first = asyncio.create_task(live.say("t1", desk.opener("a"), "first"))
    await asyncio.sleep(0.1)
    second = asyncio.create_task(live.say("t1", desk.opener("a"), "second"))
    await asyncio.sleep(0.1)

    await live.stop("t1")

    for waiting in (first, second):
        with pytest.raises(TurnStoppedError):
            await waiting
    await live.close_all()
    assert "a: second" not in desk.journal


async def test_there_is_nothing_to_stop_in_a_conversation_that_is_idle_or_not_open() -> None:
    desk, live = _Desk(), LiveConversations()
    await live.say("t1", desk.opener("a"), "x")

    assert await live.stop("t1") is False
    assert await live.stop("nobody") is False
    await live.close_all()


async def test_a_message_that_cannot_be_stopped_runs_on() -> None:
    desk, live = _Desk(delay=0.3), LiveConversations()
    working = asyncio.create_task(live.say("t1", desk.opener("a"), "saving"))
    await asyncio.sleep(0.1)
    desk.opened[0].stoppable = False

    stopped = await live.stop("t1")
    answer = await working
    await live.close_all()

    assert stopped is False and answer.summary == "heard saving"
