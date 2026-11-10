"""The engine with DeepSeek Harness as its writer's and checker's loop, against a stub endpoint.

dsh runs in its own process, spoken to over ACP, and reaches the draft through the relay. What
is asserted is what reaches the endpoint: the prompt and tools, the refusal as returned, the
checker's answer through its one tool, and the tokens recorded for every model call.
"""

from __future__ import annotations

import json
import re
import shutil
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.skills import Skill, SkillFile
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.engine import (
    RESUMES,
    Engine,
    EngineIncompleteError,
    Request,
)
from app.domains.content_engine.infrastructure.harness.brief import (
    CHECKER_PROMPT,
    CHECKER_STEPS,
    NATIVE_SKILLS_WRITER_PROMPT,
    WRITER_PROMPT,
    turns_for,
)
from app.domains.content_engine.infrastructure.harness.dsh import DshChecker, DshWriter
from app.domains.content_engine.infrastructure.harness.dsh_agent import DshModel
from app.domains.content_engine.infrastructure.harness.workspace import SkillError
from app.domains.content_engine.infrastructure.tools import Source, mounted
from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.generation_log.application.recorder import GenerationLog
from tests.content_engine_support import PLAN, TYPE, seed_lesson, server_over
from tests.external_server import external_server
from tests.harness_script import SUMMARY, calls_first, engine_script, skill_first, tool_replies
from tests.openai_stub import answer, stub_model, tool_call

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(shutil.which("dsh") is None, reason="npm i -g @deepseek-ai/dsh@0.1.5-rc.3"),
]


class CapturingLog(GenerationLog):
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def _persist(self, **fields: Any) -> None:
        self.events.append(fields)


def _system(body: dict[str, Any]) -> str:
    return "\n".join(str(m["content"]) for m in body["messages"] if m["role"] == "system")


def _tools(body: dict[str, Any]) -> list[str]:
    return sorted(tool["function"]["name"] for tool in body.get("tools") or [])


async def test_dsh_writes_and_checks_a_draft_through_the_engine(db: AsyncSession) -> None:
    await seed_lesson(db)
    log = CapturingLog()
    with stub_model(engine_script()) as (stub, base_url):
        model = DshModel("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db), lambda: DshWriter(model, log), lambda: DshChecker(model, log)
        )
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B"]
    writes = [body for body in stub.requests if _system(body) == WRITER_PROMPT]
    checks = [body for body in stub.requests if _system(body) == CHECKER_PROMPT]
    assert (len(writes), len(checks), len(stub.requests)) == (4, 2, 6)
    assert _tools(writes[0]) == [
        "mcp__engine__add_part",
        "mcp__engine__read_draft",
        "mcp__engine__revise_part",
    ]
    assert _tools(checks[0]) == ["mcp__answer__give_verdict"]
    assert "examples: is required" in tool_replies(writes)[0]
    assert [event["token_usage"]["input_tokens"] for event in log.events] == [120] * 6


async def test_a_checker_that_never_answers_stops_rather_than_passing() -> None:
    with stub_model(lambda body: answer("Looks fine to me.")) as (_, base_url):
        checker = DshChecker(DshModel("stub-model", base_url, "k"))
        with pytest.raises(CheckerStoppedError):
            await checker.errors({}, {}, {})


async def test_a_checker_answering_with_objects_for_strings_stops_rather_than_passing() -> None:
    def reply(body: dict[str, Any]) -> dict[str, Any]:
        return tool_call(_tools(body)[0], {"errors": [{"where": "s1", "error": "wrong"}]})

    with stub_model(reply) as (_, base_url):
        checker = DshChecker(DshModel("stub-model", base_url, "k"))
        with pytest.raises(CheckerStoppedError):
            await checker.errors({}, {}, {})


async def test_a_malformed_verdict_is_refused_and_the_corrected_one_kept() -> None:
    """Traced on gpt-oss: it answered with objects where the schema asks for strings."""

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        refused = any(m["role"] == "tool" for m in body["messages"])
        errors = ["s1 has no example"] if refused else [{"where": "s1", "error": "no example"}]
        return tool_call(_tools(body)[0], {"errors": errors}, call_id=f"call-{refused}")

    with stub_model(reply) as (stub, base_url):
        checker = DshChecker(DshModel("stub-model", base_url, "k"))
        found = await checker.errors({}, {}, {})

    assert found == ["s1 has no example"]
    assert "does not match the tool's schema" in tool_replies(stub.requests)[0]


async def test_an_answer_in_text_the_schema_refuses_goes_back_and_the_next_one_is_kept() -> None:
    """The answer tool never sees an answer written as text, so the checker sends it back."""

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        if any("Your answer was refused" in str(m.get("content")) for m in body["messages"]):
            return tool_call(_tools(body)[0], {"errors": ["s1 has no example"]})
        return answer('[{"error": "no example", "location": "s1"}]')

    with stub_model(reply) as (stub, base_url):
        checker = DshChecker(DshModel("stub-model", base_url, "k"))
        found = await checker.errors({}, {}, {})

    assert found == ["s1 has no example"]
    assert len(stub.requests) == 2


