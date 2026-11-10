"""Saved content is taken as a file by an MCP client: as a resource, or by a signed link."""

from __future__ import annotations

import base64
import io
import json
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, nullcontext
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi import HTTPException
from mcp import Client
from pptx import Presentation
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.api.file_routes import download_content_file_by_link
from app.domains.content.infrastructure import wiring as content_wiring
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.content_file import content_file, offers_file
from app.domains.content.infrastructure.download_links import (
    LIFETIME_SECONDS,
    SECRET_VARIABLE,
    is_valid,
    issue,
)
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.content_engine.infrastructure.tool_calls import tool_caller
from app.domains.content_engine.infrastructure.wiring import build_draft_tools
from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.content_engine.mcp.content_file import ContentFiles
from app.domains.content_engine.mcp.server import build_content_mcp
from tests.content_engine_support import PLAN, build_drafting_service, seed_lesson, server_over
from tests.test_content_file_download import _a_deck
from tests.test_slide_deck_plugin import SLIDE, _installed


@pytest.fixture(autouse=True)
def _own_server_on_the_tests_session(db: AsyncSession, monkeypatch: pytest.MonkeyPatch) -> None:
    """The route reaches the app's own MCP server; here it reads the test's session."""
    monkeypatch.setattr(content_wiring, "build_content_mcp_server", lambda: server_over(db))


PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
SECRET = "a-secret-only-the-server-knows"
NOW = 1_000_000.0


def test_a_link_is_valid_for_its_content_until_it_ends() -> None:
    expires, signature = issue(SECRET, "C1", NOW)

    assert expires == int(NOW) + LIFETIME_SECONDS
    assert is_valid(SECRET, "C1", expires, signature, NOW + LIFETIME_SECONDS - 1)
    assert not is_valid(SECRET, "C1", expires, signature, NOW + LIFETIME_SECONDS + 1)


def test_a_link_is_not_valid_for_other_content_or_another_time_or_without_a_secret() -> None:
    expires, signature = issue(SECRET, "C1", NOW)

    assert not is_valid(SECRET, "C2", expires, signature, NOW)
    assert not is_valid(SECRET, "C1", expires + 600, signature, NOW)
    assert not is_valid("another-secret", "C1", expires, signature, NOW)
    assert not is_valid(None, "C1", expires, signature, NOW)


@pytest.mark.asyncio
async def test_the_holder_of_a_link_downloads_the_deck_without_signing_in(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(SECRET_VARIABLE, SECRET)
    content_id = await _a_deck(db)
    expires, signature = issue(SECRET, content_id, time.time())

    response = await download_content_file_by_link(content_id, expires, signature, db)

    assert response.media_type == PPTX
    assert len(Presentation(io.BytesIO(response.body)).slides) == 3


@pytest.mark.asyncio
async def test_a_link_for_other_content_or_one_that_has_ended_is_refused(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(SECRET_VARIABLE, SECRET)
    content_id = await _a_deck(db)
    expires, signature = issue(SECRET, "another-content", time.time())
    ended, ended_signature = issue(SECRET, content_id, 1.0)

    for args in ((expires, signature), (ended, ended_signature)):
        with pytest.raises(HTTPException) as refused:
            await download_content_file_by_link(content_id, *args, db)
        assert (refused.value.status_code, refused.value.detail) == (403, "link_expired_or_invalid")


def _issuing(secret: str | None):
    return lambda content_id, now: issue(secret, content_id, now) if secret else None


@asynccontextmanager
async def _client(
    db: AsyncSession, secret: str | None = SECRET, *, signed_in: bool = True
) -> AsyncIterator[Client]:
    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    server = build_content_mcp(
        drafting=lambda: build_drafting_service(lambda: server),
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
        tools=build_draft_tools(),
        content_files=ContentFiles(
            build=lambda session, content_id: content_file(
                build_content_service(),
                build_content_catalogue(),
                tool_caller(lambda: server),
                session,
                content_id,
            ),
            offers=lambda session, record: offers_file(build_content_catalogue(), session, record),
            issue=_issuing(secret),
            lifetime_minutes=LIFETIME_SECONDS // 60,
        ),
    )
    async with Client(server) as client:
        with as_the_app() if signed_in else nullcontext():
            yield client


@pytest.mark.asyncio
async def test_a_client_reads_the_deck_as_a_binary_resource(db: AsyncSession) -> None:
    content_id = await _a_deck(db)

    async with _client(db) as client:
        read = await client.read_resource(f"content://{content_id}/file")

    (contents,) = read.contents
    assert contents.mime_type == "application/octet-stream"
    deck = base64.b64decode(contents.blob)
    assert len(Presentation(io.BytesIO(deck)).slides) == 3


@pytest.mark.asyncio
async def test_a_client_asks_for_a_link_that_downloads_the_same_deck(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(SECRET_VARIABLE, SECRET)
    content_id = await _a_deck(db)

    async with _client(db) as client:
        result = await client.call_tool("get_content_file_link", {"content_id": content_id})

    link = json.loads(result.content[0].text)
    url = urlparse(link["url"])
    query = parse_qs(url.query)
    assert link["expires_in_minutes"] == 15
    assert url.path in (f"/content/files/{content_id}", f"/api/content/files/{content_id}")
    response = await download_content_file_by_link(
        content_id, int(query["expires"][0]), query["signature"][0], db
    )
    assert len(Presentation(io.BytesIO(response.body)).slides) == 3


@pytest.mark.asyncio
async def test_no_link_is_made_where_links_are_not_set_up(db: AsyncSession) -> None:
    content_id = await _a_deck(db)

    async with _client(db, secret=None) as client:
        result = await client.call_tool("get_content_file_link", {"content_id": content_id})

    assert result.is_error
    assert "not set up" in result.content[0].text


@pytest.mark.asyncio
async def test_content_that_is_not_a_deck_is_not_offered_as_one(db: AsyncSession) -> None:
    await seed_lesson(db)
    async with _client(db) as client:
        result = await client.call_tool("get_content_file_link", {"content_id": "CT-missing"})

    assert result.is_error


@pytest.mark.asyncio
async def test_a_caller_who_has_not_signed_in_is_given_neither_the_file_nor_a_link(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(SECRET_VARIABLE, SECRET)
    content_id = await _a_deck(db)

    async with _client(db, signed_in=False) as client:
        link = await client.call_tool("get_content_file_link", {"content_id": content_id})
        with pytest.raises(Exception, match="Sign in"):
            await client.read_resource(f"content://{content_id}/file")

    assert link.is_error and "Sign in" in link.content[0].text


@pytest.mark.asyncio
async def test_submitting_a_deck_hands_back_its_download(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(SECRET_VARIABLE, SECRET)
    await _installed(db)
    async with _client(db) as client:
        started = await client.call_tool(
            "start_draft", {"type": "slide-deck", "plan_version_id": PLAN}
        )
        draft_id = json.loads(started.content[0].text)["draft_id"]
        for step in ("s1", "s2"):
            await client.call_tool(
                "add_part", {"draft_id": draft_id, "unit_id": step, "part": {"slides": [SLIDE]}}
            )
        submitted = await client.call_tool("submit_draft", {"draft_id": draft_id})

    saved = json.loads(submitted.content[0].text)
    assert saved["download"]["resource"] == f"content://{saved['saved_as']}/file"
    assert saved["download"]["url"].startswith("https://") or "://" in saved["download"]["url"]
    assert saved["download"]["expires_in_minutes"] == 15
