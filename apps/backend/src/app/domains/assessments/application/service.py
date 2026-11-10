from __future__ import annotations

import logging
from collections import OrderedDict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_learner_pack_gate,
)
from app.domains.assessments.application.diagnostic_service import (
    DiagnosticGenerationError,
    DiagnosticGenerationService,
)
from app.domains.assessments.application.scoring import (
    attach_survey_to_results,
    score_objective_diagnostic,
)
from app.domains.assessments.infrastructure.repository import AssessmentRepository
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.assessments.schemas import (
    AssessmentStatusResponse,
    ExitAssessmentAnswer,
    ExitAssessmentItemResponse,
    ExitAssessmentObjectiveQuestions,
    ExitAssessmentObjectiveSurvey,
    ExitAssessmentQuestionsResponse,
    ExitAssessmentSessionSurvey,
    ExitAssessmentSubmitRequest,
    ExitAssessmentSurveyAttachRequest,
    ExitTicketSubmissionCreateRequest,
)
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


# Not frozen: Python sets __traceback__ on an exception as it passes through a context manager.
@dataclass(eq=False)
class AssessmentApplicationError(Exception):
    status_code: int
    detail: str


class AssessmentApplicationService:
    def __init__(
        self,
        repository: AssessmentRepository | None = None,
        diagnostic_service: DiagnosticGenerationService | None = None,
    ) -> None:
        self.repository = repository or AssessmentRepository()
        self._diagnostic_service = diagnostic_service

    async def list_student_submissions(
        self,
        *,
        db: AsyncSession,
        student_id: str,
    ) -> list[ExitTicketSubmission]:
        """Every exit-assessment a student has submitted — drives per-lesson status."""
        return await self.repository.list_submissions_for_student(db, student_id)

    async def create_exit_ticket_submission(
        self,
        *,
        db: AsyncSession,
        payload: ExitTicketSubmissionCreateRequest,
    ) -> ExitTicketSubmission:
        await self._require_student_and_plan(db, payload.student_id, payload.plan_version_id)
        return await self._persist_submission(
            db,
            student_id=payload.student_id,
            plan_version_id=payload.plan_version_id,
            results=payload.results,
            diagnostic_id=payload.diagnostic_id,
        )

    async def generate_diagnostic(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        item_count: int = 2,
    ) -> int:
        """Generate + persist the MCQ diagnostic (tagged distractors) for a lesson.

        Refuses to regenerate once any student has answered: the new items would
        replace the very rows their responses reference (FK), silently invalidating
        their evidence. Surfaces a clean 409 instead of a deep IntegrityError (1451).
        """
        if await self._has_student_responses(db, plan_version_id):
            raise AssessmentApplicationError(409, "assessment_has_responses")
        if self._diagnostic_service is None:
            raise AssessmentApplicationError(500, "class_test_generator_not_wired")
        try:
            return await self._diagnostic_service.generate_for_plan(
                db=db, plan_version_id=plan_version_id, item_count=item_count
            )
        except DiagnosticGenerationError as error:
            raise AssessmentApplicationError(404, str(error)) from error
        except IntegrityError as error:
            # Race: a student submitted responses AFTER the _has_student_responses gate above
            # but before the regenerate's DELETE of exit_ticket_items, so the DELETE FK-violates
            # (1451). Resolve to the same intended 409 instead of a raw 500. The FK is RESTRICT
            # (not CASCADE), so the student's evidence + the old items survive — the would-be new
            # items roll back.
            await db.rollback()
            raise AssessmentApplicationError(409, "assessment_has_responses") from error

    async def _has_student_responses(self, db: AsyncSession, plan_version_id: str) -> bool:
        """True if any student has answered this plan's diagnostic (blocks regeneration)."""
        return await self.repository.has_student_responses(db, plan_version_id)

    async def assessment_status(
        self,
        *,
        db: AsyncSession,
        plan_version_ids: Sequence[str],
    ) -> list[AssessmentStatusResponse]:
        """Per-lesson assessment state (created? released?) for the given lessons."""
        with_items = await self.repository.plan_versions_with_items(db, plan_version_ids)
        released = await self.repository.released_plan_versions(db, plan_version_ids)
        return [
            AssessmentStatusResponse(
                plan_version_id=plan_version_id,
                has_assessment=plan_version_id in with_items,
                released=plan_version_id in released,
            )
            for plan_version_id in plan_version_ids
        ]

    async def release_assessment(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        released_by: str | None,
    ) -> None:
        """Release the lesson's assessment to students (teacher action)."""
        ok = await self.repository.set_assessment_released(
            db, plan_version_id=plan_version_id, released_by=released_by
        )
        if not ok:
            raise AssessmentApplicationError(404, "plan_version_not_found")

    async def get_exit_assessment_questions(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
    ) -> ExitAssessmentQuestionsResponse:
        """Serve the generated MCQ items grouped by objective (no answers/tags)."""
        plan_version = await self.repository.get_plan_version(db, plan_version_id)
        if plan_version is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")
        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        plan_objectives = session_plan.lesson_plan_objectives
        objective_text = {obj.lesson_objective_id: obj.objective_text for obj in plan_objectives}
        in_plan_order = {obj.lesson_objective_id: i for i, obj in enumerate(plan_objectives)}

        items = await self.repository.get_exit_ticket_items(db, plan_version_id)
        grouped: OrderedDict[str, list[JsonObject]] = OrderedDict()
        for item in items:
            objective_id = item.lesson_objective_id or "unassigned"
            grouped.setdefault(objective_id, []).append(
                {
                    "item_id": str(item.id),
                    "stem": item.stem,
                    "options": item.options,
                    "difficulty": item.difficulty,
                }
            )

        objectives = [
            ExitAssessmentObjectiveQuestions(
                lesson_objective_id=objective_id,
                objective_text=objective_text.get(objective_id),
                items=item_list,
            )
            for objective_id, item_list in sorted(
                grouped.items(),
                key=lambda group: in_plan_order.get(group[0], len(in_plan_order)),
            )
        ]
        return ExitAssessmentQuestionsResponse(
            plan_version_id=plan_version_id,
            subject=session_plan.subject,
            topic=session_plan.topic,
            subtopic=session_plan.subtopic,
            objectives=objectives,
        )

    async def submit_exit_assessment(
        self,
        *,
        db: AsyncSession,
        payload: ExitAssessmentSubmitRequest,
    ) -> ExitTicketSubmission:
        """Grade the student's selected options and persist the diagnostic.

        Reads correctness + the misconception from each chosen distractor, scores
        the result into the objective-indexed diagnostic, and persists it
        (the input that drives P1 personalisation).
        """
        await self._require_student_and_plan(db, payload.student_id, payload.plan_version_id)
        if not await self.repository.is_assessment_released(db, payload.plan_version_id):
            raise AssessmentApplicationError(403, "assessment_not_released")
        # One submission per (student, lesson): first wins. This early check returns a
        # friendly 409 without grading; the DB unique (uq_exit_ticket_submission_student_plan)
        # is the race backstop, converged below.
        if await self.repository.submission_exists_for_student_plan(
            db, student_id=payload.student_id, plan_version_id=payload.plan_version_id
        ):
            raise AssessmentApplicationError(409, "already_submitted")
        return await self.grade_and_persist(
            db=db,
            student_id=payload.student_id,
            plan_version_id=payload.plan_version_id,
            answers=payload.answers,
            survey=payload.survey,
            session_survey=payload.session_survey,
            survey_pending=payload.survey_pending,
            diagnostic_id=payload.diagnostic_id,
        )

    async def grade_and_persist(
        self,
        *,
        db: AsyncSession,
        student_id: str,
        plan_version_id: str,
        answers: list[ExitAssessmentAnswer],
        survey: list[ExitAssessmentObjectiveSurvey] | None = None,
        session_survey: ExitAssessmentSessionSurvey | None = None,
        survey_pending: bool = False,
        diagnostic_id: str | None = None,
        entered_by: str | None = None,
        provenance_attachment_id: str | None = None,
    ) -> ExitTicketSubmission:
        """Grade chosen options into StudentItemResponse rows + the objective diagnostic.

        The shared core of the student self-submit and the on-behalf entry (FD-04):
        correctness + the chosen-distractor misconception per item, scored into the
        results the personalisation pipeline consumes, then persisted. ``entered_by``
        + ``provenance_attachment_id`` are set for on-behalf entry (NULL for self-submit).
        """
        items = await self.repository.get_exit_ticket_items(db, plan_version_id)
        items_by_id = {str(item.id): item for item in items}

        responses: list[ExitAssessmentItemResponse] = []
        for answer in answers:
            item = items_by_id.get(answer.item_id)
            if item is None or not item.lesson_objective_id:
                continue
            is_correct = answer.selected_option == item.correct_option
            misconception = None
            if not is_correct and isinstance(item.option_misconceptions, dict):
                misconception = item.option_misconceptions.get(answer.selected_option)
            responses.append(
                ExitAssessmentItemResponse(
                    lesson_objective_id=item.lesson_objective_id,
                    item_id=answer.item_id,
                    is_correct=is_correct,
                    misconception_code=misconception,
                    stem=item.stem,
                    options=item.options if isinstance(item.options, dict) else None,
                    correct_option=item.correct_option,
                    chosen_option=answer.selected_option,
                )
            )
            db.add(
                StudentItemResponse(
                    item_id=item.id,
                    student_id=student_id,
                    choice=answer.selected_option,
                    is_correct=is_correct,
                    score=1.0 if is_correct else 0.0,
                )
            )
        if not responses:
            raise AssessmentApplicationError(422, "no_gradable_answers")

        results = score_objective_diagnostic(responses, survey, session_survey).model_dump(
            mode="json", exclude_none=True
        )
        # The pack personalises from the FULL evidence (scores + survey). In the
        # two-step student flow the survey follows in a separate call, so the submission
        # records it as pending and the pack waits for attach_exit_assessment_survey.
        return await self.persist_diagnostic(
            db=db,
            student_id=student_id,
            plan_version_id=plan_version_id,
            results=results,
            diagnostic_id=diagnostic_id,
            entered_by=entered_by,
            provenance_attachment_id=provenance_attachment_id,
            survey_pending=survey_pending,
        )

    async def persist_diagnostic(
        self,
        *,
        db: AsyncSession,
        student_id: str,
        plan_version_id: str,
        results: JsonObject,
        diagnostic_id: str | None = None,
        entered_by: str | None = None,
        provenance_attachment_id: str | None = None,
        survey_pending: bool = False,
    ) -> ExitTicketSubmission:
        """Persist an already-scored diagnostic and ask for the learner's pack.

        The seam the score-only on-behalf path uses: it builds ``results`` directly
        from per-objective scores (no per-item responses) and persists them here.
        """
        submission = await self._persist_submission(
            db,
            student_id=student_id,
            plan_version_id=plan_version_id,
            results=results,
            diagnostic_id=diagnostic_id,
            entered_by=entered_by,
            provenance_attachment_id=provenance_attachment_id,
            survey_pending=survey_pending,
        )
        await self._request_student_pack(db, student_id, plan_version_id)
        return submission

    async def attach_exit_assessment_survey(
        self,
        *,
        db: AsyncSession,
        diagnostic_id: str,
        student_id: str,
        payload: ExitAssessmentSurveyAttachRequest,
    ) -> ExitTicketSubmission:
        """Attach the post-class survey to a graded diagnostic (step 2 of 2).

        Completes the learner evidence (per-objective Confidence/Difficulty +
        session Interest/Affect) and only then triggers personalised pack
        generation — P1 must never run on a survey-less state.
        """
        # Lock the submission: the survey merge below is a read-modify-write on the results
        # JSON, so two concurrent attaches off the same snapshot would lose one survey. Under
        # the lock the second attach builds on the first's committed survey instead.
        submission = await self.repository.get_submission_by_diagnostic_id_for_update(
            db, diagnostic_id
        )
        if submission is None:
            raise AssessmentApplicationError(404, "diagnostic_not_found")
        if submission.student_id != student_id:
            raise AssessmentApplicationError(409, "student_identity_mismatch")
        submission.results = attach_survey_to_results(
            dict(submission.results or {}), payload.survey, payload.session_survey
        )
        submission.survey_pending = False
        await db.commit()
        await db.refresh(submission)
        await self._request_student_pack(db, submission.student_id, submission.plan_version_id)
        return submission

    async def _request_student_pack(
        self, db: AsyncSession, student_id: str, plan_version_id: str
    ) -> None:
        """Ask for the student's personalised pack; it is made once the gate is open.

        The gate queues a tracked generation job only when the lesson's class pack is
        approved and the learner's evidence is complete; otherwise the learner waits, and
        the class pack's approval queues them. Best-effort — never block the submission.
        """
        try:
            await build_learner_pack_gate().request(
                db, student_id=student_id, plan_version_id=plan_version_id
            )
        except Exception:  # noqa: BLE001 - enqueue failure must not fail the submit
            logging.getLogger(__name__).warning(
                "failed to enqueue student pack generation for %s",
                student_id,
                exc_info=True,
            )

    async def _require_student_and_plan(
        self, db: AsyncSession, student_id: str, plan_version_id: str
    ) -> None:
        if await self.repository.get_student(db, student_id) is None:
            raise AssessmentApplicationError(404, "student_not_found")
        if await self.repository.get_plan_version(db, plan_version_id) is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")

    async def _persist_submission(
        self,
        db: AsyncSession,
        *,
        student_id: str,
        plan_version_id: str,
        results: JsonObject,
        diagnostic_id: str | None,
        entered_by: str | None = None,
        provenance_attachment_id: str | None = None,
        survey_pending: bool = False,
    ) -> ExitTicketSubmission:
        diagnostic_id = diagnostic_id or new_public_id(PublicIdPrefix.DIAGNOSTIC)
        if await self.repository.get_submission_by_diagnostic_id(db, diagnostic_id) is not None:
            raise AssessmentApplicationError(409, "diagnostic_exists")
        submission = ExitTicketSubmission(
            diagnostic_id=diagnostic_id,
            student_id=student_id,
            plan_version_id=plan_version_id,
            results=results,
            entered_by=entered_by,
            provenance_attachment_id=provenance_attachment_id,
            survey_pending=survey_pending,
            created_at=datetime.now(timezone.utc),
        )
        try:
            return await self.repository.save_submission(db, submission)
        except IntegrityError as exc:
            # Lost a concurrent race on one of two uniques: (student, plan) — a second
            # submission for this lesson racing the early check above — or diagnostic_id.
            # Roll back the poisoned session, then surface the precise 409 (re-query with
            # plain values AFTER the rollback, never the now-expired ORM object).
            await db.rollback()
            if await self.repository.submission_exists_for_student_plan(
                db, student_id=student_id, plan_version_id=plan_version_id
            ):
                raise AssessmentApplicationError(409, "already_submitted") from exc
            raise AssessmentApplicationError(409, "diagnostic_exists") from exc
