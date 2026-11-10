"""External MCP servers a type lists: validated, stored, mounted with only the tools it allows."""

from __future__ import annotations

import contextvars
import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef, McpServerRefError
from app.domains.content.api.schemas import SpecResponse
from app.domains.content.application.errors import ContentError
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content_engine.infrastructure.engine import Request
from app.domains.content_engine.infrastructure.tools import (
    ExternalServerError,
    Source,
    mounted,
    tools_server,
)
from app.domains.content_engine.mcp.views import type_json
from app.shared.json_types import JsonObject
from tests.content_engine_support import (
    PLAN,
    SPEC,
    TYPE,
    ScriptedWriter,
    engine_over,
    part,
    seed_lesson,
)
from tests.external_server import external_server

pytestmark = pytest.mark.asyncio

GOOD = {"server": "maths", "url": "https://tools.example.org/mcp", "tools": ["solve"]}


def test_a_server_reference_reads_and_writes_the_same_record() -> None:
    record = {**GOOD, "secret": "MATHS_TOKEN"}

    assert McpServerRef.from_record(record).to_record() == record


def test_a_reader_of_the_type_sees_the_server_and_its_tools_but_not_where_it_is() -> None:
    ref = McpServerRef.from_record({**GOOD, "secret": "MATHS_TOKEN"})

    assert ref.public() == {"server": "maths", "tools": ["solve"]}


@pytest.mark.parametrize(
    "record",
    [
        {**GOOD, "server": "engine"},
        {**GOOD, "server": "Not A Slug"},
        {**GOOD, "url": "http://tools.example.org/mcp"},
        {**GOOD, "url": "https://user:pass@tools.example.org/mcp"},
        {**GOOD, "url": "ftp://tools.example.org/mcp"},
        {**GOOD, "tools": []},
        {**GOOD, "tools": ["solve", "solve"]},
        {**GOOD, "tools": ["bad name"]},
        {**GOOD, "secret": "lower"},
        {**GOOD, "token": "abc"},
    ],
)
def test_a_server_that_could_not_be_used_safely_is_refused(record: dict[str, object]) -> None:
    with pytest.raises(McpServerRefError):
        McpServerRef.from_record(record)


def test_plain_http_is_allowed_only_to_the_local_machine() -> None:
    local = {**GOOD, "url": "http://127.0.0.1:9000/mcp"}

    assert McpServerRef.from_record(local).url == "http://127.0.0.1:9000/mcp"


