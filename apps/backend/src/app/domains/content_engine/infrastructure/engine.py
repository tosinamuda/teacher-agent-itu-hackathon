"""One run of the engine: open a draft, have the writer fill it, check it, submit it.

The run goes through the MCP server in memory, so the app's writer is held to exactly the
tools, checks and schema an outside client is. The writer is offered the draft's tools and
those of the external servers its type lists, and no others.
"""

from __future__ import annotations

import contextvars
import json
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, replace
from typing import Protocol, runtime_checkable

from mcp import Client
from mcp.server import MCPServer
from mcp.types import TextResourceContents

from app.domains.content_engine.infrastructure.checker import CheckerStoppedError, unit_context
from app.domains.content_engine.infrastructure.tools import (
    WRITER_TOOLS,
    ExternalServerError,
    Source,
    tools_server,
)
from app.domains.content_engine.infrastructure.writer import WriterStoppedError, text_of
from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.generation_log.application.recorder import log_context
from app.shared.json_types import JsonObject, JsonValue

#: How many times a writer that stops with work left is run again on its draft: enough to
#: write units it left out, correct what the checker finds, and correct what a recheck finds.
RESUMES = 3


class EngineRefusedError(ValueError):
    """The engine refused the request before any writing: the message says why."""


class EngineIncompleteError(RuntimeError):
    """The writer finished without a part for every unit, or with issues left."""


#: What a run can fail with that the caller is to read, not a crash.
_REFUSALS = (
    EngineRefusedError,
    EngineIncompleteError,
    WriterStoppedError,
    CheckerStoppedError,
    ExternalServerError,
)


def _refusal_in(error: BaseException) -> Exception | None:
    """The refusal an error is or holds, however deep.

    A writer inside the draft's client raises through task groups, which wrap what it raised.
    """
    if isinstance(error, _REFUSALS):
        return error
    for inner in getattr(error, "exceptions", ()):
        found = _refusal_in(inner)
        if found is not None:
            return found
    return None


@dataclass(frozen=True)
class Built:
    #: What the draft was saved as: a content ID, or a plan version ID for a lesson plan.
    saved_as: str
    summary: str
    #: Content made from a plan version, as stored, read back through the server.
    content: JsonObject
    #: Whether this saved a new version; a revision that changed nothing leaves the content as is.
    changed: bool = True
    #: The version the content is at now.
    version: int | None = None


async def tool_json(client: Client, name: str, arguments: JsonObject) -> JsonObject:
    """A tool's JSON result; a refusal raises with the tool's reason."""
    result = await client.call_tool(name, arguments)
    if result.is_error:
        raise EngineRefusedError(text_of(result))
    return _object(json.loads(text_of(result)), name)


async def resource_json(client: Client, uri: str) -> JsonObject:
    result = await client.read_resource(uri)
    first = result.contents[0]
    if not isinstance(first, TextResourceContents):
        raise EngineRefusedError(f"{uri} is not text")
    return _object(json.loads(first.text), uri)


def _object(loaded: object, source: str) -> JsonObject:
    if not isinstance(loaded, dict):
        raise EngineRefusedError(f"{source} did not answer with a JSON object")
    return {str(key): value for key, value in loaded.items()}


def where_said(found: JsonObject) -> str:
    """The result of a text search, as a line telling the writer where the text is."""
    matches = found.get("matches")
    places = [
        f"unit_id={m['unit_id']}, path={m['path']}"
        + (f", line {m['line']}" if m.get("line") else "")
        for m in (matches if isinstance(matches, list) else [])
        if isinstance(m, dict)
    ]
    if not places:
        return (
            "The selected text is in no part of the draft; the page may draw it from the "
            "lesson's own details."
        )
    shown = "; ".join(places[:3])
    more = f" (and {len(places) - 3} more places)" if len(places) > 3 else ""
    return f"The selected text is in the draft at: {shown}{more}."


@dataclass(frozen=True)
class Request:
    """What to write: a type, what it is made from, and what to write it from."""

    type: str
    plan_version_id: str | None = None
    session_id: str | None = None
    source: str = ""
    #: The content to revise, with the teacher's feedback.
    content_id: str | None = None
    feedback: str = ""
    #: The learner to write the content for, for content made for one learner.
    student_id: str | None = None
    #: The generator to write with when it is not the type's default: its spec is the draft's.
    generator: str | None = None

    def opening(self) -> JsonObject:
        """The arguments that open the draft."""
        fields: JsonObject = {
            "type": self.type,
            "plan_version_id": self.plan_version_id,
            "session_id": self.session_id,
            "source": self.source or None,
            "content_id": self.content_id,
            "student_id": self.student_id,
            "generator": self.generator,
        }
        return {name: value for name, value in fields.items() if value is not None}


