"""An external MCP server on localhost, for the tests of a type that lists one."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from mcp.server import MCPServer
from starlette.types import ASGIApp, Receive, Scope, Send

from app.domains.content_engine.infrastructure.harness.local_server import served_locally


@dataclass
class ExternalServer:
    url: str
    #: The Authorization header of every request it received, in order.
    seen: list[str] = field(default_factory=list)


class _Recording:
    def __init__(self, app: ASGIApp, seen: list[str]) -> None:
        self._app = app
        self._seen = seen

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            headers = dict(scope.get("headers") or [])
            self._seen.append(headers.get(b"authorization", b"").decode())
        await self._app(scope, receive, send)


@asynccontextmanager
async def external_server() -> AsyncIterator[ExternalServer]:
    """A server offering ``solve``, which doubles a number, and ``forbidden``, which none lists."""
    server = MCPServer("external")

    @server.tool()
    def solve(number: int) -> str:
        """Double a number."""
        return f"the answer is {number * 2}"

    @server.tool()
    def forbidden() -> str:
        """A tool no spec may list."""
        return "never offered"

    seen: list[str] = []
    app = server.streamable_http_app(stateless_http=True, json_response=True)
    async with served_locally(_Recording(app, seen)) as port:
        yield ExternalServer(f"http://127.0.0.1:{port}/mcp", seen)
