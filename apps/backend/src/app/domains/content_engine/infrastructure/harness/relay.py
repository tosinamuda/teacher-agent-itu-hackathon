"""The writer's draft tools over HTTP, for a harness that runs in a process of its own.

A draft belongs to whoever started it, and the engine starts it as the app. So a harness in
another process cannot open the engine's server as itself; it reaches the writer's tools
through this relay, which forwards each call through the engine's own client and so calls
as the app. It listens on localhost only, and answers only a caller with its bearer token.
"""

from __future__ import annotations

import contextvars
import hmac
import json
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from mcp import Client
from mcp.server import Server
from mcp.types import CallToolResult, ContentBlock, TextContent
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.domains.content_engine.infrastructure.harness.local_server import served_locally
from app.domains.content_engine.infrastructure.tools import Source, tools_server


@dataclass(frozen=True)
class Relay:
    url: str
    token: str

    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}


def _without_skills(draft: dict[str, Any]) -> dict[str, Any]:
    """A draft's JSON without the skills its brief carries."""
    brief = draft.get("brief")
    if not isinstance(brief, dict):
        return draft
    return {**draft, "brief": {name: item for name, item in brief.items() if name != "skills"}}


def _block_without_skills(block: ContentBlock) -> ContentBlock:
    if not isinstance(block, TextContent):
        return block
    try:
        parsed = json.loads(block.text)
    except ValueError:
        return block
    if not isinstance(parsed, dict):
        return block
    return TextContent(type="text", text=json.dumps(_without_skills(parsed)))


def hide_skills(result: CallToolResult) -> CallToolResult:
    """The result with the skills left out of a draft's brief, in its text and its data.

    A harness that loads the skills itself must not be given their text again by a tool.
    """
    data = result.structured_content
    return result.model_copy(
        update={
            "content": [_block_without_skills(block) for block in result.content],
            "structured_content": _without_skills(data) if data is not None else None,
        }
    )


async def relay_server(client: Client, *, skills_hidden: bool = False) -> Server:
    """A server offering every tool ``client`` offers, each call forwarded to it.

    With ``skills_hidden`` a draft's skills are left out of what a call returns.

    The in-memory server reads who is calling from the caller's context, and a request
    arrives on a task of the HTTP server's, so each call is made in the context the relay
    was opened in: the engine's, which calls as the app.
    """
    names = frozenset(tool.name for tool in (await client.list_tools()).tools)
    return tools_server(
        [Source(client, names)],
        opened_in=contextvars.copy_context(),
        transform=hide_skills if skills_hidden else lambda result: result,
    )


class BearerOnly:
    """Refuses every HTTP request that does not carry the token."""

    def __init__(self, app: ASGIApp, token: str) -> None:
        self._app = app
        self._expected = f"Bearer {token}".encode()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        sent = dict(scope.get("headers") or []).get(b"authorization", b"")
        if scope["type"] == "http" and not hmac.compare_digest(sent, self._expected):
            await PlainTextResponse("unauthorised", status_code=401)(scope, receive, send)
            return
        await self._app(scope, receive, send)


@asynccontextmanager
async def relayed(client: Client, *, skills_hidden: bool = False) -> AsyncIterator[Relay]:
    """The relay, served on a free local port for the length of the block."""
    token = secrets.token_urlsafe(32)
    server = await relay_server(client, skills_hidden=skills_hidden)
    app = server.streamable_http_app(stateless_http=True, json_response=True)
    async with served_locally(BearerOnly(app, token)) as port:
        yield Relay(f"http://127.0.0.1:{port}/mcp", token)
