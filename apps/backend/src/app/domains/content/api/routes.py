"""Content types and their specs; content, its revisions and its approvals."""

from __future__ import annotations

import logging
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefact_revision.api.schemas import RevisionHighlight
from app.domains.artefact_revision.application.service import RevisionRecord
from app.domains.artefacts.core.application.ports import Approval
from app.domains.artefacts.types.lesson_plan.application.ownership import (
    teacher_owned_plan_version_ids,
    teacher_owns_plan_version,
)
from app.domains.content.api.schemas import (
    ApprovalRequest,
    ApprovalResponse,
    ContentResponse,
    ContentSummary,
    ContentTypeResponse,
    DefaultGeneratorRequest,
    GenerateContentRequest,
    GenerationProgress,
    GenerationProgressLine,
    RegisterTypeRequest,
    RejectionRequest,
    RevisionRequest,
    RevisionResponse,
    SpecBody,
    SpecResponse,
)
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.application.records import ContentItem, ContentRecord
from app.domains.content.domain.types import Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.content_file import offers_file
from app.domains.content.infrastructure.teacher_preferences import TeacherPreferences
from app.domains.content.infrastructure.wiring import build_content_service, build_note_reuse
from app.domains.content.jobs import generation_subject
from app.domains.content.progress import generation_channel
from app.domains.content_engine.infrastructure.progress_lines import data_of, lines_after
from app.domains.jobs.api.schemas import JobAccepted
from app.domains.teaching.application.study_results_service import StudyResultsService
from app.infra import progress
from app.infra.jobs.kinds import GENERATE_CONTENT
from app.infra.jobs.queue import JobQueue
from app.shared.auth import ROLE_TEACHER, Actor
from app.shared.authz import requires
from app.shared.schema_base import StrictRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/content", tags=["content"])


def _raise(error: ContentError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail) from error


async def _assert_owns(actor: Actor, db: AsyncSession, plan_version_id: str) -> None:
    """A teacher works only on plan versions of a class and subject they teach."""
    if (
        actor.role == ROLE_TEACHER
        and actor.teacher_id is not None
        and not await teacher_owns_plan_version(
            db, teacher_id=actor.teacher_id, plan_version_id=plan_version_id
        )
    ):
        raise HTTPException(status_code=403, detail="not_your_class")


def _summary(record: ContentRecord) -> ContentSummary:
    return ContentSummary(
        id=record.content_id,
        type=record.type,
        level=record.level,
        plan_version_id=record.plan_version_id,
        student_id=record.student_id,
        version=record.version,
        review_status=record.review_status,
        created_at=record.created_at,
        provenance=record.provenance,
        read_only=record.read_only,
        review_reason=record.review_reason,
    )


async def _item(db: AsyncSession, item: ContentItem) -> ContentResponse:
    return ContentResponse(
        **_summary(item.record).model_dump(),
        content=item.content,
        review=item.record.review,
        has_file=await offers_file(build_content_catalogue(), db, item.record),
    )


def _revision(record: RevisionRecord) -> RevisionResponse:
    return RevisionResponse(
        turn_number=record.turn_number,
        feedback=record.instruction,
        summary=record.summary,
        created_at=record.created_at,
        highlight=(
            RevisionHighlight.model_validate(record.highlight) if record.highlight else None
        ),
    )


def _approval(approval: Approval) -> ApprovalResponse:
    return ApprovalResponse(
        id=approval.approval_id,
        approved_version=approval.approved_version,
        approved_by=approval.approved_by,
        approved_at=approval.approved_at,
    )


# Types are declared before /{content_id}, so "types" is never read as a content ID.


@router.get("/types", response_model=list[ContentTypeResponse])
async def list_content_types(
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ContentTypeResponse]:
    """Every content type with its current spec, but those this teacher has switched off."""
    catalogue = build_content_catalogue()
    hidden = await TeacherPreferences().hidden(db, actor.auth_id)
    return [
        ContentTypeResponse.of(
            definition,
            spec,
            retired=await catalogue.retired(db, definition.slug),
            generators=await catalogue.generators_of(db, definition),
        )
        for definition, spec in await catalogue.types(db)
        if definition.slug not in hidden
    ]


