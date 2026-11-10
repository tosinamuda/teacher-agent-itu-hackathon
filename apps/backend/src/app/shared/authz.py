"""Casbin-backed authorization for FastAPI routes.

Two layers are checked in order on every ``enforce`` call:

1. **Policy (Casbin, declarative).** Does the user's *role* have ``act`` on the
   *kind* of object ``obj`` describes? Encoded as Casbin policies in the
   ``casbin_rule`` table; the model is in ``auth_model.conf``.
2. **Scope (Python, data-driven).** Does the user actually have authority over
   *this specific* workspace / packet / lesson? Encoded as ``check_scope`` —
   queries the live DB (``teacher_workspaces`` for teacher scope; rater and
   student branches added in Phases E/F).

Both must pass. The split is deliberate: scope checks are async DB lookups, and
forcing them into a sync Casbin matcher would be ugly. Roles + actions stay
declarative in the policy DB; scope stays in code where the data lives.
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Awaitable, Callable
from pathlib import Path

import casbin
from casbin_async_sqlalchemy_adapter import Adapter
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.db.session import engine
from app.domains.teaching.models import TeacherWorkspace
from app.shared.auth import (
    ROLE_ANONYMOUS,
    Actor,
    get_actor,
)

MODEL_PATH = str(Path(__file__).with_name("auth_model.conf"))

# Casbin role names (independent of the legacy user.role storage strings).
# DB still stores ``research_manager``; Casbin policy uses the clean ``researcher``.
CASBIN_ROLE_RESEARCHER = "researcher"
CASBIN_ROLE_TEACHER = "teacher"
CASBIN_ROLE_ADMIN = "admin"
CASBIN_ROLE_RATER = "rater"
CASBIN_ROLE_STUDENT = "student"

# Maps a ``users.role`` storage value to its Casbin policy role. The single source
# for both ``casbin_role_for`` (request-time translation) and ``grant_role_to_user``
# (the per-user grant on onboarding); mirrors
# ``migrations/data/casbin_policy_seed._USER_ROLE_TO_CASBIN`` (the bulk re-seed).
_USER_ROLE_TO_CASBIN: dict[str, str] = {
    "research_manager": CASBIN_ROLE_RESEARCHER,
    "teacher": CASBIN_ROLE_TEACHER,
    "admin": CASBIN_ROLE_ADMIN,
    "rater": CASBIN_ROLE_RATER,
    "student": CASBIN_ROLE_STUDENT,
}

# Roles that bypass the data-driven scope check (global access).
_UNSCOPED_ROLES: frozenset[str] = frozenset({CASBIN_ROLE_RESEARCHER, CASBIN_ROLE_ADMIN})


def casbin_role_for(actor_role: str) -> str:
    """Translate the actor's storage role to its Casbin policy name."""
    return _USER_ROLE_TO_CASBIN.get(actor_role, actor_role)


# ---------- Enforcer singleton ----------

_enforcer: casbin.AsyncEnforcer | None = None
_enforcer_lock = asyncio.Lock()


async def get_enforcer() -> casbin.AsyncEnforcer:
    """Return the process-wide enforcer, building it on first call.

    The enforcer is published to ``_enforcer`` only AFTER its policies finish
    loading. Assigning the half-built enforcer first (then ``await``-ing
    ``load_policy`` inside the lock) let concurrent requests read it through the
    pre-lock fast path during that ``await`` and enforce against an EMPTY policy
    set — every authorization denied with a spurious 403 on a freshly started
    server's first concurrent burst. Building into a local and publishing last
    closes that window.
    """
    global _enforcer
    if _enforcer is not None:
        return _enforcer
    async with _enforcer_lock:
        if _enforcer is None:
            adapter = Adapter(engine)
            enforcer = casbin.AsyncEnforcer(MODEL_PATH, adapter)
            await enforcer.load_policy()
            _enforcer = enforcer
    return _enforcer


async def reload_policy() -> None:
    """Re-read the policy DB into the enforcer (after seeding or admin edits)."""
    e = await get_enforcer()
    await e.load_policy()


