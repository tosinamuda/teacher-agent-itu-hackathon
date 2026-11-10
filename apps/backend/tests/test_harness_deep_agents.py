"""The engine with DeepAgents as its writer's and checker's loop, against a stub endpoint.

What is asserted is what reaches the endpoint: the tools offered, the part schema as sent,
the refusal text as returned, and the tokens recorded for every call.
"""

from __future__ import annotations

from typing import Any

import pytest
from langchain_openai import ChatOpenAI
from mcp import Client
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.harness.brief import CHECKER_PROMPT, WRITER_PROMPT
from app.domains.content_engine.infrastructure.harness.chat_log import ChatModelLog
from app.domains.content_engine.infrastructure.harness.deep_agents import (
    DeepAgentsChecker,
    DeepAgentsWriter,
)
from app.domains.content_engine.mcp.caller import as_the_app
from tests.content_engine_support import PLAN, TYPE, seed_lesson, server_over
from tests.harness_script import SUMMARY, engine_script, tool_replies
from tests.openai_stub import USAGE, answer, stub_model, tool_call

pytestmark = pytest.mark.asyncio


class CapturingLog(ChatModelLog):
    def __init__(self) -> None:
        super().__init__("openai/stub")
        self.events: list[dict[str, Any]] = []

    def _persist(self, **fields: Any) -> None:
        self.events.append(fields)


def _model(base_url: str) -> ChatOpenAI:
    return ChatOpenAI(
        model="stub-model", base_url=base_url, api_key=SecretStr("k"), use_responses_api=False
    )


def _untitled(schema: object) -> object:
    """A JSON Schema without its titles, which LangChain leaves out of what it sends."""
    if isinstance(schema, list):
        return [_untitled(item) for item in schema]
    if not isinstance(schema, dict):
        return schema
    return {
        key: {name: _untitled(value) for name, value in value.items()}
        if key == "properties"
        else _untitled(value)
        for key, value in schema.items()
        if key != "title"
    }


def _system(body: dict[str, Any]) -> object:
    return body["messages"][0]["content"]


async def test_deep_agents_writes_and_checks_a_draft_through_the_engine(db: AsyncSession) -> None:
    await seed_lesson(db)
    log = CapturingLog()
    with stub_model(engine_script()) as (stub, base_url):
        engine = Engine(
            lambda: server_over(db),
            lambda: DeepAgentsWriter(_model(base_url), [log]),
            lambda: DeepAgentsChecker(_model(base_url), [log]),
        )
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B"]
    writes = [body for body in stub.requests if _system(body) == WRITER_PROMPT]
    checks = [body for body in stub.requests if _system(body) == CHECKER_PROMPT]
    assert (len(writes), len(checks), len(stub.requests)) == (4, 2, 6)
    assert tool_replies(writes)[0].startswith("ERROR: Error executing tool add_part")
    assert "examples: is required" in tool_replies(writes)[0]
    assert [event["token_usage"] for event in log.events] == [USAGE] * 6


async def test_the_model_is_offered_exactly_the_writers_tools_with_their_schemas(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    with stub_model(engine_script()) as (stub, base_url):
        engine = Engine(lambda: server_over(db), lambda: DeepAgentsWriter(_model(base_url)))
        await engine.build(Request(type=TYPE, plan_version_id=PLAN))
    with as_the_app():
        async with Client(server_over(db)) as client:
            listed = {tool.name: tool.input_schema for tool in (await client.list_tools()).tools}

    offered = {
        t["function"]["name"]: t["function"]["parameters"] for t in stub.requests[0]["tools"]
    }
    assert sorted(offered) == ["add_part", "read_draft", "revise_part"]
    assert all(offered[name] == _untitled(listed[name]) for name in offered)


def _unreadable_first(body: dict[str, Any]) -> dict[str, Any]:
    """The script, except that the writer's first call has arguments that are not JSON."""
    if not any(m["role"] == "tool" for m in body["messages"]) and "add_part" in str(body):
        return tool_call("add_part", '{"draft_id": "x", "part": "\\(x\\)"}', call_id="bad")
    replies = [m for m in body["messages"] if m["role"] == "tool" and m["tool_call_id"] != "bad"]
    return engine_script()(
        {**body, "messages": [body["messages"][0], body["messages"][1], *replies]}
    )


async def test_a_call_whose_arguments_are_not_json_goes_back_to_the_writer(
    db: AsyncSession,
) -> None:
    """Traced on gpt-oss: a revise_part with a bad escape ended the writer silently."""
    await seed_lesson(db)
    with stub_model(_unreadable_first) as (stub, base_url):
        engine = Engine(lambda: server_over(db), lambda: DeepAgentsWriter(_model(base_url)))
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert tool_replies(stub.requests)[0].startswith(
        "ERROR: the arguments of add_part are not valid JSON"
    )
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None


@pytest.mark.parametrize(
    ("answered", "found"),
    [(answer("[]"), []), (answer('["Step 2 is wrong."]'), ["Step 2 is wrong."])],
)
async def test_a_checker_that_answers_in_text_is_read_when_its_answer_is_a_list(
    answered: dict[str, Any], found: list[str]
) -> None:
    with stub_model(lambda body: answered) as (_, base_url):
        errors = await DeepAgentsChecker(_model(base_url)).errors({}, {}, {})

    assert errors == found


@pytest.mark.parametrize(
    "answered",
    [answer(""), tool_call("Verdict", {"errors": [{"where": "s1", "error": "wrong"}]})],
    ids=["no answer", "objects for strings"],
)
async def test_a_checker_without_a_list_of_errors_stops_rather_than_passing(
    answered: dict[str, Any],
) -> None:
    """Traced on gpt-oss: a required answer tool ignored, read as "no errors"."""
    with stub_model(lambda body: answered) as (_, base_url):
        with pytest.raises(CheckerStoppedError):
            await DeepAgentsChecker(_model(base_url)).errors({}, {}, {})


def _refused(body: dict[str, Any]) -> bool:
    return any("Your answer was refused" in str(m.get("content")) for m in body["messages"])


async def test_an_answer_in_text_the_schema_refuses_goes_back_and_the_next_one_is_kept() -> None:
    """Traced on gpt-oss: it ignored the required Verdict tool and wrote objects as text."""
    objects = '[{"error": "no example", "location": "s1"}]'

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        if _refused(body):
            return tool_call("Verdict", {"errors": ["s1 has no example"]})
        return answer(objects)

    with stub_model(reply) as (stub, base_url):
        errors = await DeepAgentsChecker(_model(base_url)).errors({}, {}, {})

    assert errors == ["s1 has no example"]
    assert len(stub.requests) == 2
