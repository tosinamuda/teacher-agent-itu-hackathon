"""The conversations that are open, by the thread each belongs to.

A conversation stays open after its last message, so the next one continues it, and it is closed
when it has been idle a while, when another needs its place, and when the app stops. Closing
frees the agent's process, not its history: a writer that keeps its history under the thread's key
continues it when the conversation is opened again. Each conversation is owned by a task of its
own: the connections and the agent it holds are closed by the task that opened them, and the
messages reach that task through a queue.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass, field
from time import monotonic
from typing import Protocol

from app.domains.content_engine.domain.turn import TurnStoppedError
from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.engine import (
    Built,
    EngineIncompleteError,
    EngineRefusedError,
)
from app.domains.content_engine.infrastructure.tap import Tap, tapping
from app.domains.content_engine.infrastructure.tools import ExternalServerError
from app.domains.content_engine.infrastructure.writer import WriterStoppedError

#: How many conversations may be open at once: each holds an agent process.
LIMIT = 3
#: How long a conversation stays open with no message.
IDLE_SECONDS = 600.0

#: What a message can fail with and leave the conversation open to be continued.
_RECOVERABLE = (
    EngineRefusedError,
    EngineIncompleteError,
    WriterStoppedError,
    CheckerStoppedError,
    ExternalServerError,
)


class Speaker(Protocol):
    """What the registry needs of a conversation: it says a message, given what came before."""

    @property
    def stoppable(self) -> bool:
        """Whether the message in progress can be stopped now."""
        ...

    async def say(self, message: str, earlier: str = "", pointed: str = "") -> Built: ...

    async def stop(self) -> None: ...


Opener = Callable[[], AbstractAsyncContextManager[Speaker]]


class TooManyConversationsError(RuntimeError):
    """Every place for an open conversation is taken by one that is working."""


class _ClosedError(RuntimeError):
    """The conversation closed before it took the message."""


@dataclass
class _Pending:
    message: str
    earlier: str
    #: Where what the agent does in answering is reported, if anywhere.
    tap: Tap | None = None
    #: Text the teacher selected without saying where it is, to be found in the draft.
    pointed: str = ""
    done: asyncio.Future[Built] = field(
        default_factory=lambda: asyncio.get_running_loop().create_future()
    )


class _Live:
    """One open conversation and the task that owns it."""

    def __init__(self, idle: float) -> None:
        self.inbox: asyncio.Queue[_Pending | None] = asyncio.Queue()
        self.working = False
        self.used = monotonic()
        self._idle = idle
        self.task: asyncio.Task[None] | None = None
        self._speaker: Speaker | None = None
        self._turn: asyncio.Future[Built] | None = None
        self._stopping = False

    def start(self, opener: Opener, forget: Callable[[_Live], None]) -> None:
        self.task = asyncio.create_task(self._own(opener, forget))

    async def _own(self, opener: Opener, forget: Callable[[_Live], None]) -> None:
        try:
            async with opener() as speaker:
                await self._serve(speaker)
        except Exception as error:  # noqa: BLE001  (every waiting message is told why)
            self._refuse(error)
        finally:
            forget(self)
            self._refuse(_ClosedError("the conversation closed"))

    async def _serve(self, speaker: Speaker) -> None:
        while True:
            try:
                pending = await asyncio.wait_for(self.inbox.get(), self._idle)
            except TimeoutError:
                return
            if pending is None:
                return
            self.working = True
            self._speaker = speaker
            try:
                built = await self._run(speaker, pending)
            except TurnStoppedError as error:
                self._answer(pending, error=error)
            except _RECOVERABLE as error:
                self._answer(pending, error=error)
            except Exception as error:  # noqa: BLE001  (a broken conversation is closed)
                self._answer(pending, error=error)
                return
            else:
                self._answer(pending, built=built)
            finally:
                self.working = False
                self.used = monotonic()

    async def _run(self, speaker: Speaker, pending: _Pending) -> Built:
        """The message said as its own task, so the teacher can stop it without closing the chat."""
        with tapping(pending.tap):
            self._turn = asyncio.ensure_future(
                speaker.say(pending.message, pending.earlier, pending.pointed)
            )
            try:
                return await self._turn
            except asyncio.CancelledError:
                if self._stopping:
                    raise TurnStoppedError("the turn was stopped") from None
                raise
            finally:
                self._turn, self._stopping = None, False

    async def stop_turn(self) -> bool:
        """Stop the message in progress, and drop those waiting; whether one was in progress."""
        self._refuse(TurnStoppedError("the turn was stopped before it began"))
        turn, speaker = self._turn, self._speaker
        if turn is None or turn.done() or speaker is None or not speaker.stoppable:
            return False
        self._stopping = True
        with contextlib.suppress(Exception):
            await speaker.stop()
        turn.cancel()
        return True

    @staticmethod
    def _answer(
        pending: _Pending, *, built: Built | None = None, error: Exception | None = None
    ) -> None:
        if pending.done.done():
            return
        if error is not None:
            pending.done.set_exception(error)
        elif built is not None:
            pending.done.set_result(built)

    def _refuse(self, error: Exception) -> None:
        while not self.inbox.empty():
            pending = self.inbox.get_nowait()
            if pending is not None and not pending.done.done():
                pending.done.set_exception(error)

    def stop(self) -> None:
        self.inbox.put_nowait(None)


class LiveConversations:
    def __init__(self, *, limit: int = LIMIT, idle_seconds: float = IDLE_SECONDS) -> None:
        self._limit = limit
        self._idle = idle_seconds
        self._live: dict[str, _Live] = {}

    def is_open(self, key: str) -> bool:
        return key in self._live

    async def stop(self, key: str) -> bool:
        """Stop the message in progress in the conversation of ``key``, and drop those waiting.

        Says whether a message was in progress. The conversation stays open, and its agent keeps
        what it did, so the next message goes on from there.
        """
        live = self._live.get(key)
        return await live.stop_turn() if live is not None else False

    async def say(  # noqa: PLR0913  (a message, and what goes with it)
        self,
        key: str,
        opener: Opener,
        message: str,
        earlier: str = "",
        tap: Tap | None = None,
        pointed: str = "",
    ) -> Built:
        """Say ``message`` in the conversation of ``key``, opened with ``opener`` if it is not.

        ``earlier`` is what came before it, for an agent opened new that has not heard it. What
        the agent does in answering is reported to ``tap``. ``pointed`` is text the teacher
        selected without saying where it is, which the draft is searched for.
        """
        for _ in range(2):
            live = await self._for(key, opener)
            pending = _Pending(message, earlier, tap, pointed)
            live.inbox.put_nowait(pending)
            try:
                return await pending.done
            except _ClosedError:
                continue
        raise _ClosedError("the conversation closed twice")

    async def close_all(self) -> None:
        """Close every open conversation, as the app stops."""
        tasks = [live.task for live in self._live.values() if live.task is not None]
        for live in list(self._live.values()):
            live.stop()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _for(self, key: str, opener: Opener) -> _Live:
        if key in self._live:
            return self._live[key]
        await self._make_room()
        live = _Live(self._idle)
        self._live[key] = live
        live.start(opener, lambda gone: self._forget(key, gone))
        return live

    def _forget(self, key: str, gone: _Live) -> None:
        if self._live.get(key) is gone:
            del self._live[key]

    async def _make_room(self) -> None:
        while len(self._live) >= self._limit:
            idle = [live for live in self._live.values() if not live.working]
            if not idle:
                raise TooManyConversationsError("every open conversation is working")
            oldest = min(idle, key=lambda live: live.used)
            oldest.stop()
            if oldest.task is not None:
                with contextlib.suppress(Exception):
                    await oldest.task
