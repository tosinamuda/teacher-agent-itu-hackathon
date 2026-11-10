"""Composition root for content, and for the content engine's MCP server that serves it."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server import MCPServer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.artefacts.lesson_note.infrastructure.repository import SqlAlchemyLessonNotes
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_engine_learner_pack,
)
from app.domains.content.application.kinds import (
    ArtefactContent,
    ClassTestContent,
    ContentKind,
    LessonPlanContent,
    RevisionNoteContent,
)
from app.domains.content.application.note_reuse import NoteReuse
from app.domains.content.application.records import ContentRecords
from app.domains.content.application.service import ContentService
from app.domains.content.domain.types import BuiltIn
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.content_file import content_file, offers_file
from app.domains.content.infrastructure.download_links import (
    LIFETIME_SECONDS,
    issue,
    secret_from_environment,
)
from app.domains.content.infrastructure.generators import (
    ClassTestGenerator,
    LessonNoteGenerator,
    RevisionPackGenerator,
)
from app.domains.content.infrastructure.learner_notes import LearnerNotes
from app.domains.content.infrastructure.lesson_plans import PlanVersionFreezer
from app.domains.content.infrastructure.records import ClassTestItems, SqlAlchemyContentRecords
from app.domains.content.infrastructure.review import (
    AssessmentRelease,
    LifecycleApprover,
    RevisionConversation,
)
from app.domains.content_engine.application.comments import CommentDesk
from app.domains.content_engine.application.plugin_tools import StoredFile
from app.domains.content_engine.infrastructure.content import (
    SqlAlchemyEngineContent,
    SqlAlchemyPlanContent,
)
from app.domains.content_engine.infrastructure.engine import Engine
from app.domains.content_engine.infrastructure.generator import EngineGenerator
from app.domains.content_engine.infrastructure.harness.choice import loop_for
from app.domains.content_engine.infrastructure.learner_context import LessonLearners
from app.domains.content_engine.infrastructure.learner_generator import EngineLearnerGenerator
from app.domains.content_engine.infrastructure.live import LiveConversations
from app.domains.content_engine.infrastructure.plan_generator import PlanGenerator
from app.domains.content_engine.infrastructure.revision import EngineRevisionExecutor
from app.domains.content_engine.infrastructure.tool_calls import tool_caller
from app.domains.content_engine.infrastructure.tools import Source, mounted
from app.domains.content_engine.infrastructure.wiring import (
    build_draft_tools,
    build_drafting_service,
)
from app.domains.content_engine.mcp.content_file import ContentFiles
from app.domains.content_engine.mcp.server import build_content_mcp


def content_kinds(records: ContentRecords) -> dict[str, ContentKind]:
    """Each built-in type's handler, over the stores and gates it is decided through."""
    approver, approvals = LifecycleApprover(), ArtefactRepository()
    return {
        BuiltIn.REVISION_NOTE.value: RevisionNoteContent(
            approver, approvals, learner_notes=LearnerNotes()
        ),
        BuiltIn.LESSON_NOTE.value: ArtefactContent(approver, approvals),
        BuiltIn.CLASS_TEST.value: ClassTestContent(
            approver,
            approvals,
            questions=ClassTestItems(),
            release=AssessmentRelease(),
            records=records,
        ),
        BuiltIn.LESSON_PLAN.value: LessonPlanContent(PlanVersionFreezer()),
    }


#: The comments on content that the agent that wrote it is working on, for as long as the app runs.
COMMENT_DESK = CommentDesk(lambda: build_content_service(), AsyncSessionLocal)


def _issue_link(content_id: str, now: float) -> tuple[int, str] | None:
    secret = secret_from_environment()
    return issue(secret, content_id, now) if secret else None


async def made_file(db: AsyncSession, content_id: str) -> StoredFile:
    """The file the content's plugin makes of it, by the tool of the app's own server."""
    return await content_file(
        build_content_service(),
        build_content_catalogue(),
        tool_caller(build_content_mcp_server),
        db,
        content_id,
    )


def build_content_files() -> ContentFiles:
    return ContentFiles(
        build=made_file,
        offers=lambda db, record: offers_file(build_content_catalogue(), db, record),
        issue=_issue_link,
        lifetime_minutes=LIFETIME_SECONDS // 60,
    )


