"""Concurrency fixes from the round-7 adversarial audit (new-ground domains).

* Artefact approve vs in-place revise: both mutate review_status/manifest on the same row;
  without a lock the read-modify-writes race (lost manifest / approval silently undone / C4
  H2-gate flip). Both paths now take ``get_artefact_for_update`` (FOR UPDATE) — proven to
  serialize here.
* Diagnostic regenerate vs student submit: the DELETE of exit_ticket_items FK-violates (1451)
  when a student's responses reference them (a race past the ``_has_student_responses`` gate);
  now translated to the intended 409, not a raw 500.
* Rater ``_create_or_get``: assigning the SAME rater to the SAME scope concurrently raced the
  uq_rater_assignments_unique between find + insert → 500; now converges (idempotent).

Independent committing sessions per "process"; the LLM is never invoked.
"""

from __future__ import annotations

import asyncio
import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.assessments.application.service import (
    AssessmentApplicationError,
    AssessmentApplicationService,
)
from app.domains.evaluation.application.assignment_commands import assign_h1
from app.domains.evaluation.infrastructure.models import EvaluationRater, RaterAssignment
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
    SqlAlchemyEvaluationStore,
)
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.experiments.infrastructure.repository import ExperimentRepository

pytestmark = pytest.mark.asyncio

_LESSON_ID = uuid.UUID(int=0xB0B)


# --- P0: artefact approve vs in-place revise serialize on the row lock ---


async def test_get_artefact_for_update_serializes_approve_vs_revise(session_factory) -> None:
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        await seed.execute(
            text(
                "INSERT INTO artefacts "
                "(id, artefact_id, artefact_kind, scope, plan_version_id, manifest, review_status, "
                "created_at) VALUES (:id, 'ART-LOCK', 'post_class_review_pack', 'learner_level', "
                "'LPV-LOCK', '{}', 'pending', NOW())"
            ),
            {"id": uuid.uuid4().hex},
        )
        await seed.commit()

    repo = ArtefactRepository()
    async with session_factory() as approver:
        locked = await repo.get_artefact_for_update(approver, "ART-LOCK")
        assert locked is not None and locked.review_status == ArtefactReviewStatus.PENDING

        async def revise_rival() -> None:
            async with session_factory() as reviser:
                art = await repo.get_artefact_for_update(reviser, "ART-LOCK")  # blocks on the lock
                assert art is not None
                art.manifest = {"revised": True}
                art.review_status = ArtefactReviewStatus.PENDING
                await reviser.commit()

        task = asyncio.create_task(revise_rival())
        await asyncio.sleep(0.5)
        assert not task.done()  # the reviser is blocked on the approver's FOR UPDATE lock

        locked.review_status = ArtefactReviewStatus.APPROVED
        await approver.commit()  # release the lock
        await asyncio.wait_for(task, timeout=10)

    # Serialized: the reviser ran AFTER the approver committed, so its full write (not a torn
    # interleave) is the final state — the lock made the outcome deterministic, not a clobber.
    async with session_factory() as check:
        art = await ArtefactRepository().get_artefact(check, "ART-LOCK")
        assert art is not None
        assert art.review_status == ArtefactReviewStatus.PENDING
        assert art.manifest == {"revised": True}


# --- P1: diagnostic regenerate translates the FK violation to 409 (not 500) ---


async def test_diagnostic_regen_translates_fk_violation_to_409(session_factory) -> None:
    class _FakeDiagnosticService:
        async def generate_for_plan(self, *, db, plan_version_id, item_count) -> int:
            # The race: a student submitted responses between generate_diagnostic's
            # _has_student_responses gate and this DELETE, so the DELETE of exit_ticket_items
            # FK-violates (errno 1451). The real service raises IntegrityError here.
            raise IntegrityError("DELETE FROM exit_ticket_items ...", {}, Exception("1451 FK"))

    service = AssessmentApplicationService(diagnostic_service=_FakeDiagnosticService())
    async with session_factory() as s:
        with pytest.raises(AssessmentApplicationError) as info:
            # A plan with no committed responses → the early gate passes → reaches the fake.
            await service.generate_diagnostic(db=s, plan_version_id="LPV-RACE-NO-RESPONSES")
    assert info.value.status_code == 409
    assert info.value.detail == "assessment_has_responses"


# --- P2: same-rater-same-scope concurrent assign converges (no 500) ---


async def test_concurrent_same_rater_assign_converges(
    run_race, count_rows, session_factory
) -> None:
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            Experiment(
                experiment_id="EXP-IDEM",
                experiment_code="IDEM-001",
                investigation_db_id=uuid.uuid4(),
                teacher_workspace_id=uuid.uuid4(),
                lesson_period_id=_LESSON_ID,
            )
        )
        seed.add(EvaluationRater(rater_id="EVR-IDEM", display_name="Idem Rater"))
        await seed.commit()

    async def op(session, _i):
        # The experiments repo is session-bound, so each racer builds its own.
        experiments = ExperimentRepository(session)
        store = SqlAlchemyEvaluationStore(session, assignment_scopes=experiments)
        # SAME rater + scope every time → must converge to one assignment, not 500 on the
        # uq_rater_assignments_unique race between find_assignment and the insert.
        return await assign_h1(
            store,
            experiment_id="EXP-IDEM",
            rater_id="EVR-IDEM",
            lesson_period_id=_LESSON_ID,
            assigned_by="researcher",
        )

    out = await run_race(op, lambda _e: False, n=4)

    assert out.others == [], (
        f"a concurrent same-rater assign surfaced an error (a 500?): {out.others}"
    )
    assert len(out.wins) == 4  # all converge to the same assignment; none raises
    assert await count_rows(RaterAssignment) == 1  # exactly one assignment row
