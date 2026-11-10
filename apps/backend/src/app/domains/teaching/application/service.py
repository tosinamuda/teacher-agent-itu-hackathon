from __future__ import annotations

import uuid
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationError
from app.domains.teaching.domain import canonical_term_sort_key
from app.domains.teaching.domain.class_test_outcome import objective_outcomes, outcome_of
from app.domains.teaching.domain.learner_lessons import (
    ClassTestTaken,
    in_display_order,
    note_status,
)
from app.domains.teaching.infrastructure.class_test_repository import ClassTestRepository
from app.domains.teaching.infrastructure.learner_lessons_repository import (
    LearnerLessonsRepository,
)
from app.domains.teaching.infrastructure.repository import TeachingRepository
from app.domains.teaching.infrastructure.review_queue_repository import (
    LearnerNotes,
    ReviewQueueRepository,
)
from app.domains.teaching.schemas import (
    ClassLearnerResponse,
    ClassLearnersResponse,
    LastClassTestResponse,
    LearnerLessonResponse,
    LearnerObjectiveResponse,
    LearnerResultsResponse,
    LearnerTestResponse,
    LessonReviewResponse,
    LessonReviewsResponse,
    TeachingWorkspaceResponse,
)
from app.domains.users.application import UserApplicationService
from app.shared.json_types import JsonObject

_WEAKEST_FIRST = ("remediate", "reinforce", "extend")


