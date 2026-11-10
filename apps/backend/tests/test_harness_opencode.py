"""The engine with OpenCode as its writer's and checker's loop, against a stub endpoint.

OpenCode runs as a server in its own process and reaches the draft through the relay. What
is asserted is what reaches the endpoint: the system prompt and tools, the refusal text as
returned, and the tokens recorded for every model call.
"""

from __future__ import annotations

import json
import shutil
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import httpx
import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.skills import Skill, SkillFile
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.harness.brief import (
    CHECKER_PROMPT,
    NATIVE_SKILLS_WRITER_PROMPT,
    WRITER_PROMPT,
    as_named_by,
)
from app.domains.content_engine.infrastructure.harness.opencode import (
    OpenCodeChecker,
    OpenCodeWriter,
)
from app.domains.content_engine.infrastructure.harness.opencode_feed import TOOL_PREFIX
from app.domains.content_engine.infrastructure.harness.opencode_server import Model
from app.domains.content_engine.infrastructure.harness.relay import relayed
from app.domains.content_engine.infrastructure.tools import WRITER_TOOLS, Source, mounted
from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.generation_log.application.recorder import GenerationLog
from tests.content_engine_support import PLAN, TYPE, seed_lesson, server_over, writer_client
from tests.external_server import external_server
from tests.harness_script import (
    SUMMARY,
    calls_first,
    engine_script,
    reads_reference_first,
    skill_first,
    tool_replies,
)
from tests.openai_stub import answer, stub_model, tool_call

pytestmark = pytest.mark.asyncio

#: What OpenCode's writer is told: the tools named as OpenCode names them.
OPENCODE_WRITER_PROMPT = as_named_by(WRITER_PROMPT, TOOL_PREFIX)
OPENCODE_NATIVE_SKILLS_PROMPT = as_named_by(NATIVE_SKILLS_WRITER_PROMPT, TOOL_PREFIX)


class CapturingLog(GenerationLog):
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def _persist(self, **fields: Any) -> None:
        self.events.append(fields)


def _system(body: dict[str, Any]) -> str:
    return "\n".join(m["content"] for m in body["messages"] if m["role"] == "system")


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_opencode_writes_and_checks_a_draft_through_the_engine(db: AsyncSession) -> None:
    await seed_lesson(db)
    log = CapturingLog()
    with stub_model(engine_script()) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db),
            lambda: OpenCodeWriter(model, log),
            lambda: OpenCodeChecker(model, log),
        )
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B"]
    writes = [body for body in stub.requests if _system(body) == OPENCODE_WRITER_PROMPT]
    checks = [body for body in stub.requests if _system(body) == CHECKER_PROMPT]
    assert (len(writes), len(checks), len(stub.requests)) == (4, 2, 6)
    assert sorted(t["function"]["name"] for t in writes[0]["tools"]) == [
        "engine_add_part",
        "engine_read_draft",
        "engine_revise_part",
    ]
    assert tool_replies(writes)[0].startswith("Error executing tool add_part")
    assert "examples: is required" in tool_replies(writes)[0]
    assert [event["token_usage"]["input"] for event in log.events] == [120] * 6