class Writer(Protocol):
    """Fills an open draft through the client's tools. Returns a summary of what it did."""

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str: ...


@runtime_checkable
class Kept(Writer, Protocol):
    """A writer whose agent persists: it knows whether it has been told the brief and the thread."""

    briefed: bool


@runtime_checkable
class Stoppable(Protocol):
    """A kept writer whose run in progress can be stopped."""

    async def stop(self) -> None: ...


@runtime_checkable
class Resident(Protocol):
    """A writer that can keep its agent, and so its history, across messages.

    ``keep`` opens the agent for the draft and lesson it is given and yields a writer whose
    every ``write`` goes to that one agent, which is closed when the block ends. The agent's
    history is kept under ``key``, so an agent opened again under the same key continues it.
    """

    def keep(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, key: str
    ) -> AbstractAsyncContextManager[Kept]: ...


class Checker(Protocol):
    """Reads a finished part again and lists its real errors; empty when it has none."""

    async def errors(
        self, brief: JsonObject, unit: dict[str, object], part: JsonObject
    ) -> list[str]: ...


#: The external servers a content type lists, connected for one run of the writer.
Externals = Callable[[str], AbstractAsyncContextManager[list[Source]]]


class Engine:
    def __init__(
        self,
        server: Callable[[], MCPServer],
        writer: Callable[[], Writer],
        checker: Callable[[], Checker] | None = None,
        externals: Externals | None = None,
    ) -> None:
        """``checker`` reads each finished part again before it is saved, when given.

        ``externals`` connects the external servers a type lists, by its slug, when given.
        """
        self._server = server
        self._writer = writer
        self._checker = checker
        self._externals = externals

    async def build(self, request: Request, *, for_teacher: str | None = None) -> Built:
        """Write the requested content, as the app acting for ``for_teacher``."""
        with as_the_app(for_teacher):
            async with Client(self._server()) as client:
                # Raised inside the client's task group, a failure would leave as an
                # exception group, so it is kept and raised once the client has closed.
                try:
                    outcome: Built | Exception = await self._run(client, request)
                except Exception as error:
                    refusal = _refusal_in(error)
                    if refusal is None:
                        raise
                    outcome = refusal
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    @asynccontextmanager
    async def converse(
        self, request: Request, *, key: str, for_teacher: str | None = None
    ) -> AsyncIterator[Conversation]:
        """Content kept open with one writer, to be revised a message at a time.

        ``request.content_id`` names the content, and ``key`` the conversation: a writer that
        keeps its history under the key continues it when a conversation is opened again. A
        message that fails is raised by ``say`` inside this block, and a block that lets it
        leave would raise it as a group of errors, so the caller handles it there.
        """
        if request.content_id is None:
            raise EngineRefusedError("a conversation is about content that exists")
        async with self._conversation(request, key, for_teacher) as conversation:
            yield conversation

    async def build_kept(
        self, request: Request, *, key: str, for_teacher: str | None = None
    ) -> Built:
        """Write new content like ``build``, with a writer that keeps its history under ``key``.

        A later conversation under the same key, or one linked to it, continues the writer's
        session, so what the teacher asks of the finished content goes to the agent that made it.
        """
        async with self._conversation(request, key, for_teacher) as conversation:
            try:
                outcome: Built | Exception = await conversation.say(request.feedback)
            except Exception as error:
                refusal = _refusal_in(error)
                if refusal is None:
                    raise
                outcome = refusal
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    @asynccontextmanager
    async def _conversation(
        self, request: Request, key: str, for_teacher: str | None
    ) -> AsyncIterator[Conversation]:
        with as_the_app(for_teacher):
            async with Client(self._server()) as client, AsyncExitStack() as stack:
                yield Conversation(self, client, stack, request, key)

    async def _run(self, client: Client, request: Request) -> Built:
        draft = await tool_json(client, "start_draft", request.opening())
        lesson = await resource_json(client, str(draft["lesson_uri"]))
        if draft.get("learner_uri"):
            lesson = {**lesson, "learner": await resource_json(client, str(draft["learner_uri"]))}
        with log_context(
            kind="engine_content",
            correlation_id=draft["draft_id"],
            plan_version_id=request.plan_version_id,
            session_id=request.session_id,
            content_type=request.type,
        ):
            async with self._offered(client, str(draft["type"])) as offered:
                summary = await self._write(client, offered, draft, lesson, request, self._writer())
        saved_as = await _submit(client, str(draft["draft_id"]))
        if request.plan_version_id is None:
            return Built(saved_as, summary, {})
        stored = await resource_json(client, f"content://{saved_as}")
        return Built(saved_as, summary, _object(stored.get("content"), saved_as))

    @asynccontextmanager
    async def _offered(self, client: Client, type_slug: str) -> AsyncIterator[Client]:
        """The client the writer is given: the draft's tools and the type's external ones."""
        async with AsyncExitStack() as stack:
            external = (
                await stack.enter_async_context(self._externals(type_slug))
                if self._externals is not None
                else []
            )
            server = tools_server(
                [Source(client, frozenset(WRITER_TOOLS)), *external],
                opened_in=contextvars.copy_context(),
                skills_from=client,
            )
            yield await stack.enter_async_context(Client(server))

    async def _write(
        self,
        client: Client,
        offered: Client,
        draft: JsonObject,
        lesson: JsonObject,
        request: Request,
        writer: Writer,
    ) -> str:
        """Have the writer fill the draft, resuming it while work or errors are left.

        A writer can end its loop early, and the draft keeps every part it wrote, so the
        writer is run again on the draft as it stands, told what is still to do: units still
        missing, issues the draft reports, and then errors the checker finds in its parts.
        """
        feedback = request.feedback
        before = await _parts_before(client, draft, request)
        summary = await _resumable(writer.write(offered, draft, lesson, feedback=feedback))
        for _ in range(RESUMES):
            state = await tool_json(client, "read_draft", {"draft_id": draft["draft_id"]})
            left = _still_to_do(state) or await self._errors(state, lesson, request, before)
            if not left:
                break
            told = "\n\n".join((feedback, left)).strip()
            summary = await _resumable(writer.write(offered, state, lesson, feedback=told))
        return summary

    async def _errors(
        self, state: JsonObject, lesson: JsonObject, request: Request, before: JsonObject | None
    ) -> str:
        """What the checker finds wrong in the finished parts; empty when nothing is.

        Content written from a teacher's own document is not checked: it keeps the
        teacher's content, and correcting it is the teacher's call. A revision checks only the
        parts it changed, so a message that asks for nothing changes nothing.
        """
        if self._checker is None or request.source:
            return ""
        checker, parts, brief = self._checker(), state["parts"], state["brief"]
        if not isinstance(parts, dict) or not isinstance(brief, dict):
            return ""
        found: list[str] = []
        for unit in state["units"] if isinstance(state["units"], list) else []:
            part = parts.get(str(unit.get("unit_id"))) if isinstance(unit, dict) else None
            if before is not None and isinstance(unit, dict):
                if part == before.get(str(unit.get("unit_id"))):
                    continue
            if isinstance(unit, dict) and isinstance(part, dict):
                held = _fields_of(state.get("part_schemas"), unit)
                errors = await checker.errors(brief, unit_context(lesson, unit, held), part)
                found.extend(f"the {unit['unit_id']} part: {error}" for error in errors)
        return (
            f"A second reader found these errors; correct each with revise_part: {found}. "
            f"{READ_FIRST}"
            if found
            else ""
        )


