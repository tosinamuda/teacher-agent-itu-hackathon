"""Actor identity + the teacher/manager gate used to attribute plan approval."""

from __future__ import annotations

import uuid

import pytest
from fastapi import HTTPException

import app.domains.artefacts.types.post_class_review_pack.api.routes as review_routes
from app.shared.auth import Actor, require_teacher_or_manager


def test_display_name_prefers_full_name_then_email_then_code() -> None:
    assert (
        Actor(
            role="teacher", auth_id="code|ab", full_name="Aunty Blessing", email="a@b.com"
        ).display_name
        == "Aunty Blessing"
    )
    assert Actor(role="teacher", auth_id="code|ab", email="a@b.com").display_name == "a@b.com"
    assert Actor(role="teacher", auth_id="code|aunty-blessing").display_name == "aunty-blessing"


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["teacher", "research_manager"])
async def test_gate_allows_teacher_and_manager(role: str) -> None:
    actor = Actor(role=role, auth_id="code|x")
    assert await require_teacher_or_manager(actor) is actor


@pytest.mark.asyncio
async def test_gate_rejects_anonymous() -> None:
    with pytest.raises(HTTPException) as exc:
        await require_teacher_or_manager(Actor(role="anonymous", auth_id="anonymous"))
    assert exc.value.status_code == 403


# --- The pack-review (C4 / HITL) ownership gate ----------------------------
#
# `_assert_owns_plan` is the same pattern as lesson-plan approval: a teacher may
# only review/approve packs for a class they teach; a research-manager bypasses.
# We stub the ownership query to isolate the wrapper's branching.


@pytest.mark.asyncio
async def test_pack_gate_manager_bypasses_ownership(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _would_deny(*_args: object, **_kwargs: object) -> bool:
        return False  # consulted → would deny; a manager must not reach it

    monkeypatch.setattr(review_routes, "teacher_owns_plan_version", _would_deny)
    manager = Actor(role="research_manager", auth_id="code|uncle-tosin", teacher_id=uuid.uuid4())
    await review_routes._assert_owns_plan(manager, db=None, plan_version_id="PV-1")  # no raise


@pytest.mark.asyncio
async def test_pack_gate_teacher_denied_when_not_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _deny(*_args: object, **_kwargs: object) -> bool:
        return False

    monkeypatch.setattr(review_routes, "teacher_owns_plan_version", _deny)
    teacher = Actor(role="teacher", auth_id="code|aunty-blessing", teacher_id=uuid.uuid4())
    with pytest.raises(HTTPException) as exc:
        await review_routes._assert_owns_plan(teacher, db=None, plan_version_id="PV-1")
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_pack_gate_teacher_allowed_when_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _allow(*_args: object, **_kwargs: object) -> bool:
        return True

    monkeypatch.setattr(review_routes, "teacher_owns_plan_version", _allow)
    teacher = Actor(role="teacher", auth_id="code|aunty-blessing", teacher_id=uuid.uuid4())
    await review_routes._assert_owns_plan(teacher, db=None, plan_version_id="PV-1")  # no raise
