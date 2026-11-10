from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefacts.core.api.schemas import (
    ApprovePackRequest,
    ArtefactExportResponse,
    ArtefactResponse,
    MissingPackStudentResponse,
    RegenerateStudentPackRequest,
    RegenerateStudentPackResponse,
    ReviewPackStatusResponse,
    StudentPackGenerationStatusResponse,
)
from app.domains.artefacts.core.application.build_jobs import (
    ArtefactLifecycleError,
)
from app.domains.artefacts.core.application.service import ArtefactApplicationError
from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)

if TYPE_CHECKING:
    # Type-annotation-only — see ``api ↛ models`` rule.
    from app.domains.artefacts.core.infrastructure.models import Artefact
# Read-only ownership query — lives with the lesson-plan models (PlanVersion /
# LessonPlan) it joins; a sibling artefact type reusing it beats duplicating the
# join. Gates the teacher pack-review gate to the class the teacher actually owns.
from app.domains.artefacts.core.infrastructure.wiring import build_lifecycle_manager
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owned_plan_version_ids,
    teacher_owns_plan_version,
)
from app.domains.artefacts.types.post_class_review_pack.api.pack_access import (
    require_class,
    require_readable,
    require_teaching_role,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_names import (
    learner_names,
)
from app.domains.artefacts.types.post_class_review_pack.domain.reading import for_reading
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_review_pack_workflow,
    build_student_pack_service,
)
from app.domains.learners.application.identity import student_id_of
from app.shared.auth import ROLE_STUDENT, ROLE_TEACHER, Actor
from app.shared.authz import requires

router = APIRouter(prefix="/artefacts/post-class-review-packs", tags=["post-class-review-packs"])


def _raise_http_error(error: Exception) -> NoReturn:
    status_code = getattr(error, "status_code", None)
    if isinstance(status_code, int):
        raise HTTPException(
            status_code=status_code,
            detail=getattr(error, "detail", None),
        ) from error
    raise error


async def _assert_owns_plan(actor: Actor, db: AsyncSession, plan_version_id: str) -> None:
    """A teacher may only review/approve packs for a class + subject they teach.

    Mirrors the lesson-plan approval gate: a research-manager bypasses the check;
    a teacher is held to their own workspace (the plan's class + subject + term).
    """
    if (
        actor.role == ROLE_TEACHER
        and actor.teacher_id is not None
        and not await teacher_owns_plan_version(
            db, teacher_id=actor.teacher_id, plan_version_id=plan_version_id
        )
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only review packs for a class + subject you teach.",
        )


def _artefact_response(artefact: Artefact, learner_name: str | None = None) -> ArtefactResponse:
    return ArtefactResponse(
        artefact_id=artefact.artefact_id,
        artefact_type=ArtefactType(artefact.artefact_type),
        scope=ArtefactScope(artefact.scope),
        plan_version_id=artefact.plan_version_id,
        artefact_plan_id=artefact.source_artefact_plan_id,
        learner_id=artefact.student_id,
        learner_name=learner_name,
        manifest=for_reading(artefact.manifest),
        artefact_refs=artefact.artefact_refs,
        review_status=artefact.review_status,
        reviewed_at=artefact.reviewed_at,
        created_at=artefact.created_at,
        version=artefact.version,
    )


@router.get("/pending", response_model=list[ArtefactResponse])
async def list_pending_review_packs(
    plan_version_id: str | None = None,
    limit: int = 100,
    status: Literal["pending", "approved"] = "pending",
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ArtefactResponse]:
    """Teacher review queue: per-student packs awaiting approval, or approved already.

    Optionally scoped to one lesson.

    Scoped to the teacher's own classes — a teacher only sees packs for a class +
    subject they teach; a research-manager sees every pending pack.
    """
    owned_plan_version_ids = None
    if actor.role == ROLE_TEACHER and actor.teacher_id is not None:
        owned_plan_version_ids = await teacher_owned_plan_version_ids(
            db, teacher_id=actor.teacher_id
        )
    manager = build_lifecycle_manager()
    artefacts = await manager.list_pending_learner_packs(
        db=db,
        plan_version_id=plan_version_id,
        limit=limit,
        owned_plan_version_ids=owned_plan_version_ids,
        review_status=ArtefactReviewStatus(status),
    )
    return await _named_responses(db, artefacts)


