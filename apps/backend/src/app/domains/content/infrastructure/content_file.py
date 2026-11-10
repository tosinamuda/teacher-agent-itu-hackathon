"""Saved content as a file, made by the tool its type's plugin lists."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.errors import ContentError
from app.domains.content.application.records import ContentRecord
from app.domains.content.application.service import ContentService
from app.domains.content_engine.application.plugin_tools import (
    StoredFile,
    ToolAnswerError,
    ToolCaller,
    plugin_tool_file,
)
from app.domains.content_engine.infrastructure.tool_calls import ToolCallError


async def _specs(
    catalogue: ContentCatalogue, db: AsyncSession, record: ContentRecord
) -> list[ContentSpecification]:
    """The spec the content was made with, then the one its type has now.

    Content made before its plugin listed a file tool is made into a file by the current one.
    """
    made_with = record.provenance.get("spec_revision")
    specs = (
        [await catalogue.revision(db, record.type, made_with)] if isinstance(made_with, int) else []
    )
    return [*specs, await catalogue.current(db, record.type)]


async def offers_file(catalogue: ContentCatalogue, db: AsyncSession, record: ContentRecord) -> bool:
    """Whether a spec of the content's type lists a tool that makes it into a file."""
    return any(ref.files for spec in await _specs(catalogue, db, record) for ref in spec.mcp)


async def content_file(
    service: ContentService,
    catalogue: ContentCatalogue,
    call: ToolCaller,
    db: AsyncSession,
    content_id: str,
) -> StoredFile:
    """The file the content's plugin makes of it.

    ``ContentError`` when the plugin lists no file tool or its tool cannot make the file.
    """
    record = await service.record(db, content_id)
    made: StoredFile | None = None
    try:
        for spec in await _specs(catalogue, db, record):
            if made := await plugin_tool_file(spec, content_id, call):
                break
    except (ToolCallError, ToolAnswerError) as error:
        raise ContentError(409, f"file_unavailable:{error}") from error
    if made is None:
        raise ContentError(409, "file_unavailable:its plugin lists no file tool")
    return made
