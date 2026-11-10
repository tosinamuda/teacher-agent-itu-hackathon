"""Whether a caller may read a stored content item, for tools and resources that hand it out."""

from __future__ import annotations

from collections.abc import Callable

from mcp.server.mcpserver import Context
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.records import ContentRecord
from app.domains.content.application.service import ContentService
from app.domains.content_engine.mcp.caller import caller, permit
from app.domains.content_engine.mcp.refusals import refusing


async def may_read(
    db: AsyncSession,
    content: Callable[[], ContentService],
    content_id: str,
    ctx: Context,
    raising: type[Exception],
) -> ContentRecord:
    """The record of ``content_id``, refused with ``raising`` unless the caller may read it."""
    signed_in = await caller(db, ctx.headers)
    record = await refusing(content().record(db, content_id), raising)
    await refusing(permit(db, signed_in, "read", plan_version_id=record.plan_version_id), raising)
    return record
