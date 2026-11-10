"""The class test, revision note and lesson plan generators, shipped as plugins."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml
from mcp import Client
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.types import Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.reader import folder_digest, read_plugins
from app.domains.content.plugins.shipped import shipped_names
from app.domains.content_engine.infrastructure.harness.workspace import (
    SKILLS_DIR,
    pinned_skills,
    write_skills,
)
from app.domains.content_engine.mcp.caller import as_the_app
from tests.content_engine_support import PLAN, SESSION_PLAN, seed_lesson, server_over
from tests.plan_import_support import SECTIONS
from tests.plugin_folder import read_plugin

PLUGINS = Path(__file__).resolve().parents[3] / "plugins"
GROUP_VARS = Path(__file__).resolve().parents[3] / "deploy" / "ansible" / "group_vars" / "all.yml"


@dataclass(frozen=True)
class Kind:
    folder: str
    artefact: str
    #: The built-in type the artefact writes.
    type: str
    unit: str
    parts: tuple[str, ...]
    skill: str
    references: tuple[str, ...]


KINDS = [
    Kind(
        "class-test",
        "class-test-writer",
        "class-test",
        "lesson_objective",
        ("questions",),
        "writing-class-tests",
        ("references/answer-key.md", "references/distractors.md"),
    ),
    Kind(
        "revision-note",
        "revision-note-writer",
        "revision-note",
        "lesson_objective",
        ("title", "explanation", "figures", "worked_examples", "practice"),
        "writing-revision-notes",
        ("references/figures.md", "references/worked-examples-and-practice.md"),
    ),
    Kind(
        "lesson-plan",
        "lesson-plan-writer",
        "lesson-plan",
        "curriculum_objective",
        ("lesson_objectives",),
        "drafting-lesson-plans",
        (
            "references/evaluation-questions.md",
            "references/lesson-context.md",
            "references/steps-and-activities.md",
        ),
    ),
]
IDS = [kind.artefact for kind in KINDS]


@pytest.mark.parametrize("kind", KINDS, ids=IDS)
def test_the_generator_is_valid_with_one_entry_skill_and_its_reference_files(kind: Kind) -> None:
    plugin, problems = read_plugin(PLUGINS / kind.folder, kind.artefact)

    assert problems == [] and plugin is not None
    assert plugin.definition is None and plugin.slug == kind.type
    assert plugin.spec.unit is not None and plugin.spec.unit.value == kind.unit
    assert plugin.spec.parts is not None
    assert [part.name for part in plugin.spec.parts.fields] == list(kind.parts)
    assert [skill.slug for skill in plugin.skills] == [kind.skill]
    assert sorted(file.path for file in plugin.skills[0].files) == list(kind.references)


def test_the_lesson_plan_generator_accepts_the_parts_a_plan_is_assembled_from() -> None:
    plugin, _ = read_plugin(PLUGINS / "lesson-plan", "lesson-plan-writer")
    assert plugin is not None and plugin.spec.parts is not None
    assert plugin.spec.lesson_parts is not None

    lesson = plugin.spec.lesson_parts.validate(SECTIONS["lesson"])
    objective = plugin.spec.parts.validate(SECTIONS["cur_obj01"])

    assert lesson["intro"] and objective["lesson_objectives"]


@pytest.mark.parametrize("kind", KINDS[:2], ids=IDS[:2])
@pytest.mark.asyncio
async def test_installed_its_skills_reach_a_harness_workspace_as_the_plugin_has_them(
    kind: Kind, db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    objectives = [{"curriculum_objective_id": "cur_obj01", "objective_text": "Add fractions"}]
    await db.execute(
        update(PlanVersion)
        .where(PlanVersion.version_id == PLAN)
        .values(session_plan=SESSION_PLAN | {"curriculum_objectives": objectives})
    )
    folder = PLUGINS / kind.folder
    plugin, _ = read_plugin(folder, kind.artefact)
    assert plugin is not None
    catalogue = build_content_catalogue()
    await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(folder), "Researcher"
    )
    await catalogue.make_default(db, kind.type, Level.CLASS, kind.artefact, "Researcher")
    with as_the_app():
        async with Client(server_over(db)) as client:
            opened = await client.call_tool(
                "start_draft", {"type": kind.type, "plan_version_id": PLAN}
            )
            assert opened.structured_content is not None, opened.content
            skills = await pinned_skills(client, opened.structured_content)
    workspace = tmp_path / "workspace"
    write_skills(workspace, skills)

    source, copied = folder / "skills", workspace / SKILLS_DIR
    files = sorted(p.relative_to(source) for p in (source / kind.skill).rglob("*") if p.is_file())
    assert sorted(p.relative_to(copied) for p in copied.rglob("*") if p.is_file()) == files
    assert all((copied / f).read_bytes() == (source / f).read_bytes() for f in files)


def test_every_plugin_folder_is_installed_by_each_deploy() -> None:
    deployed = yaml.safe_load(GROUP_VARS.read_text())["content_plugins"]

    assert sorted(deployed) == sorted(
        folder.name for folder in PLUGINS.iterdir() if folder.is_dir()
    )


def test_a_plugin_the_deploy_retires_is_not_one_the_checkout_ships() -> None:
    retired = yaml.safe_load(GROUP_VARS.read_text())["retired_plugins"]

    assert retired
    assert not set(retired) & shipped_names()


@pytest.mark.asyncio
async def test_what_one_plugin_makes_is_listed_as_rows_that_name_that_plugin(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    folder = PLUGINS / "revision-note"
    plugins, problems = read_plugins(folder)
    assert len(plugins) == 2, problems
    installer = PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins())
    for plugin in plugins:
        await installer.install(db, plugin, folder_digest(folder), "Researcher")

    rows = await installer.installed(db)

    assert sorted((row.name, row.plugin) for row in rows) == [
        ("revision-note-learner-writer", "revision-note"),
        ("revision-note-writer", "revision-note"),
    ]
