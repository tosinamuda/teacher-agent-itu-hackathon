"""Seed the Casbin policy DB with role capabilities + existing role grants.

Two-part idempotent seed:

1. **Capability policies (``p`` rows)** — what each role is allowed to do.
   Static; the same set every time. Researcher = global wildcard; teacher gets
   the explicit verbs for experiments / plans / packs / governance / learners.
   Admin / rater / student capabilities seed in their respective phases.
2. **Role grants (``g`` rows)** — which existing users hold which Casbin role.
   Derived live from the ``users`` table: every user with role
   ``research_manager`` gets ``g, <user_id>, researcher``; ``teacher`` →
   ``g, <user_id>, teacher``.

Idempotent: each row is inserted only if an identical ``(ptype, v0..v5)`` row is
not already present. Safe to re-run after onboarding new users (re-derives any
missing grants) or after editing capabilities (adds new rows; never deletes).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa

CASBIN_ROLE_RESEARCHER = "researcher"
CASBIN_ROLE_TEACHER = "teacher"
CASBIN_ROLE_ADMIN = "admin"
CASBIN_ROLE_RATER = "rater"
CASBIN_ROLE_STUDENT = "student"

# (role, obj_pattern, action) — what each role can do.
_CAPABILITY_POLICIES: list[tuple[str, str, str]] = [
    # Researcher: a global wildcard. Carries every action everywhere. (For now the
    # sole researcher is also the platform operator; a future phase may narrow this
    # to research-only verbs once the frontend splits research from admin.)
    (CASBIN_ROLE_RESEARCHER, "*", "*"),
    # Teacher capabilities — scoped to "their" workspaces by the Python scope check.
    # Deliberately NO ``experiment:*`` verb: experiment detail / story /
    # statistics / export are researcher surfaces; every teacher flow rides
    # workspace:* / pack:* / lesson_plan:* (2026-06-11: a signed-in teacher
    # could open /research/experiments/… — removed).
    (CASBIN_ROLE_TEACHER, "lesson_plan:*", "author_plan"),
    (CASBIN_ROLE_TEACHER, "lesson_plan:*", "freeze_plan"),
    (CASBIN_ROLE_TEACHER, "lesson_plan:*", "read"),
    # C4 is the teacher's base-pack review + approval (pack:* approve below) —
    # there is no separate c4_decision verb any more.
    (CASBIN_ROLE_TEACHER, "learner:*", "read"),
    # FD-04: record a student's classwork responses on their behalf (no student
    # login). Its own verb — NOT the student's ``submission:*, create`` — so the
    # teacher path can't be reached by a student and vice versa.
    (CASBIN_ROLE_TEACHER, "submission:*", "enter_on_behalf"),
    (CASBIN_ROLE_TEACHER, "workspace:*", "read"),
    (CASBIN_ROLE_TEACHER, "pack:*", "read"),
    (CASBIN_ROLE_TEACHER, "pack:*", "create"),
    (CASBIN_ROLE_TEACHER, "pack:*", "regenerate"),
    (CASBIN_ROLE_TEACHER, "pack:*", "approve"),
    # Content beyond the revision pack (a lesson-note draft): drafted for
    # the teacher's own lesson and approved by them.
    (CASBIN_ROLE_TEACHER, "content:*", "read"),
    (CASBIN_ROLE_TEACHER, "content:*", "create"),
    (CASBIN_ROLE_TEACHER, "content:*", "approve"),
    (CASBIN_ROLE_TEACHER, "content:*", "reject"),
    # Revise an artefact (lesson plan / class review note / diagnostic) through the
    # HITL revision chat. Researcher rides the wildcard above; students and raters
    # never reach the revision surfaces.
    (CASBIN_ROLE_TEACHER, "artefact_revision:*", "revise"),
    # Admin: platform management — schools, workspaces, learners, user
    # onboarding. Deliberately NO research write verbs (author plan / launch /
    # rate …) so a pure-admin identity is audit-separated from a researcher.
    # Read-only on experiment metadata is permitted so the user-management UI
    # can offer "students in experiment X" as a filter — no data is mutated.
    (CASBIN_ROLE_ADMIN, "school:*", "*"),
    (CASBIN_ROLE_ADMIN, "workspace:*", "*"),
    (CASBIN_ROLE_ADMIN, "learner:*", "*"),
    (CASBIN_ROLE_ADMIN, "auth/user:*", "*"),
    (CASBIN_ROLE_ADMIN, "experiment:*", "read"),
    # Ops panel: worker/queue health, in-flight tasks, and execution recovery
    # (re-dispatch a stranded queued run, cancel a runaway one). ``read`` drives
    # the dashboard; ``manage`` gates the terminate / re-dispatch / cancel actions.
    # Which generator new content of a type is made with. A researcher holds it through the
    # wildcard; installing or changing a plugin stays the researcher's (content_type:*, revise).
    (CASBIN_ROLE_ADMIN, "content_type:*", "set_default"),
    (CASBIN_ROLE_ADMIN, "ops:*", "read"),
    (CASBIN_ROLE_ADMIN, "ops:*", "manage"),
    # Admin runs the "Assign raters" picker on each experiment — explicit
    # create + read so the verbs aren't reliant on a wildcard pattern match.
    (CASBIN_ROLE_ADMIN, "assignment:*", "read"),
    (CASBIN_ROLE_ADMIN, "assignment:*", "create"),
    # Onboarding a rater may also start their first session, so admin keeps the
    # rater self-identification verb (it used to ride on ``auth/user:*, create``).
    (CASBIN_ROLE_ADMIN, "rater_session:*", "create"),
    # ``*`` above covers create + update; ``read`` is named explicitly so the
    # list endpoint's gate (auth/user:*, read) is satisfied unambiguously by
    # both wildcards and this rule. (Casbin's matcher tolerates the explicit
    # entry — it just means "if any p row allows".)
    (CASBIN_ROLE_ADMIN, "auth/user:*", "read"),
    # Rater: read their queue + the packets, submit + revise their own ratings.
    # No per-packet assignment table yet, so any rater can rate any packet; that
    # narrows naturally if/when an assignment model arrives.
    # Self-identify into their own rater session (POST /evaluation/raters/session).
    # Its OWN verb, deliberately NOT ``auth/user:*, create`` — that broad verb
    # also guards user / school / learner onboarding, so reusing it would let a
    # rater hit those admin endpoints (privilege escalation).
    (CASBIN_ROLE_RATER, "rater_session:*", "create"),
    (CASBIN_ROLE_RATER, "pack:*", "read"),
    # Read the packets / audit items they rate (handlers scope to the actor's
    # assignments). Its own verb so teacher/student pack:* read can't reach
    # the rating surfaces.
    (CASBIN_ROLE_RATER, "rating:*", "read"),
    (CASBIN_ROLE_RATER, "rating:*", "create"),
    (CASBIN_ROLE_RATER, "rating:*", "update"),
    # Read their own assignment queue. The /my-queue handler filters to the
    # actor's rater profile, so the verb is global but the data is per-actor.
    (CASBIN_ROLE_RATER, "assignment:*", "read"),
    # Student: submit exit assessments (their own) + read their own packs. No
    # per-student scope check today — body/path no longer carries student_id,
    # so the actor's user_id IS the identity; check_scope is trivially True.
    (CASBIN_ROLE_STUDENT, "submission:*", "create"),
    (CASBIN_ROLE_STUDENT, "submission:*", "read"),
    (CASBIN_ROLE_STUDENT, "pack:*", "read"),
    # The lesson list scoped to the student's own class; never the all-schools list.
    (CASBIN_ROLE_STUDENT, "lesson_plan:*", "read_own_class"),
]

# Map user.role storage values to Casbin role names.
_USER_ROLE_TO_CASBIN: dict[str, str] = {
    "research_manager": CASBIN_ROLE_RESEARCHER,
    "teacher": CASBIN_ROLE_TEACHER,
    "admin": CASBIN_ROLE_ADMIN,
    "rater": CASBIN_ROLE_RATER,
    "student": CASBIN_ROLE_STUDENT,
}


@dataclass(frozen=True)
class _SeedReport:
    capabilities_added: int
    grants_added: int
    capabilities_total: int
    grants_total: int


def _row_exists(
    conn: sa.Connection, *, ptype: str, v0: str, v1: str, v2: str, v3: str = ""
) -> bool:
    """``True`` if a casbin_rule row with this exact (ptype, v0..v3) tuple exists.

    ``COALESCE`` wraps v2/v3 because inserts that don't populate them leave NULL,
    and NULL never compares equal to '' — the dedupe would silently fail.
    """
    return (
        conn.execute(
            sa.text(
                "SELECT 1 FROM casbin_rule "
                "WHERE ptype = :ptype AND v0 = :v0 AND v1 = :v1 "
                "AND COALESCE(v2, '') = :v2 AND COALESCE(v3, '') = :v3 LIMIT 1"
            ),
            {"ptype": ptype, "v0": v0, "v1": v1, "v2": v2, "v3": v3},
        ).first()
        is not None
    )


def _insert_policy(
    conn: sa.Connection, *, sub: str, obj: str, act: str, eft: str = "allow"
) -> bool:
    if _row_exists(conn, ptype="p", v0=sub, v1=obj, v2=act, v3=eft):
        return False
    conn.execute(
        sa.text("INSERT INTO casbin_rule (ptype, v0, v1, v2, v3) VALUES ('p', :v0, :v1, :v2, :v3)"),
        {"v0": sub, "v1": obj, "v2": act, "v3": eft},
    )
    return True


def _insert_grant(conn: sa.Connection, *, user_id: str, casbin_role: str) -> bool:
    if _row_exists(conn, ptype="g", v0=user_id, v1=casbin_role, v2=""):
        return False
    conn.execute(
        sa.text("INSERT INTO casbin_rule (ptype, v0, v1) VALUES ('g', :v0, :v1)"),
        {"v0": user_id, "v1": casbin_role},
    )
    return True


def seed_casbin_policies(conn: sa.Connection) -> _SeedReport:
    """Seed capability policies + derive role grants from the current users table."""
    capabilities_added = 0
    for sub, obj, act in _CAPABILITY_POLICIES:
        if _insert_policy(conn, sub=sub, obj=obj, act=act):
            capabilities_added += 1

    grants_added = 0
    # Read ``id`` raw and normalise it in Python. A raw read returns MySQL's bare
    # ``CHAR(32)`` hex; round-tripping through ``uuid.UUID`` then ``str(...)``
    # yields the canonical dashed form enforcement keys on (``enforce`` uses
    # ``str(actor.teacher_id)``), so the grant matches.
    user_rows = conn.execute(sa.text("SELECT id, role FROM users")).all()
    for raw_id, user_role in user_rows:
        casbin_role = _USER_ROLE_TO_CASBIN.get(user_role)
        if casbin_role is None:
            continue
        user_id = str(uuid.UUID(str(raw_id)))
        if _insert_grant(conn, user_id=user_id, casbin_role=casbin_role):
            grants_added += 1

    capabilities_total = int(
        conn.execute(sa.text("SELECT count(*) FROM casbin_rule WHERE ptype='p'")).scalar_one()
    )
    grants_total = int(
        conn.execute(sa.text("SELECT count(*) FROM casbin_rule WHERE ptype='g'")).scalar_one()
    )
    return _SeedReport(
        capabilities_added=capabilities_added,
        grants_added=grants_added,
        capabilities_total=capabilities_total,
        grants_total=grants_total,
    )
