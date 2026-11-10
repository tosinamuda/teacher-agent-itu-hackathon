"""Who is calling a tool, and whether they may.

An outside client names its caller with an access code, as the app does: the
``x-teacher-code`` header or ``Authorization: Bearer <code>``. The app's own writer runs in
this process after the app has already authorised the request that started it, so it calls
as the app and is not checked again.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owns_lesson_period,
    teacher_owns_plan_version,
)
from app.shared.auth import ROLE_TEACHER, Actor, actor_for_code
from app.shared.authz import enforce

#: What the app's own writer records as having made its drafts.
APP = "app"

#: Set while the app's own writer runs: the teacher it writes for, or "" for none.
_in_process: ContextVar[str | None] = ContextVar("content_engine_in_process", default=None)


class PermissionRefusedError(Exception):
    """The caller's role or classes do not allow the call."""


@dataclass(frozen=True)
class Caller:
    #: Who a draft is recorded as started by; only they work on it.
    by: str
    #: The signed-in person, or ``None`` for the app's own writer.
    actor: Actor | None
    #: The teacher whose work this is, recorded as the author of what it saves.
    author: str | None = None


@contextmanager
def as_the_app(for_teacher: str | None = None) -> Iterator[None]:
    """Run the app's own writer: every tool it calls in this context calls as the app.

    ``for_teacher`` is who asked for the work, already authorised by the app.
    """
    token = _in_process.set(for_teacher or "")
    try:
        yield
    finally:
        _in_process.reset(token)


def _code(headers: Mapping[str, str] | None) -> str | None:
    if not headers:
        return None
    lowered = {name.lower(): value for name, value in headers.items()}
    if lowered.get("x-teacher-code"):
        return lowered["x-teacher-code"]
    scheme, _, token = lowered.get("authorization", "").partition(" ")
    return token.strip() if scheme.lower() == "bearer" and token.strip() else None


async def caller(db: AsyncSession, headers: Mapping[str, str] | None) -> Caller:
    """The app's own writer, else the person the request's access code names."""
    for_teacher = _in_process.get()
    if for_teacher is not None:
        return Caller(by=APP, actor=None, author=for_teacher or None)
    actor = await actor_for_code(db, _code(headers))
    author = str(actor.teacher_id) if actor.teacher_id is not None else None
    return Caller(by=actor.auth_id, actor=actor, author=author)


async def permit(
    db: AsyncSession,
    caller: Caller,
    act: str,
    *,
    plan_version_id: str | None = None,
    obj: str = "content:*",
) -> None:
    """Refuse what the caller's role or classes do not allow."""
    actor = caller.actor
    if actor is None:
        return
    try:
        await enforce(actor, obj=obj, act=act, db=db)
    except HTTPException as error:
        raise PermissionRefusedError(str(error.detail)) from error
    if (
        plan_version_id is not None
        and actor.role == ROLE_TEACHER
        and actor.teacher_id is not None
        and not await teacher_owns_plan_version(
            db, teacher_id=actor.teacher_id, plan_version_id=plan_version_id
        )
    ):
        raise PermissionRefusedError(f"plan version {plan_version_id} is not one of your classes'")


async def permit_planning(db: AsyncSession, caller: Caller, session_id: str) -> None:
    """Refuse a plan for a lesson the caller may not plan: a teacher plans their own classes."""
    actor = caller.actor
    if actor is None:
        return
    try:
        await enforce(actor, obj="lesson_plan:*", act="author_plan", db=db)
    except HTTPException as error:
        raise PermissionRefusedError(str(error.detail)) from error
    if actor.role != ROLE_TEACHER or actor.teacher_id is None:
        return
    try:
        lesson_period_id = uuid.UUID(session_id)
    except ValueError as error:
        raise PermissionRefusedError(f"there is no lesson {session_id!r}") from error
    if not await teacher_owns_lesson_period(
        db, teacher_id=actor.teacher_id, lesson_period_id=lesson_period_id
    ):
        raise PermissionRefusedError(f"lesson {session_id} is not one of your classes'")
