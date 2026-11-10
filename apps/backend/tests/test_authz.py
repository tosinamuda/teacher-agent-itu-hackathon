"""Enforcer behaviour tests (Phase B of the RBAC redesign).

Two layers under test:

1. Casbin policy — does each role get the verbs it's supposed to, declared in
   ``migrations/data/casbin_policy_seed.py``? The fixture below feeds the same
   policy text into an in-memory ``StringAdapter`` so the test doesn't need the
   DB-backed adapter (the upstream adapter is exercised in production).
2. ``check_scope`` — does the Python-side per-instance check do the right thing
   for unscoped requests, globally-scoped roles, and teacher workspace
   ownership? The first two cases are exercised inline; teacher ownership is
   covered by the live integration test in ``tests/test_authz_scope.py``
   (separate file because it needs the ``db`` fixture).
"""

from __future__ import annotations

import uuid

import casbin
import pytest
from casbin import StringAdapter

from app.shared import authz
from app.shared.auth import (
    ROLE_ANONYMOUS,
    ROLE_RATER,
    ROLE_RESEARCH_MANAGER,
    ROLE_TEACHER,
    Actor,
)

# Stable test identities. UUIDs go straight into the ``g`` rows so the in-memory
# enforcer sees the same subject the production ``enforce()`` would compute.
RESEARCHER_ID = uuid.UUID(int=1)
TEACHER_JANE_ID = uuid.UUID(int=2)
TEACHER_BOB_ID = uuid.UUID(int=3)
RATER_RHEA_ID = uuid.UUID(int=4)
WORKSPACE_JANE_ID = uuid.UUID(int=10)
WORKSPACE_BOB_ID = uuid.UUID(int=11)

# Mirrors the researcher / teacher / rater capabilities in
# ``casbin_policy_seed._CAPABILITY_POLICIES``. Keep in lock-step with that seed:
# the teacher deliberately holds NO ``experiment:*`` verb (detail/story/stats are
# researcher surfaces) and NO ``c4_decision:*`` verb (C4 is now ``pack:* approve``).
POLICY_TEXT = f"""
p, researcher, *, *, allow
p, teacher, lesson_plan:*, author_plan, allow
p, teacher, lesson_plan:*, freeze_plan, allow
p, teacher, learner:*, read, allow
p, teacher, workspace:*, read, allow
p, teacher, pack:*, read, allow
p, teacher, pack:*, create, allow
p, teacher, pack:*, regenerate, allow
p, teacher, pack:*, approve, allow
p, teacher, material:*, read, allow
p, teacher, material:*, create, allow
p, teacher, material:*, approve, allow
p, teacher, artefact_revision:*, revise, allow
p, rater, rater_session:*, create, allow
p, rater, pack:*, read, allow
p, rater, rating:*, read, allow
p, rater, rating:*, create, allow
p, rater, rating:*, update, allow
p, rater, assignment:*, read, allow

g, {RESEARCHER_ID}, researcher
g, {TEACHER_JANE_ID}, teacher
g, {TEACHER_BOB_ID}, teacher
g, {RATER_RHEA_ID}, rater
""".strip()


@pytest.fixture(autouse=True)
def _stub_enforcer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace the module's async enforcer-factory with an in-memory one."""
    e = casbin.Enforcer(authz.MODEL_PATH, StringAdapter(POLICY_TEXT))

    async def _fake_get_enforcer() -> casbin.Enforcer:  # noqa: ANN202 - matches the real signature shape
        return e

    monkeypatch.setattr(authz, "get_enforcer", _fake_get_enforcer)


def _actor(*, role: str, user_id: uuid.UUID | None) -> Actor:
    return Actor(
        role=role,
        auth_id=f"code|{user_id}" if user_id else "anonymous",
        teacher_id=user_id,
        email=None,
        full_name=None,
    )


# Tests don't use the DB session for the policy layer; we still need a
# placeholder because ``enforce`` typing wants one. ``None`` is fine — the
# unscoped branch returns before any DB call.
_NO_DB = None  # type: ignore[assignment]


# ===== Anonymous always denied =====


@pytest.mark.asyncio
async def test_anonymous_is_denied() -> None:
    actor = _actor(role=ROLE_ANONYMOUS, user_id=None)
    with pytest.raises(authz._Forbidden):
        await authz.enforce(actor, obj="experiment:any", act="read", db=_NO_DB)


# ===== Researcher: global allow on every (obj, act) =====


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("obj", "act"),
    [
        ("experiment:EXP-1", "read"),
        ("experiment:EXP-1", "create"),
        ("lesson_plan:LPV-1", "freeze_plan"),
        ("study:INV-1", "end"),
        ("school:S-1", "delete"),
    ],
)
async def test_researcher_allowed_globally(obj: str, act: str) -> None:
    actor = _actor(role=ROLE_RESEARCH_MANAGER, user_id=RESEARCHER_ID)
    # No raise == allowed.
    await authz.enforce(actor, obj=obj, act=act, db=_NO_DB)


