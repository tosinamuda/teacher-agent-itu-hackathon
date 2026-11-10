"""Arm B: the content engine writing the same note, as a type registered for this run only.

The type, its spec, the draft and the content live in one transaction that is rolled back
when the arm ends, so the engine runs exactly as it does for any registered type and
nothing it stores outlives the run.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass, replace
from pathlib import Path
from time import perf_counter

import dspy
from mcp import Client
from mcp.server import MCPServer
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.concluded_record import is_concluded
from app.db.session import engine as db_engine
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.types import Audience, ContentTypeDefinition
from app.domains.content.domain.types import Engine as TypeEngine
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.content.plugins.reader import folder_digest, read_plugins
from app.domains.content_engine.application.content_destination import ContentDestination
from app.domains.content_engine.application.drafting import DraftingService
from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.content import SqlAlchemyEngineContent
from app.domains.content_engine.infrastructure.drafts import SqlAlchemyDrafts
from app.domains.content_engine.infrastructure.drawings import TexDrawings
from app.domains.content_engine.infrastructure.engine import (
    Engine,
    EngineIncompleteError,
    Request,
    Writer,
)
from app.domains.content_engine.infrastructure.harness.choice import (
    EngineLoop,
    SkillsMode,
    loop_for,
)
from app.domains.content_engine.infrastructure.lessons import SqlAlchemyLessons
from app.domains.content_engine.infrastructure.planning import LessonPlanning
from app.domains.content_engine.infrastructure.writer import WriterStoppedError
from app.domains.content_engine.mcp.server import build_content_mcp
from app.domains.generation_log.application.recorder import log_context
from app.domains.generation_log.application.spend import Spend, metered
from app.shared.json_types import JsonObject, JsonValue
from app.shared.llm_markup import reader_ready
from app.shared.session_plan_view import SessionPlanView

#: The plugin the engine writes lesson notes with when a run names no other, and the generator
#: of it a run uses. A plugin folder may hold several, so a run names which.
PLUGIN = Path(__file__).resolve().parents[4] / "plugins" / "lesson-note"
GENERATOR = "lesson-note-writer"
#: The type the generator is installed under for a run: it is rolled back with the run.
RUN_TYPE = "lesson-note-comparison"


def without_blocks(plan: SessionPlanView) -> SessionPlanView:
    """The plan with each step's blocks taken out, leaving its title, summary and activities."""
    return plan.model_copy(
        update={"steps": [step.model_copy(update={"blocks": []}) for step in plan.steps]}
    )


class PlanOnlyLessons(SqlAlchemyLessons):
    """The lesson without its approved note, which arm A never reads either.

    With ``blocks`` false the plan's steps lose their blocks too, as arm A's do.
    """

    def __init__(self, *, blocks: bool = True) -> None:
        self._blocks = blocks

    async def plan(self, db: AsyncSession, plan_version_id: str) -> SessionPlanView | None:
        plan = await super().plan(db, plan_version_id)
        return plan if plan is None or self._blocks else without_blocks(plan)

    async def approved_note_sections(
        self, db: AsyncSession, plan_version_id: str
    ) -> dict[str, str]:
        return {}


@asynccontextmanager
async def _rolled_back() -> AsyncIterator[AsyncSession]:
    """One session whose commits are savepoints inside a transaction that is rolled back."""
    async with db_engine.connect() as connection:
        outer = await connection.begin()
        session = async_sessionmaker(
            bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )()
        try:
            yield session
        finally:
            await session.close()
            await outer.rollback()


def _server(db: AsyncSession, *, blocks: bool) -> MCPServer:
    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    def drafting() -> DraftingService:
        content = SqlAlchemyEngineContent()
        return DraftingService(
            catalogue=build_content_catalogue(),
            drafts=SqlAlchemyDrafts(),
            lessons=PlanOnlyLessons(blocks=blocks),
            planning=LessonPlanning(),
            content=content,
            destinations={},
            engine_destination=ContentDestination(content),
            drawings=TexDrawings(),
        )

    return build_content_mcp(
        drafting=drafting,
        content=build_content_service,
        catalogue=build_content_catalogue,
        sessions=same_session,
    )


async def _writable(db: AsyncSession, plan_version_id: str) -> str:
    """The plan version the engine may draft against: itself, or a copy of a concluded one.

    A concluded lesson's record takes no new content, even in a transaction that is rolled
    back, so the engine drafts against an open copy of its plan that the rollback removes.
    """
    if not await is_concluded(db, plan_version_id):
        return plan_version_id
    source = await db.scalar(select(PlanVersion).where(PlanVersion.version_id == plan_version_id))
    assert source is not None
    copy_id = f"{plan_version_id}-COPY"
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        PlanVersion(
            version_id=copy_id,
            plan_id=f"{source.plan_id}-COPY",
            source_type=source.source_type,
            session_plan=source.session_plan,
            status=source.status,
        )
    )
    await db.flush()
    return copy_id


@dataclass
class _Rounds:
    """The writer, counting the rounds the engine runs it on one draft."""

    writer: Writer
    count: int = 0

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        self.count += 1
        return await self.writer.write(client, draft, lesson, feedback=feedback)


@dataclass(frozen=True)
class EngineRun:
    """Each step's note as markdown, by step ID, and what writing them took."""

    notes: dict[str, str]
    measures: JsonObject


def _measures(
    harness: EngineLoop, skills: SkillsMode, rounds: _Rounds, spend: Spend, seconds: float
) -> JsonObject:
    return {
        "harness": harness.value,
        "skills": skills.value,
        "rounds": rounds.count,
        "calls": spend.calls,
        "prompt_tokens": spend.prompt_tokens,
        "completion_tokens": spend.completion_tokens,
        "seconds": round(seconds, 1),
    }


