"""Store + fetch uploaded provenance images."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.attachments.config import get_uploads_dir
from app.domains.attachments.models import Attachment

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB — comfortably under nginx's 25m cap.


@dataclass(frozen=True)
class AttachmentError(Exception):
    status_code: int
    detail: str


class AttachmentService:
    async def save(
        self,
        db: AsyncSession,
        *,
        data: bytes,
        content_type: str,
        kind: str,
        uploaded_by: str | None,
        caption: str | None = None,
    ) -> Attachment:
        """Validate, write the bytes to disk, and record the opaque handle row."""
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise AttachmentError(415, "unsupported_image_type")
        if not data:
            raise AttachmentError(422, "empty_upload")
        if len(data) > MAX_BYTES:
            raise AttachmentError(413, "image_too_large")

        attachment_id = uuid.uuid4()
        stored_path = f"{attachment_id.hex[:2]}/{attachment_id.hex}"
        absolute = get_uploads_dir() / stored_path
        absolute.parent.mkdir(parents=True, exist_ok=True)
        absolute.write_bytes(data)

        attachment = Attachment(
            id=attachment_id,
            kind=kind,
            content_type=content_type,
            byte_size=len(data),
            sha256=hashlib.sha256(data).hexdigest(),
            stored_path=stored_path,
            caption=caption,
            uploaded_by=uploaded_by,
        )
        db.add(attachment)
        await db.commit()
        await db.refresh(attachment)
        return attachment

    async def get(self, db: AsyncSession, attachment_id: str) -> Attachment | None:
        try:
            key = uuid.UUID(attachment_id)
        except ValueError:
            return None
        result = await db.execute(select(Attachment).where(Attachment.id == key))
        return result.scalars().first()

    def absolute_path(self, attachment: Attachment) -> Path:
        return get_uploads_dir() / attachment.stored_path
