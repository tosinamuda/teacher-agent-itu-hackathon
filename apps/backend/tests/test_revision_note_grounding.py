"""A revision note is grounded in the approved lesson note, the textbook, or both, and says so."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.student_pack_service import (
    StudentPackGenerationService,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_notes import (
    SqlAlchemyApprovedLessonNotes,
)
from app.shared.session_plan_view import SessionPlanView

PLAN = "LPV-GRD"
_AT = datetime(2026, 9, 1, tzinfo=timezone.utc)
SESSION_PLAN: dict[str, Any] = {
    "subject": "Mathematics",
    "grade": "JSS1",
    "topic": "Area",
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lo1", "objective_text": "Find the area of a rectangle."},
        {"lesson_objective_id": "lo2", "objective_text": "Find the area of a garden."},
    ],
    "references": ["Textbook p.42: area = length x width"],
    "steps": [
        {"step_id": "s1", "step_kind": "core", "lesson_objective_id": "lo1", "title": "One"},
        {"step_id": "s2", "step_kind": "core", "lesson_objective_id": "lo2", "title": "Two"},
    ],
}


def _note(
    artefact_id: str, body: str, *, status: ArtefactReviewStatus, minutes: int, origin: str
) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type="lesson_note",
        scope="class_level",
        plan_version_id=PLAN,
        manifest={"plan_version_id": PLAN, "sections": [{"step_id": "s1", "body": body}]},
        artefact_refs={"origin": origin},
        review_status=status,
        reviewed_at=_AT + timedelta(minutes=minutes),
        created_at=_AT + timedelta(minutes=minutes),
    )


async def _seed(db: AsyncSession, *rows: Artefact) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            LessonPlan(
                plan_id="LP-GRD",
                lesson_period_id=uuid.uuid4(),
                title="Area",
                subject="Mathematics",
                track="General",
                grade="JSS1",
                created_by="Teacher One",
            ),
            PlanVersion(
                version_id=PLAN,
                plan_id="LP-GRD",
                source_type="manual",
                session_plan=SESSION_PLAN,
                status=PlanVersionStatus.APPROVED,
            ),
            _note(
                "AT-approved",
                "Her note on rectangles.",
                status=ArtefactReviewStatus.APPROVED,
                minutes=0,
                origin="teacher",
            ),
            _note(
                "AT-draft",
                "An unchecked draft.",
                status=ArtefactReviewStatus.PENDING,
                minutes=5,
                origin="generated",
            ),
            *rows,
        ]
    )
    await db.flush()


class _Generator:
    """Records what generation was given, and writes an empty pack from it."""

    def __init__(self) -> None:
        self.plans: list[SessionPlanView] = []
        self.experts: list[ExpertSources] = []

    async def generate(self, *, session_plan, policy, sources, specification=None):  # type: ignore[no-untyped-def]
        self.plans.append(session_plan)
        self.experts.append(sources.expert)
        request = BaseReviewPackRequestBuilder().build(
            session_plan=session_plan, policy=policy, sources=sources
        )
        return SimpleNamespace(sections=[], request=request, validation=None)


def _service(generator: _Generator) -> StudentPackGenerationService:
    return StudentPackGenerationService(
        base_generator=generator,
        learner_personaliser=object(),  # type: ignore[arg-type]
        lesson_notes=SqlAlchemyApprovedLessonNotes(),
    )


def _notes(plan: SessionPlanView) -> dict[str, str | None]:
    return {step.step_id: step.note for step in plan.steps}


@pytest.mark.asyncio
async def test_the_class_note_reads_the_approved_lesson_note_and_records_it(
    db: AsyncSession,
) -> None:
    await _seed(db)
    generator = _Generator()

    pack = await _service(generator).ensure_base_artefact(db=db, plan_version_id=PLAN)

    assert _notes(generator.plans[0]) == {"s1": "Her note on rectangles.", "s2": None}
    assert generator.experts == [ExpertSources.LESSON_NOTE]
    assert pack.artefact_refs is not None
    assert pack.artefact_refs["expert_sources"] == "lesson-note"
    assert pack.artefact_refs["lesson_note"] == {
        "id": "AT-approved",
        "version": 1,
        "origin": "teacher",
    }


@pytest.mark.asyncio
async def test_a_textbook_note_reads_no_lesson_note(db: AsyncSession) -> None:
    await _seed(db)
    generator = _Generator()

    pack = await _service(generator).ensure_base_artefact(
        db=db, plan_version_id=PLAN, expert=ExpertSources.TEXTBOOK
    )

    assert _notes(generator.plans[0]) == {"s1": None, "s2": None}
    assert generator.experts == [ExpertSources.TEXTBOOK]
    assert pack.artefact_refs is not None
    assert (pack.artefact_refs["expert_sources"], pack.artefact_refs["lesson_note"]) == (
        "textbook",
        None,
    )


@pytest.mark.asyncio
async def test_a_learners_note_is_grounded_as_the_class_note_it_adapts(db: AsyncSession) -> None:
    newer = _note(
        "AT-newer",
        "A later approved note.",
        status=ArtefactReviewStatus.APPROVED,
        minutes=10,
        origin="teacher",
    )
    class_pack = Artefact(
        artefact_id="AT-class",
        artefact_type="post_class_review_pack",
        scope="class_level",
        plan_version_id=PLAN,
        manifest={"steps": []},
        artefact_refs={
            "expert_sources": "both",
            "lesson_note": {"id": "AT-approved", "version": 1, "origin": "teacher"},
        },
        review_status=ArtefactReviewStatus.APPROVED,
    )
    await _seed(db, newer, class_pack)

    grounding = await _service(_Generator())._learner_grounding(db, class_pack)

    assert grounding.expert is ExpertSources.BOTH
    assert grounding.lesson_note is not None
    assert grounding.lesson_note.note_id == "AT-approved"


@pytest.mark.asyncio
async def test_without_a_recorded_grounding_a_learners_note_follows_the_study_rule(
    db: AsyncSession,
) -> None:
    class_pack = Artefact(
        artefact_id="AT-class",
        artefact_type="post_class_review_pack",
        scope="class_level",
        plan_version_id=PLAN,
        manifest={"steps": []},
        review_status=ArtefactReviewStatus.APPROVED,
    )
    await _seed(db, class_pack)

    grounding = await _service(_Generator())._learner_grounding(db, class_pack)

    assert grounding.expert is ExpertSources.LESSON_NOTE
    assert grounding.lesson_note is not None
    assert grounding.lesson_note.note_id == "AT-approved"
