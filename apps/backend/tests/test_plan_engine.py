"""A lesson plan the app writes itself: from the curriculum, held to the spec, and revised.

The draft tools, the lesson-plan checks and the engine are the real ones. Only the lesson's
lookup and the plan's saving are in memory, as in the plan import tests.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.artefacts.types.lesson_plan.application.manual_check import check_manual_plan
from app.domains.artefacts.types.lesson_plan.domain.plan_sections import (
    ObjectiveSection,
    assemble_plan,
    carry_figures,
    split_plan,
)
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.types import Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content_engine.infrastructure.engine import (
    Engine,
    EngineIncompleteError,
    EngineRefusedError,
    Request,
    Writer,
)
from app.domains.content_engine.infrastructure.plan_generator import PlanDraftError, PlanGenerator
from app.shared.json_types import JsonObject
from tests.plan_import_support import (
    CONTEXT,
    DOCUMENT,
    LESSON,
    PLAN_TYPE,
    SECTIONS,
    InMemoryPlanning,
    plan_server,
    seed_types,
)
from tests.plugin_folder import implementing_plan as _implementing
from tests.plugin_folder import read_plugin

pytestmark = pytest.mark.asyncio
PLAN_SLUG = "lesson-plan"
WRITER = Path(__file__).parents[3] / "plugins" / "lesson-plan"
OBJECTIVE = "cur_obj01"
OBJECTIVE_TEXT = "add fractions with a common denominator"


def _engine(db: AsyncSession, planning: InMemoryPlanning, writer: Writer) -> Engine:
    return Engine(lambda: plan_server(db, planning), lambda: writer)


class _Writer:
    """Writes the given parts: add_part for a unit with none, revise_part for one that has."""

    def __init__(self, parts: dict[str, JsonObject]) -> None:
        self.parts = parts
        self.draft: JsonObject = {}
        self.lesson: JsonObject = {}

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        if self.draft:
            return "Nothing more to write."
        self.draft, self.lesson = draft, lesson
        written = draft["parts"] if isinstance(draft.get("parts"), dict) else {}
        for unit_id, part in self.parts.items():
            tool = "revise_part" if unit_id in written else "add_part"
            await client.call_tool(
                tool, {"draft_id": draft["draft_id"], "unit_id": unit_id, "part": part}
            )
        return "Wrote the plan."


def _with_reference(reference: str) -> dict[str, JsonObject]:
    parts = copy.deepcopy(SECTIONS)
    parts["lesson"]["references"] = [reference]
    return parts


async def test_a_plan_written_from_the_curriculum_is_recorded_as_generated(
    db: AsyncSession,
) -> None:
    await seed_types(db)
    planning = InMemoryPlanning()

    await _engine(db, planning, _Writer(SECTIONS)).build(
        Request(PLAN_TYPE, session_id=LESSON), for_teacher="teacher-7"
    )

    assert planning.source_types == ["generated"]


async def test_a_plan_written_from_a_document_is_recorded_as_the_teachers(
    db: AsyncSession,
) -> None:
    await seed_types(db)
    planning = InMemoryPlanning()

    await _engine(db, planning, _Writer(SECTIONS)).build(
        Request(PLAN_TYPE, session_id=LESSON, source=DOCUMENT)
    )

    assert planning.source_types == ["document_import"]


async def test_a_reference_to_a_source_the_lesson_lacks_stops_a_plan_the_app_writes(
    db: AsyncSession,
) -> None:
    await seed_types(db)
    writer = _Writer(_with_reference("Mathematics Made Easy, page 12"))

    with pytest.raises(EngineIncompleteError, match="names no source this lesson has"):
        await _engine(db, InMemoryPlanning(), writer).build(Request(PLAN_TYPE, session_id=LESSON))


def _stating(rounding: str) -> dict[str, JsonObject]:
    """The fraction plan with a rounding in the core step's own words."""
    return json.loads(json.dumps(SECTIONS).replace('"Add the numerators."', f'"{rounding}"'))


async def test_a_wrong_rounding_stops_a_plan_the_app_writes(db: AsyncSession) -> None:
    await seed_types(db)
    writer = _Writer(_stating("Round 7,500 to 7,000 for a quick estimate."))

    with pytest.raises(EngineIncompleteError, match="7,500 rounds to 8,000"):
        await _engine(db, InMemoryPlanning(), writer).build(Request(PLAN_TYPE, session_id=LESSON))


async def test_a_teachers_own_document_keeps_a_rounding_it_states(db: AsyncSession) -> None:
    await seed_types(db)
    planning = InMemoryPlanning()

    await _engine(db, planning, _Writer(_stating("Round 7,500 to 7,000."))).build(
        Request(PLAN_TYPE, session_id=LESSON, source=DOCUMENT)
    )

    assert len(planning.saved) == 1


async def test_a_teachers_own_document_keeps_the_references_it_names(db: AsyncSession) -> None:
    await seed_types(db)
    planning = InMemoryPlanning()

    await _engine(db, planning, _Writer(_with_reference("Mathematics Made Easy"))).build(
        Request(PLAN_TYPE, session_id=LESSON, source=DOCUMENT)
    )

    assert planning.saved[0][1]["references"] == ["Mathematics Made Easy"]


