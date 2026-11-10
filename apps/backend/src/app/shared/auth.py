"""Code-identity RBAC primitives.

Identity is carried by the ``x-teacher-code`` header. A code ``X`` resolves to a
``Teacher`` row via ``auth_id = "code|X"``; the teacher's ``role`` column drives
authorization. There is intentionally no login/session layer — this is a
research prototype whose identities are short codes.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.users.application.service import UserApplicationService

ROLE_RESEARCH_MANAGER = "research_manager"
ROLE_TEACHER = "teacher"
ROLE_ADMIN = "admin"
ROLE_RATER = "rater"
ROLE_STUDENT = "student"
ROLE_ANONYMOUS = "anonymous"


@dataclass(frozen=True)
class Actor:
    """The resolved caller behind a request."""

    role: str
    auth_id: str
    teacher_id: uuid.UUID | None = None
    email: str | None = None
    full_name: str | None = None

    @property
    def is_research_manager(self) -> bool:
        return self.role == ROLE_RESEARCH_MANAGER

    @property
    def display_name(self) -> str:
        """A human label for this actor (for ``approved_by`` etc.)."""
        return self.full_name or self.email or self.auth_id.removeprefix("code|")


async def get_actor(
    x_teacher_code: str | None = Header(default=None, alias="x-teacher-code"),
    db: AsyncSession = Depends(get_db),
) -> Actor:
    """Resolve the caller from the ``x-teacher-code`` header.

    A missing header (or an unknown code) yields an anonymous actor rather than
    silently defaulting to a privileged identity, so gated routes fail closed.
    """
    return await actor_for_code(db, x_teacher_code)


async def actor_for_code(db: AsyncSession, code: str | None) -> Actor:
    """The caller an access code names; anonymous for no code or an unknown one."""
    if not code:
        return Actor(role=ROLE_ANONYMOUS, auth_id="anonymous")

    auth_id = f"code|{code}"
    user = await UserApplicationService().get_user_by_auth_id(db=db, auth_id=auth_id)
    if not user:
        return Actor(role=ROLE_ANONYMOUS, auth_id=auth_id)

    return Actor(
        role=user.role,
        auth_id=user.auth_id,
        teacher_id=user.id,
        email=user.email,
        full_name=getattr(user, "full_name", None),
    )


async def require_research_manager(actor: Actor = Depends(get_actor)) -> Actor:
    """Gate a route to research-manager actors; raise 403 otherwise."""
    if not actor.is_research_manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires the research-manager role.",
        )
    return actor


async def require_teacher_or_manager(actor: Actor = Depends(get_actor)) -> Actor:
    """Gate to a signed-in teacher or research-manager; raise 403 for anonymous.

    Used for actions that must be attributable to a real person — e.g. freezing
    (approving) a lesson plan, where ``approved_by`` has to be the actual teacher
    (or a research-manager acting on their behalf), not a free-text string.
    """
    if actor.role not in (ROLE_TEACHER, ROLE_RESEARCH_MANAGER):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in as the teacher (or a research-manager) to approve a lesson plan.",
        )
    return actor
