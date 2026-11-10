"""Saved content as a file: to a signed-in reader, or to the holder of a signed link."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.content.api.routes import owned_record
from app.domains.content.application.errors import ContentError
from app.domains.content.infrastructure.download_links import is_valid, secret_from_environment
from app.domains.content.infrastructure.wiring import made_file
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/content", tags=["content-files"])


async def _file(db: AsyncSession, content_id: str) -> Response:
    try:
        made = await made_file(db, content_id)
    except ContentError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return Response(
        made.data,
        media_type=made.media_type,
        headers={"Content-Disposition": f'attachment; filename="{content_id}.{made.extension}"'},
    )


@router.get("/{content_id}/file")
async def download_content_file(
    content_id: str,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> Response:
    await owned_record(actor, db, content_id)
    return await _file(db, content_id)


@router.get("/files/{content_id}")
async def download_content_file_by_link(
    content_id: str,
    expires: int,
    signature: str,
    db: AsyncSession = Depends(get_db),
) -> Response:
    """The file for a link the MCP server issued: the signature is the only check."""
    if not is_valid(secret_from_environment(), content_id, expires, signature, time.time()):
        raise HTTPException(status_code=403, detail="link_expired_or_invalid")
    return await _file(db, content_id)
