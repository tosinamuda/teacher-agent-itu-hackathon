"""Call a tool a plugin lists, on the app's own MCP server or on the one it links to."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Mapping
from contextlib import AsyncExitStack

from mcp import Client
from mcp.server import MCPServer
from mcp.types import CallToolResult, TextContent

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.content_engine.infrastructure.tools import open_client
from app.domains.content_engine.mcp.caller import as_the_app
from app.shared.json_types import JsonObject

#: Long enough for a tool that reads a draft with a model.
TIMEOUT_SECONDS = 180


class ToolCallError(RuntimeError):
    """A plugin's tool failed, or did not answer with a JSON object."""


def _text(result: CallToolResult) -> str:
    return "".join(c.text for c in result.content if isinstance(c, TextContent))


def _answer_of(result: CallToolResult) -> JsonObject:
    """What a tool answers, as structured content or as JSON text."""
    answer: object = result.structured_content
    if answer is None:
        try:
            answer = json.loads(_text(result))
        except ValueError as error:
            raise ToolCallError(f"the tool wrote no JSON: {error}") from error
    if not isinstance(answer, dict):
        raise ToolCallError("the tool answers a JSON object")
    return {str(key): value for key, value in answer.items()}


def tool_caller(
    own_server: Callable[[], MCPServer], environ: Mapping[str, str] = os.environ
) -> Callable[[McpServerRef, str, JsonObject], Awaitable[JsonObject]]:
    """Calls a tool with its arguments and returns the object it answers.

    A link that is a path reaches ``own_server`` inside this process, as the app. Any other link
    is reached over streamable HTTP with the token its ref names. Every call has a time limit.
    """

    async def call(ref: McpServerRef, tool: str, arguments: JsonObject) -> JsonObject:
        async with asyncio.timeout(TIMEOUT_SECONDS), AsyncExitStack() as stack:
            if ref.own:
                stack.enter_context(as_the_app())
                client = await stack.enter_async_context(Client(own_server()))
            else:
                client = await open_client(stack, ref, environ)
            result = await client.call_tool(tool, arguments)
        if result.is_error:
            raise ToolCallError(f"{ref.name}.{tool} failed: {_text(result)}")
        return _answer_of(result)

    return call