def build_content_mcp_server() -> MCPServer:
    return build_content_mcp(
        drafting=build_drafting_service,
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=AsyncSessionLocal,
        comments=COMMENT_DESK,
        tools=build_draft_tools(),
        content_files=build_content_files(),
    )


@asynccontextmanager
async def external_servers(type_slug: str) -> AsyncIterator[list[Source]]:
    """The external servers the type's current spec lists, connected for one run."""
    async with AsyncSessionLocal() as db:
        spec = await build_content_catalogue().current(db, type_slug)
    async with mounted(spec.mcp) as sources:
        yield sources


def build_content_engine() -> Engine:
    """The engine over the MCP server in memory. The writer's model opens only when it writes."""
    loop = loop_for()
    return Engine(build_content_mcp_server, loop.writer, loop.checker, external_servers)


def build_engine_learner_generator() -> EngineLearnerGenerator:
    """Writes a learner note with the engine; the writer model opens when it writes."""
    pack = build_engine_learner_pack()
    return EngineLearnerGenerator(build_content_engine(), pack, LessonLearners(pack))


#: The conversations kept open between a thread's revision turns, for as long as the app runs.
LIVE_CONVERSATIONS = LiveConversations()
#: What happens in each chat: kept for the page to replay, and shown to whoever is watching.
CHAT_FEED = ChatFeed(AsyncSessionLocal)


def build_engine_revision_executor() -> EngineRevisionExecutor:
    """Revises content the engine built. Its model opens only when it writes."""
    return EngineRevisionExecutor(
        build_content_engine(),
        SqlAlchemyEngineContent(),
        build_content_catalogue(),
        LIVE_CONVERSATIONS,
        CHAT_FEED,
    )


def build_plan_revision_executor() -> EngineRevisionExecutor:
    """Revises a lesson plan, which the engine drafts. Its model opens only when it writes."""
    return EngineRevisionExecutor(
        build_content_engine(),
        SqlAlchemyPlanContent(),
        build_content_catalogue(),
        LIVE_CONVERSATIONS,
        CHAT_FEED,
        artefact_type="lesson_plan",
    )


async def _open_creation_chat(db: AsyncSession, content_id: str, key: str) -> str:
    """The content's own chat, for the agent kept under ``key``."""
    from app.domains.artefact_revision.infrastructure.wiring import (
        build_artefact_revision_service,
    )

    stored = await SqlAlchemyContentRecords().get(db, content_id)
    if stored is None:
        raise LookupError(f"content_not_found:{content_id}")
    service = build_artefact_revision_service(
        fallback=build_engine_revision_executor(), plans=build_plan_revision_executor()
    )
    chat = await service.open_creation_chat(
        db=db, artefact_type=stored.kind, subject_id=content_id, created_by=None, agent_key=key
    )
    return chat.chat_id


def build_plan_generator() -> PlanGenerator:
    """Drafts a lesson plan with the engine. Its model opens only when it writes."""
    return PlanGenerator(build_content_engine(), CHAT_FEED, _open_creation_chat)


def build_note_reuse() -> NoteReuse:
    """Copies a lesson note onto another plan with the same steps."""
    return NoteReuse(SqlAlchemyLessonNotes(), SqlAlchemyContentRecords())


def build_content_service() -> ContentService:
    """Generators open a model only when they generate, so building this opens none."""
    records = SqlAlchemyContentRecords()
    return ContentService(
        catalogue=build_content_catalogue(),
        records=records,
        kinds=content_kinds(records),
        generators={
            BuiltIn.REVISION_NOTE.value: RevisionPackGenerator(),
            BuiltIn.CLASS_TEST.value: ClassTestGenerator(),
            BuiltIn.LESSON_NOTE.value: LessonNoteGenerator(),
        },
        engine_kind=ArtefactContent(LifecycleApprover(), ArtefactRepository()),
        engine_generator=EngineGenerator(build_content_engine(), CHAT_FEED, _open_creation_chat),
        revisions=RevisionConversation(
            build_engine_revision_executor, build_plan_revision_executor
        ),
    )