async def test_only_a_students_activity_says_whether_it_sets_work() -> None:
    parts = copy.deepcopy(SECTIONS)
    parts["lesson"]["intro"]["activities"][0]["sets_work"] = False  # type: ignore[index]

    plan = assemble_plan(
        parts["lesson"], [ObjectiveSection(OBJECTIVE, OBJECTIVE_TEXT, parts[OBJECTIVE])]
    ).content

    assert check_manual_plan(CONTEXT, plan, strict=True).passes
    steps = plan["steps"]
    assert isinstance(steps, list) and isinstance(steps[0], dict)
    assert steps[0]["activities"] == [{"who": "teacher", "what": "Ask what 1/4 means."}]


async def test_splitting_a_plan_gives_back_the_parts_it_was_assembled_from() -> None:
    lesson, sections = SECTIONS["lesson"], {OBJECTIVE: SECTIONS[OBJECTIVE]}
    plan = assemble_plan(
        lesson, [ObjectiveSection(OBJECTIVE, OBJECTIVE_TEXT, sections[OBJECTIVE])]
    ).content

    again_lesson, again_sections = split_plan(plan)

    assert again_sections == sections
    assert again_lesson["intro"] == lesson["intro"]
    assert again_lesson["evaluation"] == lesson["evaluation"]


async def test_an_older_plans_activity_lists_become_ordered_activities() -> None:
    plan = assemble_plan(
        SECTIONS["lesson"], [ObjectiveSection(OBJECTIVE, OBJECTIVE_TEXT, SECTIONS[OBJECTIVE])]
    ).content
    steps = plan["steps"]
    assert isinstance(steps, list) and isinstance(steps[0], dict)
    steps[0].pop("activities")
    steps[0]["teacher_activities"] = ["Ask what 1/4 means."]
    steps[0]["student_activities"] = ["Answer."]

    lesson, _ = split_plan(plan)

    intro = lesson["intro"]
    assert isinstance(intro, dict)
    assert intro["activities"] == [
        {"who": "teacher", "what": "Ask what 1/4 means."},
        {"who": "student", "what": "Answer."},
    ]


def _with_figure(plan: JsonObject, step: int, index: int) -> JsonObject:
    steps = plan["steps"]
    assert isinstance(steps, list) and isinstance(steps[step], dict)
    blocks = steps[step]["blocks"]
    assert isinstance(blocks, list)
    blocks.insert(
        index,
        {"id": "fig1", "type": "visual", "variant": "diagram_number_line", "caption": "A line"},
    )
    return plan


async def test_a_figure_is_not_a_part_and_stays_through_a_revision() -> None:
    sections = [ObjectiveSection(OBJECTIVE, OBJECTIVE_TEXT, SECTIONS[OBJECTIVE])]
    plan = _with_figure(assemble_plan(SECTIONS["lesson"], sections).content, 1, 1)
    lesson, parts = split_plan(plan)
    revised = assemble_plan(lesson, [ObjectiveSection(OBJECTIVE, OBJECTIVE_TEXT, parts[OBJECTIVE])])

    carried = carry_figures(plan, revised.content)

    objectives = parts[OBJECTIVE]["lesson_objectives"]
    assert isinstance(objectives, list) and isinstance(objectives[0], dict)
    kinds = [block["kind"] for block in objectives[0]["core_step"]["blocks"]]
    assert "visual" not in kinds
    steps = carried["steps"]
    assert isinstance(steps, list) and isinstance(steps[1], dict)
    blocks = steps[1]["blocks"]
    assert isinstance(blocks, list) and isinstance(blocks[1], dict)
    assert (blocks[1]["id"], blocks[1]["variant"]) == ("fig1", "diagram_number_line")


async def _saved_plan(db: AsyncSession, planning: InMemoryPlanning) -> str:
    await seed_types(db)
    await _engine(db, planning, _Writer(SECTIONS)).build(Request(PLAN_TYPE, session_id=LESSON))
    return next(iter(planning.plans))


async def _no_chat(db: AsyncSession, content_id: str, key: str) -> str:
    return ""


async def test_a_draft_the_agent_cannot_finish_says_why(db: AsyncSession) -> None:
    await seed_types(db)
    generator = PlanGenerator(
        _engine(db, InMemoryPlanning(), _Writer({})), ChatFeed(AsyncSessionLocal), _no_chat
    )

    with pytest.raises(PlanDraftError, match="could not finish a plan that passes the checks"):
        await generator.draft(db, session_id=LESSON, for_teacher=None)


async def test_the_lesson_plan_spec_accepts_the_parts_a_plan_is_assembled_from() -> None:
    spec = seed_specification("lesson_plan")
    assert spec.lesson_parts is not None and spec.parts is not None

    lesson = spec.lesson_parts.validate(SECTIONS["lesson"])
    objective = spec.parts.validate(SECTIONS[OBJECTIVE])

    assert lesson["intro"] and objective["lesson_objectives"]
    assert [skill.slug for skill in spec.skills] == ["writing-lesson-plans"]


