"""Sending a teacher's document to be written into a lesson plan, over HTTP."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator

import casbin
import pytest
import pytest_asyncio
from casbin.persist.adapters.string_adapter import StringAdapter
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.db.deps import get_db
from app.domains.content_engine.api import routes as plan_import_routes
from app.infra.jobs.kinds import IMPORT_LESSON_PLAN
from app.infra.jobs.models import Job
from app.main import app
from app.shared import authz
from app.shared.auth import Actor, get_actor
from migrations.data.casbin_policy_seed import _CAPABILITY_POLICIES
from tests.plan_import_support import DOCUMENT, LESSON, InMemoryPlanning

TEACHER = uuid.UUID(int=901)
OTHER_TEACHER = uuid.UUID(int=902)


@pytest_asyncio.fixture
async def http(db, monkeypatch) -> AsyncIterator[tuple[AsyncClient, list[Actor]]]:  # type: ignore[no-untyped-def]
    rows = [f"p, {role}, {obj}, {act}, allow" for role, obj, act in _CAPABILITY_POLICIES]
    rows += [f"g, {TEACHER}, teacher", f"g, {OTHER_TEACHER}, teacher"]
    enforcer = casbin.Enforcer(authz.MODEL_PATH, StringAdapter("\n".join(rows)))

    async def _enforcer() -> casbin.Enforcer:
        return enforcer

    async def _owns(db, *, teacher_id: uuid.UUID, lesson_period_id: uuid.UUID) -> bool:  # type: ignore[no-untyped-def]
        return teacher_id == TEACHER and str(lesson_period_id) == LESSON

    monkeypatch.setattr(authz, "get_enforcer", _enforcer)
    monkeypatch.setattr(plan_import_routes, "teacher_owns_lesson_period", _owns)
    monkeypatch.setattr(plan_import_routes, "LessonPlanning", InMemoryPlanning)
    caller = [Actor(role="teacher", auth_id=f"code|{TEACHER}", teacher_id=TEACHER)]

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
async def test_a_teacher_s_document_queues_one_import_for_their_lesson(http, db) -> None:  # type: ignore[no-untyped-def]
    client, _ = http

    first = await client.post("/plan-imports", data={"session_id": LESSON, "text": DOCUMENT})
    again = await client.post("/plan-imports", data={"session_id": LESSON, "text": DOCUMENT})
    job = (await db.execute(select(Job).where(Job.job_id == first.json()["job_id"]))).scalar_one()

    assert first.status_code == 202, first.text
    assert again.json()["job_id"] == first.json()["job_id"]
    assert (job.kind, job.args) == (
        IMPORT_LESSON_PLAN,
        [LESSON, DOCUMENT.strip(), str(TEACHER), None],
    )


@pytest.mark.asyncio
async def test_a_document_file_is_read_and_an_unreadable_one_refused(http) -> None:  # type: ignore[no-untyped-def]
    client, _ = http

    read = await client.post(
        "/plan-imports",
        data={"session_id": LESSON},
        files={"file": ("plan.md", DOCUMENT.encode(), "text/markdown")},
    )
    refused = await client.post(
        "/plan-imports",
        data={"session_id": LESSON},
        files={"file": ("plan.pages", b"...", "application/octet-stream")},
    )

    assert read.status_code == 202
    assert (refused.status_code, refused.json()["detail"]) == (
        422,
        "send one of .txt, .md, .docx, .pdf",
    )


@pytest.mark.asyncio
async def test_another_class_s_lesson_and_an_unknown_lesson_are_refused(http) -> None:  # type: ignore[no-untyped-def]
    client, caller = http
    unknown = await client.post(
        "/plan-imports", data={"session_id": str(uuid.uuid4()), "text": DOCUMENT}
    )
    caller[0] = Actor(role="teacher", auth_id=f"code|{OTHER_TEACHER}", teacher_id=OTHER_TEACHER)
    other = await client.post("/plan-imports", data={"session_id": LESSON, "text": DOCUMENT})
    caller[0] = Actor(role="teacher", auth_id=f"code|{TEACHER}", teacher_id=TEACHER)
    empty = await client.post("/plan-imports", data={"session_id": LESSON})

    assert unknown.status_code == 404
    assert other.status_code == 403
    assert (empty.status_code, empty.json()["detail"]) == (
        422,
        "send the document's text or its file",
    )
