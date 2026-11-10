"""A lesson held in memory, and the content server that drafts its plan.

The lesson-plan checks and the draft tools are the real ones; only the lesson's lookup and the
plan's saving are held in memory, so a test needs no curriculum rows.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from mcp.server import MCPServer
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.manual_check import check_manual_plan
from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.domain.plan_sections import split_plan
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.content.domain.types import BuiltIn
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.wiring import build_content_files, build_content_service
from app.domains.content_engine.application.content_destination import ContentDestination
from app.domains.content_engine.application.draft_tools import DraftTools
from app.domains.content_engine.application.drafting import DraftingService
from app.domains.content_engine.application.plan_destination import PlanDestination
from app.domains.content_engine.application.plan_review import PLAN_CHECK_TOOL, PlanReview
from app.domains.content_engine.application.planning_ports import (
    PlanLesson,
    PlanRecord,
    PlanRefusedError,
)
from app.domains.content_engine.application.plugin_tools import plugin_tool_check
from app.domains.content_engine.infrastructure.content import SqlAlchemyEngineContent
from app.domains.content_engine.infrastructure.drafts import SqlAlchemyDrafts
from app.domains.content_engine.infrastructure.drawings import TexDrawings
from app.domains.content_engine.infrastructure.lessons import SqlAlchemyLessons
from app.domains.content_engine.infrastructure.tool_calls import tool_caller
from app.domains.content_engine.mcp.server import build_content_mcp
from app.shared.json_types import JsonObject
from migrations.data.content_registry_seed import seed_content_registry

LESSON = "00000000-0000-0000-0000-000000000901"
DOCUMENT = """Lesson: Adding fractions (JSS1, week 8)
Objective: pupils add fractions that share a denominator.
Starter (5 min): ask what 1/4 means.
Main (20 min): keep the denominator, add the numerators.
Model 1/4 + 2/4 = 3/4. Pupils try 2/5 + 1/5.
Check (10 min): 3/8 + 2/8.
"""
#: The plan's parts as a writer sends them: the lesson's own part, then each curriculum
#: objective's, by unit ID.
SECTIONS: dict[str, JsonObject] = json.loads(
    (Path(__file__).parent / "fixtures" / "plan_import" / "fraction_sections.json").read_text()
)
PLAN_TYPE = BuiltIn.LESSON_PLAN.value
CONTEXT = SessionContext(
    session_id=LESSON,
    subject="Mathematics",
    track="General",
    grade="JSS1",
    term="First Term",
    week=8,
    day_index=1,
    topic="Fractions",
    subtopic="Addition of fractions",
    duration_minutes=40,
    session_objectives=[],
    general_objectives=[],
    reference_materials=[],
    performance_objectives=["add fractions with a common denominator"],
)


class InMemoryPlanning:
    """The lesson in memory, the real checks, and the saved plans kept for the test."""

    def __init__(self) -> None:
        self.saved: list[tuple[str, JsonObject, str | None]] = []
        self.source_types: list[str] = []
        self.generators: list[JsonObject] = []
        #: The plans saved, by plan ID, each at its latest version.
        self.plans: dict[str, tuple[str, JsonObject]] = {}
        self.revised: list[JsonObject] = []

    async def lesson(self, db: AsyncSession, session_id: str) -> PlanLesson | None:
        if session_id != LESSON:
            return None
        curriculum = SessionContextPayloadBuilder().build(CONTEXT).curriculum_scope
        return PlanLesson(
            LESSON,
            {"subject": "Mathematics", "grade": "JSS1", "subtopic": "Addition of fractions"},
            list(curriculum.curriculum_objectives),
        )

    async def current(self, db: AsyncSession, plan_id: str) -> PlanRecord | None:
        if plan_id not in self.plans:
            return None
        version_id, content = self.plans[plan_id]
        lesson, sections = split_plan(content)
        return PlanRecord(plan_id, LESSON, version_id, lesson, sections)

    async def revise(
        self,
        db: AsyncSession,
        plan_id: str,
        session_id: str,
        content: JsonObject,
        *,
        generator: JsonObject,
    ) -> str:
        issues = await self.issues(db, session_id, content, strict=True)
        if issues:
            raise PlanRefusedError(issues)
        version_id, saved = self.plans[plan_id]
        if split_plan(saved) == split_plan(content):
            return version_id
        self.revised.append(content)
        self.generators.append(generator)
        self.plans[plan_id] = (f"LPV-REVISED-{len(self.revised)}", content)
        return self.plans[plan_id][0]

    async def issues(
        self, db: AsyncSession, session_id: str, content: JsonObject, *, strict: bool = False
    ) -> JsonObject:
        return check_manual_plan(CONTEXT, content, strict=strict).issues

    async def save(
        self,
        db: AsyncSession,
        session_id: str,
        content: JsonObject,
        author: str | None,
        *,
        source_type: str,
        generator: JsonObject,
    ) -> str:
        issues = await self.issues(db, session_id, content)
        if issues:
            raise PlanRefusedError(issues)
        self.saved.append((session_id, content, author))
        self.source_types.append(source_type)
        self.generators.append(generator)
        self.plans[f"LP-IMPORTED-{len(self.saved)}"] = (f"LPV-IMPORTED-{len(self.saved)}", content)
        return f"LPV-IMPORTED-{len(self.saved)}"


async def seed_types(db: AsyncSession) -> None:
    await (await db.connection()).run_sync(seed_content_registry)


def drafting_over(db: AsyncSession, planning: InMemoryPlanning) -> DraftingService:
    content, catalogue = SqlAlchemyEngineContent(), build_content_catalogue()
    return DraftingService(
        catalogue=catalogue,
        drafts=SqlAlchemyDrafts(),
        lessons=SqlAlchemyLessons(),
        planning=planning,
        content=content,
        destinations={PLAN_TYPE: PlanDestination(planning)},
        engine_destination=ContentDestination(content),
        drawings=TexDrawings(),
        scripted_check=plugin_tool_check(catalogue, tool_caller(lambda: plan_server(db, planning))),
    )


def plan_server(db: AsyncSession, planning: InMemoryPlanning) -> MCPServer:
    """The content server over the lesson in memory, every call on the test's own session."""

    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    return build_content_mcp(
        drafting=lambda: drafting_over(db, planning),
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
        tools=DraftTools(
            SqlAlchemyDrafts(),
            SqlAlchemyLessons(),
            {},
            {},
            {PLAN_CHECK_TOOL: PlanReview(planning).faults},
        ),
        content_files=build_content_files(),
    )
