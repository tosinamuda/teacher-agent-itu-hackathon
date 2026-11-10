"""Deferred concurrency fixes (round-8): contained converge/lock items.

* synthetic get_or_create_rater: a concurrent same-name create raced display_name's unique →
  500 that aborted the synthetic batch; now converges (rollback + re-select).
* update_school: a concurrent rename to the same name slipped past the conflict check (TOCTOU)
  → 500; now converges to the intended 409.
* attach_exit_assessment_survey: the survey merge is a read-modify-write on results JSON;
  get_submission_by_diagnostic_id_for_update serializes concurrent attaches (no lost survey).

(audit_service's build_source_audit_items now locks each execution before its idempotency
count — it reuses ExperimentRepository.lock_execution_by_public_id, exercised by the
packet-export + execution-lifecycle lock tests.)

Independent committing sessions per "process".
"""

from __future__ import annotations

import asyncio
import uuid

import pytest
from sqlalchemy import text

from app.domains.assessments.infrastructure.repository import AssessmentRepository
from app.domains.assessments.models.exit_ticket import ExitTicketSubmission
from app.domains.evaluation.application.synthetic_support import get_or_create_rater
from app.domains.evaluation.infrastructure.models import EvaluationRater
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
    SqlAlchemyEvaluationStore,
)
from app.domains.school.application.service import SchoolApplicationError, SchoolApplicationService
from app.domains.school.models.structure import School
from app.domains.school.schemas import SchoolUpdateRequest

pytestmark = pytest.mark.asyncio


async def test_concurrent_get_or_create_rater_converges(
    run_race, count_rows, session_factory
) -> None:
    async def op(session, _i):
        rater = await get_or_create_rater(SqlAlchemyEvaluationStore(session), "Synthetic Twin")
        await session.commit()
        return rater.rater_id

    out = await run_race(op, lambda _e: False, n=4)

    assert out.others == [], f"get_or_create_rater raced to an error (a 500?): {out.others}"
    assert len(out.wins) == 4  # all converge to the one rater; none raises
    assert await count_rows(EvaluationRater, display_name="Synthetic Twin") == 1


async def test_get_or_create_rater_keeps_earlier_raters_when_a_later_one_converges(
    count_rows, session_factory
) -> None:
    """synthetic_rater builds several raters in a row (a dict comprehension over personas).
    Each rater is its own committed unit, so resolving a LATER persona — even when it has to
    converge to a rival's row — can never discard the rater already created for an EARLIER
    persona. (The old shared-transaction design rolled the whole batch back on any one
    conflict, silently losing earlier personas' raters.)"""
    async with session_factory() as work:
        a = await get_or_create_rater(
            SqlAlchemyEvaluationStore(work), "Persona A"
        )  # committed independently
        a_id = a.rater_id

        # A rival creates "Persona B" — the next resolve for B must converge to it, not 500.
        async with session_factory() as rival:
            await get_or_create_rater(SqlAlchemyEvaluationStore(rival), "Persona B")
            await rival.commit()

        b = await get_or_create_rater(SqlAlchemyEvaluationStore(work), "Persona B")
        assert b.display_name == "Persona B"
        await work.commit()

    # "Persona A" survived resolving "Persona B" (independent commits), and B converged (no dup).
    assert await count_rows(EvaluationRater, display_name="Persona A") == 1, (
        "earlier persona's rater was discarded while resolving a later persona"
    )
    assert await count_rows(EvaluationRater, display_name="Persona B") == 1
    async with session_factory() as check:
        again = await get_or_create_rater(SqlAlchemyEvaluationStore(check), "Persona A")
        assert again.rater_id == a_id  # the same committed row, not a detached/lost object


async def test_concurrent_update_school_to_same_name_converges(
    run_race, count_rows, session_factory
) -> None:
    async with session_factory() as seed:
        a = School(name="Alpha", code="AAA")
        b = School(name="Beta", code="BBB")
        seed.add_all([a, b])
        await seed.commit()
        ids = [a.id, b.id]

    service = SchoolApplicationService()

    async def op(session, i):
        # Both rename to the SAME name (ix_schools_name) — the loser slips past the conflict
        # check (TOCTOU) and must converge to a clean 409, not a raw 500.
        return await service.update_school(
            db=session,
            school_id=ids[i],
            payload=SchoolUpdateRequest(name="Collide", school_code=("AAA" if i == 0 else "BBB")),
        )

    out = await run_race(
        op,
        lambda e: isinstance(e, SchoolApplicationError) and e.status_code == 409,
        n=2,
    )

    assert out.others == [], f"update_school raced to a non-409 error (a 500?): {out.others}"
    assert len(out.wins) == 1  # one rename wins
    assert len(out.conflicts) == 1  # the other gets a clean 409 school_exists
    assert await count_rows(School, name="Collide") == 1


async def test_get_submission_for_update_serializes_survey_attach(session_factory) -> None:
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            ExitTicketSubmission(
                diagnostic_id="DIAG-LOCK",
                student_id=f"ST-{uuid.uuid4().hex[:8]}",
                plan_version_id="LPV-LOCK",
                results={},
            )
        )
        await seed.commit()

    repo = AssessmentRepository()
    async with session_factory() as attach_a:
        locked = await repo.get_submission_by_diagnostic_id_for_update(attach_a, "DIAG-LOCK")
        assert locked is not None

        async def attach_b_rival() -> None:
            async with session_factory() as attach_b:
                sub = await repo.get_submission_by_diagnostic_id_for_update(attach_b, "DIAG-LOCK")
                assert sub is not None  # blocks until A commits, then reads A's committed results
                sub.results = {**(sub.results or {}), "survey": "B"}
                await attach_b.commit()

        task = asyncio.create_task(attach_b_rival())
        await asyncio.sleep(0.5)
        assert not task.done()  # blocked on A's FOR UPDATE lock — no torn read-modify-write

        locked.results = {"survey": "A"}
        await attach_a.commit()  # release
        await asyncio.wait_for(task, timeout=10)

    # Serialized: B acquired the lock only AFTER A committed, so it merged onto A's fresh
    # committed results (last-writer wins the shared key) rather than losing a write off a
    # stale pre-A snapshot — which is exactly the lost-survey RMW the lock prevents.
    async with session_factory() as check:
        sub = await AssessmentRepository().get_submission_by_diagnostic_id(check, "DIAG-LOCK")
        assert sub is not None
        assert sub.results == {"survey": "B"}
