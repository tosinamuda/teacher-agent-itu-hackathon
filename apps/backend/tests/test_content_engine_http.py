"""The content engine over HTTP: a researcher registers a type, a teacher generates it through
the queued job, and an outside MCP client signs in with an access code.

The production permission table and routes are real. Only the model is stood in for, by a
writer that calls the same MCP tools a model does.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import casbin
import pytest
import pytest_asyncio
from casbin.persist.adapters.string_adapter import StringAdapter
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette

from app.db.deps import get_db
from app.domains.content.api import routes as content_routes
from app.domains.content.infrastructure import wiring as content_wiring
from app.domains.content_engine.mcp import caller as engine_caller
from app.domains.content_engine.mcp.server import http_route
from app.domains.users.models.user import User
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES
from tests.chat_support import feed_over
from tests.content_engine_support import (
    PLAN,
    SPEC,
    ScriptedWriter,
    engine_over,
    part,
    seed_lesson,
    server_over,
)
from tests.queued_jobs import run_queued_job

TEACHER = uuid.UUID(int=801)
RESEARCHER = uuid.UUID(int=802)
NEW_TYPE = "practice-sheet"


def _actor(user_id: uuid.UUID, role: str) -> Actor:
    return Actor(role=role, auth_id=f"code|{user_id}", teacher_id=user_id, full_name=role)


@pytest_asyncio.fixture
async def http(db, monkeypatch) -> AsyncIterator[tuple[AsyncClient, list[Actor]]]:  # type: ignore[no-untyped-def]
    rows = [f"p, {role}, {obj}, {act}, allow" for role, obj, act in _CAPABILITY_POLICIES]
    rows += [f"g, {TEACHER}, teacher", f"g, {RESEARCHER}, researcher"]
    enforcer = casbin.Enforcer(authz.MODEL_PATH, StringAdapter("\n".join(rows)))

    async def _enforcer() -> casbin.Enforcer:
        return enforcer

    async def _owns(db, *, teacher_id: uuid.UUID, plan_version_id: str) -> bool:  # type: ignore[no-untyped-def]
        return teacher_id == TEACHER and plan_version_id == PLAN

    monkeypatch.setattr(authz, "get_enforcer", _enforcer)
    monkeypatch.setattr(content_routes, "teacher_owns_plan_version", _owns)
    monkeypatch.setattr(engine_caller, "teacher_owns_plan_version", _owns)
    await seed_lesson(db)
    caller = [_actor(RESEARCHER, "research_manager")]

    async def _db() -> AsyncIterator:
        yield db

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_actor] = lambda: caller[0]
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client, caller
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_a_researcher_registers_a_type_and_a_teacher_generates_it(
    http, db, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    client, caller = http
    spec = {**SPEC, "levels": ["class"]}
    body = {"type": NEW_TYPE, "label": "Practice sheet", "audience": "learner", "spec": spec}

    registered = await client.post("/content/types", json=body)
    caller[0] = _actor(TEACHER, "teacher")
    refused = await client.post("/content/types", json={**body, "type": "another-sheet"})
    listed = (await client.get("/content/types")).json()

    assert registered.status_code == 201, registered.text
    assert registered.json()["engine"] == "mcp"
    assert registered.json()["spec"]["part_schema"]["required"] == ["title", "examples"]
    assert refused.status_code == 403
    assert [t["type"] for t in listed][-2:] == ["worked-examples", NEW_TYPE]

    writer = ScriptedWriter({"s1": [part("One")], "s2": [part("Two")]})
    monkeypatch.setattr(content_wiring, "build_content_engine", lambda: engine_over(db, writer))
    monkeypatch.setattr(content_wiring, "CHAT_FEED", feed_over(db))
    queued = await client.post("/content", json={"plan_version_id": PLAN, "type": NEW_TYPE})
    assert queued.status_code == 202, queued.text
    made = await run_queued_job(db, monkeypatch, queued.json()["job_id"])
    content = (await client.get(f"/content/{made['content_id']}")).json()  # type: ignore[index]

    assert (content["type"], content["review_status"]) == (NEW_TYPE, "pending")
    assert [s["part"]["title"] for s in content["content"]["sections"]] == ["One", "Two"]
    learner = await client.post(
        "/content", json={"plan_version_id": PLAN, "type": NEW_TYPE, "level": "learner"}
    )
    assert learner.status_code == 422


@pytest.mark.asyncio
async def test_the_teachers_words_reach_the_writer_of_an_engine_type_and_no_other(
    http,
    db,
    monkeypatch,  # type: ignore[no-untyped-def]
) -> None:
    client, _ = http
    spec = {**SPEC, "levels": ["class"]}
    body = {"type": NEW_TYPE, "label": "Practice sheet", "audience": "learner", "spec": spec}
    await client.post("/content/types", json=body)
    writer = ScriptedWriter({"s1": [part("One")], "s2": [part("Two")]})
    monkeypatch.setattr(content_wiring, "build_content_engine", lambda: engine_over(db, writer))
    monkeypatch.setattr(content_wiring, "CHAT_FEED", feed_over(db))

    asked = {"plan_version_id": PLAN, "instructions": "Two short steps, with naira."}
    queued = await client.post("/content", json={**asked, "type": NEW_TYPE})
    await run_queued_job(db, monkeypatch, queued.json()["job_id"])
    builtin = await client.post("/content", json={**asked, "type": "class-test"})

    assert queued.status_code == 202, queued.text
    assert writer.seen["feedback"] == "Two short steps, with naira."
    assert builtin.status_code == 422
    assert "instructions_apply_to_engine_types_only" in builtin.text


@asynccontextmanager
async def _mcp_over_http(db) -> AsyncIterator[AsyncClient]:  # type: ignore[no-untyped-def]
    server = server_over(db)
    mcp_app = Starlette(routes=[http_route(server, "/mcp")])
    async with server.session_manager.run():
        async with AsyncClient(
            transport=ASGITransport(app=mcp_app), base_url="http://localhost"
        ) as client:
            yield client


def _call(tool: str, arguments: dict) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }


HEADERS = {
    "accept": "application/json, text/event-stream",
    "mcp-protocol-version": "2025-06-18",
}


@pytest.mark.asyncio
async def test_an_outside_client_signs_in_with_an_access_code(http, db) -> None:  # type: ignore[no-untyped-def]
    db.add(
        User(
            id=TEACHER,
            auth_id="code|teacher-engine",
            email="teacher-engine@example.org",
            full_name="Teacher Engine",
            role="teacher",
        )
    )
    await db.flush()
    start = _call("start_draft", {"type": "worked-examples", "plan_version_id": PLAN})

    async with _mcp_over_http(db) as mcp:
        header = await mcp.post(
            "/mcp", json=start, headers={**HEADERS, "x-teacher-code": "teacher-engine"}
        )
        bearer = await mcp.post(
            "/mcp", json=start, headers={**HEADERS, "authorization": "Bearer teacher-engine"}
        )
        anonymous = await mcp.post("/mcp", json=start, headers=HEADERS)

    for signed_in in (header, bearer):
        result = signed_in.json()["result"]
        assert not result["isError"], result
        assert json.loads(result["content"][0]["text"])["units"][0]["unit_id"] == "s1"
    assert anonymous.json()["result"]["isError"]
    assert "Sign in" in anonymous.json()["result"]["content"][0]["text"]
