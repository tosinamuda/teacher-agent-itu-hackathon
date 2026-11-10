"""One exit-ticket submission per (student, lesson) — DB unique + existence guard.

A student could re-submit the same lesson's assessment, appending a 2nd submission +
a 2nd set of item-responses that double-counted per-objective mastery and learner
evidence. Product decision (2026-06-17): block re-submission — first wins, 2nd → 409.
These pin the DB unique + the existence check the service's early-409 + race-converge
rely on. Runs against the MySQL test DB (create_all carries the model constraint).
"""

from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.domains.assessments.infrastructure.repository import AssessmentRepository
from app.domains.assessments.models.exit_ticket import ExitTicketSubmission

pytestmark = pytest.mark.asyncio


def _submission(diagnostic_id: str, student_id: str, plan_version_id: str) -> ExitTicketSubmission:
    return ExitTicketSubmission(
        diagnostic_id=diagnostic_id,
        student_id=student_id,
        plan_version_id=plan_version_id,
        results={},
    )


async def test_second_submission_for_same_student_lesson_violates_unique(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_submission("DIAG-1", "ST-1", "LPV-1"))
    await db.flush()
    # A second submission for the same (student, plan) — a re-submit — is rejected by
    # uq_exit_ticket_submission_student_plan even with a fresh diagnostic_id.
    db.add(_submission("DIAG-2", "ST-1", "LPV-1"))
    with pytest.raises(IntegrityError):
        await db.flush()


async def test_submission_exists_for_student_plan(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    repo = AssessmentRepository()
    assert not await repo.submission_exists_for_student_plan(
        db, student_id="ST-9", plan_version_id="LPV-9"
    )
    db.add(_submission("DIAG-9", "ST-9", "LPV-9"))
    await db.flush()
    assert await repo.submission_exists_for_student_plan(
        db, student_id="ST-9", plan_version_id="LPV-9"
    )
    # A different lesson for the same student is still allowed (independent submissions).
    assert not await repo.submission_exists_for_student_plan(
        db, student_id="ST-9", plan_version_id="LPV-OTHER"
    )
