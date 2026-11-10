"""An MCP App that shows content in the host: a tool bound to a ``ui://`` page.

A host without MCP Apps still gets the content as JSON text from the same tool.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from pathlib import Path

from mcp.server.apps import Apps, ResourceCsp
from mcp.server.mcpserver import Context

from app.domains.content_engine.mcp.views import Payload

VIEWER_URI = "ui://content/viewer.html"
_CONVERSATION_SLOT = "<!--conversation-->"


def _page() -> str:
    """The page, with the script that talks to the agent put where the page leaves its place."""
    here = Path(__file__).parent
    page = (here / "viewer.html").read_text(encoding="utf-8")
    script = (here / "viewer_conversation.js").read_text(encoding="utf-8")
    return page.replace(_CONVERSATION_SLOT, f"<script>\n{script}</script>")


_VIEWER_HTML = _page()

#: Reads one item as the caller may see it: content, or a draft.
Read = Callable[[str, Context], Awaitable[Payload]]


def content_viewer(read_content: Read, read_draft: Read) -> Apps:
    apps = Apps()

    @apps.tool(resource_uri=VIEWER_URI, name="show_content", title="Show content")
    async def show_content(content_id: str, ctx: Context) -> Payload:
        """Show content and its review status; hosts with MCP Apps draw it as a page."""
        return await read_content(content_id, ctx)

    @apps.tool(resource_uri=VIEWER_URI, name="show_draft", title="Show draft")
    async def show_draft(draft_id: str, ctx: Context) -> Payload:
        """Show a draft as it would save so far; hosts with MCP Apps draw it as its type."""
        return await read_draft(draft_id, ctx)

    apps.add_html_resource(
        VIEWER_URI,
        _VIEWER_HTML,
        name="content-viewer",
        title="Content",
        description="Content drawn for its type, with its version and review status.",
        # KaTeX draws the maths; without it the page shows the TeX as text.
        csp=ResourceCsp(resource_domains=["https://cdn.jsdelivr.net"]),
    )
    return apps
