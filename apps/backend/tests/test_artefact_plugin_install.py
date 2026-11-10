"""Installing, updating and removing an artefact plugin."""

from __future__ import annotations

from pathlib import Path

import pytest
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.errors import ContentError
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.plugins import PluginRevision, PluginStatus
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.mcp.caller import as_the_app
from tests.content_engine_support import PLAN, seed_lesson, server_over
from tests.plugin_folder import read_plugin, rewrite, rewrite_artefact, write_plugin

pytestmark = pytest.mark.asyncio

TYPE = "plugin-examples"
SKILL = "checking-worked-answers"
SKILL_PATH = f"skills/{SKILL}/SKILL.md"


def _installer() -> PluginInstaller:
    return PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins())


def _plugin(tmp_path: Path, type_slug: str = TYPE) -> Path:
    return write_plugin(tmp_path / "p", "lesson-tools", type_slug)


async def _install(db: AsyncSession, folder: Path) -> PluginRevision:
    plugin, problems = read_plugin(folder)
    assert plugin is not None, problems
    return await _installer().install(db, plugin, folder_digest(folder), "Researcher")


async def _update(db: AsyncSession, folder: Path) -> PluginRevision:
    plugin, problems = read_plugin(folder)
    assert plugin is not None, problems
    return await _installer().update(db, plugin, folder_digest(folder), "Researcher")


def _skill_file(folder: Path) -> Path:
    return folder / "skills" / "checking-worked-answers" / "SKILL.md"


