"""Upload + download provenance images (auth-gated; never world-readable)."""

from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.attachments.application.service import AttachmentError, AttachmentService
from app.shared.auth import Actor, require_teacher_or_manager

router = APIRouter(prefix="/attachments", tags=["attachments"])


def _raise(error: AttachmentError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


class AttachmentResponse(BaseModel):
    attachment_id: str
    url: str
    content_type: str


@router.post("", response_model=AttachmentResponse)
async def upload_attachment(
    file: UploadFile = File(...),
    kind: str = Form("attachment"),
    caption: str | None = Form(None),
    actor: Actor = Depends(require_teacher_or_manager),
    db: AsyncSession = Depends(get_db),
) -> AttachmentResponse:
    """Upload a provenance image (a photo of the original); returns its opaque id + URL."""
    service = AttachmentService()
    try:
        attachment = await service.save(
            db,
            data=await file.read(),
            content_type=file.content_type or "application/octet-stream",
            kind=kind,
            uploaded_by=actor.display_name,
            caption=caption,
        )
    except AttachmentError as error:
        _raise(error)
    return AttachmentResponse(
        attachment_id=str(attachment.id),
        url=f"/attachments/{attachment.id}",
        content_type=attachment.content_type,
    )


@router.get("/{attachment_id}")
async def download_attachment(
    attachment_id: str,
    _actor: Actor = Depends(require_teacher_or_manager),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """Stream an uploaded image to an authenticated teacher/researcher."""
    service = AttachmentService()
    attachment = await service.get(db, attachment_id)
    if attachment is None:
        raise HTTPException(status_code=404, detail="attachment_not_found")
    path = service.absolute_path(attachment)
    if not path.exists():
        raise HTTPException(status_code=404, detail="attachment_file_missing")
    return FileResponse(path, media_type=attachment.content_type)