async def _named_responses(db: AsyncSession, artefacts: list[Artefact]) -> list[ArtefactResponse]:
    names = await learner_names(db, [a.student_id for a in artefacts if a.student_id])
    return [
        _artefact_response(artefact, names.get(artefact.student_id or "")) for artefact in artefacts
    ]


@router.get("/missing", response_model=list[MissingPackStudentResponse])
async def list_students_missing_pack(
    plan_version_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[MissingPackStudentResponse]:
    """Students who submitted this lesson's exit assessment but have no pack yet.

    (generation pending or failed) — the teacher's per-student regenerate queue.
    """
    await require_class(actor, db, plan_version_id)
    rows = await build_student_pack_service().list_students_missing_pack(
        db=db, plan_version_id=plan_version_id
    )
    return [
        MissingPackStudentResponse(student_id=row["student_id"], full_name=row["full_name"])
        for row in rows
    ]


@router.post("/regenerate", response_model=RegenerateStudentPackResponse)
async def regenerate_student_pack(
    payload: RegenerateStudentPackRequest,
    actor: Actor = Depends(requires(obj="pack:*", act="regenerate")),
    db: AsyncSession = Depends(get_db),
) -> RegenerateStudentPackResponse:
    """(Re)generate a student's pack via the SAME spec worker that runs on submit.

    With a student_id, regenerates that one; without, regenerates every student that
    submitted but has no pack. Each enqueued pack lands as ``pending`` for review.
    """
    await _assert_owns_plan(actor, db, payload.plan_version_id)
    queued = await build_review_pack_workflow().regenerate_packs(
        db=db,
        plan_version_id=payload.plan_version_id,
        student_id=payload.student_id,
    )
    return RegenerateStudentPackResponse(
        plan_version_id=payload.plan_version_id, queued_student_ids=queued
    )


@router.get("/statuses", response_model=list[ReviewPackStatusResponse])
async def list_review_pack_statuses(
    learner_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ReviewPackStatusResponse]:
    """List a learner's pack statuses (all states) without manifest content.

    Lets the student be shown 'awaiting review' vs 'ready' without seeing an
    unapproved pack.
    """
    if actor.role == ROLE_STUDENT:
        if learner_id != await student_id_of(actor, db):
            raise HTTPException(status_code=403, detail="You can only see your own notes.")
    else:
        await require_teaching_role(actor)
    manager = build_lifecycle_manager()
    artefacts = await manager.list_learner_artefacts(
        db=db,
        learner_id=learner_id,
        plan_version_id=None,
        limit=200,
        review_status=None,
    )
    return [
        ReviewPackStatusResponse(
            plan_version_id=artefact.plan_version_id,
            review_status=artefact.review_status,
        )
        for artefact in artefacts
    ]


@router.get("/generation-statuses", response_model=list[StudentPackGenerationStatusResponse])
async def list_generation_statuses(
    plan_version_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[StudentPackGenerationStatusResponse]:
    """The teacher's generation queue: each student's current attempt for this lesson.

    Shows queued / running / succeeded / failed per student (the async-generation
    lifecycle), so the teacher sees "generating…" / "failed → retry" rather than only
    the binary has-pack / no-pack of the ``/missing`` list. Scoped to the teacher's
    own classes.
    """
    await _assert_owns_plan(actor, db, plan_version_id)
    rows = await build_review_pack_workflow().generation_statuses(
        db=db, plan_version_id=plan_version_id
    )
    return [
        StudentPackGenerationStatusResponse(
            student_id=job.student_id,
            full_name=full_name,
            status=job.status.value if hasattr(job.status, "value") else str(job.status),
            attempt_number=job.attempt_number,
            error_category=job.error_category,
            produced_artefact_id=job.produced_artefact_id,
            updated_at=job.updated_at,
        )
        for job, full_name in rows
    ]


@router.get("/{artefact_id}", response_model=ArtefactResponse)
async def get_review_pack(
    artefact_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> ArtefactResponse:
    manager = build_lifecycle_manager()
    try:
        artefact = await manager.get_artefact(db=db, artefact_id=artefact_id)
    except ArtefactLifecycleError as error:
        _raise_http_error(error)
    await require_readable(actor, db, artefact)
    return (await _named_responses(db, [artefact]))[0]


@router.post("/{artefact_id}/approve", response_model=ArtefactResponse)
async def approve_review_pack(
    artefact_id: str,
    payload: ApprovePackRequest | None = None,
    actor: Actor = Depends(requires(obj="pack:*", act="approve")),
    db: AsyncSession = Depends(get_db),
) -> ArtefactResponse:
    """Approve a pending pack — the teacher gate (HITL) that lets the student see it.

    Gated to a signed-in teacher or research-manager; a teacher may only approve a
    pack for a class they teach. The approver is recorded from the authenticated
    actor, never a client-supplied string. If ``expected_version`` is supplied and the
    pack has since been revised (or re-approved), the approval is rejected with 409 so
    the teacher re-reviews the current content rather than blessing a manifest they
    never saw.
    """
    manager = build_lifecycle_manager()
    try:
        artefact = await manager.get_artefact(db=db, artefact_id=artefact_id)
    except ArtefactLifecycleError as error:
        _raise_http_error(error)
    await _assert_owns_plan(actor, db, artefact.plan_version_id)
    try:
        artefact = await manager.approve_artefact(
            db=db,
            artefact_id=artefact_id,
            reviewed_by=actor.display_name,
            expected_version=payload.expected_version if payload else None,
        )
    except (ArtefactLifecycleError, ArtefactApplicationError) as error:
        _raise_http_error(error)
    return (await _named_responses(db, [artefact]))[0]


@router.get("", response_model=list[ArtefactResponse])
async def list_review_packs(
    learner_id: str | None = None,
    plan_version_id: str | None = None,
    review_status: str | None = None,
    limit: int = 50,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ArtefactResponse]:
    """List packs through the learner-facing visibility default (approved-only.

    for learner queries; pass ``review_status="all"`` to opt out). The teacher
    review queue uses ``GET /pending``, not this route.

    A learner lists only their own approved notes; anyone else names the lesson they teach.
    """
    if actor.role == ROLE_STUDENT:
        learner_id, review_status = await student_id_of(actor, db), None
    else:
        await require_class(actor, db, plan_version_id)
    artefacts = await build_review_pack_workflow().list_learner_packs(
        db=db,
        learner_id=learner_id,
        plan_version_id=plan_version_id,
        review_status=review_status,
        limit=limit,
    )
    return [_artefact_response(artefact) for artefact in artefacts]


@router.post("/{artefact_id}/export", response_model=ArtefactExportResponse)
async def export_review_pack(
    artefact_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> ArtefactExportResponse:
    manager = build_lifecycle_manager()
    try:
        await require_readable(
            actor,
            db,
            await manager.get_artefact(db=db, artefact_id=artefact_id),
            learner_may=False,
        )
        artefact = await manager.export_artefact(db=db, artefact_id=artefact_id)
    except (ArtefactLifecycleError, ArtefactApplicationError) as error:
        _raise_http_error(error)
    return ArtefactExportResponse(
        artefact_id=artefact.artefact_id,
        artefact_refs=artefact.artefact_refs or {},
    )


@router.get("/{artefact_id}/pack.pdf")
async def download_review_pack_pdf(
    artefact_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """Render the pack to PDF (WeasyPrint), matching the lesson-plan/audit exports."""
    import re as _re

    from app.domains.evaluation.application.worksheet_html.pack_renderer import render_pack_pdf

    manager = build_lifecycle_manager()
    try:
        artefact = await manager.get_artefact(db=db, artefact_id=artefact_id)
    except ArtefactLifecycleError as error:
        _raise_http_error(error)
    await require_readable(actor, db, artefact)
    manifest = artefact.manifest if isinstance(artefact.manifest, dict) else {}
    label = manifest.get("subtopic") or manifest.get("title") or artefact_id
    pdf_bytes = render_pack_pdf(manifest, pack_label=artefact_id)
    slug = _re.sub(r"[^a-z0-9]+", "-", str(label).lower()).strip("-") or "review-pack"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{slug}-pack.pdf"'},
    )


@router.get("/{artefact_id}/download")
async def download_review_pack(
    artefact_id: str,
    actor: Actor = Depends(requires(obj="pack:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    manager = build_lifecycle_manager()
    try:
        await require_readable(
            actor,
            db,
            await manager.get_artefact(db=db, artefact_id=artefact_id),
            learner_may=False,
        )
        artefact, manifest_path = await manager.resolve_download_manifest_path(
            db=db,
            artefact_id=artefact_id,
        )
    except (ArtefactLifecycleError, ArtefactApplicationError) as error:
        _raise_http_error(error)
    return FileResponse(
        manifest_path,
        media_type="application/json",
        filename=f"{artefact.artefact_id}.json",
    )
