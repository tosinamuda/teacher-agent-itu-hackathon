"""The lesson a class-test reader checks items against: the approved note, else the plan."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.assessments.application.diagnostic_service import DiagnosticGenerationService
from app.domains.assessments.infrastructure.lesson_notes import ApprovedLessonNoteText
from app.shared.session_plan_view import SessionPlanView

PLAN = "LPV-CONTEXT-1"
_PLAN_VIEW = SessionPlanView.model_validate(
    {"steps": [{"step_id": "s1", "step_kind": "core", "content": "Improper: top ≥ bottom."}]}
)


def _note(artefact_id: str, body: str, status: ArtefactReviewStatus) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type=ArtefactType.LESSON_NOTE.value,
        scope=ArtefactScope.CLASS_LEVEL.value,
        plan_version_id=PLAN,
        manifest={"plan_version_id": PLAN, "sections": [{"step_id": "s1", "body": body}]},
        review_status=status,
        reviewed_at=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_only_an_approved_note_is_the_lesson(db) -> None:  # type: ignore[no-untyped-def]
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(_note("ART-PENDING", "A draft nobody approved.", ArtefactReviewStatus.PENDING))
    await db.flush()
    notes = ApprovedLessonNoteText()

    assert await notes.text(db, PLAN) is None

    db.add(
        _note(
            "ART-APPROVED", "Improper means numerator ≥ denominator.", ArtefactReviewStatus.APPROVED
        )
    )
    await db.flush()

    assert await notes.text(db, PLAN) == "Improper means numerator ≥ denominator."


@pytest.mark.asyncio
async def test_without_an_approved_note_the_reader_is_given_the_plan(db) -> None:  # type: ignore[no-untyped-def]
    service = DiagnosticGenerationService(lesson_notes=ApprovedLessonNoteText())

    taught = await service._taught(db, PLAN, _PLAN_VIEW)

    assert "Improper: top ≥ bottom." in taught
