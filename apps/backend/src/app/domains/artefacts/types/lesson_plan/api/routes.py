from __future__ import annotations

import re
import uuid
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.types.lesson_plan.api.schemas import (
    DraftingProgress,
    ManualPlanContextResponse,
    OutlineStep,
    PlanGenerateRequest,
    PlanGenerateResponse,
    PlanManualCreateRequest,
    PlanManualEditRequest,
    PlanOutline,
    PlanReuseRequest,
    PlanReuseResponse,
    PlanVersionSummary,
    ProgressLine,
)
from app.domains.artefacts.types.lesson_plan.application.errors import (
    PlanLookupNotFoundError,
    PlanNotOwnedByTeacherError,
    PlanValidationError,
    SessionNotFoundError,
)
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owns_lesson_period,
)
from app.domains.artefacts.types.lesson_plan.application.reuse_for_teacher import (
    reuse_plan_for_lesson,
)
from app.domains.artefacts.types.lesson_plan.application.service import (
    LessonPlanApplicationService,
)
from app.domains.artefacts.types.lesson_plan.deps import (
    get_content_specifications,
    lesson_plan_service,
)
from app.domains.artefacts.types.lesson_plan.drafting.deps import (
    get_lesson_generation_service,
    get_session_plan_validator,
)
from app.domains.artefacts.types.lesson_plan.jobs import drafting_channel, drafting_subject
from app.domains.assessments.infrastructure.wiring import build_diagnostic_service
from app.domains.content_engine.infrastructure.plan_progress import drafting_outline
from app.domains.content_engine.infrastructure.progress_lines import data_of, lines_after
from app.domains.jobs.api.schemas import JobAccepted
from app.domains.learners.infrastructure.repository import LearnerRepository
from app.infra import progress
from app.infra.jobs.kinds import GENERATE_LESSON_PLAN
from app.infra.jobs.queue import JobQueue
from app.shared.auth import ROLE_TEACHER, Actor
from app.shared.authz import requires

if TYPE_CHECKING:
    from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
        LessonGenerationService,
    )
    from app.domains.artefacts.types.lesson_plan.drafting.validation.validator_service import (
        SessionPlanValidatorService,
    )


router = APIRouter(prefix="/artefacts/lesson-plans", tags=["lesson-plans"])


def get_lesson_plan_application_service(
    db: AsyncSession = Depends(get_db),
    generator: LessonGenerationService = Depends(get_lesson_generation_service),
    validator: SessionPlanValidatorService = Depends(get_session_plan_validator),
    specifications: ContentSpecifications = Depends(get_content_specifications),
) -> LessonPlanApplicationService:
    return lesson_plan_service(
        db,
        generator=generator,
        validator=validator,
        specifications=specifications,
        diagnostic_service=build_diagnostic_service(),
    )


@router.post("/{plan_or_version_id}/manual-edit", response_model=PlanGenerateResponse)
async def manual_edit_plan(
    plan_or_version_id: str,
    payload: PlanManualEditRequest,
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> PlanGenerateResponse:
    """Persist a teacher's hand-edit as a new chained draft version.

    Gated to a teacher who owns the lesson (research-manager bypasses). The whole
    edited plan is validated against ``SessionPlan``; a structural break returns
    422 with the field errors, not a 500.
    """
    owner_teacher_id = actor.teacher_id if actor.role == "teacher" else None
    try:
        return await service.manual_edit(
            plan_or_version_id=plan_or_version_id,
            edited_session_plan=payload.session_plan,
            owner_teacher_id=owner_teacher_id,
        )
    except PlanNotOwnedByTeacherError:
        raise HTTPException(
            status_code=403,
            detail="You can only edit a lesson plan for a class + subject you teach.",
        ) from None
    except PlanLookupNotFoundError:
        raise HTTPException(status_code=404, detail="plan_not_found") from None
    except PlanValidationError as error:
        raise HTTPException(status_code=422, detail=error.detail) from None


async def _own_lesson(
    actor: Actor, db: AsyncSession, service: LessonPlanApplicationService, session_id: str
) -> None:
    """Refuse a lesson that does not exist, or that a teacher does not teach."""
    try:
        lesson_period_id = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="session not found") from None
    if not await service.has_session(session_id):
        raise HTTPException(status_code=404, detail="session not found")
    if (
        actor.role == ROLE_TEACHER
        and actor.teacher_id is not None
        and not await teacher_owns_lesson_period(
            db, teacher_id=actor.teacher_id, lesson_period_id=lesson_period_id
        )
    ):
        raise HTTPException(status_code=403, detail="not_your_class")


