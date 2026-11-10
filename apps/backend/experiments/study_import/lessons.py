"""Each studied lesson's plan and note, and the class's learners, as the app keeps them.

The plan is the one the study's generator read, and the teacher's; the note is Part 1's
corrected note. Both come from the study's record, so both are approved as they stand: what
the study used is what the teacher gave it.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.lesson_note.domain.note import LessonNote, NoteSection
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.learners.models import LearnerProfile
from app.shared.time import utc_now
from experiments.study_import.dataset import StudyLesson
from experiments.study_import.school import GRADE, TEACHER_NAME, LessonPlace

TRACK = "General"


@dataclass(frozen=True)
class ImportedLesson:
    lesson: StudyLesson
    place: LessonPlace
    plan_version_id: str


def plan_version_id(lesson: str) -> str:
    return f"LPV-STUDY-{lesson}"


def learner_id(pseudonym: str) -> str:
    """``student-03`` in the study's record is ``ST-STUDY-03`` in the app."""
    return f"ST-STUDY-{pseudonym.removeprefix('student-')}"


def plan_rows(lesson: StudyLesson, place: LessonPlace) -> tuple[LessonPlan, PlanVersion]:
    """The lesson's plan and its one version: the plan as the study's generator read it."""
    plan = lesson.plan
    plan_id = f"LP-STUDY-{lesson.lesson}"
    return (
        LessonPlan(
            plan_id=plan_id,
            lesson_period_id=place.lesson_period_id,
            title=str(plan.get("title") or plan.get("subtopic") or plan.get("topic")),
            subject=str(plan["subject"]),
            track=str(plan.get("track") or TRACK),
            grade=str(plan["grade"]),
            created_by=TEACHER_NAME,
        ),
        PlanVersion(
            version_id=plan_version_id(lesson.lesson),
            plan_id=plan_id,
            source_type="study_record",
            session_plan=plan,
            run_metadata={"source": "study_record", "lesson": lesson.lesson},
            status=PlanVersionStatus.APPROVED,
            approved_at=utc_now(),
            approved_by=TEACHER_NAME,
        ),
    )


def lesson_note_row(lesson: StudyLesson) -> Artefact:
    """The lesson's note, Part 1's corrected note for each step that has one."""
    version_id = plan_version_id(lesson.lesson)
    note = LessonNote(
        plan_version_id=version_id,
        sections=[NoteSection(step_id=step, body=body) for step, body in lesson.note_sections],
    )
    return Artefact(
        artefact_id=f"AT-STUDY-{lesson.lesson}-note",
        artefact_type=ArtefactType.LESSON_NOTE.value,
        scope=ArtefactScope.CLASS_LEVEL.value,
        plan_version_id=version_id,
        manifest=note.model_dump(mode="json"),
        artefact_refs={"origin": "study_record"},
        review_status=ArtefactReviewStatus.APPROVED,
        reviewed_by=TEACHER_NAME,
        reviewed_at=utc_now(),
    )


def learner_rows(pseudonyms: set[str], class_id: object) -> list[LearnerProfile]:
    """The class's learners, known only by the study's pseudonyms."""
    return [
        LearnerProfile(
            student_id=learner_id(pseudonym),
            full_name=pseudonym,
            grade=GRADE,
            track=TRACK,
            class_id=class_id,
        )
        for pseudonym in sorted(pseudonyms)
    ]