async def test_a_plan_is_reopened_as_a_draft_with_its_parts(db: AsyncSession) -> None:
    planning = InMemoryPlanning()
    plan_id = await _saved_plan(db, planning)
    writer = _Writer({})

    await _engine(db, planning, writer).build(
        Request(PLAN_TYPE, session_id=LESSON, content_id=plan_id, feedback="Shorten the intro.")
    )

    parts = writer.draft["parts"]
    assert isinstance(parts, dict) and set(parts) == {"lesson", OBJECTIVE}
    assert parts[OBJECTIVE] == SECTIONS[OBJECTIVE]
    assert planning.revised == []


async def test_a_revised_part_is_saved_as_the_plans_next_version(db: AsyncSession) -> None:
    planning = InMemoryPlanning()
    plan_id = await _saved_plan(db, planning)
    shorter = copy.deepcopy(SECTIONS["lesson"])
    shorter["intro"]["estimated_minutes"] = 3  # type: ignore[index]

    built = await _engine(db, planning, _Writer({"lesson": shorter})).build(
        Request(PLAN_TYPE, session_id=LESSON, content_id=plan_id, feedback="Shorten the intro.")
    )

    assert built.saved_as == "LPV-REVISED-1"
    steps = planning.revised[0]["steps"]
    assert isinstance(steps, list) and isinstance(steps[0], dict)
    assert steps[0]["estimated_minutes"] == 3


async def test_a_revision_that_changes_nothing_saves_no_version(db: AsyncSession) -> None:
    planning = InMemoryPlanning()
    plan_id = await _saved_plan(db, planning)

    built = await _engine(db, planning, _Writer({})).build(
        Request(PLAN_TYPE, session_id=LESSON, content_id=plan_id, feedback="Is this fine?")
    )

    assert built.saved_as == "LPV-IMPORTED-1"
    assert planning.revised == []


async def test_a_plan_that_does_not_exist_cannot_be_revised(db: AsyncSession) -> None:
    planning = InMemoryPlanning()
    await _saved_plan(db, planning)

    with pytest.raises(EngineRefusedError, match="to revise"):
        await _engine(db, planning, _Writer({})).build(
            Request(PLAN_TYPE, session_id=LESSON, content_id="LP-NO-SUCH-PLAN")
        )


async def test_a_plan_records_the_generator_whose_spec_it_was_written_to(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_types(db)
    catalogue = build_content_catalogue()
    own = await catalogue.current(db, PLAN_SLUG)
    plugin, problems = read_plugin(_implementing(tmp_path / "p", own))
    assert plugin is not None, problems
    installer = PluginInstaller(catalogue, SqlAlchemyPlugins())
    installed = await installer.install(db, plugin, "digest", "Researcher")
    planning = InMemoryPlanning()

    await _engine(db, planning, _Writer(SECTIONS)).build(Request(PLAN_TYPE, session_id=LESSON))
    assert planning.generators[-1] == {"harness": "engine", "schema": "spec", "ref": "builtin",
                                       "spec_revision": own.revision}  # fmt: skip

    await catalogue.make_default(db, PLAN_SLUG, Level.CLASS, "plan-writer", "Researcher")
    writer = _Writer(SECTIONS)
    await _engine(db, planning, writer).build(Request(PLAN_TYPE, session_id=LESSON))
    assert writer.draft["spec_revision"] == installed.spec_revision
    assert planning.generators[-1] == {"harness": "engine", "schema": "spec",
                                       "ref": "plan-writer",
                                       "spec_revision": installed.spec_revision}  # fmt: skip


async def test_the_shipped_plugin_writes_the_plan_to_the_apps_own_spec(db: AsyncSession) -> None:
    await seed_types(db)
    catalogue = build_content_catalogue()
    own = await catalogue.current(db, PLAN_SLUG)
    plugin, problems = read_plugin(WRITER, "lesson-plan-writer")
    assert plugin is not None, problems
    installed = await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(
        db, plugin, "digest", "Researcher"
    )
    mine = await catalogue.generator(
        db, await catalogue.type(db, PLAN_SLUG), Level.CLASS, "lesson-plan-writer"
    )
    assert mine.spec_revision is not None
    spec = await catalogue.revision(db, PLAN_SLUG, mine.spec_revision)
    assert (mine.harness.value, mine.spec_revision) == ("engine", installed.spec_revision)
    assert (spec.unit, spec.requirements) == (own.unit, own.requirements)
    assert (spec.lesson_parts, spec.parts) == (own.lesson_parts, own.parts)
    assert [skill.slug for skill in spec.skills] == ["drafting-lesson-plans"]
    assert (await catalogue.current(db, PLAN_SLUG)).revision == own.revision

    await catalogue.make_default(db, PLAN_SLUG, Level.CLASS, "lesson-plan-writer", "Researcher")
    planning = InMemoryPlanning()
    await _engine(db, planning, _Writer(SECTIONS)).build(Request(PLAN_TYPE, session_id=LESSON))
    assert planning.generators[-1]["ref"] == "lesson-plan-writer"
