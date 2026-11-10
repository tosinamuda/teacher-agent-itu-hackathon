"""A plugin links to the app's MCP server, and the app calls the check tools it lists."""

from __future__ import annotations

import base64
import io
import json
from types import SimpleNamespace
from typing import Any

import pytest
from mcp import Client
from pptx import Presentation
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.additions import ADDERS
from app.domains.content_engine.application.plugin_tools import (
    ToolAnswerError,
    plugin_tool_additions,
    plugin_tool_check,
    plugin_tool_file,
)
from app.domains.content_engine.files import BUILDERS
from app.domains.content_engine.infrastructure.wiring import build_draft_tools
from app.domains.content_engine.mcp.caller import as_the_app
from app.shared.json_types import JsonObject
from tests.content_engine_support import PLAN, seed_lesson, server_over
from tests.plugin_folder import read_plugin
from tests.test_slide_deck_plugin import PLUGIN, SLIDE, _installed


class _Catalogue:
    def __init__(self, *refs: McpServerRef) -> None:
        self._refs = refs

    async def revision(self, db: AsyncSession, slug: str, revision: int) -> Any:
        return SimpleNamespace(mcp=self._refs)


def _draft() -> Any:
    return SimpleNamespace(type="slide-deck", spec_revision=3, draft_id="D-1")


@pytest.mark.asyncio
async def test_a_check_tool_is_called_with_the_drafts_id() -> None:
    seen: list[tuple[str, str, JsonObject]] = []

    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        seen.append((ref.name, tool, arguments))
        return {"faults": [f"fault of {tool}"]}

    own = McpServerRef("lpcg", "/mcp", (), checks=("check_a", "check_b"))
    elsewhere = McpServerRef("other", "https://checks.example.org/mcp", ("read",), checks=("c",))
    check = plugin_tool_check(_Catalogue(own, elsewhere), call)  # type: ignore[arg-type]

    faults = await check(None, _draft())  # type: ignore[arg-type]

    assert faults == ["fault of check_a"]
    assert seen == [("lpcg", "check_a", {"draft_id": "D-1"})]


@pytest.mark.asyncio
async def test_the_checks_are_called_in_order_until_one_finds_a_fault() -> None:
    seen: list[str] = []

    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        seen.append(tool)
        return {"faults": ["too long"] if tool == "check_b" else []}

    own = McpServerRef("lpcg", "/mcp", (), checks=("check_a", "check_b", "reads_with_a_model"))
    check = plugin_tool_check(_Catalogue(own), call)  # type: ignore[arg-type]

    assert await check(None, _draft()) == ["too long"]  # type: ignore[arg-type]
    assert seen == ["check_a", "check_b"]


@pytest.mark.asyncio
async def test_a_spec_that_lists_no_check_has_no_faults() -> None:
    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        raise AssertionError("nothing to call")

    only_writer_tools = McpServerRef("other", "https://checks.example.org/mcp", ("read",))

    check = plugin_tool_check(_Catalogue(only_writer_tools), call)  # type: ignore[arg-type]

    assert await check(None, _draft()) == []  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("record", "told"),
    [
        ({"server": "lpcg", "url": "/mcp", "tools": ["x"]}, "checks, adds and files only"),
        (
            {"server": "lpcg", "url": "/mcp", "tools": [], "secret": "TOKEN"},
            "checks, adds and files only",
        ),
        (
            {"server": "lpcg", "url": "/../mcp", "tools": [], "checks": ["c"]},
            "checks, adds and files only",
        ),
        ({"server": "lpcg", "url": "/mcp", "tools": []}, "list each tool"),
        ({"server": "s", "url": "http://example.org/mcp", "checks": ["c"]}, "reached over https"),
    ],
)
def test_a_link_to_a_server_is_refused_when_it_is_unsafe_or_lists_no_tool(
    record: JsonObject, told: str
) -> None:
    with pytest.raises(ValueError, match=told):
        McpServerRef.from_record(record)


def test_a_link_that_is_a_path_is_the_apps_own_server_and_keeps_its_checks() -> None:
    ref = McpServerRef.from_record({"server": "lpcg", "url": "/mcp", "checks": ["check_a"]})

    assert ref.own and ref.checks == ("check_a",)
    assert McpServerRef.from_record(ref.to_record()) == ref


async def _started_deck(client: Client, title: str) -> str:
    started = await client.call_tool("start_draft", {"type": "slide-deck", "plan_version_id": PLAN})
    assert started.structured_content is not None
    draft_id = str(started.structured_content["draft_id"])
    for unit in ("s1", "s2"):
        part = {"slides": [{**SLIDE, "title": title}]}
        added = await client.call_tool(
            "add_part", {"draft_id": draft_id, "unit_id": unit, "part": part}
        )
        assert not added.is_error
    return draft_id


@pytest.mark.asyncio
async def test_the_check_tool_of_the_apps_server_answers_the_faults_of_a_stored_draft(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    plugin, _ = read_plugin(PLUGIN)
    assert plugin is not None
    await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(PLUGIN), "Researcher"
    )

    with as_the_app():
        async with Client(server_over(db)) as client:
            draft_id = await _started_deck(client, " ".join(["word"] * 11))
            answered = await client.call_tool("check_slide_deck", {"draft_id": draft_id})

    assert answered.structured_content is not None
    assert [f.split(":")[0] for f in answered.structured_content["faults"]] == ["s1", "s2"]
    assert all("the title runs past 10" in f for f in answered.structured_content["faults"])


