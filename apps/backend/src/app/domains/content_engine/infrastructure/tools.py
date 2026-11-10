"""The tools a writer is offered: the draft's own, and those of the external servers its type lists.

A writer is given one MCP client. Behind it the tools of several servers sit side by side, each
server's tools under its own prefix, and only the tools a source names are offered at all. The
credentials of an external server stay with the app's connection to it: a writer, in this process
or another, sees only the tools.
"""

from __future__ import annotations

import asyncio
import contextvars
import os
from collections.abc import AsyncIterator, Callable, Mapping, Sequence
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass

from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.server import Server, ServerRequestContext
from mcp.shared._httpx_utils import create_mcp_http_client
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListToolsResult,
    PaginatedRequestParams,
    ReadResourceRequestParams,
    ReadResourceResult,
    TextContent,
)

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef

#: The tools of the engine's own server a writer is offered. Starting and submitting drafts is
#: the engine's job.
WRITER_TOOLS = ("add_part", "revise_part", "read_draft")


#: The resources a writer may read: its type's skills, at the revision the spec pins, and the
#: files of the plugin that made the type.
SKILL_URIS = ("skill://", "plugin-skills://")


class ExternalServerError(RuntimeError):
    """An external server a type lists cannot be used: no credential, or not the tools listed."""


@dataclass(frozen=True)
class Source:
    """The named tools of one client, offered as ``<prefix><tool>``."""

    client: Client
    names: frozenset[str]
    prefix: str = ""


def tools_server(
    sources: Sequence[Source],
    *,
    opened_in: contextvars.Context,
    transform: Callable[[CallToolResult], CallToolResult] = lambda result: result,
    skills_from: Client | None = None,
) -> Server:
    """A server offering the named tools of each source, each call forwarded to its source.

    A request arrives on a task of the server's own, so each call is made in ``opened_in``, the
    context the app's own client was opened in, which calls as the app. ``transform`` is applied
    to each result before it is returned. Given ``skills_from``, the server also lets a client
    read a skill from it, and nothing else it holds.
    """
    offered = {(s.prefix + name): (s, name) for s in sources for name in s.names}

    async def list_tools(
        ctx: ServerRequestContext, params: PaginatedRequestParams | None
    ) -> ListToolsResult:
        tools = []
        for source in sources:
            listed = await asyncio.create_task(source.client.list_tools(), context=opened_in)
            tools += [
                tool.model_copy(update={"name": source.prefix + tool.name})
                for tool in listed.tools
                if tool.name in source.names
            ]
        return ListToolsResult(tools=tools)

    async def call_tool(ctx: ServerRequestContext, params: CallToolRequestParams) -> CallToolResult:
        found = offered.get(params.name)
        if found is None:
            refusal = TextContent(type="text", text=f"there is no tool {params.name}")
            return CallToolResult(content=[refusal], is_error=True)
        source, name = found
        call = source.client.call_tool(name, params.arguments or {})
        return transform(await asyncio.create_task(call, context=opened_in))

    async def read_resource(
        ctx: ServerRequestContext, params: ReadResourceRequestParams
    ) -> ReadResourceResult:
        if skills_from is None or not str(params.uri).startswith(SKILL_URIS):
            raise ValueError(f"there is no resource {params.uri}")
        read = skills_from.read_resource(str(params.uri))
        return ReadResourceResult(
            contents=(await asyncio.create_task(read, context=opened_in)).contents
        )

    return Server(
        "content-engine",
        on_list_tools=list_tools,
        on_call_tool=call_tool,
        on_read_resource=read_resource if skills_from is not None else None,
    )


async def open_client(
    stack: AsyncExitStack, ref: McpServerRef, environ: Mapping[str, str]
) -> Client:
    """A client of the server ``ref`` links to, closed with ``stack``.

    The bearer token is read from the environment variable the ref names and is sent only to
    this server. ``ExternalServerError`` when the token is not set.
    """
    headers: dict[str, str] = {}
    if ref.secret is not None:
        token = environ.get(ref.secret)
        if not token:
            raise ExternalServerError(f"{ref.name}: {ref.secret} is not set")
        headers["Authorization"] = f"Bearer {token}"
    transport = streamable_http_client(ref.url, http_client=create_mcp_http_client(headers=headers))
    return await stack.enter_async_context(Client(transport))


async def _connect(
    stack: AsyncExitStack, refs: Sequence[McpServerRef], environ: Mapping[str, str]
) -> tuple[list[Source], ExternalServerError | None]:
    """Connect to each server a writer uses; the problem with the first that cannot be used."""
    sources: list[Source] = []
    for ref in (r for r in refs if r.tools):
        try:
            client = await open_client(stack, ref, environ)
        except ExternalServerError as error:
            return sources, error
        missing = set(ref.tools) - {tool.name for tool in (await client.list_tools()).tools}
        if missing:
            return sources, ExternalServerError(f"{ref.name} has no tools {sorted(missing)}")
        sources.append(Source(client, frozenset(ref.tools), prefix=f"{ref.name}__"))
    return sources, None


@asynccontextmanager
async def mounted(
    refs: Sequence[McpServerRef], environ: Mapping[str, str] = os.environ
) -> AsyncIterator[list[Source]]:
    """Connect to each external server; the sources offer only the tools its ref allows.

    The bearer token is read from the environment variable the ref names, and is sent only to
    the server it belongs to. A server that cannot be used is raised once every connection is
    closed, so it is not wrapped in the group of errors a connection's own task raises.
    """
    async with AsyncExitStack() as stack:
        sources, problem = await _connect(stack, refs, environ)
        if problem is None:
            yield sources
    if problem is not None:
        raise problem
