"""Saved content as a file an MCP client can take: a resource of its bytes, and a download link.

A client that reads binary resources reads ``content://{content_id}/file``. One that passes only
tools to its model, or cannot save a resource as a file, asks ``get_content_file_link`` for a
link its user opens in a browser. Content has a file when its type's plugin lists a file tool.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.records import ContentRecord
from app.domains.content.application.service import ContentService
from app.domains.content_engine.application.plugin_tools import StoredFile
from app.domains.content_engine.mcp.reading import may_read
from app.domains.content_engine.mcp.refusals import Sessions, refusing
from app.domains.content_engine.mcp.views import Payload

#: Where the API answers on a public host: the web server serves it under this path.
PUBLIC_API_PATH = "/api"
LINK_PATH = "/content/files/{content_id}"
#: The type of the file differs by content, and a resource template names one type.
RESOURCE_TYPE = "application/octet-stream"
_LOCAL_HOSTS = ("localhost", "127.0.0.1", "[::1]")


@dataclass(frozen=True)
class ContentFiles:
    """What the server needs to hand saved content out as a file."""

    #: The file the content's plugin makes of it.
    build: Callable[[AsyncSession, str], Awaitable[StoredFile]]
    #: Whether the content's type has a tool that makes it into a file.
    offers: Callable[[AsyncSession, ContentRecord], Awaitable[bool]]
    #: When a link to the content ends, and its signature; none where links are not set up.
    issue: Callable[[str, float], tuple[int, str] | None]
    #: How long a link lasts, for the message that hands it out.
    lifetime_minutes: int


def _header(headers: Mapping[str, str] | None, name: str) -> str:
    return next((v for k, v in (headers or {}).items() if k.lower() == name), "")


def _origin(headers: Mapping[str, str] | None) -> str:
    host = _header(headers, "x-forwarded-host") or _header(headers, "host")
    local = host.startswith(_LOCAL_HOSTS)
    scheme = _header(headers, "x-forwarded-proto") or ("http" if local else "https")
    return f"{scheme}://{host}"


def _link(headers: Mapping[str, str] | None, content_id: str, issued: tuple[int, str]) -> str:
    expires, signature = issued
    prefix = "" if _header(headers, "host").startswith(_LOCAL_HOSTS) else PUBLIC_API_PATH
    path = LINK_PATH.format(content_id=content_id)
    return f"{_origin(headers)}{prefix}{path}?expires={expires}&signature={signature}"


def download_of(
    headers: Mapping[str, str] | None, content_id: str, files: ContentFiles
) -> dict[str, str | int]:
    """How to take saved content as a file: its resource, and a link where links are set up."""
    taken: dict[str, str | int] = {"resource": f"content://{content_id}/file"}
    if (issued := files.issue(content_id, time.time())) is not None:
        taken |= {
            "url": _link(headers, content_id, issued),
            "expires_in_minutes": files.lifetime_minutes,
        }
    return taken


def add_content_file(
    server: MCPServer,
    content: Callable[[], ContentService],
    sessions: Sessions,
    files: ContentFiles,
) -> None:
    @server.resource("content://{content_id}/file", mime_type=RESOURCE_TYPE, name="content_file")
    async def file_resource(content_id: str, ctx: Context) -> bytes:
        """The file of saved content, if the caller may read its lesson's content."""
        async with sessions() as db:
            await may_read(db, content, content_id, ctx, ResourceError)
            return (await refusing(files.build(db, content_id), ResourceError)).data

    @server.tool()
    async def get_content_file_link(content_id: str, ctx: Context) -> Payload:
        """A link that downloads saved content as a file, for a person to open.

        Only content whose type's plugin lists a file tool has one, such as a slide deck. The
        link works without signing in and ends after a few minutes: give it to the teacher at
        once. Ask again for a new one.
        """
        async with sessions() as db:
            record = await may_read(db, content, content_id, ctx, ToolError)
            has_file = await files.offers(db, record)
        if not has_file:
            raise ToolError(f"{content_id} is {record.type} content, which has no file")
        issued = files.issue(content_id, time.time())
        if issued is None:
            raise ToolError("download links are not set up on this server")
        return {
            "url": _link(ctx.headers, content_id, issued),
            "expires_in_minutes": files.lifetime_minutes,
        }
