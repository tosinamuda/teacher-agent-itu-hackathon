"""Enter a student's exit-assessment responses on their behalf (FD-04).

A researcher/teacher records what a student answered (no student login). This
reuses the same grading/scoring/persistence as the student self-submit, but as a
separate flow: the self-submit binds identity to the signed-in student and rejects
acting as anyone else, so it cannot be reused here. Two input modes — per-item
chosen options (full signal) or per-objective scores (score-only, band but no
misconception). The entering account is stamped as ``entered_by``.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.application.marked_work import marked_work_results
from app.domains.assessments.application.scoring import (
    ObjectiveDiagnosticResults,
    ScoredObjectiveDiagnostic,
    SessionSurveyResult,
)
from app.domains.assessments.application.service import (
    AssessmentApplicationError,
    AssessmentApplicationService,
)
from app.domains.assessments.infrastructure.repository import AssessmentRepository
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.onbehalf_schemas import (
    OnBehalfContextResponse,
    OnBehalfItem,
    OnBehalfObjective,
    OnBehalfResponseRequest,
    OnBehalfResponseResult,
)
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class OnBehalfResponseService:
    def __init__(
        self,
        repository: AssessmentRepository | None = None,
        assessment_service: AssessmentApplicationService | None = None,
    ) -> None:
        self.repository = repository or AssessmentRepository()
        self._assessment = assessment_service or AssessmentApplicationService(self.repository)

    async def context(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
    ) -> OnBehalfContextResponse:
        """The items to record choices against + which students already submitted."""
        plan_version = await self.repository.get_plan_version(db, plan_version_id)
        if plan_version is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")
        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        items = await self.repository.get_exit_ticket_items(db, plan_version_id)
        submitted = await self.repository.submitted_student_ids(db, plan_version_id)
        return OnBehalfContextResponse(
            plan_version_id=plan_version_id,
            subject=session_plan.subject,
            topic=session_plan.topic,
            subtopic=session_plan.subtopic,
            objectives=[
                OnBehalfObjective(
                    lesson_objective_id=objective.lesson_objective_id,
                    objective_text=objective.objective_text,
                )
                for objective in session_plan.lesson_plan_objectives
                if objective.lesson_objective_id
            ],
            items=[
                OnBehalfItem(
                    item_id=str(item.id),
                    lesson_objective_id=item.lesson_objective_id,
                    stem=item.stem,
                    options=item.options,
                )
                for item in items
            ],
            submitted_student_ids=sorted(submitted),
        )

    async def enter(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        request: OnBehalfResponseRequest,
        entered_by: str | None,
    ) -> OnBehalfResponseResult:
        """Grade + persist a student's responses on their behalf (first entry wins)."""
        if await self.repository.get_plan_version(db, plan_version_id) is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")
        if await self.repository.get_student(db, request.student_id) is None:
            raise AssessmentApplicationError(404, "student_not_found")
        if await self.repository.submission_exists_for_student_plan(
            db, student_id=request.student_id, plan_version_id=plan_version_id
        ):
            raise AssessmentApplicationError(409, "already_submitted")

        submission, scored = await self._record(
            db=db,
            plan_version_id=plan_version_id,
            request=request,
            entered_by=entered_by,
        )

        return OnBehalfResponseResult(
            diagnostic_id=submission.diagnostic_id,
            student_id=submission.student_id,
            plan_version_id=plan_version_id,
            objectives_scored=scored,
        )

    async def _record(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        request: OnBehalfResponseRequest,
        entered_by: str | None,
    ) -> tuple[ExitTicketSubmission, int]:
        """Persist the one kind of entry the request holds; return it and how many were scored."""
        if request.answers:
            submission = await self._assessment.grade_and_persist(
                db=db,
                student_id=request.student_id,
                plan_version_id=plan_version_id,
                answers=request.answers,
                survey=request.survey,
                session_survey=request.session_survey,
                entered_by=entered_by,
                provenance_attachment_id=request.provenance_attachment_id,
            )
            return submission, len({answer.item_id for answer in request.answers})
        if request.marked_work:
            results = marked_work_results(
                request.marked_work, request.survey, request.session_survey
            )
            scored = len(
                {e.lesson_objective_id for e in request.marked_work if e.mark != "unmarked"}
            )
        else:
            results = self._score_only_results(request)
            scored = len(request.objective_scores)
        submission = await self._assessment.persist_diagnostic(
            db=db,
            student_id=request.student_id,
            plan_version_id=plan_version_id,
            results=results,
            entered_by=entered_by,
            provenance_attachment_id=request.provenance_attachment_id,
        )
        return submission, scored

    def _score_only_results(self, request: OnBehalfResponseRequest) -> JsonObject:
        """Build the diagnostic results from per-objective scores alone.

        No per-item evidence and no misconception (N/A) — but score/max_score is all
        LearnerStateService needs to derive the band, so P0/P1 still run.
        """
        objectives = [
            ScoredObjectiveDiagnostic(
                lesson_objective_id=entry.lesson_objective_id,
                score=entry.score,
                max_score=entry.max_score,
            )
            for entry in request.objective_scores
        ]
        session = None
        if request.session_survey is not None and (
            request.session_survey.interest is not None or request.session_survey.affect is not None
        ):
            session = SessionSurveyResult(
                interest=request.session_survey.interest,
                affect=request.session_survey.affect,
            )
        return ObjectiveDiagnosticResults(objectives=objectives, session=session).model_dump(
            mode="json", exclude_none=True
        )
