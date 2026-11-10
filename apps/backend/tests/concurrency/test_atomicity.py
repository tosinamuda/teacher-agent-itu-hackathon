"""Atomicity + consistency properties behind the PR-#79 reliability work.

* User and rater onboarding rows share one commit or rollback.
* The rollback-expiry hazard the synthetic-student batch fix guards against:
  a ``rollback`` expires every ORM object, so a value must be snapshotted to a
  plain Python value *before* the rollback or the next access detonates.
* ``run_with_deadlock_retry`` runs a real self-committing operation end to end
  (the transient-retry logic itself is unit-tested in ``test_db_retry``).
* The unique constraints PR #79 relies on are actually present in the schema —
  a drift guard so a dropped model constraint can't silently disable the races'
  last line of defence.
"""

from __future__ import annotations

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import MissingGreenlet

from app.db.retry import run_with_deadlock_retry
from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.school.models.structure import School
from app.domains.users.infrastructure.sqlalchemy_onboarding_store import (
    SqlAlchemyUserOnboardingStore,
)
from app.domains.users.models import User

pytestmark = pytest.mark.asyncio

# The unique constraints PR #79 added / depends on. If a model loses one of
# these, ``create_all`` stops emitting it and this set stops matching — before
# the missing guard silently lets a race through in production.
_PR79_UNIQUE_CONSTRAINTS = frozenset(
    {
        "uq_classes_school_name",
        "uq_courses_subject_grade",
        "uq_tcs_class_course_term_year",
        "uq_workspace_teacher_tcs",
        "uq_execution_attempt",
        "uq_revision_thread_type_subject_slot",
        "uq_revision_turn_thread_number",
        "uq_evaluation_ratings_packet_rater",
        "uq_evaluation_audit_ratings_item_rater",
        "uq_exit_ticket_submission_student_plan",
    }
)


async def test_onboard_rollback_discards_user_and_rater(session_factory, count_rows) -> None:
    async with session_factory() as session:
        store = SqlAlchemyUserOnboardingStore(session)
        user = await store.stage_user(
            auth_id="code|ORPHAN",
            email="orphan@x.test",
            full_name="Orphan Rater",
            role="rater",
        )
        await store.stage_rater_profile(user_id=user.id, display_name="Orphan Rater")
        await store.rollback()

    assert await count_rows(User, id=user.id) == 0
    assert await count_rows(EvaluationRater, user_id=user.id) == 0


async def test_onboard_commit_persists_user_and_rater_together(session_factory, count_rows) -> None:
    async with session_factory() as session:
        store = SqlAlchemyUserOnboardingStore(session)
        user = await store.stage_user(
            auth_id="code|ATOMIC-RATER",
            email="atomic-rater@x.test",
            full_name="Atomic Rater",
            role="rater",
        )
        await store.stage_rater_profile(user_id=user.id, display_name="Atomic Rater")
        await store.commit()

    assert await count_rows(User, id=user.id) == 1
    assert await count_rows(EvaluationRater, user_id=user.id) == 1


async def test_rollback_expires_orm_but_snapshot_survives(session_factory) -> None:
    async with session_factory() as seed:
        seed.add(School(name="Snap High", code="SNAP"))
        await seed.commit()

    async with session_factory() as session:
        # Load the row via a query (this is what synthetic_student does up front);
        # the SELECT opens a transaction and puts the object in the identity map.
        school = (await session.execute(select(School).where(School.code == "SNAP"))).scalar_one()

        # The fix's pattern: capture plain values BEFORE the rollback.
        snapshot_code = school.code

        # A per-item failure rolls back — which expires EVERY ORM object loaded in
        # the session (rollback expiry isn't governed by expire_on_commit).
        await session.rollback()

        # The snapshot is a plain str — still usable, no DB access.
        assert snapshot_code == "SNAP"

        # Touching an expired ORM attribute triggers a lazy refresh = async I/O
        # under a sync attribute access = MissingGreenlet. This is exactly what
        # detonated the synthetic-student batch before it snapshotted up front.
        with pytest.raises(MissingGreenlet):
            _ = school.name


async def test_deadlock_retry_runs_a_real_operation(session_factory, count_rows) -> None:
    async with session_factory() as session:

        async def operation() -> str:
            session.add(School(name="Retry High", code="RETRY"))
            await session.commit()
            return "ok"

        result = await run_with_deadlock_retry(session, operation)
        assert result == "ok"

    assert await count_rows(School, code="RETRY") == 1


async def test_pr79_unique_constraints_present_in_schema(session_factory) -> None:
    async with session_factory() as session:
        rows = (
            (
                await session.execute(
                    text(
                        "SELECT DISTINCT constraint_name "
                        "FROM information_schema.table_constraints "
                        "WHERE table_schema = DATABASE() AND constraint_type = 'UNIQUE'"
                    )
                )
            )
            .scalars()
            .all()
        )

    missing = _PR79_UNIQUE_CONSTRAINTS - set(rows)
    assert not missing, f"unique constraints missing from the schema: {sorted(missing)}"
