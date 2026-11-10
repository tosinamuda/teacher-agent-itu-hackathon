"""Comment on content, and read the conversation: the tools a content page calls.

A comment goes to the agent that wrote the content, which keeps its place between comments.
It is taken at once and answered in the background, so the page asks ``conversation_state``
whether the agent is still working and when a new version is there.
"""

from __future__ import annotations

from collections.abc import Callable

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ToolError

from app.domains.content.application.service import ContentService
from app.domains.content_engine.application.comments import Comment, CommentDesk
from app.domains.content_engine.mcp.caller import APP, caller, permit
from app.domains.content_engine.mcp.refusals import Sessions, refusing
from app.domains.content_engine.mcp.views import Payload
from app.shared.json_types import JsonObject

#: What a comment, and the text it points at, may hold.
MAX_COMMENT = 4000
MAX_SELECTED = 2000
_REVISE = "artefact_revision:*"


def _highlight(
    unit_id: str | None, path: str | None, selected_text: str | None
) -> JsonObject | None:
    kept: JsonObject = {}
    if unit_id:
        kept["unit_id"] = unit_id
    if path:
        kept["path"] = path
    if selected_text and selected_text.strip():
        kept["selected_text"] = selected_text.strip()
    return kept or None


def add_comment_tools(
    server: MCPServer,
    content: Callable[[], ContentService],
    comments: CommentDesk,
    sessions: Sessions,
) -> None:
    @server.tool()
    async def comment_on_content(
        content_id: str,
        comment: str,
        ctx: Context,
        unit_id: str | None = None,
        path: str | None = None,
        selected_text: str | None = None,
        chat_id: str | None = None,
    ) -> Payload:
        """Comment on content, to the agent that wrote it; it carries on from where it was.

        Leave out ``chat_id`` to comment in the content's own chat, or name another chat on it.

        Name where the comment is with ``unit_id``, the ``path`` of a field in its part and the
        ``selected_text``, or leave them out to comment on the whole. The comment is taken at
        once and the agent works on it after: ask ``conversation_state`` how it is going.
        """
        text = comment.strip()
        if not text or len(text) > MAX_COMMENT or len(selected_text or "") > MAX_SELECTED:
            raise ToolError(f"a comment is 1 to {MAX_COMMENT} characters")
        async with sessions() as db:
            signed_in = await caller(db, ctx.headers)
            record = await refusing(content().record(db, content_id))
            await refusing(
                permit(db, signed_in, "revise", plan_version_id=record.plan_version_id, obj=_REVISE)
            )
            by = signed_in.actor.display_name if signed_in.actor is not None else APP
        waiting = comments.take(
            content_id, Comment(text, _highlight(unit_id, path, selected_text), by), chat_id
        )
        return {"content_id": content_id, "accepted": True, "waiting": waiting}

    @server.tool()
    async def conversation_state(
        content_id: str, ctx: Context, chat_id: str | None = None
    ) -> Payload:
        """The conversation about content: its turns, its version, and whether the agent works.

        The turns are those of every chat on the content; whether the agent works is the content's
        own chat's, or the chat ``chat_id`` names.
        """
        async with sessions() as db:
            signed_in = await caller(db, ctx.headers)
            service = content()
            record = await refusing(service.record(db, content_id))
            await refusing(permit(db, signed_in, "read", plan_version_id=record.plan_version_id))
            turns = await refusing(service.revisions(db, content_id))
        return {
            "content_id": content_id,
            "version": record.version,
            "review_status": record.review_status,
            **comments.standing(content_id, chat_id),
            "turns": [
                {
                    "turn_number": turn.turn_number,
                    "comment": turn.instruction,
                    "highlight": turn.highlight,
                    "summary": turn.summary,
                    "created_at": turn.created_at.isoformat(),
                }
                for turn in turns
            ],
        }
