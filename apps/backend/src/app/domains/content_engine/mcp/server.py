"""The content engine over MCP: tools that write a draft part by part, and what they read.

Every type is drafted with the same tools. Starting and submitting a draft checks the caller
may make content for its lesson; the other tools work only on the caller's own drafts.
Approval is not here. Only a person approves content, in the app, so nothing an MCP client
does reaches a learner by itself.
"""

from __future__ import annotations

from collections.abc import Callable

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from mcp.server.transport_security import TransportSecuritySettings
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.routing import Route

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.errors import ContentError
from app.domains.content.application.records import ContentItem
from app.domains.content.application.service import ContentService
from app.domains.content_engine.application.comments import CommentDesk
from app.domains.content_engine.application.draft_tools import DraftTools
from app.domains.content_engine.application.draft_view import DraftView
from app.domains.content_engine.application.drafting import DraftingService, LessonRef
from app.domains.content_engine.files import BUILDERS
from app.domains.content_engine.mcp.caller import Caller, caller, permit, permit_planning
from app.domains.content_engine.mcp.comment_tools import add_comment_tools
from app.domains.content_engine.mcp.content_file import (
    ContentFiles,
    add_content_file,
    download_of,
)
from app.domains.content_engine.mcp.discovery_tools import add_discovery_tools
from app.domains.content_engine.mcp.draft_tools import add_draft_tools
from app.domains.content_engine.mcp.file_tools import add_file_tools
from app.domains.content_engine.mcp.refusals import Sessions, a_part, refusing
from app.domains.content_engine.mcp.skill_resources import add_skill_resources
from app.domains.content_engine.mcp.viewer import content_viewer
from app.domains.content_engine.mcp.views import Payload, as_payload, content_json, type_json

INSTRUCTIONS = """\
Write content of a registered type for one lesson, one part per unit.
1. Read content-types:// for the types and their specs. A type made from a plan version
   takes plan_version_id; a lesson plan is made from its lesson period and takes session_id.
2. start_draft(type, plan_version_id or session_id) opens a draft. Pass source to write from
   a document, such as a teacher's own plan. It returns the brief, the units, the part
   schema for each kind of unit, and lesson_uri: read it, or call read_lesson(draft_id), for
   what the lesson is. list_content_types lists what can be written, and find_lessons(query)
   finds a teacher's lessons by topic, week or class.
3. Write one part per unit with add_part; each part must match its unit's schema. Change a
   part with revise_part. Each returns what is still missing and, once nothing is, the
   issues that stop the draft being saved.
4. submit_draft saves it for the teacher to review. A teacher approves it in the app.
5. show_draft(draft_id) and show_content(content_id) show it; hosts with MCP Apps draw a page.
6. Saved content whose type has a file, such as a slide deck, comes back from submit_draft with
   its download. Read the resource content://{content_id}/file, or call
   get_content_file_link(content_id) for a link the teacher opens to download it.

A type's spec pins the skills its content is written with, and a draft's brief carries them.
Read skills:// for every skill (skills://?search=working to narrow it), and skill://{slug} for one.
plugin-skills://{type} holds the skill files of the plugin that made a type.
"""


async def _signed_in(db: AsyncSession, ctx: Context) -> Caller:
    return await caller(db, ctx.headers)


def build_content_mcp(
    *,
    drafting: Callable[[], DraftingService],
    content: Callable[[], ContentService],
    catalogue: Callable[[], ContentCatalogue],
    sessions: Sessions,
    comments: CommentDesk | None = None,
    content_files: ContentFiles | None = None,
    tools: DraftTools | None = None,
) -> MCPServer:
    """The server, over services built per call so each call opens only what it uses.

    With ``comments``, a client can comment on content and read the conversation about it.
    With ``content_files``, a client can take content whose type has a file as that file.
    With ``tools``, a plugin can have its type's drafts checked and finished by the tools it lists.
    """
    viewer = content_viewer(
        lambda content_id, ctx: _read_content(
            content, catalogue, sessions, content_id, ctx, ToolError
        ),
        lambda draft_id, ctx: _read_draft(drafting, sessions, draft_id, ctx),
    )
    server = MCPServer("plan-to-tutor-content", instructions=INSTRUCTIONS, extensions=[viewer])
    _add_tools(server, drafting, content, sessions, content_files)
    _add_resources(
        server, drafting=drafting, content=content, catalogue=catalogue, sessions=sessions
    )
    add_skill_resources(server, catalogue, sessions)
    add_discovery_tools(server, drafting, catalogue, sessions)
    if comments is not None:
        add_comment_tools(server, content, comments, sessions)
    if content_files is not None:
        add_content_file(server, content, sessions, content_files)
    add_file_tools(server, content, sessions, BUILDERS)
    if tools is not None:
        add_draft_tools(server, tools, sessions)
    return server


def http_route(server: MCPServer, path: str) -> Route:
    """The server as one stateless HTTP route that answers in JSON.

    Every tool and resource checks the caller's access code, and the API answers at its
    public hostnames, so the SDK's localhost-only host check is off.
    """
    endpoint = server.streamable_http_app(
        streamable_http_path=path,
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )
    return Route(path, endpoint, methods=["GET", "POST", "DELETE"])


