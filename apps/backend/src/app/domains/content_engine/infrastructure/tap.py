"""What a chat hears of an agent at work: its text as it is written, its tools, its views.

A run of the agent reports each thing to the tap of the message it is answering, when there is
one. The tap is the message's, not the agent's, so one agent answering many messages reports each
to its own chat. A harness that has no events to report leaves the tap unused.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Protocol

from app.shared.json_types import JsonObject

#: Kept in the chat's transcript; the page replays it. The rest is only for a page that is
#: watching: the text so far, and whether the agent is busy.
PERSISTED = frozenset(
    {
        "user_message",
        "agent_text",
        "thinking",
        "tool",
        "view",
        "turn_done",
        "turn_failed",
        "turn_stopped",
    }
)


@dataclass(frozen=True)
class AgentChatEvent:
    kind: str
    data: JsonObject

    @property
    def persisted(self) -> bool:
        return self.kind in PERSISTED


class Tap(Protocol):
    async def emit(self, event: AgentChatEvent) -> None: ...


@dataclass(frozen=True)
class TapGroup:
    """Several taps that hear the same events."""

    taps: tuple[Tap, ...]

    async def emit(self, event: AgentChatEvent) -> None:
        for tap in self.taps:
            await tap.emit(event)


_CURRENT: ContextVar[Tap | None] = ContextVar("chat_tap", default=None)


@contextmanager
def tapping(tap: Tap | None) -> Iterator[None]:
    """Report what the agent does in this block to ``tap``."""
    token = _CURRENT.set(tap)
    try:
        yield
    finally:
        _CURRENT.reset(token)


def current_tap() -> Tap | None:
    return _CURRENT.get()


async def emit(kind: str, data: JsonObject) -> None:
    """Report to the tap of the message being answered, if there is one."""
    if (tap := _CURRENT.get()) is not None:
        await tap.emit(AgentChatEvent(kind, data))