async def test_install_registers_the_type_with_its_skills_and_servers(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    recorded = await _install(db, _plugin(tmp_path))

    catalogue = build_content_catalogue()
    spec = await catalogue.current(db, TYPE)
    assert (recorded.name, recorded.revision, recorded.spec_revision, recorded.status) == (
        "lesson-tools",
        1,
        1,
        PluginStatus.INSTALLED,
    )
    assert [(r.slug, r.revision) for r in spec.skills] == [(SKILL, 1)]
    assert [s.name for s in spec.mcp] == ["maths"]
    assert "line by line" in (await catalogue.skills.skill(db, SKILL)).instructions


async def test_a_plugin_installed_twice_or_over_a_type_in_use_is_refused(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    await _install(db, folder)

    with pytest.raises(ContentError, match="plugin_installed:lesson-tools"):
        await _install(db, folder)
    rewrite_artefact(folder, lambda r: r.update({"type": "lesson-note"}))
    other = write_plugin(tmp_path / "q", "other-tools", "lesson-note")
    with pytest.raises(ContentError, match="content_type_exists:lesson-note"):
        await _install(db, other)


async def test_sync_installs_then_updates_and_changes_nothing_when_nothing_changed(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    plugin, _ = read_plugin(folder)
    assert plugin is not None

    first = await _installer().sync(db, plugin, folder_digest(folder), "Researcher")
    again = await _installer().sync(db, plugin, folder_digest(folder), "Researcher")
    _skill_file(folder).write_text(_skill_file(folder).read_text() + "Check every answer.\n")
    changed_plugin, _ = read_plugin(folder)
    assert changed_plugin is not None
    changed = await _installer().sync(db, changed_plugin, folder_digest(folder), "Researcher")

    assert (first.revision, again.revision, changed.revision) == (1, 1, 2)


async def test_a_skill_name_is_shared_by_equal_text_and_refused_for_different_text(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    await _install(db, _plugin(tmp_path))
    same = write_plugin(tmp_path / "q", "other-tools", "other-examples")
    differs = write_plugin(tmp_path / "r", "third-tools", "third-examples")
    _skill_file(differs).write_text(_skill_file(differs).read_text() + "Check every answer.\n")

    await _install(db, same)
    with pytest.raises(ContentError, match=f"skill_name_in_use:{SKILL}"):
        await _install(db, differs)

    catalogue = build_content_catalogue()
    assert (await catalogue.skills.skill(db, SKILL)).revision == 1
    assert [
        (r.slug, r.revision) for r in (await catalogue.current(db, "other-examples")).skills
    ] == [(SKILL, 1)]


async def test_a_refused_install_stores_no_skill(db: AsyncSession, tmp_path: Path) -> None:
    await seed_lesson(db)
    folder = write_plugin(tmp_path / "p", "lesson-tools", "lesson-note")

    with pytest.raises(ContentError, match="content_type_exists"):
        await _install(db, folder)

    assert await build_content_catalogue().skills.find(db, SKILL) is None


async def test_an_unchanged_folder_updates_to_nothing_and_a_changed_skill_is_a_new_revision(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    first = await _install(db, folder)

    same = await _update(db, folder)
    assert (same.revision, same.digest) == (first.revision, first.digest)

    _skill_file(folder).write_text(_skill_file(folder).read_text() + "Check every answer.\n")
    changed = await _update(db, folder)

    catalogue = build_content_catalogue()
    assert (changed.revision, changed.spec_revision) == (2, 2)
    assert [(r.slug, r.revision) for r in (await catalogue.current(db, TYPE)).skills] == [
        (SKILL, 2)
    ]
    old = await catalogue.revision(db, TYPE, 1)
    assert [(r.slug, r.revision) for r in old.skills] == [(SKILL, 1)]


async def test_an_update_that_changes_only_the_version_keeps_the_spec_revision(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    await _install(db, folder)
    rewrite(folder / "plugin.json", lambda r: r.update({"version": "1.0.1"}))

    updated = await _update(db, folder)

    assert (updated.revision, updated.version, updated.spec_revision) == (2, "1.0.1", 1)


async def test_an_update_may_not_change_the_type_it_added(db: AsyncSession, tmp_path: Path) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    await _install(db, folder)
    rewrite_artefact(folder, lambda r: r.update({"label": "Renamed"}))

    with pytest.raises(ContentError, match="plugin_type_is_fixed"):
        await _update(db, folder)


async def test_remove_stops_new_drafts_and_leaves_the_type_readable(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    await _install(db, _plugin(tmp_path))

    removed = await _installer().remove(db, "lesson-tools", "Researcher")

    catalogue = build_content_catalogue()
    assert removed.status is PluginStatus.REMOVED
    assert await catalogue.retired(db, TYPE)
    assert (await catalogue.type(db, TYPE)).slug == TYPE
    with as_the_app():
        async with Client(server_over(db)) as client:
            opened = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            listed = await client.call_tool("list_content_types", {})
    assert opened.is_error
    assert "has been removed" in str(opened.content)
    assert listed.structured_content is not None
    offered = {t["type"]: t["draftable"] for t in listed.structured_content["types"]}
    assert offered[TYPE] is False


async def test_a_removed_plugin_can_be_updated_to_install_again(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    await _install(db, folder)
    await _installer().remove(db, "lesson-tools", None)

    again = await _update(db, folder)

    assert again.status is PluginStatus.INSTALLED
    assert not await build_content_catalogue().retired(db, TYPE)


async def test_an_unknown_plugin_cannot_be_updated_or_removed(db: AsyncSession) -> None:
    with pytest.raises(ContentError, match="unknown_plugin:nothing"):
        await _installer().remove(db, "nothing", None)


async def test_installed_lists_each_plugin_once_at_its_latest_revision(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    await _install(db, folder)
    _skill_file(folder).write_text(_skill_file(folder).read_text() + "More.\n")
    await _update(db, folder)

    listed = await _installer().installed(db)

    assert [(p.name, p.revision) for p in listed] == [("lesson-tools", 2)]


async def test_the_files_a_revision_was_installed_with_are_kept_for_its_spec_revision(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = _plugin(tmp_path)
    first_files = read_plugin(folder)[0]
    assert first_files is not None
    await _install(db, folder)
    _skill_file(folder).write_text(_skill_file(folder).read_text() + "Check every answer.\n")
    await _update(db, folder)
    catalogue = build_content_catalogue()

    one = await catalogue.plugin_files(db, TYPE, 1)
    two = await catalogue.plugin_files(db, TYPE, 2)

    assert one is not None and two is not None
    assert (one.name, one.revision, one.files) == ("lesson-tools", 1, dict(first_files.files))
    assert (two.revision, "Check every answer." in two.files[SKILL_PATH]) == (2, True)
    assert await catalogue.plugin_files(db, TYPE, 3) is None
    await _installer().remove(db, "lesson-tools", "Researcher")
    assert await catalogue.plugin_files(db, TYPE, 2) is None
