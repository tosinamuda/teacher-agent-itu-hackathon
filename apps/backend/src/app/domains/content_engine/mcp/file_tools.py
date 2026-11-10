"""The file tools of the app's MCP server: a plugin lists one to have its content made into a file.

A tool takes the ID of saved content and answers
``{"file": {"extension", "media_type", "data"}}``, ``data`` being the file's bytes in base64. The
app calls it as itself; any other caller reads only the content it may read.
"""

from __future__ import annotations

import asyncio
import base64
from collections.abc import Callable, Mapping

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ToolError

from app.domains.content.application.service import ContentService
from app.domains.content_engine.files.builder import FileBuilder, FileRefusedError
from app.domains.content_engine.mcp.reading import may_read
from app.domains.content_engine.mcp.refusals import Sessions, refusing
from app.domains.content_engine.mcp.views import Payload


def add_file_tools(
    server: MCPServer,
    content: Callable[[], ContentService],
    sessions: Sessions,
    builders: Mapping[str, FileBuilder],
) -> None:
    for tool, build in builders.items():
        _add(server, content, sessions, tool, build)


def _add(
    server: MCPServer,
    content: Callable[[], ContentService],
    sessions: Sessions,
    tool: str,
    build: FileBuilder,
) -> None:
    @server.tool(
        name=tool,
        description=(
            "The file of saved content, as its extension, its media type and its bytes in "
            "base64. Reads only content you may read."
        ),
    )
    async def make(content_id: str, ctx: Context) -> Payload:
        async with sessions() as db:
            await may_read(db, content, content_id, ctx, ToolError)
            item = await refusing(content().get(db, content_id))
        try:
            # A drawing is compiled by TeX, which blocks: keep the event loop free.
            built = await asyncio.to_thread(build, item.content)
        except FileRefusedError as error:
            raise ToolError(str(error)) from error
        return {
            "file": {
                "extension": built.extension,
                "media_type": built.media_type,
                "data": base64.b64encode(built.data).decode("ascii"),
            }
        }
