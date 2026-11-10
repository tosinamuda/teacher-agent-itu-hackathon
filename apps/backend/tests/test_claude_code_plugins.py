"""The plugins load in Claude Code from the one manifest each has, and the marketplace."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from app.domains.content.plugins.reader import read_plugins

ROOT = Path(__file__).resolve().parents[3]
MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
CONNECTION = "lpcg"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = _json(MARKETPLACE)["plugins"]
    return entries


def _listed() -> list[tuple[str, Path]]:
    return [(entry["name"], ROOT / entry["source"]) for entry in _entries()]


def _types() -> list[tuple[str, Path]]:
    return [(name, folder) for name, folder in _listed() if name != CONNECTION]


def test_claude_code_lists_the_plugins_codex_lists() -> None:
    codex = {entry["name"] for entry in _json(CODEX_MARKETPLACE)["plugins"]}

    assert {name for name, _ in _listed()} == codex


def test_every_plugin_folder_the_app_ships_is_listed() -> None:
    shipped = {folder.name for folder in (ROOT / "plugins").iterdir() if folder.is_dir()}

    assert {name for name, _ in _types()} == shipped


@pytest.mark.parametrize(("name", "folder"), _listed())
def test_a_listed_plugin_has_one_manifest_that_names_it_and_skills_to_load(
    name: str, folder: Path
) -> None:
    entry = next(entry for entry in _entries() if entry["name"] == name)
    portable = _json(folder / "plugin.json")

    assert portable["name"] == name
    assert entry["description"] == portable["description"]
    assert not (folder / ".claude-plugin").exists()
    assert list(folder.glob("skills/*/SKILL.md"))


@pytest.mark.parametrize(("name", "folder"), _types())
def test_a_type_plugin_depends_on_the_plugin_that_holds_the_connection(
    name: str, folder: Path
) -> None:
    entry = next(entry for entry in _entries() if entry["name"] == name)

    assert entry["dependencies"] == [CONNECTION]
    assert not (folder / ".mcp.json").exists()


def test_the_connection_reaches_the_apps_server_with_the_access_code_from_the_environment() -> None:
    folder = dict(_listed())[CONNECTION]
    servers = _json(folder / ".mcp.json")["mcpServers"]

    assert list(servers) == [CONNECTION]
    server = servers[CONNECTION]
    assert server["type"] == "http"
    assert server["url"].endswith("/api/mcp}")
    assert server["headers"] == {"Authorization": "Bearer ${LPCG_ACCESS_CODE}"}


@pytest.mark.parametrize(("name", "folder"), _types())
def test_the_app_reads_each_shipped_plugin_into_the_artefacts_its_files_name(
    name: str, folder: Path
) -> None:
    plugins, problems = read_plugins(folder)

    assert [problem for problem in problems if problem.severity.value == "error"] == []
    assert plugins
    assert all(plugin.manifest.name == name for plugin in plugins)