@router.post("/types", response_model=ContentTypeResponse, status_code=201)
async def register_content_type(
    body: RegisterTypeRequest,
    actor: Actor = Depends(requires(obj="content_type:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> ContentTypeResponse:
    """Register a type the content engine builds. It can be generated as soon as it exists."""
    try:
        definition, spec = await build_content_catalogue().register(
            db,
            slug=body.type,
            label=body.label,
            audience=body.audience,
            made_from_a_plan_version=body.made_from_a_plan_version,
            spec_fields=body.spec.as_fields(),
            created_by=actor.display_name,
        )
    except ContentError as error:
        _raise(error)
    return ContentTypeResponse.of(definition, spec)


@router.get("/types/{type}", response_model=ContentTypeResponse)
async def get_content_type(
    type: str,
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> ContentTypeResponse:
    catalogue = build_content_catalogue()
    try:
        definition, spec = await catalogue.type(db, type), await catalogue.current(db, type)
    except ContentError as error:
        _raise(error)
    return ContentTypeResponse.of(
        definition, spec, generators=await catalogue.generators_of(db, definition)
    )


@router.put("/types/{type}/default-generator", response_model=ContentTypeResponse)
async def set_default_generator(
    type: str,
    body: DefaultGeneratorRequest,
    actor: Actor = Depends(requires(obj="content_type:*", act="set_default")),
    db: AsyncSession = Depends(get_db),
) -> ContentTypeResponse:
    """Make a generator the one new content of the type is made with.

    Content already made keeps the generator it records. A native pipeline is never switched.
    """
    catalogue = build_content_catalogue()
    try:
        binding = await catalogue.make_default(
            db, type, body.level, body.generator, actor.display_name
        )
        definition, spec = await catalogue.type(db, type), await catalogue.current(db, type)
    except ContentError as error:
        _raise(error)
    await db.commit()
    logger.info(
        "default generator of %s at %s is now %s (by %s)",
        type,
        body.level.value,
        binding.ref,
        actor.display_name,
    )
    return ContentTypeResponse.of(
        definition, spec, generators=await catalogue.generators_of(db, definition)
    )


@router.get("/types/{type}/specs", response_model=list[SpecResponse])
async def list_specs(
    type: str,
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[SpecResponse]:
    """Every revision of the type's spec, oldest first."""
    try:
        history = await build_content_catalogue().history(db, type)
    except ContentError as error:
        _raise(error)
    return [SpecResponse.of(spec) for spec in history]


@router.post("/types/{type}/specs", response_model=SpecResponse, status_code=201)
async def add_spec(
    type: str,
    body: SpecBody,
    actor: Actor = Depends(requires(obj="content_type:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> SpecResponse:
    """Add the type's next spec revision. Content already made keeps the revision it used."""
    try:
        spec = await build_content_catalogue().add(db, type, body.as_fields(), actor.display_name)
    except ContentError as error:
        _raise(error)
    return SpecResponse.of(spec)


@router.get("/types/{type}/specs/{revision}", response_model=SpecResponse)
async def get_spec(
    type: str,
    revision: int,
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> SpecResponse:
    try:
        spec = await build_content_catalogue().revision(db, type, revision)
    except ContentError as error:
        _raise(error)
    return SpecResponse.of(spec)


@router.post("", response_model=JobAccepted, status_code=202)
async def generate_content(
    body: GenerateContentRequest,
    actor: Actor = Depends(requires(obj="content:*", act="create")),
    db: AsyncSession = Depends(get_db),
) -> JobAccepted:
    """Queue the content's generation from a frozen plan version; follow the job it returns.

    What generation would refuse outright is refused here, at once. The content, when made,
    stays pending until approved.
    """
    await _assert_owns(actor, db, body.plan_version_id)
    preferences = TeacherPreferences()
    if body.type in await preferences.hidden(db, actor.auth_id):
        raise HTTPException(status_code=409, detail="material_is_switched_off")
    choices = GenerationChoices(
        pipeline=body.pipeline,
        sources=body.sources.value if body.sources else None,
        instructions=body.instructions,
    )
    try:
        await build_content_service().check_generation(
            db,
            plan_version_id=body.plan_version_id,
            type=body.type,
            level=body.level,
            choices=choices,
        )
    except ContentError as error:
        _raise(error)
    job_id = await JobQueue(db).ensure(
        GENERATE_CONTENT,
        body.plan_version_id,
        body.type,
        body.level.value,
        choices.pipeline,
        choices.sources,
        choices.instructions,
        subject=generation_subject(body.plan_version_id, body.type, body.level),
        requested_by=actor.auth_id,
    )
    return JobAccepted(job_id=job_id)


class ReuseNoteRequest(StrictRequest):
    #: The lesson note to copy.
    source_content_id: str = Field(..., min_length=1)
    #: The plan version to copy it onto.
    plan_version_id: str = Field(..., min_length=1)


class ReusedNote(BaseModel):
    content_id: str


async def _assert_can_copy_note_from(actor: Actor, db: AsyncSession, content_id: str) -> None:
    """A note is copied from a class the teacher teaches or from an evaluation lesson."""
    try:
        record = await build_content_service().record(db, content_id)
    except ContentError as error:
        _raise(error)
    if await StudyResultsService().is_evaluation_lesson(db, record.plan_version_id):
        return
    await _assert_owns(actor, db, record.plan_version_id)


@router.post("/reuse-note", response_model=ReusedNote, status_code=201)
async def reuse_lesson_note(
    body: ReuseNoteRequest,
    actor: Actor = Depends(requires(obj="content:*", act="create")),
    db: AsyncSession = Depends(get_db),
) -> ReusedNote:
    """Copy a lesson note onto a plan with the same steps. It waits for the teacher's review."""
    await _assert_owns(actor, db, body.plan_version_id)
    await _assert_can_copy_note_from(actor, db, body.source_content_id)
    try:
        content_id = await build_note_reuse()(
            db, source_id=body.source_content_id, plan_version_id=body.plan_version_id
        )
    except ContentError as error:
        _raise(error)
    return ReusedNote(content_id=content_id)


@router.get("/generation-progress", response_model=GenerationProgress)
async def generation_progress(
    plan_version_id: str,
    type: str,
    after: int = Query(0, ge=0),
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> GenerationProgress:
    """What the agent making this content is doing, from the latest run's start on."""
    await _assert_owns(actor, db, plan_version_id)
    channel = generation_channel(plan_version_id, type)
    fresh = lines_after(await progress.after(db, channel, 0), after)
    return GenerationProgress(
        lines=[
            GenerationProgressLine(id=event_id, kind=str(event.get("kind")), data=data_of(event))
            for event_id, event in fresh
        ],
        next=fresh[-1][0] if fresh else after,
    )


@router.get("", response_model=list[ContentSummary])
async def find_content(
    plan_version_id: str | None = None,
    type: str | None = None,
    level: Level | None = None,
    student_id: str | None = None,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ContentSummary]:
    """Content matching every filter given, newest first. A teacher sees only their classes'."""
    if plan_version_id is not None:
        await _assert_owns(actor, db, plan_version_id)
    records = await build_content_service().find(
        db, plan_version_id=plan_version_id, type=type, level=level, student_id=student_id
    )
    if actor.role == ROLE_TEACHER and actor.teacher_id is not None and plan_version_id is None:
        owned = set(await teacher_owned_plan_version_ids(db, teacher_id=actor.teacher_id))
        records = [record for record in records if record.plan_version_id in owned]
    return [_summary(record) for record in records]


async def owned_record(actor: Actor, db: AsyncSession, content_id: str) -> ContentRecord:
    try:
        record = await build_content_service().record(db, content_id)
    except ContentError as error:
        _raise(error)
    await _assert_owns(actor, db, record.plan_version_id)
    return record


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: str,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> ContentResponse:
    await owned_record(actor, db, content_id)
    return await _item(db, await build_content_service().get(db, content_id))


@router.post("/{content_id}/revisions", response_model=RevisionResponse, status_code=201)
async def revise_content(
    content_id: str,
    body: RevisionRequest,
    actor: Actor = Depends(requires(obj="artefact_revision:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> RevisionResponse:
    """Revise it with the teacher's feedback. It goes back to pending review."""
    await owned_record(actor, db, content_id)
    try:
        revision = await build_content_service().revise(
            db,
            content_id=content_id,
            feedback=body.feedback,
            requested_by=actor.display_name,
            highlight=body.highlight.model_dump(exclude_none=True) if body.highlight else None,
        )
    except ContentError as error:
        _raise(error)
    return _revision(revision)


@router.get("/{content_id}/revisions", response_model=list[RevisionResponse])
async def list_revisions(
    content_id: str,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[RevisionResponse]:
    await owned_record(actor, db, content_id)
    return [_revision(r) for r in await build_content_service().revisions(db, content_id)]


@router.post("/{content_id}/approvals", response_model=ContentResponse, status_code=201)
async def approve_content(
    content_id: str,
    body: ApprovalRequest,
    actor: Actor = Depends(requires(obj="content:*", act="approve")),
    db: AsyncSession = Depends(get_db),
) -> ContentResponse:
    """Approve the version the teacher reviewed. A class test is then sent to its students."""
    await owned_record(actor, db, content_id)
    try:
        item = await build_content_service().approve(
            db,
            content_id=content_id,
            expected_version=body.expected_version,
            approved_by=actor.display_name,
        )
    except ContentError as error:
        _raise(error)
    return await _item(db, item)


@router.post("/{content_id}/rejections", response_model=ContentResponse, status_code=201)
async def reject_content(
    content_id: str,
    body: RejectionRequest,
    actor: Actor = Depends(requires(obj="content:*", act="reject")),
    db: AsyncSession = Depends(get_db),
) -> ContentResponse:
    """Reject the pending version the teacher reviewed, or withdraw an approved one."""
    await owned_record(actor, db, content_id)
    try:
        item = await build_content_service().reject(
            db,
            content_id=content_id,
            expected_version=body.expected_version,
            rejected_by=actor.display_name,
            reason=body.reason,
        )
    except ContentError as error:
        _raise(error)
    return await _item(db, item)


@router.get("/{content_id}/approvals", response_model=list[ApprovalResponse])
async def list_approvals(
    content_id: str,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[ApprovalResponse]:
    await owned_record(actor, db, content_id)
    return [_approval(a) for a in await build_content_service().approvals(db, content_id)]
