"""The evaluation's class results on a lesson: read them, and bring a study lesson's in."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.application.onbehalf_service import OnBehalfResponseService
from app.domains.assessments.application.service import AssessmentApplicationError
from app.domains.assessments.onbehalf_schemas import OnBehalfResponseRequest
from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationError
from app.domains.teaching.domain.study_results import learner_results
from app.domains.teaching.infrastructure.study_results_repository import StudyResultsRepository
from app.domains.teaching.schemas import (
    StandInPairRequest,
    StandInResponse,
    StudyLearnerResultResponse,
    StudyObjectiveResultResponse,
    StudyResultsResponse,
    StudySourceResponse,
)


class StudyResultsService:
    def __init__(self, repository: StudyResultsRepository | None = None) -> None:
        self._repository = repository or StudyResultsRepository()

    async def sources(
        self, db: AsyncSession, lesson_period_id: uuid.UUID | None = None
    ) -> list[StudySourceResponse]:
        """The evaluation's lessons whose marks or note fit the lesson's approved plan.

        A lesson that fits neither is left out, so the teacher is never offered one that cannot
        be brought in.
        """
        target = (
            await self._repository.approved_version_of(db, lesson_period_id)
            if lesson_period_id is not None
            else None
        )
        have = await self._repository.objective_ids(db, target) if target else None
        steps = await self._repository.plan_step_ids(db, target) if target else set()
        found = []
        for source in await self._repository.sources(db):
            marked = await self._repository.question_objectives(db, source.plan_version_id)
            note = await self._repository.approved_note(db, source.plan_version_id)
            found.append(
                StudySourceResponse(
                    plan_version_id=source.plan_version_id,
                    lesson_title=source.lesson_title,
                    learners=source.learners,
                    fits=have is None or marked <= have,
                    lesson_note_id=note[0] if note else None,
                    note_fits=bool(note and steps and steps <= note[1]),
                )
            )
        usable = [source for source in found if source.fits or source.note_fits]
        return sorted(usable, key=lambda source: not source.fits)

    async def results(
        self, db: AsyncSession, workspace_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> StudyResultsResponse:
        """The results imported onto the lesson, each learner placed by their weakest objective."""
        await self._in_workspace(db, workspace_id, lesson_period_id)
        version = await self._repository.version_with_results(db, lesson_period_id)
        if version is None:
            return StudyResultsResponse(imported=False, learners=[])
        texts = await self._repository.objective_texts(db, version)
        scripts = await self._repository.scripts(db, version)
        return StudyResultsResponse(
            imported=True,
            learners=[
                StudyLearnerResultResponse(
                    student_id=found.student_id,
                    full_name=found.full_name,
                    teacher_total=found.teacher_total,
                    band=found.band,
                    correct=found.correct,
                    out_of=found.out_of,
                    objectives=[
                        StudyObjectiveResultResponse(
                            lesson_objective_id=o.lesson_objective_id,
                            objective_text=texts.get(o.lesson_objective_id, o.lesson_objective_id),
                            band=o.band,
                            correct=o.correct,
                            out_of=o.out_of,
                            misconceptions=o.misconceptions,
                        )
                        for o in found.objectives
                    ],
                )
                for found in learner_results(scripts)
            ],
        )

    async def import_results(
        self,
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lesson_period_id: uuid.UUID,
        from_plan_version_id: str,
    ) -> StudyResultsResponse:
        """Copy a study lesson's marked classwork onto this lesson's approved plan.

        The plan must be approved, have no results yet, and have every objective the classwork
        was marked against.
        """
        await self._in_workspace(db, workspace_id, lesson_period_id)
        target = await self._repository.approved_version_of(db, lesson_period_id)
        if target is None:
            raise TeachingSequenceApplicationError(409, "approve_the_plan_first")
        if await self._repository.has_scripts(db, target):
            raise TeachingSequenceApplicationError(409, "class_results_already_imported")
        if not await self._repository.has_scripts(db, from_plan_version_id):
            raise TeachingSequenceApplicationError(404, "study_results_not_found")
        marked = await self._repository.question_objectives(db, from_plan_version_id)
        missing = sorted(marked - await self._repository.objective_ids(db, target))
        if missing:
            raise TeachingSequenceApplicationError(
                422, f"the_plan_lacks_the_objectives:{','.join(missing)}"
            )
        await self._repository.copy(db, from_plan_version_id, target)
        await db.commit()
        return await self.results(db, workspace_id, lesson_period_id)

    async def stand_in(
        self,
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lesson_period_id: uuid.UUID,
        pairs: list[StandInPairRequest],
        entered_by: str | None,
    ) -> StandInResponse:
        """Give each class learner the marks of a study learner as their own results.

        The marks are entered for the learner as a teacher enters a learner's classwork, so the
        learner's note is queued and made as any other. The results must be imported first.
        """
        await self._in_workspace(db, workspace_id, lesson_period_id)
        target = await self._repository.approved_version_of(db, lesson_period_id)
        if target is None:
            raise TeachingSequenceApplicationError(409, "approve_the_plan_first")
        if not await self._repository.has_scripts(db, target):
            raise TeachingSequenceApplicationError(409, "import_the_class_results_first")
        entries = []
        for pair in pairs:
            work = await self._repository.marked_work(db, target, pair.study_student_id)
            if all(entry.mark == "unmarked" for entry in work):
                raise TeachingSequenceApplicationError(
                    422, f"nothing_marked:{pair.study_student_id}"
                )
            entries.append((pair, work))
        for pair, work in entries:
            marks_of = await self._repository.learner_name(db, pair.study_student_id)
            try:
                await OnBehalfResponseService().enter(
                    db=db,
                    plan_version_id=target,
                    request=OnBehalfResponseRequest(student_id=pair.student_id, marked_work=work),
                    entered_by=f"{entered_by or 'Teacher'} · marks of {marks_of}",
                )
            except AssessmentApplicationError as error:
                raise TeachingSequenceApplicationError(error.status_code, error.detail) from error
        return StandInResponse(made=pairs)

    async def is_evaluation_lesson(self, db: AsyncSession, plan_version_id: str) -> bool:
        """Whether the plan version is one of the evaluation's own lessons."""
        return await self._repository.is_evaluation_version(db, plan_version_id)

    async def _in_workspace(
        self, db: AsyncSession, workspace_id: uuid.UUID, lesson_period_id: uuid.UUID
    ) -> None:
        if not await self._repository.lesson_in_workspace(db, workspace_id, lesson_period_id):
            raise TeachingSequenceApplicationError(404, "workspace_or_lesson_not_found")
