"""The lesson note generator, shipped as a plugin: its skills reach a writer, its lines fit."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from mcp import Client
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.infrastructure.harness.workspace import (
    SKILLS_DIR,
    pinned_skills,
    write_skills,
)
from app.domains.content_engine.mcp.caller import as_the_app
from experiments.lesson_note_engine.engine_arm import RUN_TYPE, _install
from tests.content_engine_support import PLAN, SESSION_PLAN, seed_lesson, server_over
from tests.plugin_folder import read_plugin

PLUGIN = Path(__file__).resolve().parents[3] / "plugins" / "lesson-note"
WRITER = "lesson-note-writer"
NOTE = BuiltIn.LESSON_NOTE.value
SKILL = "writing-lesson-notes"


async def _installed_as_default(db: AsyncSession, subject: str | None = None) -> None:
    await seed_lesson(db)
    if subject is not None:
        await db.execute(
            update(PlanVersion)
            .where(PlanVersion.version_id == PLAN)
            .values(session_plan=SESSION_PLAN | {"subject": subject})
        )
    plugin, problems = read_plugin(PLUGIN, WRITER)
    assert plugin is not None, problems
    catalogue = build_content_catalogue()
    await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(PLUGIN), "Researcher"
    )
    await catalogue.make_default(db, NOTE, Level.CLASS, WRITER, "Researcher")


def test_the_lesson_note_generator_is_valid_and_writes_notes_with_one_skill() -> None:
    plugin, problems = read_plugin(PLUGIN, WRITER)

    assert problems == []
    assert plugin is not None and plugin.definition is None and plugin.slug == NOTE
    assert plugin.spec.unit is not None and plugin.spec.unit.value == "plan_step"
    assert plugin.spec.parts is not None
    assert [part.name for part in plugin.spec.parts.fields] == [
        "teaching_points",
        "figures",
        "worked_examples",
        "questions_for_the_class",
        "on_the_board",
    ]
    assert [skill.slug for skill in plugin.skills] == [SKILL]
    assert sorted(file.path for file in plugin.skills[0].files) == [
        "references/figures.md",
        "references/worked-solutions.md",
    ]


@pytest.mark.asyncio
async def test_installed_its_skills_are_copied_into_a_harness_workspace_as_the_plugin_has_them(
    db: AsyncSession, tmp_path: Path
) -> None:
    await _installed_as_default(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            opened = await client.call_tool("start_draft", {"type": NOTE, "plan_version_id": PLAN})
            assert opened.structured_content is not None
            skills = await pinned_skills(client, opened.structured_content)
    assert all(skill.has_references for skill in skills)
    workspace = tmp_path / "workspace"
    write_skills(workspace, skills)

    source = PLUGIN / "skills"
    copied = workspace / SKILLS_DIR
    files = sorted(p.relative_to(source) for p in (source / SKILL).rglob("*") if p.is_file())
    assert sorted(p.relative_to(copied) for p in copied.rglob("*") if p.is_file()) == files
    assert all((copied / f).read_bytes() == (source / f).read_bytes() for f in files)


def _noun_example() -> dict[str, object]:
    return {
        "teaching_points": [
            "A proper noun names one particular person, place or thing.",
            "A common noun names any one of a kind of person, place or thing.",
        ],
        "worked_examples": [
            {
                "problem": "Which kind of noun is Chimaka?",
                "solution": [
                    {"working": "Chimaka → proper noun", "commentary": "It names a person."}
                ],
                "answer": "A proper noun",
            }
        ],
        "questions_for_the_class": [
            {
                "question": "Name a common noun.",
                "expected_answer": "Any noun for a class of things",
            },
            {"question": "Name a proper noun.", "expected_answer": "Any name, such as Ibadan"},
        ],
        "on_the_board": "Proper noun: Chimaka",
    }


async def _added_for(db: AsyncSession, subject: str) -> tuple[bool, str]:
    await _installed_as_default(db, subject)
    with as_the_app():
        async with Client(server_over(db)) as client:
            opened = await client.call_tool("start_draft", {"type": NOTE, "plan_version_id": PLAN})
            assert opened.structured_content is not None
            added = await client.call_tool(
                "add_part",
                {
                    "draft_id": opened.structured_content["draft_id"],
                    "unit_id": "s1",
                    "part": _noun_example(),
                },
            )
    return added.is_error, json.dumps([c.model_dump() for c in added.content])


@pytest.mark.asyncio
async def test_a_language_lesson_writes_its_working_as_plain_text(db: AsyncSession) -> None:
    refused, said = await _added_for(db, "English Language")

    assert not refused, said


@pytest.mark.asyncio
async def test_a_mathematics_lesson_still_writes_each_working_line_as_a_formula(
    db: AsyncSession,
) -> None:
    refused, said = await _added_for(db, "Mathematics")

    assert refused and "between $ signs" in said


@pytest.mark.asyncio
async def test_the_comparison_arm_installs_the_generator_as_a_type_of_its_own_run(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)

    slug = await _install(db, PLUGIN, WRITER)

    spec = await build_content_catalogue().current(db, slug)
    assert slug == RUN_TYPE
    assert [ref.slug for ref in spec.skills] == [SKILL]