async def grant_role_to_user(*, user_id: uuid.UUID, user_role: str) -> None:
    """Insert the Casbin ``g, <user_id>, <role>`` grant for a freshly-onboarded user.

    Idempotent: Casbin returns ``False`` if the (user_id, role) pair already
    exists; we don't care either way. Writes through the SQLAlchemy adapter so
    the in-memory enforcer + the ``casbin_rule`` table stay in sync without a
    server restart or a re-seed.

    A concurrent grant that slips past the in-memory check is now caught by the
    ``casbin_rule`` unique index (migration 0004): the loser's commit raises
    ``IntegrityError``, which we absorb — the grant existing is the desired end
    state — and reload the policy so in-memory matches the DB.
    """
    casbin_role = _USER_ROLE_TO_CASBIN.get(user_role)
    if casbin_role is None:
        return
    e = await get_enforcer()
    try:
        await e.add_grouping_policy(str(user_id), casbin_role)
    except IntegrityError:
        await reload_policy()


async def revoke_role_from_user(*, user_id: uuid.UUID, user_role: str) -> None:
    """Remove the Casbin ``g, <user_id>, <role>`` grant — onboarding compensation.

    The inverse of ``grant_role_to_user``, used to undo a grant when a later
    onboarding step fails (the grant is out-of-band from the request's DB
    transaction, so it can't roll back with it). Idempotent: a missing grant is a
    no-op.
    """
    casbin_role = _USER_ROLE_TO_CASBIN.get(user_role)
    if casbin_role is None:
        return
    e = await get_enforcer()
    await e.remove_grouping_policy(str(user_id), casbin_role)


# ---------- Scope (data-driven) ----------


async def user_owns_workspace(
    *, user_id: uuid.UUID, workspace_id: uuid.UUID, db: AsyncSession
) -> bool:
    """Truth: does this user teach this workspace? Queries teacher_workspaces."""
    result = await db.execute(
        select(TeacherWorkspace.id).where(
            TeacherWorkspace.teacher_id == user_id,
            TeacherWorkspace.id == workspace_id,
        )
    )
    return result.scalar_one_or_none() is not None


def _parse_scoped_dom(dom: str) -> tuple[str, str]:
    """Split a scoped domain string into ``(kind, id)`` — e.g. ``workspace|UUID``."""
    kind, _, ident = dom.partition("|")
    return kind, ident


async def check_scope(
    *,
    actor: Actor,
    casbin_role: str,
    dom: str,
    db: AsyncSession,
) -> bool:
    """Whether this actor has authority over the specific instance ``dom`` names.

    Returns True for unscoped requests (``dom`` is None / ``*``) and for globally
    scoped roles (researcher, admin). For teachers, checks workspace ownership.
    Rater + student branches land in Phases E / F.
    """
    if not dom or dom == "*":
        return True
    if casbin_role in _UNSCOPED_ROLES:
        return True
    kind, ident = _parse_scoped_dom(dom)
    if casbin_role == CASBIN_ROLE_TEACHER and kind == "workspace":
        if actor.teacher_id is None:
            return False
        try:
            workspace_id = uuid.UUID(ident)
        except ValueError:
            return False
        return await user_owns_workspace(user_id=actor.teacher_id, workspace_id=workspace_id, db=db)
    return False


# ---------- The public surface ----------


class _Forbidden(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def enforce(
    actor: Actor,
    *,
    obj: str,
    act: str,
    db: AsyncSession,
    dom: str | None = None,
) -> None:
    """Allow if policy + scope both permit, else raise 403.

    ``obj`` is a resource pattern like ``experiment:EXP-123`` or ``lesson_plan:*``.
    ``act`` is the verb (``read``, ``author_plan``, ``freeze_plan`` …).
    ``dom``, when given, names the specific instance the actor must have
    authority over (e.g. ``workspace|<uuid>``); omit for unscoped/global checks.
    """
    if actor.role == ROLE_ANONYMOUS or actor.teacher_id is None:
        raise _Forbidden("Sign in to perform this action.")
    role = casbin_role_for(actor.role)
    sub = str(actor.teacher_id)
    e = await get_enforcer()
    if not e.enforce(sub, obj, act):
        raise _Forbidden(f"Your role ({role}) is not permitted to {act} on {obj}.")
    if not await check_scope(actor=actor, casbin_role=role, dom=dom or "*", db=db):
        raise _Forbidden("You are not authorized for this specific resource.")


def requires(*, obj: str, act: str) -> Callable[..., Awaitable[Actor]]:
    """FastAPI dependency factory for routes whose scope is global.

    Use the explicit ``await enforce(actor, obj=..., act=..., dom=..., db=...)``
    inside the handler for routes that need per-resource scope (e.g.
    plan-authoring against a specific workspace).
    """

    async def _dep(
        actor: Actor = Depends(get_actor),
        db: AsyncSession = Depends(get_db),
    ) -> Actor:
        await enforce(actor, obj=obj, act=act, db=db)
        return actor

    return _dep