async def test_the_relay_answers_only_its_token_and_offers_only_the_writers_tools(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    listing = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    accept = {"Accept": "application/json, text/event-stream"}
    with as_the_app():
        async with (
            Client(server_over(db)) as base,
            writer_client(base) as client,
            relayed(client) as relay,
        ):
            async with httpx.AsyncClient() as http:
                refused = await http.post(relay.url, json=listing, headers=accept)
                listed = await http.post(relay.url, json=listing, headers=accept | relay.headers())

    assert refused.status_code == 401
    assert sorted(tool["name"] for tool in listed.json()["result"]["tools"]) == sorted(WRITER_TOOLS)


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_a_checker_answering_with_objects_for_strings_stops_rather_than_passing() -> None:
    """Traced on gpt-oss: OpenCode did not hold its answer to the schema's list of strings."""
    objects = tool_call("StructuredOutput", {"errors": [{"where": "s1", "error": "wrong"}]})
    with stub_model(lambda body: objects) as (_, base_url):
        checker = OpenCodeChecker(Model("stub-model", base_url, "k"))
        with pytest.raises(CheckerStoppedError):
            await checker.errors({}, {}, {})


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_an_answer_the_schema_refuses_goes_back_and_the_next_one_is_kept() -> None:
    """Traced on gpt-oss: OpenCode passed objects where the Verdict schema asks for strings."""

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        refused = any("Your answer was refused" in str(m.get("content")) for m in body["messages"])
        errors = ["s1 has no example"] if refused else [{"where": "s1", "error": "no example"}]
        return tool_call("StructuredOutput", {"errors": errors})

    with stub_model(reply) as (_, base_url):
        checker = OpenCodeChecker(Model("stub-model", base_url, "k"))
        errors = await checker.errors({}, {}, {})

    assert errors == ["s1 has no example"]


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_a_verdict_written_as_text_is_read_when_the_model_ignores_the_answer_tool() -> None:
    """Traced on gpt-oss: a valid verdict in its reply, and OpenCode reported an error for it."""
    written = answer('{"errors": ["the classwork question has no answer"]}')

    with stub_model(lambda body: written) as (stub, base_url):
        checker = OpenCodeChecker(Model("stub-model", base_url, "k"))
        errors = await checker.errors({}, {}, {})

    assert errors == ["the classwork question has no answer"]
    assert len(stub.requests) == 1


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_native_skills_are_files_opencode_offers_and_loads_not_text_in_the_brief(
    db: AsyncSession,
) -> None:
    await seed_lesson(db, skills=("show-the-working",))
    log = CapturingLog()
    with stub_model(skill_first("show-the-working")) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db),
            lambda: OpenCodeWriter(model, log, native_skills=True),
            lambda: OpenCodeChecker(model, log),
        )
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    writes = [
        body for body in stub.requests if _system(body).startswith(OPENCODE_NATIVE_SKILLS_PROMPT)
    ]
    assert writes
    listed = _system(writes[0])[len(OPENCODE_NATIVE_SKILLS_PROMPT) :]
    assert "<name>show-the-working</name>" in listed
    assert "customize-opencode" not in listed
    assert "skill" in [tool["function"]["name"] for tool in writes[0]["tools"]]
    assert "Work every example line by line" not in str(writes[0]["messages"])
    loaded = [text for text in tool_replies(writes) if "Work every example line by line" in text]
    assert loaded
    workspaces = [
        event["request"]["workspace"] for event in log.events if "workspace" in event["request"]
    ]
    assert workspaces
    assert set(workspaces[0]["skills"]) == {"show-the-working"}


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_a_reference_file_of_a_skill_is_read_from_the_workspace_by_opencode(
    db: AsyncSession,
) -> None:
    files = (SkillFile("references/rules.md", "Rule one: keep every line."),)
    skill = Skill("check-rules", 1, "Check rules", "Use to check a part.", "See the rules.", files)
    await seed_lesson(db, skills=("check-rules",), new_skills=(skill,))
    with stub_model(reads_reference_first("references/rules.md")) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db),
            lambda: OpenCodeWriter(model, native_skills=True),
            lambda: OpenCodeChecker(model),
        )
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    assert any("Rule one: keep every line." in text for text in tool_replies(stub.requests))


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_opencode_reads_only_the_skill_files_it_was_given(db: AsyncSession) -> None:
    files = (SkillFile("references/rules.md", "Rule one."),)
    skill = Skill("check-rules", 1, "Check rules", "Use to check a part.", "See the rules.", files)
    await seed_lesson(db, skills=("check-rules",), new_skills=(skill,))

    def reply(body: dict[str, Any]) -> dict[str, Any]:
        if not any(m["role"] == "tool" for m in body["messages"]):
            return tool_call("read", {"filePath": "/etc/hosts"})
        return engine_script()(body)

    with stub_model(reply) as (stub, base_url):
        model = Model("stub-model", base_url, "k")
        engine = Engine(
            lambda: server_over(db),
            lambda: OpenCodeWriter(model, native_skills=True),
            lambda: OpenCodeChecker(model),
        )
        await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert "prevents you from using this specific tool call" in tool_replies(stub.requests)[0]


@pytest.mark.skipif(shutil.which("opencode") is None, reason="npm i -g opencode-ai@1.18.32")
async def test_opencode_reaches_an_external_tool_the_type_lists_and_never_sees_its_token(
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

        script = calls_first("engine_maths__solve", {"number": 21})
        with stub_model(script) as (stub, base_url):
            model = Model("stub-model", base_url, "k")
            engine = Engine(
                lambda: server_over(db),
                lambda: OpenCodeWriter(model),
                lambda: OpenCodeChecker(model),
                externals,
            )
            built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == SUMMARY
    offered = [[t["function"]["name"] for t in body.get("tools") or []] for body in stub.requests]
    writes = [names for names in offered if "engine_maths__solve" in names]
    assert writes
    assert any("the answer is 42" in text for text in tool_replies(stub.requests))
    assert "s3cret-token" not in json.dumps(stub.requests)
    assert set(external.seen) == {"Bearer s3cret-token"}