async def _permit_lesson(db: AsyncSession, signed_in: Caller, lesson: LessonRef) -> None:
    """Refuse a lesson the caller may not make content for."""
    if lesson.session_id is not None:
        await refusing(permit_planning(db, signed_in, lesson.session_id))
    else:
        await refusing(permit(db, signed_in, "create", plan_version_id=lesson.plan_version_id))


def _lesson_of(view: DraftView) -> LessonRef:
    return LessonRef(view.draft.plan_version_id, view.draft.session_id, view.draft.student_id)


def _add_tools(
    server: MCPServer,
    drafting: Callable[[], DraftingService],
    content: Callable[[], ContentService],
    sessions: Sessions,
    content_files: ContentFiles | None,
) -> None:
    @server.tool()
    async def start_draft(
        type: str,
        ctx: Context,
        plan_version_id: str | None = None,
        session_id: str | None = None,
        source: str | None = None,
        content_id: str | None = None,
        student_id: str | None = None,
        generator: str | None = None,
    ) -> Payload:
        """Open a draft of a content type for a lesson.

        Give plan_version_id for a type made from a plan version, or session_id for a lesson
        plan, which is made from its lesson period. Pass source to write from a document, and
        content_id to revise that content: the draft starts with its parts. Pass student_id to
        write the content for one learner, from the lesson's plan_version_id; the result then
        names learner_uri, the resource to read the learner from. Pass generator to write with a
        generator that is not the type's default. Returns the draft
        ID, the brief, the units to write one part each for, the JSON Schema of each kind of
        unit's part, and lesson_uri, the resource to read the lesson from.
        """
        lesson = LessonRef(plan_version_id, session_id, student_id)
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            await _permit_lesson(db, signed_in, lesson)
            view = await refusing(
                drafting().start(
                    db,
                    type=type,
                    lesson=lesson,
                    created_by=signed_in.by,
                    author=signed_in.author,
                    source=source or "",
                    content_id=content_id,
                    generator=generator,
                )
            )
            return as_payload(view.as_json())

    async def _put(
        draft_id: str, unit_id: str, part: Payload | str, ctx: Context, *, replace: bool
    ) -> Payload:
        part = a_part(part)
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            stored = await refusing(
                drafting().put(
                    db,
                    draft_id=draft_id,
                    unit_id=unit_id,
                    part=part,
                    replace=replace,
                    by=signed_in.by,
                )
            )
            return as_payload(stored)

    @server.tool()
    async def add_part(draft_id: str, unit_id: str, part: Payload | str, ctx: Context) -> Payload:
        """Write the part for one unit of the draft. It must match its unit's part schema.

        Returns the part as stored, the units still missing, and, once none is, the issues
        that stop the draft being saved.
        """
        return await _put(draft_id, unit_id, part, ctx, replace=False)

    @server.tool()
    async def revise_part(
        draft_id: str, unit_id: str, part: Payload | str, ctx: Context
    ) -> Payload:
        """Replace the part already written for one unit, as add_part writes one.

        The new part replaces the old one whole, so send every field of it: read the draft, and
        send the part as it stands with your change made. A part that holds only what you
        changed is refused for what it leaves out.
        """
        return await _put(draft_id, unit_id, part, ctx, replace=True)

    @server.tool()
    async def read_draft(draft_id: str, ctx: Context, fields: list[str] | None = None) -> Payload:
        """The draft: its brief, units, parts so far, what is missing, and its issues.

        It is long. Name the ``fields`` you need, such as ["parts", "missing", "issues"], to
        get only those; the draft_id is always there. The fields are brief, units, missing,
        issues, parts, part_schemas and pinned_skills.
        """
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            view = await refusing(drafting().read(db, draft_id=draft_id, by=signed_in.by))
            whole = as_payload(view.as_json())
            if fields is None:
                return whole
            return {
                name: value for name, value in whole.items() if name == "draft_id" or name in fields
            }

    @server.tool()
    async def locate_text(draft_id: str, text: str, ctx: Context) -> Payload:
        """Find where text the teacher selected is in the draft.

        Returns the unit and the path of each field of a part that holds the text, the line of
        the field it is on when the field has several, and the text around it. Use it when the
        teacher pointed at text without saying where it is, then revise that unit's part.
        No match means the text is not in any part: it may be drawn by the page, such as a
        heading made from the lesson's own details.
        """
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            found = await refusing(
                drafting().locate(db, draft_id=draft_id, text=text, by=signed_in.by)
            )
            return {
                "count": len(found),
                "matches": [
                    {
                        "unit_id": p.unit_id,
                        "path": p.path,
                        **({"line": p.line} if p.line else {}),
                        "context": p.context,
                    }
                    for p in found
                ],
            }

    @server.tool()
    async def submit_draft(draft_id: str, ctx: Context) -> Payload:
        """Save the finished draft for the teacher to review and approve in the app.

        Saved content that has a file comes back with its download: the resource and a link.
        """
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            service = drafting()
            view = await refusing(service.read(db, draft_id=draft_id, by=signed_in.by))
            await _permit_lesson(db, signed_in, _lesson_of(view))
            saved_as = await refusing(service.submit(db, draft_id=draft_id, by=signed_in.by))
            saved: Payload = {
                "type": view.draft.type,
                "saved_as": saved_as,
                "review_status": "pending",
            }
            made = await content().find_record(db, saved_as)
            if content_files is not None and made and await content_files.offers(db, made):
                saved["download"] = download_of(ctx.headers, saved_as, content_files)
            return saved


