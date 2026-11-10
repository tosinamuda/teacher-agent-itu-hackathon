"""Teaching workspace routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.teaching.api.sequence_routes import router as sequence_router
from app.domains.teaching.application import (
    TeachingSequenceApplicationError,
    TeachingWorkspaceApplicationService,
)
from app.domains.teaching.application.learner_answers import LearnerAnswers
from app.domains.teaching.application.lesson_start_over import LessonStartOver
from app.domains.teaching.application.study_results_service import StudyResultsService
from app.domains.teaching.schemas import (
    ClassLearnersResponse,
    LearnerAnswersResponse,
    LearnerResultsResponse,
    LessonReviewsResponse,
    StandInRequest,
    StandInResponse,
    StartOverResponse,
    StudyResultsRequest,
    StudyResultsResponse,
    StudySourceResponse,
    TeachingWorkspaceResponse,
)
from app.shared.auth import Actor, get_actor
from app.shared.authz import enforce, requires

router = APIRouter(prefix="/teaching", tags=["teaching"])
router.include_router(sequence_router)


@router.get("/workspaces", response_model=list[TeachingWorkspaceResponse])
async def list_teaching_workspaces(
    x_teacher_code: str | None = Header(default=None, alias="x-teacher-code"),
    db: AsyncSession = Depends(get_db),
) -> list[TeachingWorkspaceResponse]:
    service = TeachingWorkspaceApplicationService()
    return await service.list_workspaces(db=db, teacher_code=x_teacher_code)


@router.get("/workspaces/{workspace_id}/learners", response_model=ClassLearnersResponse)
async def class_learners(
    workspace_id: uuid.UUID,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> ClassLearnersResponse:
    """The workspace's class, each learner with their latest class test and its band."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    try:
        return await TeachingWorkspaceApplicationService().class_learners(
            db=db, workspace_id=workspace_id
        )
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("/workspaces/{workspace_id}/lesson-reviews", response_model=LessonReviewsResponse)
async def lesson_reviews(
    workspace_id: uuid.UUID,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> LessonReviewsResponse:
    """What waits for the teacher in each lesson: plans, class materials and learners' notes."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    return await TeachingWorkspaceApplicationService().lesson_reviews(
        db=db, workspace_id=workspace_id
    )


@router.get("/study-results/sources", response_model=list[StudySourceResponse])
async def study_result_sources(
    lesson_period_id: uuid.UUID | None = None,
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[StudySourceResponse]:
    """The evaluation's lessons whose marked classwork can be imported onto a lesson.

    With a lesson, those whose objectives its approved plan has come first and say so.
    """
    return await StudyResultsService().sources(db, lesson_period_id)


@router.get(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/study-results",
    response_model=StudyResultsResponse,
)
async def lesson_study_results(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> StudyResultsResponse:
    """The evaluation's class results imported onto the lesson, each learner banded."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    try:
        return await StudyResultsService().results(db, workspace_id, lesson_period_id)
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/learners/{student_id}/answers",
    response_model=LearnerAnswersResponse,
)
async def lesson_learner_answers(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    student_id: str,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> LearnerAnswersResponse:
    """What one learner answered on the lesson, question by question."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    try:
        return await LearnerAnswers().of(db, workspace_id, lesson_period_id, student_id)
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.post(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/study-results",
    response_model=StudyResultsResponse,
    status_code=201,
)
async def import_study_results(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    body: StudyResultsRequest,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> StudyResultsResponse:
    """Import a study lesson's marked classwork onto the lesson's approved plan."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    try:
        return await StudyResultsService().import_results(
            db, workspace_id, lesson_period_id, body.from_plan_version_id
        )
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.post(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/study-results/stand-ins",
    response_model=StandInResponse,
    status_code=201,
)
async def stand_in_for_learners(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    body: StandInRequest,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> StandInResponse:
    """Make class learners' results from study learners' marks, so their notes are made."""
    await enforce(
        actor, obj="submission:*", act="enter_on_behalf", db=db, dom=f"workspace|{workspace_id}"
    )
    try:
        return await StudyResultsService().stand_in(
            db, workspace_id, lesson_period_id, body.pairs, actor.display_name
        )
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/start-over",
    response_model=StartOverResponse,
)
async def preview_start_over(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> StartOverResponse:
    """What clearing the lesson would remove, and whether it may be cleared at all."""
    await enforce(
        actor, obj="lesson_plan:*", act="author_plan", db=db, dom=f"workspace|{workspace_id}"
    )
    try:
        plan = await LessonStartOver().preview(db, workspace_id, lesson_period_id)
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return StartOverResponse(counts=plan.counts, blocked=plan.blocked)


@router.delete(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/start-over",
    response_model=StartOverResponse,
)
async def start_over(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> StartOverResponse:
    """Clear what was made for the lesson. The lesson, its class and the learners stay."""
    await enforce(
        actor, obj="lesson_plan:*", act="author_plan", db=db, dom=f"workspace|{workspace_id}"
    )
    try:
        removed = await LessonStartOver().clear(db, workspace_id, lesson_period_id)
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return StartOverResponse(counts=removed)


@router.get(
    "/workspaces/{workspace_id}/learners/{student_id}/results",
    response_model=LearnerResultsResponse,
)
async def learner_results(
    workspace_id: uuid.UUID,
    student_id: str,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> LearnerResultsResponse:
    """One learner's class tests for the workspace's subject, and how they did per objective."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    try:
        return await TeachingWorkspaceApplicationService().learner_results(
            db=db, workspace_id=workspace_id, student_id=student_id
        )
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get(
    "/workspaces/{workspace_id}/lessons/{lesson_period_id}/evidence",
    response_model=ClassLearnersResponse,
)
async def lesson_evidence(
    workspace_id: uuid.UUID,
    lesson_period_id: uuid.UUID,
    actor: Actor = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
) -> ClassLearnersResponse:
    """How each learner of the class did on one lesson's class test."""
    await enforce(actor, obj="learner:*", act="read", db=db, dom=f"workspace|{workspace_id}")
    try:
        return await TeachingWorkspaceApplicationService().class_learners(
            db=db, workspace_id=workspace_id, lesson_period_id=lesson_period_id
        )
    except TeachingSequenceApplicationError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