async def test_a_valid_answer_on_the_last_allowed_model_call_is_kept() -> None:
    """Traced on gpt-oss: text, then objects the schema refuses, then a valid list on call 3."""

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        tools = _tools(body)
        refused = sum(m["role"] == "tool" for m in body["messages"])
        resent = any("Your answer was refused" in str(m.get("content")) for m in body["messages"])
        if not resent:
            return answer("**Errors**\n1. s1 has no example")
        errors = ["s1 has no example"] if refused else [{"where": "s1", "error": "no example"}]
        return tool_call(tools[0], {"errors": errors}, call_id=f"call-{refused}")

    with stub_model(reply) as (stub, base_url):
        checker = DshChecker(DshModel("stub-model", base_url, "k"))
        found = await checker.errors({}, {}, {})

    assert found == ["s1 has no example"]
    assert len(stub.requests) == CHECKER_STEPS


async def test_a_writer_past_its_model_calls_is_stopped(db: AsyncSession) -> None:
    """The DSPy writer's ``max_iters`` holds here too: dsh sets no limit of its own.

    A stopped writer is resumed ``RESUMES`` times, each run stopped at the same limit.
    """
    await seed_lesson(db)

    def reads_forever(body: dict[str, Any]) -> dict[str, Any]:
        tools = _tools(body)
        read = next((name for name in tools if name.endswith("read_draft")), None)
        if read is None:
            return tool_call(tools[0], {"errors": []})
        return tool_call(read, {"draft_id": "x"}, call_id=f"call-{len(body['messages'])}")

    with stub_model(reads_forever) as (stub, base_url):
        model = DshModel("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db), lambda: DshWriter(model), lambda: DshChecker(model)
        )
        with pytest.raises(EngineIncompleteError):
            await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    writes = [body for body in stub.requests if _system(body) == WRITER_PROMPT]
    assert len(writes) == (1 + RESUMES) * turns_for({"units": ["s1", "s2"]})


async def test_native_skills_are_files_dsh_offers_and_loads_not_text_in_the_brief(
    db: AsyncSession,
) -> None:
    await seed_lesson(db, skills=("show-the-working",))
    log = CapturingLog()
    with stub_model(skill_first("show-the-working")) as (stub, base_url):
        model = DshModel("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db),
            lambda: DshWriter(model, log, native_skills=True),
            lambda: DshChecker(model, log),
        )
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    writes = [body for body in stub.requests if NATIVE_SKILLS_WRITER_PROMPT in _system(body)]
    assert writes
    assert "skill" in _tools(writes[0])
    reminder = str(writes[0]["messages"][-1]["content"])
    assert re.findall(r"^- `([^`]+)`", reminder, re.M) == ["show-the-working"]
    assert "Work every example line by line" not in str(writes[0]["messages"][0])
    loaded = [text for text in tool_replies(writes) if "Work every example line by line" in text]
    assert loaded
    workspaces = [
        event["request"]["workspace"] for event in log.events if "workspace" in event["request"]
    ]
    assert workspaces
    assert set(workspaces[0]["skills"]) == {"show-the-working"}


async def test_dsh_refuses_a_skill_whose_reference_files_it_could_not_read(
    db: AsyncSession,
) -> None:
    files = (SkillFile("references/rules.md", "Rule one."),)
    skill = Skill("check-rules", 1, "Check rules", "Use to check a part.", "See the rules.", files)
    await seed_lesson(db, skills=("check-rules",), new_skills=(skill,))
    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            assert started.structured_content is not None
            writer = DshWriter(
                DshModel("stub-model", "http://127.0.0.1:1", "k"), native_skills=True
            )
            with pytest.raises(SkillError, match="reference files"):
                await writer.write(client, started.structured_content, {}, feedback="")


async def test_dsh_reaches_an_external_tool_the_type_lists_and_never_sees_its_token(
    db: AsyncSession,
) -> None:
    async with external_server() as external:
        maths = {
            "server": "maths",
            "url": external.url,
            "tools": ["solve"],
            "secret": "MATHS_TOKEN",
        }
        await seed_lesson(db, mcp=(maths,))

        @asynccontextmanager
        async def externals(slug: str) -> AsyncIterator[list[Source]]:
            spec = await build_content_catalogue().current(db, slug)
            async with mounted(spec.mcp, {"MATHS_TOKEN": "s3cret-token"}) as sources:
                yield sources

        script = calls_first("mcp__engine__maths__solve", {"number": 21})
        with stub_model(script) as (stub, base_url):
            model = DshModel("stub-model", base_url, "k")
            engine = Engine(
                lambda: server_over(db),
                lambda: DshWriter(model),
                lambda: DshChecker(model),
                externals,
            )
            built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    writes = [body for body in stub.requests if "mcp__engine__maths__solve" in _tools(body)]
    assert writes
    assert any("the answer is 42" in text for text in tool_replies(stub.requests))
    assert "s3cret-token" not in json.dumps(stub.requests)
    assert set(external.seen) == {"Bearer s3cret-token"}