def _add_resources(
    server: MCPServer,
    *,
    drafting: Callable[[], DraftingService],
    content: Callable[[], ContentService],
    catalogue: Callable[[], ContentCatalogue],
    sessions: Sessions,
) -> None:
    @server.resource("content-types://{?engine}", mime_type="application/json")
    async def content_types(ctx: Context, engine: str | None = None) -> list[Payload]:
        """Every content type with its current spec; ``?engine=mcp`` lists the engine's."""
        async with sessions() as db:
            await refusing(permit(db, await _signed_in(db, ctx), "read"), ResourceError)
            return [
                as_payload(type_json(t, spec))
                for t, spec in await catalogue().types(db)
                if engine is None or t.engine.value == engine
            ]

    @server.resource("content-type://{type}", mime_type="application/json")
    async def content_type(type: str, ctx: Context) -> Payload:
        """One content type with its current spec and part schema."""
        async with sessions() as db:
            await refusing(permit(db, await _signed_in(db, ctx), "read"), ResourceError)
            types = catalogue()
            definition = await refusing(types.type(db, type), ResourceError)
            spec = await refusing(types.current(db, type), ResourceError)
            return as_payload(type_json(definition, spec))

    @server.resource("lesson://{plan_version_id}", mime_type="application/json")
    async def lesson(plan_version_id: str, ctx: Context) -> Payload:
        """What a writer may read about a lesson: its plan and its approved lesson note."""
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            await refusing(
                permit(db, signed_in, "read", plan_version_id=plan_version_id), ResourceError
            )
            return as_payload(await refusing(drafting().lesson(db, plan_version_id), ResourceError))

    @server.resource("learner://{draft_id}", mime_type="application/json")
    async def learner(draft_id: str, ctx: Context) -> Payload:
        """The learner a draft is made for: the class note to adapt and the learner's state."""
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            return as_payload(
                await refusing(
                    drafting().learner(db, draft_id=draft_id, by=signed_in.by), ResourceError
                )
            )

    @server.resource("lesson-period://{session_id}", mime_type="application/json")
    async def lesson_period(session_id: str, ctx: Context) -> Payload:
        """A lesson period without a plan yet: its subject, topic and curriculum objectives."""
        async with sessions() as db:
            signed_in = await _signed_in(db, ctx)
            await refusing(permit_planning(db, signed_in, session_id), ResourceError)
            return as_payload(
                await refusing(drafting().lesson_period(db, session_id), ResourceError)
            )

    @server.resource("content://{content_id}", mime_type="application/json")
    async def content_item(content_id: str, ctx: Context) -> Payload:
        """Content and its review status."""
        return await _read_content(content, catalogue, sessions, content_id, ctx, ResourceError)


async def _built_with(
    catalogue: ContentCatalogue, db: AsyncSession, item: ContentItem
) -> ContentSpecification | None:
    """The spec revision an engine item was built with; none for content with no sections."""
    given = item.record.provenance.get("specification")
    revision = given.get("revision") if isinstance(given, dict) else None
    if not isinstance(revision, int) or "sections" not in item.content:
        return None
    try:
        return await catalogue.revision(db, item.record.type, revision)
    except ContentError:
        return None


async def _read_content(
    content: Callable[[], ContentService],
    catalogue: Callable[[], ContentCatalogue],
    sessions: Sessions,
    content_id: str,
    ctx: Context,
    raising: type[Exception],
) -> Payload:
    """One content item, if the caller may read its lesson's content."""
    async with sessions() as db:
        signed_in = await _signed_in(db, ctx)
        service = content()
        record = await refusing(service.record(db, content_id), raising)
        await refusing(
            permit(db, signed_in, "read", plan_version_id=record.plan_version_id), raising
        )
        item = await service.get(db, content_id)
        return as_payload(content_json(item, await _built_with(catalogue(), db, item)))


async def _read_draft(
    drafting: Callable[[], DraftingService], sessions: Sessions, draft_id: str, ctx: Context
) -> Payload:
    """A draft as the viewer draws its type, as it would save so far; only its writer sees it."""
    async with sessions() as db:
        signed_in = await _signed_in(db, ctx)
        preview = await refusing(drafting().preview(db, draft_id=draft_id, by=signed_in.by))
        return {
            "content_id": preview.draft.draft_id,
            "type": preview.draft.type,
            "plan_version_id": preview.draft.plan_version_id,
            "version": None,
            "review_status": preview.status(),
            "content": preview.content,
        }
