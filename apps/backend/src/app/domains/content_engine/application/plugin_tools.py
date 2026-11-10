"""What a plugin's tools say about a draft: its faults when looked over, additions when saved."""

from __future__ import annotations

import base64
import binascii
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content_engine.application.content_destination import Additions, Check
from app.domains.content_engine.domain.draft import Draft
from app.shared.json_types import JsonObject

#: Calls one tool of a server with its arguments; returns the object it answers.
ToolCaller = Callable[[McpServerRef, str, JsonObject], Awaitable[JsonObject]]


class ToolAnswerError(ValueError):
    """A plugin's tool answered something other than what its kind of tool answers."""


def _faults(tool: str, answer: JsonObject) -> list[str]:
    faults = answer.get("faults")
    if not isinstance(faults, list) or not all(isinstance(fault, str) for fault in faults):
        raise ToolAnswerError(f'{tool} answers {{"faults": [...]}}, one string for each fault')
    return [fault for fault in faults if isinstance(fault, str)]


def _fields(tool: str, answer: JsonObject) -> JsonObject:
    fields = answer.get("additions")
    if not isinstance(fields, dict):
        raise ToolAnswerError(f'{tool} answers {{"additions": {{...}}}}, the fields to add')
    return {str(name): value for name, value in fields.items()}


def plugin_tool_check(catalogue: ContentCatalogue, call: ToolCaller) -> Check:
    """A check that calls the check tools the draft's spec lists, each with the draft's ID.

    A tool answers ``{"faults": [...]}``: what it finds in the draft as it is stored. The server
    it belongs to is the one the plugin's ``mcp.json`` links to. The tools are called in the order
    listed, and the first that finds faults ends the check, so a tool that costs a model call
    is listed last and reads only a draft the cheaper tools pass. A spec that lists no check tool
    has no faults.
    """

    async def check(db: AsyncSession, draft: Draft) -> list[str]:
        spec = await catalogue.revision(db, draft.type, draft.spec_revision)
        for ref in spec.mcp:
            for tool in ref.checks:
                faults = _faults(tool, await call(ref, tool, {"draft_id": draft.draft_id}))
                if faults:
                    return faults
        return []

    return check


def plugin_tool_additions(call: ToolCaller) -> Additions:
    """What the spec's adding tools answer, each called with the draft's ID, merged in order.

    A tool answers ``{"additions": {...}}``: fields to save beside what the writer wrote.
    """

    async def additions(draft: Draft, spec: ContentSpecification) -> JsonObject:
        added: JsonObject = {}
        for ref in spec.mcp:
            for tool in ref.adds:
                added |= _fields(tool, await call(ref, tool, {"draft_id": draft.draft_id}))
        return added

    return additions


@dataclass(frozen=True)
class StoredFile:
    """The file a plugin's tool made of saved content."""

    extension: str
    media_type: str
    data: bytes


def _file(tool: str, answer: JsonObject) -> StoredFile:
    made = answer.get("file")
    fields = made if isinstance(made, dict) else {}
    extension, media_type, data = (fields.get(k) for k in ("extension", "media_type", "data"))
    if not (isinstance(extension, str) and isinstance(media_type, str) and isinstance(data, str)):
        raise ToolAnswerError(
            f'{tool} answers {{"file": {{"extension", "media_type", "data"}}}}, data in base64'
        )
    try:
        return StoredFile(extension, media_type, base64.b64decode(data, validate=True))
    except binascii.Error as error:
        raise ToolAnswerError(f"{tool} answers data that is not base64: {error}") from error


async def plugin_tool_file(
    spec: ContentSpecification, content_id: str, call: ToolCaller
) -> StoredFile | None:
    """The file the spec's first file tool makes of the saved content; none if it lists no tool.

    The tool is called with the content's ID and answers ``{"file": {...}}``.
    """
    for ref in spec.mcp:
        for tool in ref.files:
            return _file(tool, await call(ref, tool, {"content_id": content_id}))
    return None
