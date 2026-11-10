"""A page comments on content and watches the agent answer: the tools, and the desk behind them."""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.service import RevisionRecord
from app.domains.artefact_revision.models.revision import RevisionThread, RevisionTurn
from app.domains.content.application.errors import ContentError
from app.domains.content.infrastructure import wiring
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.content_engine.application.comments import CommentDesk
from app.domains.content_engine.infrastructure.content import SqlAlchemyEngineContent
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.live import LiveConversations
from app.domains.content_engine.infrastructure.revision import EngineRevisionExecutor
from app.domains.content_engine.infrastructure.wiring import build_drafting_service
from app.domains.content_engine.infrastructure.writer import WriterStoppedError, text_of
from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.content_engine.mcp.server import build_content_mcp
from app.domains.content_engine.mcp.viewer import _VIEWER_HTML
from app.shared.json_types import JsonObject
from tests.content_engine_support import (
    PLAN,
    TYPE,
    ScriptedWriter,
    engine_over,
    part,
    seed_lesson,
    server_over,
)
from tests.conversation_support import Kept

pytestmark = pytest.mark.asyncio

POINTED: JsonObject = {"unit_id": "s2", "path": "examples.0.solution", "selected_text": "3/4"}


class _Reviser:
    """Stands in for the agent: it records what it was asked and how many ran at once."""

    def __init__(self, delay: float = 0.0, gate: asyncio.Event | None = None) -> None:
        self.asked: list[tuple[str, JsonObject | None]] = []
        self.delay = delay
        #: When set, a revision waits until the test opens it.
        self.gate = gate
        self.fail: Exception | None = None
        self._running = 0
        self.most_at_once = 0

    async def revise(
        self,
        db: AsyncSession,
        *,
        content_id: str,
        feedback: str,
        requested_by: str | None,
        highlight: JsonObject | None = None,
        chat_id: str | None = None,
    ) -> RevisionRecord:
        self._running += 1
        self.most_at_once = max(self.most_at_once, self._running)
        try:
            if self.gate is not None:
                await self.gate.wait()
            await asyncio.sleep(self.delay)
            if self.fail is not None:
                raise self.fail
            self.asked.append((feedback, highlight))
            return RevisionRecord(
                len(self.asked), feedback, "Done.", None, datetime.now(timezone.utc)
            )
        finally:
            self._running -= 1


@asynccontextmanager
async def _server(db: AsyncSession, reviser: _Reviser) -> AsyncIterator[tuple[Client, CommentDesk]]:
    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    desk = CommentDesk(lambda: reviser, same_session)
    server = build_content_mcp(
        drafting=build_drafting_service,
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
        comments=desk,
    )
    with as_the_app():
        async with Client(server) as client:
            yield client, desk
    await desk.close()


async def _content(db: AsyncSession) -> str:
    await seed_lesson(db)
    built = await engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )
    return built.saved_as


async def _quiet(desk: CommentDesk, content_id: str) -> None:
    for _ in range(200):
        standing = desk.standing(content_id)
        if not standing["working"] and not standing["waiting"]:
            return
        await asyncio.sleep(0.01)
    raise AssertionError("the desk never went quiet")


async def _state(client: Client, content_id: str) -> dict[str, Any]:
    shown = await client.call_tool("conversation_state", {"content_id": content_id})
    state = json.loads(text_of(shown))
    assert isinstance(state, dict)
    return state


async def test_a_comment_is_taken_at_once_and_the_agent_works_on_it_after(db: AsyncSession) -> None:
    content_id = await _content(db)
    gate = asyncio.Event()
    reviser = _Reviser(gate=gate)
    async with _server(db, reviser) as (client, desk):
        taken = await client.call_tool(
            "comment_on_content",
            {"content_id": content_id, "comment": "Simpler.", **POINTED},
        )
        working = await _state(client, content_id)
        gate.set()
        await _quiet(desk, content_id)
        after = await _state(client, content_id)

    assert json.loads(text_of(taken)) == {
        "content_id": content_id,
        "accepted": True,
        "waiting": 1,
    }
    assert working["working"] is True
    assert (after["working"], after["waiting"], after["error"]) == (False, 0, None)
    assert reviser.asked == [("Simpler.", POINTED)]


async def test_comments_on_one_content_are_worked_one_at_a_time_in_order(db: AsyncSession) -> None:
    content_id = await _content(db)
    reviser = _Reviser(delay=0.03)
    async with _server(db, reviser) as (client, desk):
        for text in ("one", "two", "three"):
            await client.call_tool(
                "comment_on_content", {"content_id": content_id, "comment": text}
            )
        await _quiet(desk, content_id)

    assert [asked[0] for asked in reviser.asked] == ["one", "two", "three"]
    assert reviser.most_at_once == 1