# ===== Teacher: only the declared (obj, act) pairs =====


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("obj", "act"),
    [
        ("lesson_plan:LPV-1", "author_plan"),
        ("lesson_plan:LPV-1", "freeze_plan"),
        ("learner:any", "read"),
        ("workspace:any", "read"),
        ("pack:any", "read"),
        ("pack:any", "create"),
        ("pack:any", "regenerate"),
        # C4 base-pack validation is the teacher's pack approval (no separate
        # ``c4_decision`` verb any more). Also gates GET /experiments/{id}/summary
        # — the teacher reaches it via author_plan (mirrors the experiments list).
        ("pack:any", "approve"),
        # HITL revision chat (lesson plan / class review note / diagnostic).
        ("artefact_revision:any", "revise"),
    ],
)
async def test_teacher_allowed_for_declared_capabilities(obj: str, act: str) -> None:
    actor = _actor(role=ROLE_TEACHER, user_id=TEACHER_JANE_ID)
    await authz.enforce(actor, obj=obj, act=act, db=_NO_DB)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("obj", "act", "reason"),
    [
        # The boundary this whole bug turns on: experiment detail/story/stats are
        # researcher surfaces, so the teacher role holds no ``experiment:*`` verb.
        # Their experiment-plan page rides ``lesson_plan:*`` / ``pack:*`` instead
        # (e.g. GET /experiments/{id}/summary, gated by author_plan).
        ("experiment:EXP-1", "read", "experiment detail is a researcher surface"),
        ("experiment:EXP-1", "create", "teachers don't create experiments"),
        ("experiment:EXP-1", "end", "teachers don't end studies"),
        ("c4_decision:any", "create", "no c4_decision verb — C4 is pack:* approve now"),
        ("study:INV-1", "read", "study object is researcher-only"),
        ("lesson_plan:LPV-1", "delete", "teachers don't delete plans"),
        ("school:S-1", "read", "schools are admin-only"),
    ],
)
async def test_teacher_denied_for_undeclared_capabilities(obj: str, act: str, reason: str) -> None:
    actor = _actor(role=ROLE_TEACHER, user_id=TEACHER_JANE_ID)
    with pytest.raises(authz._Forbidden):
        await authz.enforce(actor, obj=obj, act=act, db=_NO_DB)


# ===== Scope short-circuits =====


@pytest.mark.asyncio
async def test_researcher_bypasses_scope_check() -> None:
    """A researcher with a workspace-scoped dom still passes (global access)."""
    actor = _actor(role=ROLE_RESEARCH_MANAGER, user_id=RESEARCHER_ID)
    # No DB needed — the unscoped-role branch returns before any lookup.
    await authz.enforce(
        actor,
        obj="lesson_plan:LPV-1",
        act="freeze_plan",
        db=_NO_DB,
        dom=f"workspace|{WORKSPACE_JANE_ID}",
    )


@pytest.mark.asyncio
async def test_unscoped_request_skips_scope_check_for_teacher() -> None:
    """``dom`` omitted means the route didn't care about scope; teacher still gets the verb."""
    actor = _actor(role=ROLE_TEACHER, user_id=TEACHER_JANE_ID)
    await authz.enforce(actor, obj="pack:any", act="read", db=_NO_DB)


@pytest.mark.asyncio
async def test_check_scope_rejects_unparseable_workspace_id() -> None:
    """A garbled ``workspace|...`` dom is rejected without a DB call."""
    actor = _actor(role=ROLE_TEACHER, user_id=TEACHER_JANE_ID)
    allowed = await authz.check_scope(
        actor=actor, casbin_role=authz.CASBIN_ROLE_TEACHER, dom="workspace|not-a-uuid", db=_NO_DB
    )
    assert allowed is False


@pytest.mark.asyncio
async def test_check_scope_rejects_unknown_kind() -> None:
    """A teacher asked about ``packet|...`` (not their scope) is denied without a DB call."""
    actor = _actor(role=ROLE_TEACHER, user_id=TEACHER_JANE_ID)
    allowed = await authz.check_scope(
        actor=actor, casbin_role=authz.CASBIN_ROLE_TEACHER, dom=f"packet|{uuid.uuid4()}", db=_NO_DB
    )
    assert allowed is False


# ===== Rater: can self-identify, cannot escalate to admin onboarding =====


@pytest.mark.asyncio
async def test_rater_can_create_session() -> None:
    """A rater holds the dedicated ``rater_session:*, create`` verb for self-identification."""
    actor = _actor(role=ROLE_RATER, user_id=RATER_RHEA_ID)
    # No raise == allowed (matches POST /evaluation/raters/session's gate).
    await authz.enforce(actor, obj="rater_session:*", act="create", db=_NO_DB)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("obj", "act", "reason"),
    [
        ("auth/user:*", "create", "rater must not onboard users"),
        ("school:*", "create", "rater must not create schools"),
        ("learner:*", "create", "rater must not create learners"),
        ("artefact_revision:*", "revise", "raters don't revise artefacts"),
    ],
)
async def test_rater_cannot_reach_admin_onboarding(obj: str, act: str, reason: str) -> None:
    """The session verb is scoped: a rater can't piggy-back onto the broad onboarding verbs."""
    actor = _actor(role=ROLE_RATER, user_id=RATER_RHEA_ID)
    with pytest.raises(authz._Forbidden):
        await authz.enforce(actor, obj=obj, act=act, db=_NO_DB)