async def test_a_spec_stores_the_servers_it_lists_and_refuses_the_same_one_twice(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    catalogue = build_content_catalogue()

    stored = await catalogue.add(db, TYPE, {**SPEC, "mcp": [GOOD]}, "Researcher")
    read = await catalogue.current(db, TYPE)

    assert [ref.to_record() for ref in stored.mcp] == [GOOD]
    assert read.mcp == stored.mcp
    with pytest.raises(ContentError, match="listed once"):
        await catalogue.add(db, TYPE, {**SPEC, "mcp": [GOOD, GOOD]}, "Researcher")


async def test_only_the_tools_a_ref_lists_are_offered_each_under_its_servers_name() -> None:
    async with external_server() as external:
        ref = McpServerRef("maths", external.url, ("solve",), "MATHS_TOKEN")
        async with mounted([ref], {"MATHS_TOKEN": "s3cret"}) as sources:
            server = tools_server(sources, opened_in=contextvars.copy_context())
            async with Client(server) as client:
                offered = [tool.name for tool in (await client.list_tools()).tools]
                answered = await client.call_tool("maths__solve", {"number": 4})
                refused = await client.call_tool("maths__forbidden", {})

    assert offered == ["maths__solve"]
    assert "the answer is 8" in str(answered.content)
    assert refused.is_error


async def test_the_token_goes_to_its_own_server_only_and_only_as_a_bearer_header() -> None:
    async with external_server() as external:
        ref = McpServerRef("maths", external.url, ("solve",), "MATHS_TOKEN")
        async with mounted([ref], {"MATHS_TOKEN": "s3cret"}):
            pass

    assert external.seen
    assert set(external.seen) == {"Bearer s3cret"}


async def test_a_server_with_no_secret_is_called_without_credentials() -> None:
    async with external_server() as external:
        async with mounted([McpServerRef("maths", external.url, ("solve",))], {}):
            pass

    assert set(external.seen) == {""}


async def test_a_secret_that_is_not_set_stops_the_run_before_anything_is_connected() -> None:
    ref = McpServerRef("maths", "http://127.0.0.1:1/mcp", ("solve",), "MATHS_TOKEN")

    with pytest.raises(ExternalServerError, match="MATHS_TOKEN is not set"):
        async with mounted([ref], {}):
            pass


async def test_a_listed_tool_the_server_does_not_have_stops_the_run() -> None:
    async with external_server() as external:
        ref = McpServerRef("maths", external.url, ("solve", "missing"))
        with pytest.raises(ExternalServerError, match="no tools .*missing"):
            async with mounted([ref], {}):
                pass


async def test_a_source_offers_only_the_tools_it_names(db: AsyncSession) -> None:
    async with external_server() as external:
        async with Client(external.url) as client:
            server = tools_server(
                [Source(client, frozenset({"forbidden"}), prefix="x__")],
                opened_in=contextvars.copy_context(),
            )
            async with Client(server) as offered:
                names = [tool.name for tool in (await offered.list_tools()).tools]

    assert names == ["x__forbidden"]


MATHS = {**GOOD, "server": "maths", "secret": "MATHS_TOKEN"}


class _Recording(ScriptedWriter):
    """A scripted writer that also calls the external tool and notes what it was offered."""

    def __init__(self) -> None:
        super().__init__({"s1": [part("A")], "s2": [part("B")]})
        self.offered: list[str] = []
        self.answer = ""

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        self.offered = sorted(tool.name for tool in (await client.list_tools()).tools)
        self.answer = str((await client.call_tool("maths__solve", {"number": 21})).content)
        return await super().write(client, draft, lesson, feedback=feedback)


async def test_a_writer_is_offered_the_drafts_tools_and_the_types_external_ones_and_no_more(
    db: AsyncSession,
) -> None:
    async with external_server() as external:
        await seed_lesson(db, mcp=({**MATHS, "url": external.url},))

        @asynccontextmanager
        async def externals(slug: str) -> AsyncIterator[list[Source]]:
            spec = await build_content_catalogue().current(db, slug)
            async with mounted(spec.mcp, {"MATHS_TOKEN": "s3cret"}) as sources:
                yield sources

        writer = _Recording()
        engine = engine_over(db, writer, externals)
        built = await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    assert built.summary == "Wrote 2 part(s)."
    assert writer.offered == ["add_part", "maths__solve", "read_draft", "revise_part"]
    assert "the answer is 42" in writer.answer
    assert set(external.seen) == {"Bearer s3cret"}
    assert external.url not in json.dumps(writer.seen["draft"])
    assert "s3cret" not in json.dumps(writer.seen["draft"])


async def test_a_type_whose_server_cannot_be_used_stops_the_build_with_the_reason(
    db: AsyncSession,
) -> None:
    await seed_lesson(db, mcp=({**MATHS, "url": "http://127.0.0.1:1/mcp"},))

    @asynccontextmanager
    async def externals(slug: str) -> AsyncIterator[list[Source]]:
        spec = await build_content_catalogue().current(db, slug)
        async with mounted(spec.mcp, {}) as sources:
            yield sources

    engine = engine_over(db, _Recording(), externals)

    with pytest.raises(ExternalServerError, match="MATHS_TOKEN is not set"):
        await engine.build(Request(type=TYPE, plan_version_id=PLAN))


async def test_the_api_and_the_mcp_view_show_a_types_servers_but_not_where_they_are(
    db: AsyncSession,
) -> None:
    await seed_lesson(db, mcp=(MATHS,))
    catalogue = build_content_catalogue()
    definition, spec = (await catalogue.types(db))[-1]

    view = type_json(definition, spec)["spec"]
    assert isinstance(view, dict)

    assert SpecResponse.of(spec).mcp == [{"server": "maths", "tools": ["solve"]}]
    assert view["mcp"] == [{"server": "maths", "tools": ["solve"]}]
