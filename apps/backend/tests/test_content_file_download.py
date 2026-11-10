"""Saved content is downloaded as the file its plugin's tool makes, by whoever may read it."""

from __future__ import annotations

import base64
import io
import json
import shutil
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pptx import Presentation
from sqlalchemy.ext.asyncio import AsyncSession

import app.domains.content.api.routes as content_routes
from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.content.api.file_routes import download_content_file
from app.domains.content.api.routes import get_content
from app.domains.content.application.errors import ContentError
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.infrastructure import wiring as content_wiring
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.content_file import content_file, offers_file
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.infrastructure.engine import Request
from app.shared.auth import Actor
from app.shared.json_types import JsonObject
from tests.content_engine_support import PLAN, ScriptedWriter, engine_over, seed_lesson, server_over
from tests.plugin_folder import read_plugin
from tests.test_slide_deck_plugin import PLUGIN, SLIDE, _installed


@pytest.fixture(autouse=True)
def _own_server_on_the_tests_session(db: AsyncSession, monkeypatch: pytest.MonkeyPatch) -> None:
    """The route reaches the app's own MCP server; here it reads the test's session."""
    monkeypatch.setattr(content_wiring, "build_content_mcp_server", lambda: server_over(db))


PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
TEACHER = Actor(role="teacher", auth_id="code|t", teacher_id=uuid.UUID(int=1))
RESEARCHER = Actor(role="research_manager", auth_id="code|r", teacher_id=uuid.UUID(int=2))


async def _a_deck(db: AsyncSession) -> str:
    await _installed(db)
    deck = {"slides": [SLIDE]}
    built = await engine_over(db, ScriptedWriter({"s1": [deck], "s2": [deck]})).build(
        Request(type="slide-deck", plan_version_id=PLAN)
    )
    return built.saved_as


@pytest.mark.asyncio
async def test_a_researcher_downloads_the_deck_as_a_powerpoint_file(db: AsyncSession) -> None:
    content_id = await _a_deck(db)

    response = await download_content_file(content_id, RESEARCHER, db)

    assert response.media_type == PPTX
    assert response.headers["content-disposition"] == f'attachment; filename="{content_id}.pptx"'
    slides = list(Presentation(io.BytesIO(response.body)).slides)
    assert [slide.shapes.title.text for slide in slides] == [
        "Adding fractions",
        *[SLIDE["title"]] * 2,
    ]
    assert slides[0].placeholders[1].text_frame.text == "Mathematics · JSS1 · Fractions"
    assert slides[1].placeholders[1].text_frame.text.splitlines() == [
        "1/4 + 2/4",
        "Add the tops, keep the bottom",
    ]


@pytest.mark.asyncio
async def test_a_teacher_of_another_class_is_refused_the_deck(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    content_id = await _a_deck(db)

    async def not_theirs(*_args: object, **_kwargs: object) -> bool:
        return False

    monkeypatch.setattr(content_routes, "teacher_owns_plan_version", not_theirs)

    with pytest.raises(HTTPException) as refused:
        await download_content_file(content_id, TEACHER, db)

    assert (refused.value.status_code, refused.value.detail) == (403, "not_your_class")


async def _a_deck_from_plugin(db: AsyncSession, plugin: Path) -> str:
    await seed_lesson(db)
    read, _ = read_plugin(plugin)
    assert read is not None
    await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
        db, read, folder_digest(plugin), "Researcher"
    )
    deck = {"slides": [SLIDE]}
    built = await engine_over(db, ScriptedWriter({"s1": [deck], "s2": [deck]})).build(
        Request(type="slide-deck", plan_version_id=PLAN)
    )
    return built.saved_as


def _plugin_without_a_file_tool(tmp_path: Path) -> Path:
    copy = tmp_path / "slide-deck"
    shutil.copytree(PLUGIN, copy)
    artefact = copy / "com.tosinamuda.lpcg/slide-deck.json"
    record = json.loads(artefact.read_text())
    del record["files"]
    artefact.write_text(json.dumps(record))
    return copy


@pytest.mark.asyncio
async def test_a_deck_whose_plugin_lists_no_file_tool_is_refused_with_the_reason(
    db: AsyncSession, tmp_path: Path
) -> None:
    content_id = await _a_deck_from_plugin(db, _plugin_without_a_file_tool(tmp_path))

    with pytest.raises(HTTPException) as refused:
        await download_content_file(content_id, RESEARCHER, db)

    assert refused.value.status_code == 409
    assert refused.value.detail == "file_unavailable:its plugin lists no file tool"


class _Specs:
    """A catalogue whose every spec lists ``refs``."""

    def __init__(self, *refs: McpServerRef) -> None:
        self._spec = SimpleNamespace(mcp=refs)

    async def revision(self, db: object, slug: str, revision: int) -> SimpleNamespace:
        return self._spec

    async def current(self, db: object, slug: str) -> SimpleNamespace:
        return self._spec


class _Records:
    def __init__(self, type: str) -> None:
        self._record = SimpleNamespace(type=type, provenance={"spec_revision": 2})

    async def record(self, db: object, content_id: str) -> SimpleNamespace:
        return self._record


@pytest.mark.asyncio
async def test_content_of_any_type_is_made_into_the_file_its_spec_lists_a_tool_for() -> None:
    asked: list[tuple[str, JsonObject]] = []

    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        asked.append((tool, arguments))
        data = base64.b64encode(b"Adding fractions").decode()
        return {"file": {"extension": "txt", "media_type": "text/plain", "data": data}}

    listed = _Specs(McpServerRef("lpcg", "/mcp", (), files=("build_note_file",)))
    unlisted = _Specs(McpServerRef("lpcg", "/mcp", (), checks=("check_lesson_note",)))
    record = SimpleNamespace(type="lesson-note", provenance={"spec_revision": 2})

    made = await content_file(_Records("lesson-note"), listed, call, None, "AT-1")  # type: ignore[arg-type]

    assert (made.extension, made.media_type, made.data) == (
        "txt",
        "text/plain",
        b"Adding fractions",
    )
    assert asked == [("build_note_file", {"content_id": "AT-1"})]
    assert await offers_file(listed, None, record)  # type: ignore[arg-type]
    assert not await offers_file(unlisted, None, record)  # type: ignore[arg-type]
    with pytest.raises(ContentError, match="its plugin lists no file tool"):
        await content_file(_Records("lesson-note"), unlisted, call, None, "AT-1")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_content_whose_type_lists_a_file_tool_says_it_has_a_file(db: AsyncSession) -> None:
    content_id = await _a_deck(db)

    assert (await get_content(content_id, RESEARCHER, db)).has_file


@pytest.mark.asyncio
async def test_content_whose_type_lists_no_file_tool_says_it_has_none(
    db: AsyncSession, tmp_path: Path
) -> None:
    content_id = await _a_deck_from_plugin(db, _plugin_without_a_file_tool(tmp_path))

    assert not (await get_content(content_id, RESEARCHER, db)).has_file