@router.post("/generate", response_model=JobAccepted, status_code=202)
async def generate_plan(
    payload: PlanGenerateRequest,
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
    db: AsyncSession = Depends(get_db),
) -> JobAccepted:
    """Queue a lesson plan's draft and return the job to follow. An author only: it spends."""
    await _own_lesson(actor, db, service, payload.session_id)
    job_id = await JobQueue(db).ensure(
        GENERATE_LESSON_PLAN,
        payload.session_id,
        payload.teacher_id,
        subject=drafting_subject(payload.session_id),
        requested_by=actor.auth_id,
    )
    return JobAccepted(job_id=job_id)


async def _outline(db: AsyncSession, session_id: str) -> PlanOutline | None:
    written = await drafting_outline(db, session_id)
    if written is None:
        return None
    return PlanOutline(
        objectives=written.objectives,
        steps=[OutlineStep(title=s.title, minutes=s.minutes) for s in written.steps],
        written=written.written,
        total=written.total,
    )


@router.get("/drafting-progress", response_model=DraftingProgress)
async def drafting_progress(
    session_id: str,
    after: int = Query(0, ge=0),
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="read")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
    db: AsyncSession = Depends(get_db),
) -> DraftingProgress:
    """What the agent drafting the lesson's plan is doing, from the latest draft's start on."""
    await _own_lesson(actor, db, service, session_id)
    fresh = lines_after(await progress.after(db, drafting_channel(session_id), 0), after)
    return DraftingProgress(
        lines=[
            ProgressLine(id=event_id, kind=str(event.get("kind")), data=data_of(event))
            for event_id, event in fresh
        ],
        next=fresh[-1][0] if fresh else after,
        outline=await _outline(db, session_id),
    )


