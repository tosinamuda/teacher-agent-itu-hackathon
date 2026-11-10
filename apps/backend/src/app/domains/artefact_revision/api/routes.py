"""Artefact-revision chat routes: threads + turns."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.artefact_revision.api.schemas import (
    CreateThreadRequest,
    RevisionHighlight,
    RevisionThreadResponse,
    RevisionTurnResponse,
    SubmitTurnRequest,
    SubmitTurnResponse,
)
from app.domains.artefact_revision.application import (
    ArtefactRevisionError,
    ArtefactRevisionService,
)
from app.domains.artefact_revision.infrastructure.wiring import (
    build_artefact_revision_service,
)
from app.shared.auth import Actor
from app.shared.authz import requires

# Revising an artefact (lesson plan / class revision note / diagnostic) is a teacher or
# researcher action; the chat triggers LLM generation, so it must not be open to
# anonymous callers. Granted to teacher + researcher in the Casbin policy seed.
_requires_revise = requires(obj="artefact_revision:*", act="revise")

if TYPE_CHECKING:
    # Type-annotation-only — see ``api ↛ models`` rule.
    from app.domains.artefact_revision.models.revision import RevisionTurn

router = APIRouter(prefix="/artefact-revisions", tags=["artefact-revisions"])


def _turn_response(turn: RevisionTurn) -> RevisionTurnResponse:
    return RevisionTurnResponse(
        revision_turn_id=turn.revision_turn_id,
        turn_number=turn.turn_number,
        instruction=turn.instruction,
        highlight=RevisionHighlight(**turn.highlight) if turn.highlight else None,
        base_version_id=turn.base_version_id,
        result_version_id=turn.result_version_id,
        summary=turn.summary,
        validation_passed=turn.validation_passed,
        created_at=turn.created_at,
    )


@router.post("/threads", response_model=RevisionThreadResponse)
async def create_thread(
    payload: CreateThreadRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(_requires_revise),
) -> RevisionThreadResponse:
    """Get or create the revision thread for an artefact, with the current artefact seed."""
    service = build_artefact_revision_service()
    try:
        await service.get_or_create_thread(
            db=db,
            artefact_type=payload.artefact_type,
            subject_id=payload.subject_id,
            created_by=None,
        )
        view = await _view_for_subject(service, db, payload.artefact_type, payload.subject_id)
    except ArtefactRevisionError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return view


@router.get("/threads/{thread_id}", response_model=RevisionThreadResponse)
async def get_thread(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(_requires_revise),
) -> RevisionThreadResponse:
    """Fetch a thread: its turns + the current artefact (chat seed)."""
    service = build_artefact_revision_service()
    try:
        view = await service.get_thread_view(db=db, thread_id=thread_id)
    except ArtefactRevisionError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return RevisionThreadResponse(
        revision_thread_id=view.thread.revision_thread_id,
        artefact_type=view.thread.artefact_type,
        subject_id=view.thread.subject_id,
        current_version_id=view.current_version_id,
        current_session_plan=view.current_session_plan,
        turns=[_turn_response(turn) for turn in view.turns],
    )


@router.post("/threads/{thread_id}/turns", response_model=SubmitTurnResponse)
async def submit_turn(
    thread_id: str,
    payload: SubmitTurnRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(_requires_revise),
) -> SubmitTurnResponse:
    """Submit a teacher instruction (+ optional highlight); returns the revised artefact."""
    service = build_artefact_revision_service()
    try:
        turn, outcome = await service.submit_turn(
            db=db,
            thread_id=thread_id,
            instruction=payload.instruction,
            highlight=payload.highlight.model_dump() if payload.highlight else None,
        )
    except ArtefactRevisionError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return SubmitTurnResponse(
        turn=_turn_response(turn),
        result_version_id=outcome.result_version_id,
        session_plan=outcome.session_plan,
        validation_passed=outcome.validation_passed,
    )


async def _view_for_subject(
    service: ArtefactRevisionService,
    db: AsyncSession,
    artefact_type: str,
    subject_id: str,
) -> RevisionThreadResponse:
    thread = await service.get_or_create_thread(
        db=db, artefact_type=artefact_type, subject_id=subject_id, created_by=None
    )
    view = await service.get_thread_view(db=db, thread_id=thread.revision_thread_id)
    return RevisionThreadResponse(
        revision_thread_id=view.thread.revision_thread_id,
        artefact_type=view.thread.artefact_type,
        subject_id=view.thread.subject_id,
        current_version_id=view.current_version_id,
        current_session_plan=view.current_session_plan,
        turns=[_turn_response(turn) for turn in view.turns],
    )
