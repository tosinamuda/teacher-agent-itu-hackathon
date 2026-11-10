import uuid

import pytest
from sqlalchemy import text

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.teaching.application import TeachingWorkspaceApplicationService
from app.domains.teaching.infrastructure.learner_lessons_repository import (
    LearnerLessonsRepository,
)
from app.domains.teaching.infrastructure.review_queue_repository import (
    LearnerNotes,
    ReviewQueueRepository,
)
from app.domains.teaching.models import LessonPeriod, SchemeOfWork, TeacherWorkspace


def _artefact(
    version: str, scope: ArtefactScope, status: ArtefactReviewStatus, student: str | None = None
) -> Artefact:
    return Artefact(
        student_id=student,
        artefact_id=f"A-{uuid.uuid4().hex[:12]}",
        artefact_type="lesson-note",
        scope=scope.value,
        plan_version_id=version,
        manifest={},
        review_status=status,
    )


async def _seed(db) -> tuple[uuid.UUID, uuid.UUID, uuid.UUID]:  # type: ignore[no-untyped-def]
    """A workspace with a busy lesson and a quiet one; their ids."""
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    offering, workspace = uuid.uuid4(), uuid.uuid4()
    week, busy, quiet = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    db.add_all(
        [
            TermClassSubject(
                id=offering, course_id=uuid.uuid4(), class_id=uuid.uuid4(), term="1st", year="y"
            ),
            TeacherWorkspace(id=workspace, term_class_subject_id=offering, teacher_id=uuid.uuid4()),
            SchemeOfWork(id=week, term_class_subject_id=offering, week_number=1, title="W"),
            LessonPeriod(id=busy, scheme_of_work_id=week, period_number=1),
            LessonPeriod(id=quiet, scheme_of_work_id=week, period_number=2),
            LessonPlan(
                plan_id="P-BUSY",
                lesson_period_id=busy,
                title="Busy",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
            LessonPlan(
                plan_id="P-BUSY-2",
                lesson_period_id=busy,
                title="Busy again",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
            LessonPlan(
                plan_id="P-QUIET",
                lesson_period_id=quiet,
                title="Quiet",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
            PlanVersion(
                version_id="V-BUSY",
                plan_id="P-BUSY",
                source_type="generated",
                session_plan={},
                status=PlanVersionStatus.DRAFT,
            ),
            PlanVersion(
                version_id="V-QUIET",
                plan_id="P-QUIET",
                source_type="generated",
                session_plan={},
                status=PlanVersionStatus.APPROVED,
            ),
        ]
    )
    await db.flush()
    db.add_all(
        [
            _artefact("V-BUSY", ArtefactScope.CLASS_LEVEL, ArtefactReviewStatus.PENDING),
            _artefact("V-BUSY", ArtefactScope.LEARNER_LEVEL, ArtefactReviewStatus.PENDING, "S-1"),
            _artefact("V-BUSY", ArtefactScope.LEARNER_LEVEL, ArtefactReviewStatus.PENDING, "S-1"),
            _artefact("V-BUSY", ArtefactScope.LEARNER_LEVEL, ArtefactReviewStatus.APPROVED, "S-2"),
            _artefact("V-QUIET", ArtefactScope.LEARNER_LEVEL, ArtefactReviewStatus.APPROVED, "S-1"),
            _artefact("V-QUIET", ArtefactScope.LEARNER_LEVEL, ArtefactReviewStatus.REJECTED, "S-3"),
            _artefact("V-QUIET", ArtefactScope.CLASS_LEVEL, ArtefactReviewStatus.APPROVED),
        ]
    )
    await db.flush()
    return workspace, busy, quiet


@pytest.mark.asyncio
async def test_each_lesson_counts_what_waits_for_the_teacher(db) -> None:  # type: ignore[no-untyped-def]
    workspace, busy, _ = await _seed(db)

    response = await TeachingWorkspaceApplicationService().lesson_reviews(
        db=db, workspace_id=workspace
    )

    assert [
        (r.lesson_period_id, r.plans_to_approve, r.materials_to_review, r.notes_to_review)
        for r in response.lessons
    ] == [(busy, 1, 1, 2)]
    assert response.lessons[0].oldest_kind in {"plan", "lesson-note"}


@pytest.mark.asyncio
async def test_each_learner_counts_their_notes_to_review_and_approved(db) -> None:  # type: ignore[no-untyped-def]
    workspace, _, _ = await _seed(db)

    notes = await ReviewQueueRepository().notes_by_learner(db, workspace)

    assert notes == {"S-1": LearnerNotes(2, 1), "S-2": LearnerNotes(0, 1)}


@pytest.mark.asyncio
async def test_a_learners_lessons_say_where_their_revision_note_stands(db) -> None:  # type: ignore[no-untyped-def]
    workspace, busy, quiet = await _seed(db)

    lessons = await LearnerLessonsRepository().lessons_of(db, workspace, "S-2")

    by_lesson = {lesson.lesson_period_id: lesson for lesson in lessons}
    assert [lesson.title for lesson in lessons] == ["Busy", "Quiet"]
    assert by_lesson[busy].note is not None
    assert by_lesson[busy].note.status == ArtefactReviewStatus.APPROVED
    assert by_lesson[quiet].note is None