class TeachingWorkspaceApplicationService:
    def __init__(
        self,
        users: UserApplicationService | None = None,
        repository: TeachingRepository | None = None,
        class_tests: ClassTestRepository | None = None,
        review_queue: ReviewQueueRepository | None = None,
        learner_lessons: LearnerLessonsRepository | None = None,
    ) -> None:
        self.users = users or UserApplicationService()
        self.repository = repository or TeachingRepository()
        self.class_tests = class_tests or ClassTestRepository()
        self.review_queue = review_queue or ReviewQueueRepository()
        self.learner_lessons = learner_lessons or LearnerLessonsRepository()

    async def list_workspaces(
        self,
        *,
        db: AsyncSession,
        teacher_code: str | None,
    ) -> list[TeachingWorkspaceResponse]:
        # No identity → no workspaces. Do NOT fall back to a privileged default
        # identity (the old `code|uncle-tosin` default leaked the researcher's
        # workspaces to any unauthenticated caller).
        if not teacher_code:
            return []

        teacher = await self.users.get_user_by_auth_id(db=db, auth_id=f"code|{teacher_code}")
        if not teacher:
            return []

        workspaces = await self.repository.list_workspaces_for_teacher(
            db,
            teacher.id,
            canonical_only=True,
        )
        responses = [
            TeachingWorkspaceResponse(
                id=workspace.id,
                course_id=workspace.term_class_subject.course_id,
                term_class_subject_id=workspace.term_class_subject.id,
                class_id=(
                    workspace.term_class_subject.classroom.id
                    if workspace.term_class_subject.classroom
                    else None
                ),
                class_name=(
                    workspace.term_class_subject.classroom.name
                    if workspace.term_class_subject.classroom
                    else None
                ),
                school_id=(
                    workspace.term_class_subject.classroom.school.id
                    if workspace.term_class_subject.classroom
                    and workspace.term_class_subject.classroom.school
                    else None
                ),
                school_name=(
                    workspace.term_class_subject.classroom.school.name
                    if workspace.term_class_subject.classroom
                    and workspace.term_class_subject.classroom.school
                    else None
                ),
                name=(
                    f"{workspace.term_class_subject.course.name} - "
                    f"{workspace.term_class_subject.term}"
                ),
                subject_name=workspace.term_class_subject.course.subject.name,
                subject_code=workspace.term_class_subject.course.subject.code,
                grade_level=workspace.term_class_subject.course.grade_level.name,
                term=workspace.term_class_subject.term,
                is_primary=workspace.is_primary,
                teacher_id=str(workspace.teacher_id),
                settings=_settings_json(workspace.settings),
                created_at=workspace.created_at,
            )
            for workspace in workspaces
            if workspace.term_class_subject and workspace.term_class_subject.course
        ]
        return sorted(
            responses,
            key=lambda workspace: (
                0 if workspace.is_primary else 1,
                canonical_term_sort_key(workspace.term),
                workspace.name,
            ),
        )

    async def class_learners(
        self,
        *,
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lesson_period_id: uuid.UUID | None = None,
    ) -> ClassLearnersResponse:
        """Each learner of the workspace's class with how they did on their latest class test.

        The latest for the subject, or for one lesson when `lesson_period_id` is given.
        """
        rows = await self.class_tests.learners_with_latest_test(db, workspace_id, lesson_period_id)
        if rows is None:
            raise TeachingSequenceApplicationError(404, "workspace_or_lesson_not_found")
        notes = await self.review_queue.notes_by_learner(db, workspace_id)
        learners: list[ClassLearnerResponse] = []
        for row in rows:
            outcome = (
                outcome_of(row.student_id, row.latest_test.results) if row.latest_test else None
            )
            last_test = (
                LastClassTestResponse(
                    lesson_title=row.latest_test.lesson_title,
                    band=outcome.band,
                    correct=outcome.correct,
                    out_of=outcome.out_of,
                    taken_at=row.latest_test.taken_at,
                )
                if row.latest_test and outcome
                else None
            )
            learners.append(
                ClassLearnerResponse(
                    student_id=row.student_id,
                    full_name=row.full_name,
                    last_test=last_test,
                    notes_to_review=notes.get(row.student_id, LearnerNotes()).to_review,
                    notes_approved=notes.get(row.student_id, LearnerNotes()).approved,
                )
            )
        return ClassLearnersResponse(learners=learners)

    async def lesson_reviews(
        self, *, db: AsyncSession, workspace_id: uuid.UUID
    ) -> LessonReviewsResponse:
        """What waits for the teacher in each lesson of the workspace's subject."""
        counts = await self.review_queue.counts_by_lesson(db, workspace_id)
        return LessonReviewsResponse(
            lessons=[
                LessonReviewResponse(
                    lesson_period_id=lesson,
                    plans_to_approve=found.plans_to_approve,
                    materials_to_review=found.materials_to_review,
                    notes_to_review=found.notes_to_review,
                    oldest_kind=found.oldest_kind,
                    waiting_since=found.oldest_since,
                )
                for lesson, found in counts.items()
            ]
        )

    async def learner_results(
        self, *, db: AsyncSession, workspace_id: uuid.UUID, student_id: str
    ) -> LearnerResultsResponse:
        """One learner's class tests for the workspace's subject, and how they did per objective."""
        found = await self.class_tests.results_for_learner(db, workspace_id, student_id)
        if found is None:
            raise TeachingSequenceApplicationError(404, "learner_not_in_workspace_class")
        tests: list[LearnerTestResponse] = []
        objectives: list[LearnerObjectiveResponse] = []
        for test in found.tests:
            outcome = outcome_of(student_id, test.results)
            if outcome is None:
                continue
            tests.append(
                LearnerTestResponse(
                    lesson_period_id=test.lesson_period_id,
                    lesson_title=test.lesson_title,
                    band=outcome.band,
                    correct=outcome.correct,
                    out_of=outcome.out_of,
                    taken_at=test.taken_at,
                    entered_by=test.entered_by,
                )
            )
            for objective in objective_outcomes(student_id, test.results):
                text = found.objective_texts.get(
                    (test.plan_version_id, objective.lesson_objective_id)
                )
                objectives.append(
                    LearnerObjectiveResponse(
                        objective_text=text or objective.lesson_objective_id,
                        lesson_period_id=test.lesson_period_id,
                        lesson_title=test.lesson_title,
                        band=objective.band,
                        correct=objective.correct,
                        out_of=objective.out_of,
                    )
                )
        objectives.sort(key=lambda objective: _WEAKEST_FIRST.index(objective.band))
        return LearnerResultsResponse(
            student_id=student_id,
            full_name=found.full_name,
            tests=tests,
            objectives=objectives,
            lessons=await self._learner_lessons(db, workspace_id, student_id, tests),
        )

    async def _learner_lessons(
        self,
        db: AsyncSession,
        workspace_id: uuid.UUID,
        student_id: str,
        tests: list[LearnerTestResponse],
    ) -> list[LearnerLessonResponse]:
        planned = await self.learner_lessons.lessons_of(db, workspace_id, student_id)
        by_lesson = {test.lesson_period_id: test for test in tests}
        ordered = in_display_order(
            planned, [ClassTestTaken(test.lesson_period_id, test.taken_at) for test in tests]
        )
        return [
            LearnerLessonResponse(
                lesson_period_id=lesson.lesson_period_id,
                lesson_title=lesson.title,
                correct=test.correct if (test := by_lesson.get(lesson.lesson_period_id)) else None,
                out_of=test.out_of if test else None,
                band=test.band if test else None,
                revision_note=note_status(lesson.note, test is not None),
                revision_note_id=lesson.note.artefact_id if lesson.note else None,
            )
            for lesson in ordered
        ]


def _settings_json(value: object) -> JsonObject | None:
    if not isinstance(value, dict):
        return None
    return cast(JsonObject, value)
