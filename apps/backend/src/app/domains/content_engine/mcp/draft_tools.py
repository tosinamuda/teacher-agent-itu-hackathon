"""The tools of the app's MCP server that a plugin lists: they check a draft or finish its content.

Each takes the ID of a draft. A check tool answers ``{"faults": [...]}``: what the rule of its type
finds in the draft as it is stored. An adding tool answers ``{"additions": {...}}``: the fields to
save beside what the writer wrote. The app calls them as itself; any other caller reads only its
own drafts.
"""

from __future__ import annotations

from mcp.server import MCPServer
from mcp.server.mcpserver import Context

from app.domains.content_engine.application.draft_tools import DraftTools
from app.domains.content_engine.mcp.caller import caller
from app.domains.content_engine.mcp.refusals import Sessions, refusing
from app.domains.content_engine.mcp.views import Payload


def add_draft_tools(server: MCPServer, tools: DraftTools, sessions: Sessions) -> None:
    for tool in tools.check_tools:
        _add_check(server, tools, sessions, tool)
    for tool in tools.add_tools:
        _add_addition(server, tools, sessions, tool)


async def _only_by(sessions: Sessions, ctx: Context) -> str | None:
    """Who may read the draft: the app reads any, a signed-in caller only their own."""
    async with sessions() as db:
        signed_in = await caller(db, ctx.headers)
    return signed_in.by if signed_in.actor is not None else None


def _add_check(server: MCPServer, tools: DraftTools, sessions: Sessions, tool: str) -> None:
    @server.tool(
        name=tool,
        description=(
            "The faults of a draft as it is stored, found by the rules of its type; an empty "
            "list means it passes. Reads only your own drafts."
        ),
    )
    async def check(draft_id: str, ctx: Context) -> Payload:
        only_by = await _only_by(sessions, ctx)
        async with sessions() as db:
            faults = await refusing(tools.faults(db, tool=tool, draft_id=draft_id, only_by=only_by))
        return {"faults": faults}


def _add_addition(server: MCPServer, tools: DraftTools, sessions: Sessions, tool: str) -> None:
    @server.tool(
        name=tool,
        description=(
            "The fields to save beside the content of a draft, which the app knows from the "
            "lesson. Reads only your own drafts."
        ),
    )
    async def addition(draft_id: str, ctx: Context) -> Payload:
        only_by = await _only_by(sessions, ctx)
        async with sessions() as db:
            added = await refusing(
                tools.additions(db, tool=tool, draft_id=draft_id, only_by=only_by)
            )
        return {"additions": added}
