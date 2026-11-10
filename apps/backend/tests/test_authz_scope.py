"""Live integration coverage for ``check_scope`` (per-instance authorization).

Companion to ``test_authz.py`` (which pins policy semantics): this exercises the
Python-side scope check against the real DB — unscoped requests, globally-scoped
roles, and teacher workspace ownership (owns vs not own vs malformed). The
``test_authz.py`` docstring referenced this file, but it had gone missing, leaving
``user_owns_workspace`` / ``check_scope`` (the RBAC scope gate) uncovered.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text

from app.domains.teaching.models import TeacherWorkspace
from app.shared.auth import Actor
from app.shared.authz import (
    CASBIN_ROLE_ADMIN,
    CASBIN_ROLE_RESEARCHER,
    CASBIN_ROLE_TEACHER,
    check_scope,
)

pytestmark = pytest.mark.asyncio


def _teacher(teacher_id: uuid.UUID) -> Actor:
    return Actor(role="teacher", auth_id="code|t", teacher_id=teacher_id)


async def _seed_workspace(db, teacher_id: uuid.UUID) -> TeacherWorkspace:
    # FK checks off: term_class_subject_id's target is irrelevant to ownership.
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    workspace = TeacherWorkspace(
        teacher_id=teacher_id, term_class_subject_id=uuid.uuid4(), is_primary=True
    )
    db.add(workspace)
    await db.flush()
    return workspace


async def test_unscoped_request_is_allowed(db) -> None:
    allowed = await check_scope(
        actor=_teacher(uuid.uuid4()), casbin_role=CASBIN_ROLE_TEACHER, dom="*", db=db
    )
    assert allowed is True


async def test_global_roles_bypass_scope(db) -> None:
    actor = Actor(role="research_manager", auth_id="code|r", teacher_id=uuid.uuid4())
    dom = f"workspace|{uuid.uuid4()}"
    assert (
        await check_scope(actor=actor, casbin_role=CASBIN_ROLE_RESEARCHER, dom=dom, db=db) is True
    )
    assert await check_scope(actor=actor, casbin_role=CASBIN_ROLE_ADMIN, dom=dom, db=db) is True


async def test_teacher_owns_workspace(db) -> None:
    teacher_id = uuid.uuid4()
    workspace = await _seed_workspace(db, teacher_id)
    allowed = await check_scope(
        actor=_teacher(teacher_id),
        casbin_role=CASBIN_ROLE_TEACHER,
        dom=f"workspace|{workspace.id}",
        db=db,
    )
    assert allowed is True


async def test_teacher_does_not_own_workspace(db) -> None:
    workspace = await _seed_workspace(db, uuid.uuid4())  # owned by someone else
    allowed = await check_scope(
        actor=_teacher(uuid.uuid4()),
        casbin_role=CASBIN_ROLE_TEACHER,
        dom=f"workspace|{workspace.id}",
        db=db,
    )
    assert allowed is False


async def test_malformed_workspace_id_is_denied(db) -> None:
    allowed = await check_scope(
        actor=_teacher(uuid.uuid4()),
        casbin_role=CASBIN_ROLE_TEACHER,
        dom="workspace|not-a-uuid",
        db=db,
    )
    assert allowed is False