async def test_a_failure_is_told_to_the_page_and_cleared_by_the_next_comment(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    reviser = _Reviser()
    async with _server(db, reviser) as (client, desk):
        reviser.fail = ContentError(409, "lesson_concluded")
        await client.call_tool("comment_on_content", {"content_id": content_id, "comment": "x"})
        await _quiet(desk, content_id)
        failed = await _state(client, content_id)
        reviser.fail = WriterStoppedError("the writer stopped: out of turns")
        await client.call_tool("comment_on_content", {"content_id": content_id, "comment": "y"})
        await _quiet(desk, content_id)
        stopped = await _state(client, content_id)
        reviser.fail = None
        await client.call_tool("comment_on_content", {"content_id": content_id, "comment": "z"})
        await _quiet(desk, content_id)
        recovered = await _state(client, content_id)

    assert failed["error"] == "lesson_concluded"
    assert "out of turns" in str(stopped["error"])
    assert recovered["error"] is None


async def test_the_state_carries_the_version_the_review_status_and_each_turn_with_where_it_pointed(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    record = await build_content_service().record(db, content_id)
    thread = RevisionThread(
        revision_thread_id="RT-1", artefact_type=record.kind, subject_id=content_id, created_by=None
    )
    db.add(thread)
    await db.flush()
    db.add(
        RevisionTurn(
            revision_turn_id="RTN-1",
            thread_db_id=thread.id,
            turn_number=1,
            instruction="Simpler.",
            highlight=POINTED,
            summary="Shortened it.",
            validation_passed=True,
        )
    )
    await db.flush()

    async with _server(db, _Reviser()) as (client, _):
        state = await _state(client, content_id)

    assert (state["version"], state["review_status"]) == (1, "pending")
    assert state["turns"][0]["comment"] == "Simpler."
    assert state["turns"][0]["highlight"] == POINTED
    assert state["turns"][0]["summary"] == "Shortened it."


async def test_a_comment_that_is_empty_or_too_long_is_refused_and_so_is_content_that_is_not_there(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    async with _server(db, _Reviser()) as (client, _):
        empty = await client.call_tool(
            "comment_on_content", {"content_id": content_id, "comment": " "}
        )
        long = await client.call_tool(
            "comment_on_content", {"content_id": content_id, "comment": "x" * 4001}
        )
        missing = await client.call_tool(
            "comment_on_content", {"content_id": "AT-none", "comment": "x"}
        )

    assert empty.is_error and long.is_error and missing.is_error


async def test_a_caller_who_has_not_signed_in_is_refused(db: AsyncSession) -> None:
    content_id = await _content(db)

    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    desk = CommentDesk(lambda: _Reviser(), same_session)
    server = build_content_mcp(
        drafting=build_drafting_service,
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
        comments=desk,
    )
    async with Client(server) as client:
        commented = await client.call_tool(
            "comment_on_content", {"content_id": content_id, "comment": "x"}
        )
        state = await client.call_tool("conversation_state", {"content_id": content_id})

    assert commented.is_error and "Sign in" in text_of(commented)
    assert state.is_error
    assert desk.standing(content_id)["waiting"] == 0


async def test_comments_reach_one_kept_agent_and_each_saves_the_next_version(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    content_id = await _content(db)
    writer, live = Kept([("s2", "B, simpler"), ("s1", "A, clearer")]), LiveConversations()
    engine = Engine(lambda: server_over(db), lambda: writer)
    catalogue = build_content_catalogue()
    monkeypatch.setattr(
        wiring,
        "build_engine_revision_executor",
        lambda: EngineRevisionExecutor(engine, SqlAlchemyEngineContent(), catalogue, live),
    )

    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    desk = CommentDesk(build_content_service, same_session)
    server = build_content_mcp(
        drafting=build_drafting_service,
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
        comments=desk,
    )
    with as_the_app():
        async with Client(server) as client:
            await client.call_tool(
                "comment_on_content", {"content_id": content_id, "comment": "Simpler.", **POINTED}
            )
            await _quiet(desk, content_id)
            await client.call_tool(
                "comment_on_content", {"content_id": content_id, "comment": "Clearer."}
            )
            await _quiet(desk, content_id)
            state = await _state(client, content_id)
    await desk.close()
    await live.close_all()

    turns = state["turns"]
    assert isinstance(turns, list) and all(isinstance(turn, dict) for turn in turns)
    assert (state["version"], state["error"], len(turns)) == (3, None, 2)
    assert [turn["comment"] for turn in turns if isinstance(turn, dict)] == ["Simpler.", "Clearer."]
    first = turns[0]
    assert isinstance(first, dict) and first["highlight"] == POINTED
    assert writer.events == ["opened", "closed"]


async def test_the_page_calls_only_tools_the_server_has(db: AsyncSession) -> None:
    page = _VIEWER_HTML
    called = set(re.findall(r'const (?:COMMENT|STATE|CONTENT) = "([a-z_]+)"', page))

    async with _server(db, _Reviser()) as (client, _):
        offered = {tool.name for tool in (await client.list_tools()).tools}

    assert called == {"comment_on_content", "conversation_state", "show_content"}
    assert called <= offered
    assert "<!--conversation-->" not in page
