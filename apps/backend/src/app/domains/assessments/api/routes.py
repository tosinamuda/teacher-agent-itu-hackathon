"""Assessment / exit-ticket submission routes."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db

if TYPE_CHECKING:
    from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.application.classwork_service import ClassworkApplicationService
from app.domains.assessments.application.onbehalf_service import OnBehalfResponseService
from app.domains.assessments.application.service import (
    AssessmentApplicationError,
    AssessmentApplicationService,
)
from app.domains.assessments.classwork_schemas import (
    ClassworkCoverageResponse,
    DeriveMisconceptionsRequest,
    DeriveMisconceptionsResponse,
    ManualClassworkContextResponse,
    ManualClassworkCreateRequest,
)
from app.domains.assessments.onbehalf_schemas import (
    OnBehalfContextResponse,
    OnBehalfResponseRequest,
    OnBehalfResponseResult,
)
from app.domains.assessments.schemas import (
    AssessmentStatusResponse,
    ExitAssessmentQuestionsResponse,
    ExitAssessmentSubmitRequest,
    ExitAssessmentSurveyAttachRequest,
    ExitTicketSubmissionCreateRequest,
    ExitTicketSubmissionResponse,
)
from app.domains.learners.application.identity import student_id_of
from app.shared.auth import (
    ROLE_RESEARCH_MANAGER,
    ROLE_TEACHER,
    Actor,
    get_actor,
    require_teacher_or_manager,
)
from app.shared.authz import requires

router = APIRouter(prefix="/assessments", tags=["assessments"])


def _raise_http_error(error: AssessmentApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


def _submission_response(submission: ExitTicketSubmission) -> ExitTicketSubmissionResponse:
    return ExitTicketSubmissionResponse(
        diagnostic_id=submission.diagnostic_id,
        student_id=submission.student_id,
        plan_version_id=submission.plan_version_id,
        created_at=submission.created_at,
        survey_pending=submission.survey_pending,
    )


@router.post("/exit-ticket-submissions", response_model=ExitTicketSubmissionResponse)
async def create_exit_ticket_submission(
    payload: ExitTicketSubmissionCreateRequest,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(requires(obj="submission:*", act="create")),
) -> ExitTicketSubmissionResponse:
    """Submit raw exit-ticket results.

    The body's ``student_id`` is ignored — identity is the authenticated actor's
    student profile (callers can no longer claim to be someone else).
    """
    actor_student_id = await student_id_of(actor, db)
    payload = payload.model_copy(update={"student_id": actor_student_id})
    service = AssessmentApplicationService()
    try:
        submission = await service.create_exit_ticket_submission(db=db, payload=payload)
    except AssessmentApplicationError as error:
        _raise_http_error(error)
    return _submission_response(submission)


@router.get(
    "/exit-assessment/submissions",
    response_model=list[ExitTicketSubmissionResponse],
)
async def list_exit_assessment_submissions(
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(requires(obj="submission:*", act="read")),
) -> list[ExitTicketSubmissionResponse]:
    """List your own exit-assessment submissions (drives per-lesson status)."""
    student_id = await student_id_of(actor, db)
    service = AssessmentApplicationService()
    submissions = await service.list_student_submissions(db=db, student_id=student_id)
    return [_submission_response(submission) for submission in submissions]


@router.get(
    "/exit-assessment/{plan_version_id}/classwork/context",
    response_model=ManualClassworkContextResponse,
)
async def get_manual_classwork_context(
    plan_version_id: str,
    _actor: Actor = Depends(require_teacher_or_manager),
    db: AsyncSession = Depends(get_db),
) -> ManualClassworkContextResponse:
    """Form prerequisites for entering classwork by hand (objectives, KCs, existing items)."""
    service = ClassworkApplicationService()
    try:
        return await service.classwork_context(db=db, plan_version_id=plan_version_id)
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.post(
    "/exit-assessment/{plan_version_id}/classwork/manual",
    response_model=ClassworkCoverageResponse,
)
async def create_manual_classwork(
    plan_version_id: str,
    payload: ManualClassworkCreateRequest,
    _actor: Actor = Depends(require_teacher_or_manager),
    db: AsyncSession = Depends(get_db),
) -> ClassworkCoverageResponse:
    """Persist hand-entered classwork as exit-ticket items (replaces the plan's set).

    Returns the coverage report so the UI flags zero-item objectives immediately.
    """
    service = ClassworkApplicationService()
    try:
        return await service.create_manual_classwork(
            db=db, plan_version_id=plan_version_id, items=payload.items
        )
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.post(
    "/exit-assessment/{plan_version_id}/classwork/derive-misconceptions",
    response_model=DeriveMisconceptionsResponse,
)
async def derive_classwork_misconceptions(
    plan_version_id: str,
    payload: DeriveMisconceptionsRequest,
    _actor: Actor = Depends(require_teacher_or_manager),
    db: AsyncSession = Depends(get_db),
) -> DeriveMisconceptionsResponse:
    """Suggest a misconception code for each wrong option of the entered items (FD-03).

    Suggestions only — the teacher reviews/edits them, then the normal classwork save
    persists them onto the items.
    """
    service = ClassworkApplicationService()
    try:
        return await service.derive_misconceptions(
            db=db, plan_version_id=plan_version_id, items=payload.items
        )
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.get(
    "/exit-assessment/{plan_version_id}/classwork/coverage",
    response_model=ClassworkCoverageResponse,
)
async def get_manual_classwork_coverage(
    plan_version_id: str,
    _actor: Actor = Depends(require_teacher_or_manager),
    db: AsyncSession = Depends(get_db),
) -> ClassworkCoverageResponse:
    """Items-per-objective coverage for a lesson's classwork (zero-item objectives flagged)."""
    service = ClassworkApplicationService()
    try:
        return await service.compute_classwork_coverage(db=db, plan_version_id=plan_version_id)
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.get(
    "/exit-assessment/{plan_version_id}/responses/manual/context",
    response_model=OnBehalfContextResponse,
)
async def get_onbehalf_responses_context(
    plan_version_id: str,
    _actor: Actor = Depends(requires(obj="submission:*", act="enter_on_behalf")),
    db: AsyncSession = Depends(get_db),
) -> OnBehalfContextResponse:
    """Items to record a student's choices against + which students already submitted."""
    service = OnBehalfResponseService()
    try:
        return await service.context(db=db, plan_version_id=plan_version_id)
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.post(
    "/exit-assessment/{plan_version_id}/responses/manual",
    response_model=OnBehalfResponseResult,
)
async def enter_onbehalf_responses(
    plan_version_id: str,
    payload: OnBehalfResponseRequest,
    actor: Actor = Depends(requires(obj="submission:*", act="enter_on_behalf")),
    db: AsyncSession = Depends(get_db),
) -> OnBehalfResponseResult:
    """Record a student's responses on their behalf — grades + derives learner state (FD-04)."""
    service = OnBehalfResponseService()
    try:
        return await service.enter(
            db=db, plan_version_id=plan_version_id, request=payload, entered_by=actor.display_name
        )
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.get("/exit-assessment/status", response_model=list[AssessmentStatusResponse])
async def list_assessment_status(
    plan_version_ids: list[str] = Query(default=[]),
    db: AsyncSession = Depends(get_db),
) -> list[AssessmentStatusResponse]:
    """Per-lesson assessment state (created? released?) for the given lessons.

    Lets the teacher's lesson-prep queue show, in one request, whether each
    lesson's assessment has been created and sent to students.
    """
    service = AssessmentApplicationService()
    return await service.assessment_status(db=db, plan_version_ids=plan_version_ids)


@router.get(
    "/exit-assessment/{plan_version_id}/questions",
    response_model=ExitAssessmentQuestionsResponse,
)
async def get_exit_assessment_questions(
    plan_version_id: str,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> ExitAssessmentQuestionsResponse:
    """Per-objective assessment items for a lesson (student-facing, no answers).

    Teachers + research managers always see it (for preview); everyone else
    (students) only once the teacher has released the assessment.
    """
    service = AssessmentApplicationService()
    is_previewer = actor.role in (ROLE_TEACHER, ROLE_RESEARCH_MANAGER)
    try:
        if not is_previewer and not await service.repository.is_assessment_released(
            db, plan_version_id
        ):
            raise AssessmentApplicationError(403, "assessment_not_released")
        return await service.get_exit_assessment_questions(db=db, plan_version_id=plan_version_id)
    except AssessmentApplicationError as error:
        _raise_http_error(error)


@router.post("/exit-assessment", response_model=ExitTicketSubmissionResponse)
async def submit_exit_assessment(
    payload: ExitAssessmentSubmitRequest,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(requires(obj="submission:*", act="create")),
) -> ExitTicketSubmissionResponse:
    """Submit graded responses; server scores them into the diagnostic.

    Identity is the authenticated actor's student profile. If the body names a
    DIFFERENT student (e.g. the portal's "act as learner" view is out of sync
    with the signed-in user), the submission is rejected outright — silently
    re-attributing it would corrupt that learner's evidence (2026-06-10 dress
    rehearsal finding). The objective-indexed diagnostic personalises the
    per-student review pack.
    """
    actor_student_id = await student_id_of(actor, db)
    if payload.student_id and payload.student_id != actor_student_id:
        raise HTTPException(status_code=409, detail="student_identity_mismatch")
    payload = payload.model_copy(update={"student_id": actor_student_id})
    service = AssessmentApplicationService()
    try:
        submission = await service.submit_exit_assessment(db=db, payload=payload)
    except AssessmentApplicationError as error:
        _raise_http_error(error)
    return _submission_response(submission)


@router.post(
    "/exit-assessment/{diagnostic_id}/survey",
    response_model=ExitTicketSubmissionResponse,
)
async def attach_exit_assessment_survey(
    diagnostic_id: str,
    payload: ExitAssessmentSurveyAttachRequest,
    db: AsyncSession = Depends(get_db),
    actor: Actor = Depends(requires(obj="submission:*", act="create")),
) -> ExitTicketSubmissionResponse:
    """Attach the post-class survey to the student's graded diagnostic (step 2).

    The student first submits answers (graded immediately), then the survey
    screen follows. Completing it fills the per-objective Confidence/Difficulty
    + session Interest/Affect into the diagnostic and triggers personalised pack
    generation. Identity must match the diagnostic's student.
    """
    actor_student_id = await student_id_of(actor, db)
    service = AssessmentApplicationService()
    try:
        submission = await service.attach_exit_assessment_survey(
            db=db,
            diagnostic_id=diagnostic_id,
            student_id=actor_student_id,
            payload=payload,
        )
    except AssessmentApplicationError as error:
        _raise_http_error(error)
    return _submission_response(submission)