@pytest.mark.asyncio
async def test_the_check_tool_refuses_a_draft_that_is_not_there(db: AsyncSession) -> None:
    with as_the_app():
        async with Client(server_over(db)) as client:
            answered = await client.call_tool("check_slide_deck", {"draft_id": "D-missing"})

    assert answered.is_error
    assert "there is no draft" in json.dumps([c.model_dump() for c in answered.content])


SHIPPED = PLUGIN.parent


@pytest.mark.parametrize(
    ("folder", "artefact"),
    [
        ("slide-deck", "slide-deck"),
        ("lesson-note", "lesson-note-writer"),
        ("revision-note", "revision-note-writer"),
        ("revision-note", "revision-note-learner-writer"),
        ("class-test", "class-test-writer"),
        ("lesson-plan", "lesson-plan-writer"),
    ],
)
def test_each_shipped_writer_links_to_a_check_tool_the_apps_server_has(
    folder: str, artefact: str
) -> None:
    plugin, problems = read_plugin(SHIPPED / folder, artefact)

    assert plugin is not None and problems == []
    (ref,) = plugin.servers
    assert ref.own and ref.url == "/mcp"
    assert set(ref.checks) <= set(build_draft_tools().check_tools) and ref.checks
    assert set(ref.adds) <= set(ADDERS)
    assert set(ref.files) <= set(BUILDERS)


@pytest.mark.asyncio
async def test_a_writer_plugin_that_implements_a_type_binds_its_checks_to_the_spec_it_adds(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    folder = SHIPPED / "lesson-note"
    plugin, _ = read_plugin(folder, "lesson-note-writer")
    assert plugin is not None
    catalogue = build_content_catalogue()
    await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(folder), "Researcher"
    )

    generators = await catalogue.generators_of(db, await catalogue.type(db, "lesson-note"))
    binding = next(g for g in generators if g.ref == "lesson-note-writer")
    assert binding.spec_revision is not None
    spec = await catalogue.revision(db, "lesson-note", binding.spec_revision)

    assert [(ref.name, ref.checks, ref.adds) for ref in spec.mcp] == [
        ("lpcg", ("check_lesson_note",), ())
    ]


@pytest.mark.asyncio
async def test_a_check_tool_that_answers_something_else_stops_the_draft() -> None:
    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        return {"faults": "none"}

    ref = McpServerRef("lpcg", "/mcp", (), checks=("check_a",))
    check = plugin_tool_check(_Catalogue(ref), call)  # type: ignore[arg-type]

    with pytest.raises(ToolAnswerError, match="one string for each fault"):
        await check(None, _draft())  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_the_fields_every_adding_tool_answers_are_added_in_order() -> None:
    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        return {"additions": {tool: arguments["draft_id"], "shared": tool}}

    ref = McpServerRef("lpcg", "/mcp", (), adds=("first", "second"))
    spec = SimpleNamespace(mcp=(ref,))

    added = await plugin_tool_additions(call)(_draft(), spec)  # type: ignore[arg-type]

    assert added == {"first": "D-1", "second": "D-1", "shared": "second"}


@pytest.mark.asyncio
async def test_the_cover_tool_answers_the_cover_of_the_drafts_lesson(db: AsyncSession) -> None:
    await _installed(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            draft_id = await _started_deck(client, "Adding")
            answered = await client.call_tool("slide_deck_cover", {"draft_id": draft_id})

    assert answered.structured_content is not None
    cover = answered.structured_content["additions"]["cover"]
    assert cover["title"] and cover["objectives"]


@pytest.mark.asyncio
async def test_the_file_tool_answers_the_decks_powerpoint_file_and_refuses_unknown_content(
    db: AsyncSession,
) -> None:
    await _installed(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            draft_id = await _started_deck(client, "Adding")
            submitted = await client.call_tool("submit_draft", {"draft_id": draft_id})
            assert not submitted.is_error and submitted.structured_content is not None
            content_id = str(submitted.structured_content["saved_as"])
            made = await client.call_tool("build_slide_deck_file", {"content_id": content_id})
            unknown = await client.call_tool("build_slide_deck_file", {"content_id": "AT-missing"})

    assert made.structured_content is not None
    file = made.structured_content["file"]
    slides = Presentation(io.BytesIO(base64.b64decode(file["data"]))).slides
    assert (file["extension"], len(slides)) == ("pptx", 3)
    assert unknown.is_error


@pytest.mark.asyncio
async def test_a_file_tool_that_answers_data_that_is_not_base64_stops_the_download() -> None:
    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        return {"file": {"extension": "pptx", "media_type": "x", "data": "not base64!"}}

    ref = McpServerRef("lpcg", "/mcp", (), files=("build",))
    spec = SimpleNamespace(mcp=(ref,))

    with pytest.raises(ToolAnswerError, match="not base64"):
        await plugin_tool_file(spec, "AT-1", call)  # type: ignore[arg-type]
    assert await plugin_tool_file(SimpleNamespace(mcp=()), "AT-1", call) is None  # type: ignore[arg-type]