class Conversation:
    """One piece of content kept open with one writer, so each message continues the last.

    Every message opens the latest version as a draft, has the writer work on it and saves the
    next version. A writer that keeps its agent between messages keeps its history with it,
    and any other writer is run afresh on each message.
    """

    def __init__(
        self, engine: Engine, client: Client, stack: AsyncExitStack, request: Request, key: str
    ) -> None:
        self._engine = engine
        self._client = client
        self._stack = stack
        self._request = request
        self._key = key
        self._offered: Client | None = None
        self._kept: Kept | None = None
        self._saving = False

    @property
    def stoppable(self) -> bool:
        """Whether a message in progress can be stopped: not while its version is being saved."""
        return not self._saving

    async def stop(self) -> None:
        """Ask the agent to stop what it is doing, when it can be asked."""
        if isinstance(self._kept, Stoppable):
            await self._kept.stop()

    async def say(self, message: str, earlier: str = "", pointed: str = "") -> Built:
        """Have the writer act on ``message`` and save the version it makes.

        ``earlier`` is what came before the message, told only to a writer that does not already
        have it in its history. ``pointed`` is text the teacher selected without saying where it
        is: the draft is searched for it, and the writer is told the unit and field it is in.
        """
        before = await self._version()
        draft = await tool_json(self._client, "start_draft", self._request.opening())
        if pointed:
            message = f"{message}\n\n{await self._where(draft, pointed)}"
        request = replace(self._request, feedback=message)
        lesson = await resource_json(self._client, str(draft["lesson_uri"]))
        with log_context(
            kind="engine_content",
            correlation_id=draft["draft_id"],
            plan_version_id=request.plan_version_id,
            session_id=request.session_id,
            content_type=request.type,
        ):
            offered = await self._offer(str(draft["type"]))
            writer = await self._writer_for(offered, draft, lesson)
            if not (isinstance(writer, Kept) and writer.briefed):
                request = replace(request, feedback="\n\n".join(filter(None, (message, earlier))))
            summary = await self._engine._write(
                self._client, offered, draft, lesson, request, writer
            )
        self._saving = True
        try:
            saved_as = await _submit(self._client, str(draft["draft_id"]))
        finally:
            self._saving = False
        if request.plan_version_id is None and request.content_id is None:
            return Built(saved_as, summary, {})
        stored = await resource_json(self._client, f"content://{request.content_id or saved_as}")
        after = stored.get("version")
        return Built(
            saved_as,
            summary,
            _object(stored.get("content"), saved_as),
            before is None or after != before,
            after if isinstance(after, int) else None,
        )

    async def _where(self, draft: JsonObject, pointed: str) -> str:
        """Where the text the teacher selected is in the open draft, said for the writer."""
        found = await tool_json(
            self._client, "locate_text", {"draft_id": draft["draft_id"], "text": pointed}
        )
        return where_said(found)

    async def _version(self) -> object | None:
        """The version the content is at, when this conversation revises content that exists."""
        if self._request.content_id is None:
            return None
        stored = await resource_json(self._client, f"content://{self._request.content_id}")
        return stored.get("version")

    async def _offer(self, type_slug: str) -> Client:
        if self._offered is None:
            self._offered = await self._stack.enter_async_context(
                self._engine._offered(self._client, type_slug)
            )
        return self._offered

    async def _writer_for(self, offered: Client, draft: JsonObject, lesson: JsonObject) -> Writer:
        writer = self._kept or self._engine._writer()
        if self._kept is None and isinstance(writer, Resident):
            self._kept = await self._stack.enter_async_context(
                writer.keep(offered, draft, lesson, key=self._key)
            )
            return self._kept
        return writer


