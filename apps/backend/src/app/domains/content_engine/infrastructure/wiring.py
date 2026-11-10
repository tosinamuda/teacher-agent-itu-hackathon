"""Composition root for drafting content, whatever its type."""

from __future__ import annotations

from collections.abc import Callable

from mcp.server import MCPServer

from app.domains.artefacts.lesson_note.infrastructure.repository import SqlAlchemyLessonNotes
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_engine_learner_pack,
)
from app.domains.assessments.application.item_reader import DspyItemReader
from app.domains.assessments.infrastructure.lesson_notes import ApprovedLessonNoteText
from app.domains.assessments.infrastructure.repository import ClassTestMaterials
from app.domains.content.domain.types import BuiltIn
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content_engine.additions import ADDERS
from app.domains.content_engine.application.content_destination import ContentDestination
from app.domains.content_engine.application.draft_tools import DraftTools
from app.domains.content_engine.application.drafting import DraftingService
from app.domains.content_engine.application.lesson_note_destination import LessonNoteDestination
from app.domains.content_engine.application.plan_destination import PlanDestination
from app.domains.content_engine.application.plan_review import PLAN_CHECK_TOOL, PlanReview
from app.domains.content_engine.application.plugin_tools import (
    plugin_tool_additions,
    plugin_tool_check,
)
from app.domains.content_engine.infrastructure.class_test_destination import ClassTestDestination
from app.domains.content_engine.infrastructure.class_test_reading import (
    SECOND_READING_TOOL,
    SecondReading,
)
from app.domains.content_engine.infrastructure.content import SqlAlchemyEngineContent
from app.domains.content_engine.infrastructure.drafts import SqlAlchemyDrafts
from app.domains.content_engine.infrastructure.drawings import TexDrawings
from app.domains.content_engine.infrastructure.learner_context import LessonLearners
from app.domains.content_engine.infrastructure.learner_revision_note_destination import (
    LearnerRevisionNoteDestination,
)
from app.domains.content_engine.infrastructure.lessons import SqlAlchemyLessons
from app.domains.content_engine.infrastructure.planning import LessonPlanning
from app.domains.content_engine.infrastructure.revision_note_destination import (
    RevisionNoteDestination,
)
from app.domains.content_engine.infrastructure.tool_calls import tool_caller
from app.domains.content_engine.rules import RULES


def build_draft_tools() -> DraftTools:
    reading = SecondReading(lambda: DspyItemReader(), ApprovedLessonNoteText())
    plan = PlanReview(LessonPlanning())
    return DraftTools(
        SqlAlchemyDrafts(),
        SqlAlchemyLessons(),
        RULES,
        ADDERS,
        {SECOND_READING_TOOL: reading.faults, PLAN_CHECK_TOOL: plan.faults},
    )


def _own_mcp_server() -> MCPServer:
    """The app's own MCP server, which a plugin's link to ``/mcp`` reaches inside this process."""
    from app.domains.content.infrastructure.wiring import (  # noqa: PLC0415  # imports this module
        build_content_mcp_server,
    )

    return build_content_mcp_server()


def build_drafting_service(
    own_mcp_server: Callable[[], MCPServer] = _own_mcp_server,
) -> DraftingService:
    """``own_mcp_server`` is the server a plugin's link to ``/mcp`` reaches inside this process."""
    content, planning = SqlAlchemyEngineContent(), LessonPlanning()
    catalogue = build_content_catalogue()
    learner_pack = build_engine_learner_pack()
    lessons = SqlAlchemyLessons()
    return DraftingService(
        catalogue=catalogue,
        drafts=SqlAlchemyDrafts(),
        lessons=lessons,
        planning=planning,
        content=content,
        destinations={
            BuiltIn.LESSON_PLAN.value: PlanDestination(planning),
            BuiltIn.LESSON_NOTE.value: LessonNoteDestination(SqlAlchemyLessonNotes()),
            BuiltIn.REVISION_NOTE.value: RevisionNoteDestination(),
            BuiltIn.CLASS_TEST.value: ClassTestDestination(ClassTestMaterials()),
        },
        engine_destination=ContentDestination(
            content, plugin_tool_additions(tool_caller(own_mcp_server))
        ),
        scripted_check=plugin_tool_check(catalogue, tool_caller(own_mcp_server)),
        drawings=TexDrawings(),
        learners=LessonLearners(learner_pack),
        learner_destinations={
            BuiltIn.REVISION_NOTE.value: LearnerRevisionNoteDestination(learner_pack)
        },
    )