async def _register(db: AsyncSession, chosen: JsonObject) -> None:
    await build_content_catalogue().register(
        db,
        slug=str(chosen["type"]),
        label=str(chosen["label"]),
        audience=Audience(str(chosen["audience"])),
        made_from_a_plan_version=True,
        spec_fields=chosen["spec"],
        created_by="lesson-note-comparison",
    )


async def _install(db: AsyncSession, folder: Path, generator: str) -> str:
    """Install the folder's named generator as a type of this run's own; its slug."""
    plugins, problems = read_plugins(folder)
    writer = next((plugin for plugin in plugins if plugin.name == generator), None)
    if writer is None:
        raise SystemExit(
            "\n".join(str(problem) for problem in problems) or f"no {generator} in {folder}"
        )
    definition = ContentTypeDefinition(
        slug=RUN_TYPE,
        kind=ContentTypeDefinition.kind_for(RUN_TYPE),
        label="Lesson note (comparison)",
        audience=Audience.TEACHER,
        engine=TypeEngine.MCP,
        made_from_a_plan_version=True,
        position=0,
    )
    as_type = replace(writer, name=RUN_TYPE, definition=definition, implements=None)
    installer = PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins())
    await installer.install(db, as_type, folder_digest(folder), "lesson-note-comparison")
    return RUN_TYPE


async def engine_notes(
    plan: SessionPlanView,
    plan_version_id: str,
    lm: dspy.BaseLM,
    *,
    candidate: JsonObject | None = None,
    plugin: Path = PLUGIN,
    generator: str = GENERATOR,
    blocks: bool = True,
    harness: EngineLoop = EngineLoop.DSPY,
    skills: SkillsMode = SkillsMode.PINNED,
    prepare: Callable[[AsyncSession], Awaitable[None]] | None = None,
) -> EngineRun:
    """The notes written on ``harness``'s loop, with the type of ``plugin`` or of ``candidate``.

    ``candidate`` is a type and spec written as JSON, for the older ablations.

    A draft the engine could not finish is recorded as such, with no notes, rather than
    stopping the run: whether a loop finishes its drafts is one of the things measured.
    ``prepare`` runs first in the transaction, such as to seed a lesson a trace writes.
    """
    loop, started = loop_for(harness, lm=lm, skills=skills), perf_counter()
    async with _rolled_back() as db:
        if prepare is not None:
            await prepare(db)
        if candidate is not None:
            await _register(db, candidate)
            slug = str(candidate["type"])
        else:
            slug = await _install(db, plugin, generator)
        with (
            log_context(
                kind="lesson_note_comparison",
                arm="engine",
                harness=harness.value,
                skills=skills.value,
                correlation_id=plan_version_id,
            ),
            metered() as spend,
        ):
            writable = await _writable(db, plan_version_id)
            rounds = _Rounds(loop.writer())
            engine = Engine(lambda: _server(db, blocks=blocks), lambda: rounds, loop.checker)
            try:
                built = await engine.build(Request(slug, plan_version_id=writable))
            except (EngineIncompleteError, WriterStoppedError, CheckerStoppedError) as error:
                failed = _measures(harness, skills, rounds, spend, perf_counter() - started)
                return EngineRun(
                    {step.step_id: "" for step in plan.steps}, failed | {"failure": str(error)}
                )
    measures = _measures(harness, skills, rounds, spend, perf_counter() - started)
    return EngineRun(_notes(built.content), measures | {"failure": None})


def _notes(content: JsonObject) -> dict[str, str]:
    sections = content["sections"]
    assert isinstance(sections, list)
    return {
        str(section["unit_id"]): note_markdown(section["part"])
        for section in sections
        if isinstance(section, dict) and isinstance(section["part"], dict)
    }


def _entries(value: JsonValue) -> list[JsonObject]:
    return [entry for entry in value if isinstance(entry, dict)] if isinstance(value, list) else []


def _solution(example: JsonObject) -> str:
    lines = [
        f"{step['working']}  \n*{step['commentary']}*" for step in _entries(example.get("solution"))
    ]
    return "\n\n".join([*lines, f"**Answer:** {example['answer']}"])


def _figures(part: JsonObject) -> list[str]:
    """Each drawing under its caption: the caption is tidied, the TikZ stays as it was drawn."""
    shown = []
    for number, figure in enumerate(_entries(part.get("figures")), start=1):
        caption = reader_ready(f"**Figure {number}.** {figure['caption']}")
        shown.append(f"{caption}\n\n\\begin{{center}}\n{figure['drawing']}\n\\end{{center}}")
    return shown


def note_markdown(part: JsonObject) -> str:
    """One step's note: explanation, figures, worked examples with solutions, then classwork.

    Only the text is tidied for the reader; a drawing is TikZ and goes out as it was checked.
    """
    text = [str(part["explanation"])] if part.get("explanation") else []
    for number, example in enumerate(_entries(part.get("worked_examples")), start=1):
        text.append(
            f"#### Example {number}.\n\n{example['problem']}\n\n"
            f"**Solution**\n\n{_solution(example)}"
        )
    classwork = _entries(part.get("classwork"))
    if classwork:
        text.append("#### Classwork")
        text.extend(
            f"**Question {number}.**\n\n{item['question']}\n\n*Answer:*\n\n{item['answer']}"
            for number, item in enumerate(classwork, start=1)
        )
    tidied = [reader_ready(block) for block in text]
    lead = tidied[:1] if part.get("explanation") else []
    return "\n\n".join([*lead, *_figures(part), *tidied[len(lead) :]])
