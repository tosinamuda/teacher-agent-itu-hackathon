"""Identity introspection routes."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.evaluation.infrastructure.repository import EvaluationRepository
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.learners.infrastructure.repository import LearnerRepository
from app.domains.users.api.deps import role_grants, user_onboarding_store
from app.domains.users.application.onboarding import (
    RoleGrantPort,
    UserOnboardingCommand,
    UserOnboardingError,
    UserOnboardingStore,
    onboard_user,
)
from app.domains.users.application.service import UserApplicationService
from app.shared.auth import (
    ROLE_ADMIN,
    ROLE_RATER,
    ROLE_RESEARCH_MANAGER,
    ROLE_STUDENT,
    ROLE_TEACHER,
    Actor,
    get_actor,
)
from app.shared.authz import requires
from app.shared.schema_base import StrictRequest, UtcDatetime

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthMeResponse(BaseModel):
    """The resolved caller behind the current request.

    Role-specific scope ids (``rater_id``, ``student_id``) are populated only
    for that role so the frontend can branch its home without a second fetch.
    """

    role: str
    auth_id: str
    email: str | None = None
    full_name: str | None = None
    # The user's UUID — kept named ``teacher_id`` for frontend compat. It is
    # the same id for every role; rename in a later pass.
    teacher_id: str | None = None
    is_research_manager: bool
    # Public scope ids — populated per-role; everyone else gets None.
    rater_id: str | None = None
    student_id: str | None = None


@router.get("/me", response_model=AuthMeResponse)
async def get_me(
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> AuthMeResponse:
    """Return the caller's role + identity so the UI can gate surfaces + scope lists."""
    rater_id: str | None = None
    student_id: str | None = None
    if actor.teacher_id is not None:
        if actor.role == ROLE_RATER:
            rater = await EvaluationRepository(db).get_rater_by_user_id(user_id=actor.teacher_id)
            rater_id = rater.rater_id if rater is not None else None
        elif actor.role == ROLE_STUDENT:
            learner = await LearnerRepository().get_learner_by_user_id(db, actor.teacher_id)
            student_id = learner.student_id if learner is not None else None
    return AuthMeResponse(
        role=actor.role,
        auth_id=actor.auth_id,
        email=actor.email,
        full_name=actor.full_name,
        teacher_id=str(actor.teacher_id) if actor.teacher_id is not None else None,
        is_research_manager=actor.is_research_manager,
        rater_id=rater_id,
        student_id=student_id,
    )


# --- User management (Phase I) ---


# Roles an admin can onboard via the unified user-create endpoint. A ``student``
# login must be paired with an existing StudentProfile (``student_id`` required) —
# the profile itself comes from the class roster (POST /learners).
_ONBOARDABLE_ROLES = Literal["research_manager", "teacher", "rater", "admin", "student"]


class UserSummaryResponse(BaseModel):
    """One row in the user list — base fields + the role-linked public id when present."""

    id: str
    auth_id: str
    email: str | None
    full_name: str | None
    role: str
    created_at: UtcDatetime | None
    # When the user is bound to a role-specific profile, its public id is surfaced
    # here so the admin can see "this teacher login = X workspaces" at a glance
    # without another fetch (workspace count is a TODO; rater_id / student_id
    # land cleanly).
    rater_id: str | None = None
    student_id: str | None = None


class UserCreateRequest(StrictRequest):
    """Onboard a user. ``code`` becomes the login (auth_id = code|<code>)."""

    code: str = Field(..., min_length=1, max_length=64)
    # Plain string by design — matches the User model and avoids the
    # email-validator dependency. UI should validate shape client-side.
    email: str = Field(..., min_length=3, max_length=255)
    full_name: str | None = Field(default=None, max_length=128)
    role: _ONBOARDABLE_ROLES
    # Required when ``role == "student"``: the StudentProfile (public id) this
    # login is bound to. The profile's portal code is set to ``code`` too, so
    # the student has ONE code for both sign-in and the portal.
    student_id: str | None = Field(default=None, max_length=64)


