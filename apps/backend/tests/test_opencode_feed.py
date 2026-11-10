"""OpenCode's events become what a chat shows: text as it is written, tools, and busy or idle."""

from __future__ import annotations

import pytest

from app.domains.content_engine.infrastructure.harness.opencode_feed import Feed
from app.domains.content_engine.infrastructure.tap import AgentChatEvent
from app.shared.json_types import JsonObject

pytestmark = pytest.mark.asyncio

SESSION = "ses_1"


class _Heard:
    def __init__(self) -> None:
        self.events: list[AgentChatEvent] = []

    async def emit(self, event: AgentChatEvent) -> None:
        self.events.append(event)

    def kinds(self) -> list[str]:
        return [event.kind for event in self.events]


def _message(message_id: str, role: str, session: str = SESSION) -> JsonObject:
    return {
        "type": "message.updated",
        "properties": {"sessionID": session, "info": {"id": message_id, "role": role}},
    }


def _part(part: JsonObject, session: str = SESSION) -> JsonObject:
    return {
        "type": "message.part.updated",
        "properties": {"sessionID": session, "part": {"sessionID": session, **part}},
    }


def _delta(message_id: str, part_id: str, delta: str) -> JsonObject:
    return {
        "type": "message.part.delta",
        "properties": {
            "sessionID": SESSION,
            "messageID": message_id,
            "partID": part_id,
            "field": "text",
            "delta": delta,
        },
    }


async def _feed(*events: JsonObject) -> _Heard:
    heard = _Heard()
    feed = Feed(SESSION, heard)
    for event in events:
        await feed.take(event)
    return heard


async def test_reasoning_is_kept_apart_from_the_reply_though_its_deltas_arrive_as_text() -> None:
    done = {
        "id": "r1",
        "messageID": "a1",
        "type": "reasoning",
        "text": "Plan it.",
        "time": {"end": 1},
    }
    heard = await _feed(
        _message("a1", "assistant"),
        _part({"id": "r1", "messageID": "a1", "type": "reasoning", "text": ""}),
        _delta("a1", "r1", "Plan "),
        _delta("a1", "r1", "it."),
        _part(done),
        _part(done),
        _part({"id": "p1", "messageID": "a1", "type": "text", "text": ""}),
        _delta("a1", "p1", "Done."),
        _part({"id": "p1", "messageID": "a1", "type": "text", "text": "Done.", "time": {"end": 2}}),
        _part({"id": "s1", "messageID": "a1", "type": "step-finish"}),
    )

    said = [(event.kind, event.data["text"]) for event in heard.events if "text" in event.data]
    assert ("thinking", "Plan it.") in said
    assert said.count(("thinking", "Plan it.")) == 1
    assert [text for kind, text in said if kind == "agent_text"] == ["Done."]
    assert all("Plan" not in str(e.data) for e in heard.events if e.kind == "partial")


async def test_reasoning_that_never_ends_is_kept_when_the_session_goes_idle() -> None:
    heard = await _feed(
        _message("a1", "assistant"),
        _part({"id": "r1", "messageID": "a1", "type": "reasoning", "text": ""}),
        _delta("a1", "r1", "Half a thought."),
        {
            "type": "session.status",
            "properties": {"sessionID": SESSION, "status": {"type": "idle"}},
        },
    )

    assert [e.data["text"] for e in heard.events if e.kind == "thinking"] == ["Half a thought."]


async def test_text_is_shown_as_it_grows_and_kept_once_when_it_is_done() -> None:
    heard = await _feed(
        _message("u1", "user"),
        _part({"id": "pu", "messageID": "u1", "type": "text", "text": "Make it simpler."}),
        _message("a1", "assistant"),
        _part({"id": "p1", "messageID": "a1", "type": "text", "text": ""}),
        _delta("a1", "p1", "Simplified "),
        _delta("a1", "p1", "step 1."),
        _part(
            {
                "id": "p1",
                "messageID": "a1",
                "type": "text",
                "text": "Simplified step 1.",
                "time": {"start": 1, "end": 2},
            }
        ),
        _part({"id": "sf", "messageID": "a1", "type": "step-finish"}),
    )

    assert heard.kinds() == ["partial", "partial", "agent_text"]
    assert [e.data["text"] for e in heard.events] == [
        "Simplified ",
        "Simplified step 1.",
        "Simplified step 1.",
    ]


async def test_the_users_own_message_is_left_out() -> None:
    heard = await _feed(
        _message("u1", "user"),
        _part({"id": "pu", "messageID": "u1", "type": "text", "text": "hello"}),
        _delta("u1", "pu", "more"),
    )

    assert heard.events == []


async def test_text_not_closed_by_the_agent_is_kept_when_its_step_finishes() -> None:
    heard = await _feed(
        _message("a1", "assistant"),
        _delta("a1", "p1", "Done."),
        _part({"id": "sf", "messageID": "a1", "type": "step-finish"}),
        _part({"id": "sf2", "messageID": "a1", "type": "step-finish"}),
    )

    assert heard.kinds() == ["partial", "agent_text"]


async def test_a_tool_is_shown_working_then_kept_once_with_where_it_worked() -> None:
    running = {"id": "t1", "messageID": "a1", "type": "tool", "tool": "engine_revise_part"}
    heard = await _feed(
        _message("a1", "assistant"),
        _part({**running, "state": {"status": "pending", "input": {}}}),
        _part(
            {**running, "state": {"status": "completed", "input": {"unit_id": "s2", "part": {}}}}
        ),
        _part({**running, "state": {"status": "completed", "input": {"unit_id": "s2"}}}),
    )

    assert heard.kinds() == ["working_on", "tool"]
    assert heard.events[1].data == {"tool": "revise_part", "status": "completed", "unit_id": "s2"}


async def test_a_skill_and_a_file_read_are_named() -> None:
    skill = {"id": "t1", "messageID": "a1", "type": "tool", "tool": "skill"}
    read = {"id": "t2", "messageID": "a1", "type": "tool", "tool": "read"}
    path = "/srv/run/.agents/skills/writing-lesson-plans/references/steps-and-activities.md"
    heard = await _feed(
        _message("a1", "assistant"),
        _part(
            {**skill, "state": {"status": "completed", "input": {"name": "writing-lesson-plans"}}}
        ),
        _part({**read, "state": {"status": "completed", "input": {"filePath": path}}}),
    )

    assert [event.data.get("detail") for event in heard.events] == [
        "writing-lesson-plans",
        "writing-lesson-plans/references/steps-and-activities.md",
    ]


async def test_busy_and_idle_are_shown_and_another_session_is_ignored() -> None:
    heard = await _feed(
        {
            "type": "session.status",
            "properties": {"sessionID": SESSION, "status": {"type": "busy"}},
        },
        _part({"id": "p9", "messageID": "x", "type": "text", "text": "no"}, session="ses_2"),
        {
            "type": "session.status",
            "properties": {"sessionID": SESSION, "status": {"type": "idle"}},
        },
    )

    assert [e.data for e in heard.events] == [{"working": True}, {"working": False}]
    assert not any(event.persisted for event in heard.events)