def _fields_of(schemas: JsonValue, unit: JsonObject) -> list[str]:
    """The names of the fields a unit's part holds, from the JSON Schema of its kind of unit."""
    schema = schemas.get(str(unit.get("unit"))) if isinstance(schemas, dict) else None
    properties = schema.get("properties") if isinstance(schema, dict) else None
    return [str(name) for name in properties] if isinstance(properties, dict) else []


async def _parts_before(client: Client, draft: JsonObject, request: Request) -> JsonObject | None:
    """The parts a revision starts from; none for content that is being made."""
    if request.content_id is None:
        return None
    state = await tool_json(client, "read_draft", {"draft_id": draft["draft_id"]})
    parts = state["parts"]
    return {str(unit): part for unit, part in parts.items()} if isinstance(parts, dict) else {}


async def _resumable(writing: Awaitable[str]) -> str:
    """The writer's summary; a writer that ran out of turns is resumed on its draft instead."""
    try:
        return await writing
    except WriterStoppedError:
        return ""


#: Said with each repair, so the writer names the tool that reads the parts as they stand.
READ_FIRST = 'Read the parts as they stand with read_draft, fields ["parts"], before you revise.'


def _still_to_do(state: JsonObject) -> str:
    """What a resumed writer is told is left; empty when nothing is."""
    lines = []
    if state["missing"]:
        lines.append(f"Write the parts still missing, for the units: {state['missing']}.")
    if state["issues"]:
        lines.append(f"Fix these issues with revise_part: {state['issues']}. {READ_FIRST}")
    return " ".join(lines)


async def _submit(client: Client, draft_id: str) -> str:
    state = await tool_json(client, "read_draft", {"draft_id": draft_id})
    if state["missing"]:
        raise EngineIncompleteError(f"the writer left units without a part: {state['missing']}")
    if state["issues"]:
        raise EngineIncompleteError(f"the writer left issues: {state['issues']}")
    submitted = await tool_json(client, "submit_draft", {"draft_id": draft_id})
    return str(submitted["saved_as"])
