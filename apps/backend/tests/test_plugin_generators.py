"""A plugin that implements a type adds a generator to it and leaves the type's spec alone."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.errors import ContentError
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.generators import GeneratorKind, GeneratorStatus
from app.domains.content.domain.plugins import PluginRevision, PluginStatus
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.reader import folder_digest
from tests.content_engine_support import PARTS, seed_lesson
from tests.plugin_folder import implementing_plan, read_plugin, rewrite_artefact, write_plugin

pytestmark = pytest.mark.asyncio

PLAN = BuiltIn.LESSON_PLAN.value


def _installer() -> PluginInstaller:
    return PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins())


async def _install(db: AsyncSession, folder: Path) -> PluginRevision:
    plugin, problems = read_plugin(folder)
    assert plugin is not None, problems
    return await _installer().install(db, plugin, folder_digest(folder), "Researcher")


async def test_installing_a_generator_keeps_the_types_spec_and_default(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    catalogue = build_content_catalogue()
    own = await catalogue.current(db, PLAN)

    recorded = await _install(
        db, implementing_plan(tmp_path / "p", own, requirements=["Be brief."])
    )

    assert (await catalogue.current(db, PLAN)).revision == own.revision
    assert [s.revision for s in await catalogue.history(db, PLAN)][-1] == own.revision
    assert (recorded.type_slug, recorded.implements, recorded.status) == (
        PLAN,
        True,
        PluginStatus.INSTALLED,
    )
    assert recorded.spec_revision > own.revision
    definition = await catalogue.type(db, PLAN)
    default = await catalogue.generator(db, definition, Level.CLASS)
    assert default.ref == "builtin"
    mine = await catalogue.generator(db, definition, Level.CLASS, "plan-writer")
    assert (mine.harness, mine.status, mine.spec_revision) == (
        GeneratorKind.ENGINE,
        GeneratorStatus.AVAILABLE,
        recorded.spec_revision,
    )
    assert not await catalogue.retired(db, PLAN)


async def test_a_generator_may_not_change_the_types_schemas_or_level(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    own = await build_content_catalogue().current(db, PLAN)
    folder = implementing_plan(tmp_path / "p", own, parts=PARTS)
    with pytest.raises(ContentError) as changed:
        await _install(db, folder)
    assert changed.value.status_code == 422
    assert changed.value.detail.startswith("invalid_generator:")
    assert "parts" in changed.value.detail


async def test_a_type_that_takes_no_generator_refuses_one(db: AsyncSession, tmp_path: Path) -> None:
    await seed_lesson(db)
    own = await build_content_catalogue().current(db, PLAN)
    folder = implementing_plan(tmp_path / "p", own)
    rewrite_artefact(folder, lambda a: a.update(implements="exam-questions"))
    with pytest.raises(ContentError) as refused:
        await _install(db, folder)
    assert "takes no generator" in refused.value.detail


async def test_an_update_changes_the_spec_and_removing_retires_the_generator(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    catalogue = build_content_catalogue()
    own = await catalogue.current(db, PLAN)
    folder = implementing_plan(tmp_path / "p", own, requirements=["Be brief."])
    first = await _install(db, folder)

    rewrite_artefact(folder, lambda a: a["spec"].update(requirements=["Be thorough."]))
    plugin, _ = read_plugin(folder)
    assert plugin is not None
    second = await _installer().update(db, plugin, folder_digest(folder), "Researcher")
    assert second.spec_revision == first.spec_revision + 1
    definition = await catalogue.type(db, PLAN)
    assert (
        await catalogue.generator(db, definition, Level.CLASS, "plan-writer")
    ).spec_revision == (second.spec_revision)

    removed = await _installer().remove(db, "plan-writer", "Researcher")
    assert removed.status is PluginStatus.REMOVED
    with pytest.raises(ContentError):
        await catalogue.generator(db, definition, Level.CLASS, "plan-writer")
    assert (await catalogue.generator(db, definition, Level.CLASS)).ref == "builtin"


async def test_a_new_draft_is_written_to_the_default_generators_spec(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    catalogue = build_content_catalogue()
    own = await catalogue.current(db, PLAN)
    installed = await _install(
        db, implementing_plan(tmp_path / "p", own, requirements=["Be brief."])
    )

    assert (await catalogue.drafting_spec(db, PLAN)).revision == own.revision

    await catalogue.make_default(db, PLAN, Level.CLASS, "plan-writer", "Researcher")
    assert (await catalogue.drafting_spec(db, PLAN)).revision == installed.spec_revision
    assert (await catalogue.current(db, PLAN)).revision == own.revision
    with pytest.raises(ContentError) as in_use:
        await _installer().remove(db, "plan-writer", "Researcher")
    assert in_use.value.detail == f"generator_is_default:{PLAN}:plan-writer"

    await catalogue.make_default(db, PLAN, Level.CLASS, "builtin", "Researcher")
    assert (await catalogue.drafting_spec(db, PLAN)).revision == own.revision


async def test_a_plugin_names_a_type_or_one_to_implement_and_not_both(tmp_path: Path) -> None:
    both = write_plugin(tmp_path / "both", "both", "worked-examples")
    rewrite_artefact(both, lambda a: a.update(implements=PLAN))
    plugin, problems = read_plugin(both)
    assert plugin is None
    assert any("implements" in p.message for p in problems)

    neither = write_plugin(tmp_path / "neither", "neither", "worked-examples")
    rewrite_artefact(neither, lambda a: a.pop("type"))
    assert read_plugin(neither)[0] is None
