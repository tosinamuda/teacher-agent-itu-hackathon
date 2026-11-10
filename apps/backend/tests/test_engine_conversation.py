"""Content kept open with one writer: each message revises the latest version and saves the next."""

from __future__ import annotations

import asyncio
import re
import shutil
import time
from collections.abc import Callable
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content_engine.domain.turn import TurnStoppedError
from app.domains.content_engine.infrastructure.chat import HeldTap
from app.domains.content_engine.infrastructure.engine import Engine, EngineRefusedError, Request
from app.domains.content_engine.infrastructure.harness import opencode
from app.domains.content_engine.infrastructure.harness.opencode import OpenCodeWriter
from app.domains.content_engine.infrastructure.harness.opencode_server import Model
from app.domains.content_engine.infrastructure.live import LiveConversations
from app.domains.content_engine.infrastructure.tap import tapping
from tests.content_engine_support import (
    PLAN,
    TYPE,
    ScriptedWriter,
    engine_over,
    part,
    seed_lesson,
    server_over,
)
from tests.conversation_support import Kept, Messages
from tests.harness_script import message_text
from tests.openai_stub import Reply, answer, stub_model, tool_call

pytestmark = pytest.mark.asyncio


async def _first_version(db: AsyncSession) -> str:
    built = await engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )
    return built.saved_as


async def _titles(db: AsyncSession, content_id: str) -> tuple[int, list[str]]:
    record = await SqlAlchemyContentRecords().get(db, content_id)
    assert record is not None
    return record.version, [s["part"]["title"] for s in record.manifest["sections"]]


async def test_each_message_saves_the_next_version_of_the_same_content(db: AsyncSession) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    writer = Messages([("s2", "B, simpler"), ("s1", "A, clearer")])
    engine = Engine(lambda: server_over(db), lambda: writer)

    async with engine.converse(
        Request(TYPE, plan_version_id=PLAN, content_id=content_id), key="T-1"
    ) as chat:
        first = await chat.say("Simpler s2.")
        second = await chat.say("Clearer s1.")

    assert (first.saved_as, second.saved_as) == (content_id, content_id)
    assert writer.heard == ["Simpler s2.", "Clearer s1."]
    assert await _titles(db, content_id) == (3, ["A, clearer", "B, simpler"])


