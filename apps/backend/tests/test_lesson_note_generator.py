"""A plugin that implements the lesson note writes parts that are saved as the note's markdown."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.part_markdown import part_as_markdown
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.application.kinds import ArtefactContent
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.application.service import ContentService
from app.domains.content.domain.generators import GeneratorKind
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content.infrastructure.review import LifecycleApprover
from app.domains.content.infrastructure.wiring import content_kinds
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.infrastructure.engine import EngineIncompleteError, Request
from app.domains.content_engine.infrastructure.wiring import build_drafting_service
from tests.content_engine_support import PLAN, ScriptedWriter, engine_over, seed_lesson
from tests.plugin_folder import read_plugin
from tests.test_content_api import _Generator, _Revisions

WRITER = Path(__file__).parents[3] / "plugins" / "lesson-note"
NOTE = BuiltIn.LESSON_NOTE.value


async def _installed(db: AsyncSession) -> None:
    await seed_lesson(db)
    plugin, problems = read_plugin(WRITER, "lesson-note-writer")
    assert plugin is not None, problems
    await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(WRITER), "Researcher"
    )


@pytest.mark.asyncio
async def test_the_shipped_plugin_implements_the_lesson_note_beside_the_pipeline(
    db: AsyncSession,
) -> None:
    await _installed(db)
    catalogue = build_content_catalogue()
    definition = await catalogue.type(db, NOTE)

    assert (
        await catalogue.generator(db, definition, Level.CLASS)
    ).harness is GeneratorKind.DSPY_PIPELINE
    mine = await catalogue.generator(db, definition, Level.CLASS, "lesson-note-writer")
    assert (mine.harness, mine.spec_revision) == (GeneratorKind.ENGINE, 2)
    assert (await catalogue.current(db, NOTE)).revision == 1


@pytest.mark.asyncio
async def test_a_drafted_note_is_stored_as_a_lesson_note_with_a_markdown_section_for_each_step(
    db: AsyncSession,
) -> None:
    await _installed(db)
    catalogue = build_content_catalogue()
    await catalogue.make_default(db, NOTE, Level.CLASS, "lesson-note-writer", "Researcher")
    step = {
        "teaching_points": [
            "A fraction is a part of a whole: in 3/4 the denominator 4 says the whole is cut "
            "into four equal parts and the numerator 3 says how many parts are taken.",
            "Fractions with the same denominator add by adding their numerators and keeping "
            "the denominator, so 1/4 + 2/4 = 3/4.",
        ],
        "questions_for_the_class": [
            {"question": "What is $\\frac{1}{2}$ of 10?", "expected_answer": "5"},
            {"question": "What is 1/4 + 2/4?", "expected_answer": "3/4"},
        ],
        "on_the_board": "Same denominator: add the numerators, keep the denominator.",
    }
    second = {
        **step,
        "questions_for_the_class": [
            {"question": "What is 3/8 + 2/8?", "expected_answer": "5/8"},
            {"question": "What is 2/5 + 1/5?", "expected_answer": "3/5"},
        ],
    }
    writer = ScriptedWriter({"s1": [step], "s2": [second]})

    built = await engine_over(db, writer).build(Request(type=NOTE, plan_version_id=PLAN))

    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert (record.type, record.kind, record.review_status) == (NOTE, "lesson_note", "pending")
    assert [s["step_id"] for s in record.manifest["sections"]] == ["s1", "s2"]
    body = str(record.manifest["sections"][0]["body"])
    assert body.startswith("#### Teaching points\n\n- A fraction is a part of a whole")
    assert "#### Questions for the class" in body and "**Expected answer.**" in body
    assert body.rstrip().endswith("keep the denominator.")
    assert record.provenance["generator"] == {
        "harness": "engine",
        "schema": "spec",
        "ref": "lesson-note-writer",
        "spec_revision": 2,
    }
    assert record.review is not None
    assert [(c["check"], c["passed"]) for c in record.review["checks"]] == [
        ("note_substance", True),
        ("no_second_thoughts", True),
        ("size_rule_correct", True),
        ("rounding_correct", True),
        ("distinct_questions", True),
        ("rounding_taught", True),
    ]


@pytest.mark.asyncio
async def test_generation_goes_to_the_engine_when_a_plugin_is_the_default(
    db: AsyncSession,
) -> None:
    await _installed(db)
    catalogue = build_content_catalogue()
    pipeline, engine = _Generator("AT-pipeline"), _Generator("AT-engine")
    records = SqlAlchemyContentRecords()
    service = ContentService(
        catalogue=catalogue,
        records=records,
        kinds=content_kinds(records),
        generators={t.value: pipeline for t in BuiltIn if t is not BuiltIn.LESSON_PLAN},
        engine_kind=ArtefactContent(LifecycleApprover(), ArtefactRepository()),
        engine_generator=engine,
        revisions=_Revisions(),
    )
    asked = GenerationChoices(instructions="Keep it short.")

    with pytest.raises(ContentError) as native:
        await service.check_generation(
            db, plan_version_id=PLAN, type=NOTE, level=Level.CLASS, choices=asked
        )
    assert native.value.detail == "instructions_apply_to_engine_types_only"

    await catalogue.make_default(db, NOTE, Level.CLASS, "lesson-note-writer", "Researcher")
    await service.check_generation(
        db, plan_version_id=PLAN, type=NOTE, level=Level.CLASS, choices=asked
    )

    await catalogue.make_default(db, NOTE, Level.CLASS, "builtin", "Researcher")
    with pytest.raises(ContentError):
        await service.check_generation(
            db, plan_version_id=PLAN, type=NOTE, level=Level.CLASS, choices=asked
        )


def test_a_part_is_set_down_as_headed_markdown_in_the_specs_order() -> None:
    plugin, _ = read_plugin(WRITER, "lesson-note-writer")
    assert plugin is not None and plugin.spec.parts is not None
    part = {
        "worked_examples": [
            {
                "problem": "Add $\\frac{1}{4}+\\frac{1}{4}$.",
                "solution": [{"working": "$\\frac{2}{4}$", "commentary": "Add the tops."}],
                "answer": "$\\frac{1}{2}$",
            }
        ],
        "teaching_points": ["Fractions share a denominator."],
    }

    text = part_as_markdown(part, plugin.spec.parts.fields)

    assert text.index("#### Teaching points") < text.index("#### Worked examples")
    assert "**1.**\n\n**Problem.**" in text
    assert "- $\\frac{2}{4}$ — Add the tops." in text
    assert "**Answer.**\n\n$\\frac{1}{2}$" in text


@pytest.mark.asyncio
async def test_the_note_is_draftable_only_while_a_plugin_is_its_default(db: AsyncSession) -> None:
    await _installed(db)
    catalogue = build_content_catalogue()
    note = await catalogue.type(db, NOTE)
    drafting = build_drafting_service()

    assert not await drafting.drafts(db, note)
    await catalogue.make_default(db, NOTE, Level.CLASS, "lesson-note-writer", "Researcher")
    assert await drafting.drafts(db, note)
    await catalogue.make_default(db, NOTE, Level.CLASS, "builtin", "Researcher")
    assert not await drafting.drafts(db, note)


@pytest.mark.asyncio
async def test_a_step_with_too_little_to_teach_from_is_sent_back(db: AsyncSession) -> None:
    await _installed(db)
    await build_content_catalogue().make_default(
        db, NOTE, Level.CLASS, "lesson-note-writer", "Researcher"
    )
    thin = {
        "teaching_points": ["Place value.", "Fractions."],
        "questions_for_the_class": [
            {"question": "What is 1/2 of 10?", "expected_answer": "5"},
            {"question": "What is 1/4 + 2/4?", "expected_answer": "3/4"},
        ],
        "on_the_board": "Add numerators.",
    }
    writer = ScriptedWriter({"s1": [thin], "s2": [thin]})

    with pytest.raises(EngineIncompleteError, match="characters of text; add substance"):
        await engine_over(db, writer).build(Request(type=NOTE, plan_version_id=PLAN))


@pytest.mark.asyncio
async def test_the_original_generator_can_be_named_while_a_plugin_is_the_default(
    db: AsyncSession,
) -> None:
    await _installed(db)
    catalogue = build_content_catalogue()
    pipeline, engine = _Generator("AT-pipeline"), _Generator("AT-engine")
    records = SqlAlchemyContentRecords()
    service = ContentService(
        catalogue=catalogue,
        records=records,
        kinds=content_kinds(records),
        generators={t.value: pipeline for t in BuiltIn if t is not BuiltIn.LESSON_PLAN},
        engine_kind=ArtefactContent(LifecycleApprover(), ArtefactRepository()),
        engine_generator=engine,
        revisions=_Revisions(),
    )
    await catalogue.make_default(db, NOTE, Level.CLASS, "lesson-note-writer", "Researcher")

    async def chosen(pin: str | None):  # type: ignore[no-untyped-def]
        return await service._generator_for(
            db,
            plan_version_id=PLAN,
            type=NOTE,
            level=Level.CLASS,
            choices=GenerationChoices(pipeline=pin),
        )

    default, default_binding = await chosen(None)
    original, original_binding = await chosen("builtin")

    assert (default is engine, default_binding.ref) == (True, "lesson-note-writer")
    assert (original is pipeline, original_binding.ref) == (True, "builtin")
    with pytest.raises(ContentError) as unknown:
        await chosen("no-such-generator")
    assert unknown.value.detail == "unknown_generator:lesson-note:no-such-generator"
    with pytest.raises(ContentError) as sources:
        await service._generator_for(
            db,
            plan_version_id=PLAN,
            type=NOTE,
            level=Level.CLASS,
            choices=GenerationChoices(sources="both"),
        )
    assert sources.value.detail == "sources_apply_to_the_revision_note_only"
