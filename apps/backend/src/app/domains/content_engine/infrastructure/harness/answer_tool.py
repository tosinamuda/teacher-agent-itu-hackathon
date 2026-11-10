"""One tool a harness in its own process answers through, for a harness without structured output.

The checker's verdict comes back as a native tool call, as DeepAgents' answer tool and
OpenCode's structured output bring it, rather than as JSON the model writes in its reply.
"""

from __future__ import annotations

import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server import Server, ServerRequestContext
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListToolsResult,
    PaginatedRequestParams,
    TextContent,
    Tool,
)
from pydantic import BaseModel, ValidationError

from app.domains.content_engine.infrastructure.harness.local_server import served_locally
from app.domains.content_engine.infrastructure.harness.relay import BearerOnly, Relay
from app.shared.json_types import JsonObject


@dataclass
class Answer:
    """What the tool was last called with; nothing until it is called."""

    arguments: JsonObject | None = None


def answer_server(tool: Tool, schema: type[BaseModel], answer: Answer) -> Server:
    """A server offering only ``tool``, keeping in ``answer`` the last call ``schema`` allows.

    A call the schema does not allow is refused with the reason, as the engine's draft tools
    refuse a part, so the model can answer again.
    """

    async def list_tools(
        ctx: ServerRequestContext, params: PaginatedRequestParams | None
    ) -> ListToolsResult:
        return ListToolsResult(tools=[tool])

    async def call_tool(ctx: ServerRequestContext, params: CallToolRequestParams) -> CallToolResult:
        if params.name != tool.name:
            refusal = TextContent(type="text", text=f"there is no tool {params.name}")
            return CallToolResult(content=[refusal], is_error=True)
        arguments = dict(params.arguments or {})
        try:
            schema.model_validate(arguments)
        except ValidationError as error:
            reason = f"Error: the answer does not match the tool's schema: {error}"
            return CallToolResult(content=[TextContent(type="text", text=reason)], is_error=True)
        answer.arguments = arguments
        return CallToolResult(content=[TextContent(type="text", text="Recorded.")])

    return Server("answer", on_list_tools=list_tools, on_call_tool=call_tool)


@asynccontextmanager
async def answering(tool: Tool, schema: type[BaseModel]) -> AsyncIterator[tuple[Relay, Answer]]:
    """The tool served on a free local port behind a bearer token, and what it was told."""
    answer = Answer()
    token = secrets.token_urlsafe(32)
    server = answer_server(tool, schema, answer)
    app = server.streamable_http_app(stateless_http=True, json_response=True)
    async with served_locally(BearerOnly(app, token)) as port:
        yield Relay(f"http://127.0.0.1:{port}/mcp", token), answer
