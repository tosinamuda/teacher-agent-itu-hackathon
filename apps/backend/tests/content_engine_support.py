"""A lesson with an approved note, a registered engine type, and the engine's MCP server."""

from __future__ import annotations

import contextvars
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp import Client
from mcp.server import MCPServer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.domain.skills import Skill
from app.domains.content.domain.types import Audience
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.wiring import build_content_files, build_content_service
from app.domains.content_engine.infrastructure.engine import Engine, Externals
from app.domains.content_engine.infrastructure.tools import WRITER_TOOLS, Source, tools_server
from app.domains.content_engine.infrastructure.wiring import (
    build_draft_tools,
    build_drafting_service,
)
from app.domains.content_engine.mcp.server import build_content_mcp
from app.shared.json_types import JsonObject, JsonValue
from migrations.data.content_registry_seed import seed_content_registry

PLAN = "LPV-ENGINE-1"
TYPE = "worked-examples"
PARTS: list[JsonValue] = [
    {"name": "title", "description": "A heading for the learner", "type": "text"},
    {
        "name": "examples",
        "description": "Worked examples, each solved step by step",
        "type": "items",
        "fields": [
            {"name": "problem", "description": "The problem", "type": "markdown"},
            {"name": "solution", "description": "The working and answer", "type": "markdown"},
        ],
    },
]
SPEC: JsonObject = {
    "material": "worked examples for one step of the lesson",
    "audience": "{reader} revising at home",
    "levels": ["class_level"],
    "requirements": ["Show every step of the working."],
    "unit": "plan_step",
    "parts": PARTS,
}
SESSION_PLAN: JsonObject = {
    "subject": "Mathematics",
    "grade": "JSS1",
    "topic": "Fractions",
    "title": "Adding fractions",
    "lesson_plan_objectives": [
        {
            "lesson_objective_id": "lop01",
            "objective_text": "Add fractions with a common denominator",
        }
    ],
    "steps": [
        {"step_id": "s1", "step_kind": "core", "lesson_objective_id": "lop01", "title": "Same"},
        {"step_id": "s2", "step_kind": "core", "lesson_objective_id": "lop01", "title": "Mixed"},
    ],
}
NOTE_S1 = "Keep the denominator; add the numerators."


def part(title: str) -> JsonObject:
    return {"title": title, "examples": [{"problem": "1/4 + 2/4", "solution": "3/4"}]}


async def seed_lesson(
    db: AsyncSession,
    *,
    concluded: bool = False,
    skills: tuple[str, ...] = (),
    new_skills: tuple[Skill, ...] = (),
    mcp: tuple[JsonObject, ...] = (),
) -> None:
    """The lesson and its type; ``skills`` are the skills the type's spec pins.

    ``new_skills`` are added to the library first, so a spec can pin a skill the seed lacks.
    """
    await (await db.connection()).run_sync(seed_content_registry)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            PlanVersion(
                version_id=PLAN,
                plan_id="P-ENGINE-1",
                source_type="experiment_manual",
                session_plan=SESSION_PLAN,
                status=PlanVersionStatus.APPROVED,
            ),
            Artefact(
                artefact_id="AT-NOTE-1",
                artefact_type="lesson_note",
                scope=ArtefactScope.CLASS_LEVEL.value,
                plan_version_id=PLAN,
                manifest={
                    "artefact_type": "lesson_note",
                    "plan_version_id": PLAN,
                    "sections": [{"step_id": "s1", "body": NOTE_S1}],
                },
                artefact_refs={"origin": "teacher"},
                review_status=ArtefactReviewStatus.APPROVED,
            ),
        ]
    )
    await db.flush()
    for skill in new_skills:
        await build_content_catalogue().skills.add(db, skill, None)
    pinned: JsonObject = {}
    if skills:
        pinned["skills"] = [{"skill": slug, "revision": 1} for slug in skills]
    if mcp:
        pinned["mcp"] = list(mcp)
    await build_content_catalogue().register(
        db,
        slug=TYPE,
        label="Worked examples",
        audience=Audience.LEARNER,
        made_from_a_plan_version=True,
        spec_fields=SPEC | pinned,
        created_by="Researcher",
    )
    if concluded:
        await db.execute(
            text("UPDATE plan_versions SET concluded_at = NOW() WHERE version_id = :v"), {"v": PLAN}
        )


@asynccontextmanager
async def writer_client(client: Client) -> AsyncIterator[Client]:
    """The client a writer is given for a draft with no external servers: its three tools."""
    server = tools_server(
        [Source(client, frozenset(WRITER_TOOLS))],
        opened_in=contextvars.copy_context(),
        skills_from=client,
    )
    async with Client(server) as offered:
        yield offered


def server_over(db: AsyncSession) -> MCPServer:
    """The engine's server, every call on the test's own session."""

    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    return build_content_mcp(
        drafting=lambda: build_drafting_service(lambda: server_over(db)),
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
        tools=build_draft_tools(),
        content_files=build_content_files(),
    )


class ScriptedWriter:
    """Writes as a model would, through the MCP tools, from a script of parts.

    ``script`` maps a unit to the parts to try in order; a refused part is followed by the
    next, the way a model corrects itself after reading the tool's error.
    """

    def __init__(self, script: dict[str, list[object]], *, revise: bool = False) -> None:
        self.script = script
        self.revise = revise
        self.seen: dict[str, object] = {}
        self.refusals: list[str] = []

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        self.seen = {"draft": draft, "lesson": lesson, "feedback": feedback}
        tool = "revise_part" if self.revise else "add_part"
        for unit_id, attempts in self.script.items():
            for attempt in attempts:
                result = await client.call_tool(
                    tool, {"draft_id": draft["draft_id"], "unit_id": unit_id, "part": attempt}
                )
                if not result.is_error:
                    break
                self.refusals.append(result.content[0].text)  # type: ignore[union-attr]
        return f"Wrote {len(self.script)} part(s)."


def engine_over(
    db: AsyncSession, writer: ScriptedWriter, externals: Externals | None = None
) -> Engine:
    return Engine(lambda: server_over(db), lambda: writer, externals=externals)
