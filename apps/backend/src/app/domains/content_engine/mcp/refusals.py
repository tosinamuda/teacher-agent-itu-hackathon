"""Refusals as MCP errors, and the database sessions each call opens."""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager
from typing import TypeVar

from mcp.server.mcpserver.exceptions import ToolError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.errors import ContentError
from app.domains.content_engine.domain.draft import DraftError
from app.domains.content_engine.mcp.caller import PermissionRefusedError
from app.domains.content_engine.mcp.views import Payload

T = TypeVar("T")

#: Opens a database session for one tool call or resource read.
Sessions = Callable[[], AbstractAsyncContextManager[AsyncSession]]


async def refusing(call: Awaitable[T], raising: type[Exception] = ToolError) -> T:
    """Turn a refusal into an error the client reads: a tool's, or a resource's."""
    try:
        return await call
    except (DraftError, PermissionRefusedError) as error:
        raise raising(str(error)) from error
    except ContentError as error:
        raise raising(error.detail) from error


def a_part(raw: Payload | str) -> Payload:
    """The part a writer sent, as an object: a JSON object written out as text is read as one.

    A model that sends the part as a string would otherwise have its whole call refused before
    this tool runs, with a message that does not say what was wrong.
    """
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw)
    except ValueError as error:
        raise ToolError(
            f"the part is not valid JSON ({error}): send it as a JSON object"
        ) from error
    if not isinstance(parsed, dict):
        raise ToolError("the part is a JSON object of its fields, not a list or a value")
    return parsed