@router.get("/users", response_model=list[UserSummaryResponse])
async def list_users(
    role: str | None = None,
    experiment_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="auth/user:*", act="read")),
) -> list[UserSummaryResponse]:
    """List every user, optionally filtered by role and/or experiment.

    Admin-only via ``auth/user:*, read`` (researcher gets it via the global
    wildcard). The role-linked public ids (rater_id / student_id) are joined
    in so a single round-trip drives the management list.

    ``experiment_id`` narrows to logins paired with a student profile that
    appears in any focal case or condition run of that experiment — used by
    the admin "students in experiment X" filter. Non-student users always
    drop out when this filter is set.
    """
    service = UserApplicationService()
    users = await service.list_users(db=db)
    # Optional filter; done in Python because the table is small.
    if role:
        users = [u for u in users if u.role == role]
    if experiment_id:
        student_ids = await ExperimentRepository(db).list_student_ids_for_experiment(experiment_id)
        allowed_user_ids = await LearnerRepository().list_user_ids_for_student_ids(db, student_ids)
        users = [u for u in users if u.id in allowed_user_ids]
    # Batched lookups for the role-linked public ids — keeps it one trip per
    # role family instead of N round trips through the user list.
    eval_repo = EvaluationRepository(db)
    learner_repo = LearnerRepository()
    rater_id_by_user: dict[str, str] = {}
    student_id_by_user: dict[str, str] = {}
    for user in users:
        if user.role == ROLE_RATER:
            rater = await eval_repo.get_rater_by_user_id(user_id=user.id)
            if rater is not None:
                rater_id_by_user[str(user.id)] = rater.rater_id
        elif user.role == ROLE_STUDENT:
            learner = await learner_repo.get_learner_by_user_id(db, user.id)
            if learner is not None:
                student_id_by_user[str(user.id)] = learner.student_id

    return [
        UserSummaryResponse(
            id=str(user.id),
            auth_id=user.auth_id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at,
            rater_id=rater_id_by_user.get(str(user.id)),
            student_id=student_id_by_user.get(str(user.id)),
        )
        for user in users
    ]


@router.post("/users", response_model=UserSummaryResponse)
async def create_user(
    payload: UserCreateRequest,
    store: UserOnboardingStore = Depends(user_onboarding_store),
    grants: RoleGrantPort = Depends(role_grants),
    _actor: Actor = Depends(requires(obj="auth/user:*", act="create")),
) -> UserSummaryResponse:
    """Onboard a user with role-driven side effects.

    ``rater`` also creates an ``EvaluationRater`` row linked to the user, so
    the new user immediately has a rater profile for assignments.
    ``student`` requires ``student_id`` and binds the login to that existing
    StudentProfile (sets ``user_id`` AND the profile's portal ``code``), so the
    student signs in and submits as one identity.
    ``researcher`` / ``admin`` / ``teacher`` create no extra rows (a teacher's
    workspace is assigned separately under Setup).
    """
    try:
        user = await onboard_user(
            UserOnboardingCommand(
                code=payload.code,
                email=str(payload.email),
                full_name=payload.full_name,
                role=payload.role,
                student_id=payload.student_id,
            ),
            store=store,
            role_grants=grants,
        )
    except UserOnboardingError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error

    return UserSummaryResponse(
        id=str(user.id),
        auth_id=user.auth_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=user.created_at,
        rater_id=user.rater_id,
        student_id=user.student_id,
    )


# ``ROLE_RESEARCH_MANAGER``, ``ROLE_TEACHER``, ``ROLE_ADMIN`` referenced via
# Literal above for OpenAPI; bind them here so the import order is intentional.
_ = (ROLE_RESEARCH_MANAGER, ROLE_TEACHER, ROLE_ADMIN)
