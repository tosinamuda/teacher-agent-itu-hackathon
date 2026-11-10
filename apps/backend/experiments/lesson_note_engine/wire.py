"""A proxy between a harness and the generator's endpoint that keeps every exchange as sent.

Whatever a harness says it sends, this is what reached the endpoint: the request body, and
the response body as it came back, a stream included.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.routing import Route

from app.domains.content_engine.infrastructure.harness.local_server import served_locally
from app.shared.json_types import JsonObject

#: The headers a call needs upstream; the rest belong to the hop to the proxy.
_FORWARDED = ("authorization", "content-type", "accept")


@dataclass(frozen=True)
class Exchange:
    request: JsonObject
    status: int
    #: The body as it came back: one JSON object, or a stream of ``data:`` lines.
    response: str


@dataclass
class RecordingProxy:
    upstream: str
    http: httpx.AsyncClient
    exchanges: list[Exchange] = field(default_factory=list)

    async def forward(self, request: Request) -> Response:
        body = await request.body()
        headers = {name: value for name, value in request.headers.items() if name in _FORWARDED}
        sent = self.http.build_request(
            request.method, self.upstream + request.url.path, content=body, headers=headers
        )
        answered = await self.http.send(sent, stream=True)
        return StreamingResponse(
            self._kept(json.loads(body), answered),
            status_code=answered.status_code,
            media_type=answered.headers.get("content-type"),
        )

    async def _kept(self, request: JsonObject, answered: httpx.Response) -> AsyncIterator[bytes]:
        chunks: list[bytes] = []
        async for chunk in answered.aiter_bytes():
            chunks.append(chunk)
            yield chunk
        await answered.aclose()
        text = b"".join(chunks).decode("utf-8", errors="replace")
        self.exchanges.append(Exchange(request, answered.status_code, text))


@asynccontextmanager
async def recording(upstream: str) -> AsyncIterator[tuple[RecordingProxy, str]]:
    """The proxy to ``upstream`` (a host root), and the base URL a harness calls it on."""
    async with httpx.AsyncClient(timeout=600) as http:
        proxy = RecordingProxy(upstream.rstrip("/"), http)
        routes = [Route("/{path:path}", proxy.forward, methods=["GET", "POST"])]
        async with served_locally(Starlette(routes=routes)) as port:
            yield proxy, f"http://127.0.0.1:{port}/v1"
