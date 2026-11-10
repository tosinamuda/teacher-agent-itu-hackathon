"""Comments on content, answered in the background by the agent that wrote it.

A comment goes to the content's revision thread, which keeps one agent open between turns, so
the agent continues from the comment before. An agent's turn takes minutes, so the comment is
taken at once and worked on after: the desk says whether it is working, how many comments wait,
and what failed. Comments in one chat run one at a time, in the order they came; chats on the
same content take turns where the work is done.
"""

from __future__ import annotations

import asyncio
from collections import deque
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass, field
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.service import RevisionRecord
from app.domains.content.application.errors import ContentError
from app.domains.content_engine.domain.turn import TurnStoppedError
from app.shared.json_types import JsonObject

Sessions = Callable[[], AbstractAsyncContextManager[AsyncSession]]


class Reviser(Protocol):
    """What the desk needs of the content service: to revise content from a comment."""

    async def revise(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        feedback: str,
        requested_by: str | None,
        highlight: JsonObject | None = None,
        chat_id: str | None = None,
    ) -> RevisionRecord: ...


@dataclass(frozen=True)
class Comment:
    text: str
    highlight: JsonObject | None
    requested_by: str | None


@dataclass
class _Standing:
    """What one chat's comments are doing."""

    waiting: deque[Comment] = field(default_factory=deque)
    working: bool = False
    error: str | None = None
    worker: asyncio.Task[None] | None = None


def _key(content_id: str, chat_id: str | None) -> str:
    return f"{content_id}|{chat_id or ''}"


class CommentDesk:
    def __init__(self, content: Callable[[], Reviser], sessions: Sessions) -> None:
        self._content = content
        self._sessions = sessions
        self._standing: dict[str, _Standing] = {}

    def take(self, content_id: str, comment: Comment, chat_id: str | None = None) -> int:
        """Take a comment to work on, and say how many are waiting, this one included."""
        standing = self._standing.setdefault(_key(content_id, chat_id), _Standing())
        standing.waiting.append(comment)
        if standing.worker is None or standing.worker.done():
            standing.worker = asyncio.create_task(self._work(content_id, chat_id, standing))
        return len(standing.waiting) + (1 if standing.working else 0)

    def drop_waiting(self, content_id: str, chat_id: str | None = None) -> int:
        """Drop the comments in a chat that have not begun; how many there were."""
        found = self._standing.get(_key(content_id, chat_id))
        if found is None:
            return 0
        dropped = len(found.waiting)
        found.waiting.clear()
        return dropped

    def standing(self, content_id: str, chat_id: str | None = None) -> JsonObject:
        """Whether the agent is working on a comment, how many wait, and the last failure."""
        found = self._standing.get(_key(content_id, chat_id))
        if found is None:
            return {"working": False, "waiting": 0, "error": None}
        return {"working": found.working, "waiting": len(found.waiting), "error": found.error}

    async def close(self) -> None:
        """Stop working, as the app stops; a comment not yet answered is lost."""
        workers = [s.worker for s in self._standing.values() if s.worker is not None]
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    async def _work(self, content_id: str, chat_id: str | None, standing: _Standing) -> None:
        while standing.waiting:
            comment = standing.waiting.popleft()
            standing.working = True
            try:
                async with self._sessions() as db:
                    await self._content().revise(
                        db,
                        content_id=content_id,
                        feedback=comment.text,
                        requested_by=comment.requested_by,
                        highlight=comment.highlight,
                        chat_id=chat_id,
                    )
                standing.error = None
            except TurnStoppedError:
                standing.error = None
            except ContentError as error:
                standing.error = error.detail
            except Exception as error:  # noqa: BLE001  (the agent's failure is the teacher's to read)
                standing.error = str(error) or type(error).__name__
            finally:
                standing.working = False