async def test_a_writer_that_keeps_its_agent_is_opened_once_and_closed_with_the_conversation(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    writer = Kept([("s2", "B, simpler"), ("s1", "A, clearer")])
    engine = Engine(lambda: server_over(db), lambda: writer)

    async with engine.converse(
        Request(TYPE, plan_version_id=PLAN, content_id=content_id), key="T-1"
    ) as chat:
        await chat.say("Simpler s2.")
        await chat.say("Clearer s1.")
        assert writer.events == ["opened"]

    assert writer.events == ["opened", "closed"]


async def test_a_conversation_is_about_content_that_exists(db: AsyncSession) -> None:
    await seed_lesson(db)
    engine = engine_over(db, ScriptedWriter({}))

    with pytest.raises(EngineRefusedError, match="content that exists"):
        async with engine.converse(Request(TYPE, plan_version_id=PLAN), key="T-1"):
            pass


def _plan(turns: list[list[tuple[str, str]]], summaries: list[str]) -> Reply:
    """A model that revises the units each user message asks for, then summarises the turn."""

    def drafts(body: dict[str, Any]) -> list[str]:
        users = [message_text(m) for m in body["messages"] if m["role"] == "user"]
        return [
            found.group(1)
            for found in (re.search(r"## draft_id\s+(\S+)", u) for u in users)
            if found
        ]

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        messages = body["messages"]
        last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
        turn = sum(1 for m in messages if m["role"] == "user") - 1
        done = sum(1 for m in messages[last_user:] if m["role"] == "tool")
        if done >= len(turns[turn]):
            return answer(summaries[turn])
        unit, title = turns[turn][done]
        arguments = {"draft_id": drafts(body)[-1], "unit_id": unit, "part": part(title)}
        return tool_call("engine_revise_part", arguments, call_id=f"call-{turn}-{done}")

    return reply


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_opencode_keeps_one_session_so_a_message_continues_from_the_last(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    opened: list[str] = []
    real = opencode.served

    def counting(*arguments: Any, **keywords: Any) -> Any:
        opened.append("served")
        return real(*arguments, **keywords)

    monkeypatch.setattr(opencode, "served", counting)
    script = _plan(
        [[("s2", "B, simpler")], [("s1", "A, clearer")]], ["Simplified s2.", "Clarified s1."]
    )
    with stub_model(script) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(lambda: server_over(db), lambda: OpenCodeWriter(model))
        request = Request(TYPE, plan_version_id=PLAN, content_id=content_id)
        async with engine.converse(request, key="T-1") as chat:
            first = await chat.say("Simpler s2.")
            second = await chat.say("Clearer s1.")

    assert (first.summary, second.summary) == ("Simplified s2.", "Clarified s1.")
    assert opened == ["served"]
    assert await _titles(db, content_id) == (3, ["A, clearer", "B, simpler"])
    second_turn = next(
        body
        for body in stub.requests
        if sum(1 for m in body["messages"] if m["role"] == "user") == 2
    )
    users = [message_text(m) for m in second_turn["messages"] if m["role"] == "user"]
    assert "## lesson" in users[0] and "## lesson" not in users[1]
    assert "Simpler s2." in users[0] and "Clearer s1." in users[1]
    assert any(
        m["role"] == "assistant" and "Simplified s2." in message_text(m)
        for m in second_turn["messages"]
    )


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_a_conversation_opened_again_continues_the_session_the_last_one_left(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    script = _plan(
        [[("s2", "B, simpler")], [("s1", "A, clearer")]], ["Simplified s2.", "Clarified s1."]
    )
    with stub_model(script) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(lambda: server_over(db), lambda: OpenCodeWriter(model))
        request = Request(TYPE, plan_version_id=PLAN, content_id=content_id)
        async with engine.converse(request, key="T-1") as chat:
            await chat.say("Simpler s2.", "1. asked: shorter")
        async with engine.converse(request, key="T-1") as chat:
            second = await chat.say("Clearer s1.", "1. asked: shorter\n2. asked: Simpler s2.")

    assert second.summary == "Clarified s1."
    assert await _titles(db, content_id) == (3, ["A, clearer", "B, simpler"])
    resumed = next(
        body
        for body in stub.requests
        if sum(1 for m in body["messages"] if m["role"] == "user") == 2
    )
    users = [message_text(m) for m in resumed["messages"] if m["role"] == "user"]
    assert "## lesson" in users[0] and "## lesson" not in users[1]
    assert "1. asked: shorter" in users[0] and "asked:" not in users[1]
    assert "Clearer s1." in users[1]


async def test_content_made_with_instructions_is_saved_with_the_first_message_as_feedback(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    writer = ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})
    request = Request(TYPE, plan_version_id=PLAN, feedback="Two steps, plainly.")

    built = await engine_over(db, writer).build_kept(request, key="new-1")

    assert writer.seen["feedback"] == "Two steps, plainly."
    assert await _titles(db, built.saved_as) == (1, ["A", "B"])


def _creation_then_revision(body: dict[str, Any]) -> dict[str, Any]:
    """Add each step's part in the first message, then revise one in the second."""
    messages = body["messages"]
    users = [message_text(m) for m in messages if m["role"] == "user"]
    draft = re.findall(r"## draft_id\s+(\S+)", " ".join(users))[-1]
    last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
    done = sum(1 for m in messages[last_user:] if m["role"] == "tool")
    if len(users) == 1:
        if done >= 2:
            return answer("Wrote both steps.")
        unit, title = [("s1", "A"), ("s2", "B")][done]
        arguments = {"draft_id": draft, "unit_id": unit, "part": part(title)}
        return tool_call("engine_add_part", arguments, call_id=f"add-{done}")
    if done >= 1:
        return answer("Clarified s1.")
    arguments = {"draft_id": draft, "unit_id": "s1", "part": part("A, clearer")}
    return tool_call("engine_revise_part", arguments, call_id="revise-1")


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_a_comment_under_the_key_the_content_was_made_with_goes_to_the_same_agent(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    with stub_model(_creation_then_revision) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(lambda: server_over(db), lambda: OpenCodeWriter(model))
        made = await engine.build_kept(
            Request(TYPE, plan_version_id=PLAN, feedback="Two steps."), key="new-1"
        )
        revised_request = Request(TYPE, plan_version_id=PLAN, content_id=made.saved_as)
        async with engine.converse(revised_request, key="new-1") as chat:
            second = await chat.say("Clearer s1.", "1. asked: Two steps.")

    assert second.summary == "Clarified s1."
    assert await _titles(db, made.saved_as) == (2, ["A, clearer", "B"])
    revising = next(
        body
        for body in stub.requests
        if sum(1 for m in body["messages"] if m["role"] == "user") == 2
    )
    users = [message_text(m) for m in revising["messages"] if m["role"] == "user"]
    assert "Two steps." in users[0] and "## lesson" in users[0]
    assert "## lesson" not in users[1] and "asked:" not in users[1]


async def test_a_message_that_changes_nothing_saves_no_version(db: AsyncSession) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    writer = Messages([("s2", "B"), ("s2", "B, simpler")])
    engine = Engine(lambda: server_over(db), lambda: writer)

    async with engine.converse(
        Request(TYPE, plan_version_id=PLAN, content_id=content_id), key="T-1"
    ) as chat:
        same = await chat.say("Leave s2.")
        different = await chat.say("Simpler s2.")

    assert (same.changed, different.changed) == (False, True)
    assert await _titles(db, content_id) == (2, ["A", "B, simpler"])


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_what_an_opencode_writer_does_reaches_the_tap_of_the_message_it_answers(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    held = HeldTap()
    with stub_model(_creation_then_revision) as (_, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(lambda: server_over(db), lambda: OpenCodeWriter(model))
        with tapping(held):
            await engine.build_kept(
                Request(TYPE, plan_version_id=PLAN, feedback="Two steps."), key="new-1"
            )

    tools = [e.data for e in held.held if e.kind == "tool"]
    said = [e.data["text"] for e in held.held if e.kind == "agent_text"]
    assert [(t["tool"], t["status"], t["unit_id"]) for t in tools] == [
        ("add_part", "completed", "s1"),
        ("add_part", "completed", "s2"),
    ]
    assert said == ["Wrote both steps."]


class _AlwaysFinds:
    """A second reader that always finds a fault in whatever part it is given."""

    def __init__(self) -> None:
        self.checked: list[str] = []

    async def errors(self, brief, unit, part):  # type: ignore[no-untyped-def]
        self.checked.append(str(part["title"]))
        return ["this part is wrong."]


async def test_a_revision_is_checked_only_where_it_changed_so_asking_for_nothing_changes_nothing(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    asks_nothing, asks_for_s2 = Messages([("s2", "B")]), Messages([("s2", "B, simpler")] * 4)
    checker = _AlwaysFinds()

    async def revise(writer: Messages) -> Any:
        engine = Engine(lambda: server_over(db), lambda: writer, lambda: checker)
        request = Request(TYPE, plan_version_id=PLAN, content_id=content_id)
        async with engine.converse(request, key="T-1") as chat:
            return await chat.say("Look at it.")

    same = await revise(asks_nothing)
    changed = await revise(asks_for_s2)

    assert (same.changed, len(asks_nothing.heard)) == (False, 1)
    assert "A" not in checker.checked and "B, simpler" in checker.checked
    assert changed.changed is True and len(asks_for_s2.heard) > 1


async def _until(condition: Callable[[], bool], timeout: float = 60.0) -> None:
    """Wait until something has happened, such as the model receiving a request."""
    deadline = time.monotonic() + timeout
    while not condition():
        if time.monotonic() > deadline:
            raise TimeoutError("it did not happen")
        await asyncio.sleep(0.05)


def _slow_then_revise(body: dict[str, Any]) -> dict[str, Any]:
    """The first message waits on the model for a while; the second revises a part at once."""
    messages = body["messages"]
    users = [message_text(m) for m in messages if m["role"] == "user"]
    if len(users) == 1:
        time.sleep(3)
        return answer("Too late.")
    draft = re.findall(r"## draft_id\s+(\S+)", " ".join(users))[-1]
    last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
    if any(m["role"] == "tool" for m in messages[last_user:]):
        return answer("Simplified s2.")
    arguments = {"draft_id": draft, "unit_id": "s2", "part": part("B, simpler")}
    return tool_call("engine_revise_part", arguments)


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_stopping_the_agent_mid_run_saves_nothing_and_the_next_message_goes_on_in_its_session(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    content_id = await _first_version(db)
    with stub_model(_slow_then_revise) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(lambda: server_over(db), lambda: OpenCodeWriter(model))
        request = Request(TYPE, plan_version_id=PLAN, content_id=content_id)
        live = LiveConversations()

        def opener():  # type: ignore[no-untyped-def]
            return engine.converse(request, key="T-1")

        slow = asyncio.create_task(live.say("T-1", opener, "Take your time."))
        await _until(lambda: bool(stub.requests))
        stopped = await live.stop("T-1")
        with pytest.raises(TurnStoppedError):
            await slow
        unchanged = await _titles(db, content_id)
        after = await live.say("T-1", opener, "Simpler s2.")
        await live.close_all()

    assert stopped is True and unchanged == (1, ["A", "B"])
    assert after.changed is True and after.summary == "Simplified s2."
    assert await _titles(db, content_id) == (2, ["A", "B, simpler"])
    resumed = next(
        body
        for body in stub.requests
        if sum(1 for m in body["messages"] if m["role"] == "user") == 2
    )
    users = [message_text(m) for m in resumed["messages"] if m["role"] == "user"]
    assert "Take your time." in users[0] and "## lesson" not in users[1]


async def test_a_held_event_keeps_the_time_it_happened_when_it_is_written_into_a_chat_later() -> (
    None
):
    import time

    from app.domains.content_engine.infrastructure.chat import HeldTap
    from app.domains.content_engine.infrastructure.tap import AgentChatEvent

    held = HeldTap()
    before = time.time()
    await held.emit(AgentChatEvent("tool", {"tool": "add_part", "status": "completed"}))
    await held.emit(AgentChatEvent("working_on", {"unit_id": "s1"}))

    assert [event.kind for event in held.held] == ["tool"]
    stamped = held.held[0].data
    assert stamped["tool"] == "add_part" and before - 1 <= float(stamped["at"]) <= time.time() + 1  # type: ignore[arg-type]