@router.get("", response_model=list[PlanVersionSummary])
async def list_lesson_plan_versions(
    subject: str | None = None,
    track: str | None = None,
    grade: str | None = None,
    term: str | None = None,
    week: int | None = None,
    session_id: str | None = None,
    teacher_id: str | None = None,
    latest_only: bool = False,
    limit: int = Query(50, ge=1, le=200),
    _actor: Actor = Depends(requires(obj="lesson_plan:*", act="read")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> list[PlanVersionSummary]:
    return await service.list_versions(
        subject=subject,
        track=track,
        grade=grade,
        term=term,
        week=week,
        session_id=session_id,
        teacher_id=teacher_id,
        latest_only=latest_only,
        limit=limit,
    )


@router.get("/for-my-class", response_model=list[PlanVersionSummary])
async def list_my_class_lesson_plans(
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="read_own_class")),
    db: AsyncSession = Depends(get_db),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> list[PlanVersionSummary]:
    """The lessons taught to the signed-in student's own class, and no other."""
    learner = (
        await LearnerRepository().get_learner_by_user_id(db, actor.teacher_id)
        if actor.teacher_id
        else None
    )
    if learner is None or learner.class_id is None:
        raise HTTPException(status_code=403, detail="no_student_class_bound_to_this_user")
    return await service.list_versions(
        class_id=learner.class_id,
        subject=None,
        track=None,
        grade=None,
        term=None,
        week=None,
        session_id=None,
        teacher_id=None,
        latest_only=False,
        limit=200,
    )


@router.get("/manual/context", response_model=ManualPlanContextResponse)
async def manual_plan_context(
    session_id: str,
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> ManualPlanContextResponse:
    """Lesson identity + curriculum objectives for the manual-entry form (FD-01)."""
    try:
        return await service.manual_context(session_id=session_id)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="session not found") from None


@router.post("/manual", response_model=PlanGenerateResponse)
async def create_manual_plan(
    payload: PlanManualCreateRequest,
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> PlanGenerateResponse:
    """Persist a teacher's hand-entered lesson plan as a new draft version (FD-01).

    Gated to a teacher (or research-manager). Lesson identity and the curriculum
    objectives are forced from the lesson's session context; the submitted plan
    content is validated against ``SessionPlan`` and every lesson objective must
    map to a curriculum objective of the lesson, else 422.
    """
    teacher_id = payload.teacher_id or (str(actor.teacher_id) if actor.teacher_id else None)
    # A teacher may only author a plan for a lesson they own; a research-manager
    # bypasses the check (it does the field data entry for any teacher's lesson).
    owner_teacher_id = actor.teacher_id if actor.role == "teacher" else None
    try:
        return await service.create_manual(
            session_id=payload.session_id,
            session_plan_content=payload.session_plan,
            teacher_id=teacher_id,
            owner_teacher_id=owner_teacher_id,
        )
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="session not found") from None
    except PlanNotOwnedByTeacherError:
        raise HTTPException(
            status_code=403,
            detail="You can only author a lesson plan for a class + subject you teach.",
        ) from None
    except PlanValidationError as error:
        raise HTTPException(status_code=422, detail=error.detail) from None


@router.post("/reuse", response_model=PlanReuseResponse)
async def reuse_lesson_plan(
    payload: PlanReuseRequest,
    actor: Actor = Depends(requires(obj="lesson_plan:*", act="author_plan")),
    db: AsyncSession = Depends(get_db),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> PlanReuseResponse:
    """Use an existing plan as this lesson's plan: it is saved as a draft to review and accept."""
    try:
        reused = await reuse_plan_for_lesson(
            db,
            service,
            actor,
            session_id=payload.session_id,
            source_plan_version_id=payload.source_plan_version_id,
            session_plan=payload.session_plan,
            curriculum_choices=payload.curriculum_choices,
        )
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="session not found") from None
    except PlanLookupNotFoundError:
        raise HTTPException(status_code=404, detail="source_plan_not_found") from None
    except PlanNotOwnedByTeacherError:
        raise HTTPException(status_code=403, detail="not_your_lesson") from None
    except PlanValidationError as error:
        raise HTTPException(status_code=422, detail=error.detail) from None
    if reused.plan is None:
        return PlanReuseResponse(
            status="needs_curriculum_choice", unmapped=reused.unmapped, choices=reused.choices
        )
    return PlanReuseResponse(
        status="reused", plan=PlanGenerateResponse.model_validate(reused.plan, from_attributes=True)
    )


@router.get("/{plan_id}", response_model=PlanGenerateResponse)
async def get_lesson_plan(
    plan_id: str,
    _actor: Actor = Depends(requires(obj="lesson_plan:*", act="read")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> PlanGenerateResponse:
    try:
        return await service.get_plan(plan_id=plan_id)
    except PlanLookupNotFoundError:
        raise HTTPException(status_code=404, detail="plan not found") from None


@router.get("/{plan_id}/lesson-plan.pdf")
async def download_lesson_plan_pdf(
    plan_id: str,
    _actor: Actor = Depends(requires(obj="lesson_plan:*", act="read")),
    service: LessonPlanApplicationService = Depends(get_lesson_plan_application_service),
) -> Response:
    """Render the lesson plan to PDF (WeasyPrint), matching the pack/audit exports."""
    from app.domains.evaluation.application.worksheet_html.lesson_plan_renderer import (
        render_lesson_plan_pdf,
    )

    try:
        plan = await service.get_plan(plan_id=plan_id)
    except PlanLookupNotFoundError:
        raise HTTPException(status_code=404, detail="plan not found") from None
    session_plan = plan.session_plan.model_dump(mode="json")
    label = session_plan.get("subtopic") or session_plan.get("topic") or "lesson-plan"
    pdf_bytes = render_lesson_plan_pdf(session_plan, plan_label=f"v{plan_id}")
    slug = re.sub(r"[^a-z0-9]+", "-", str(label).lower()).strip("-") or "lesson-plan"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{slug}-lesson-plan.pdf"'},
    )
