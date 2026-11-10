"""``plugin.json``: the portable manifest of an Agent Plugins 1.0.0 package."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.domains.content.plugins.problems import Problem
from app.domains.content.plugins.standard import breaks_the_standard

MANIFEST = "plugin.json"
#: The reverse-domain namespace under ``extensions`` that holds this app's own plugin data.
NAMESPACE = "com.tosinamuda.lpcg"


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    description: str
    #: The files, from ``extensions.com.tosinamuda.lpcg.artefacts``, that say what the plugin
    #: adds: each a type, or a generator for a type that exists. Paths as ``./path`` in the plugin.
    artefacts: tuple[str, ...]


def _artefact_paths(folder: Path, ours: object) -> tuple[tuple[str, ...], list[Problem]]:
    """The artefact files the manifest's extension names, or what is wrong with the naming."""
    where = f"extensions.{NAMESPACE}"
    fields = {str(key): value for key, value in ours.items()} if isinstance(ours, dict) else {}
    paths = fields.get("artefacts")
    problems = [
        Problem(MANIFEST, f"{where}.{key} is not a field here")
        for key in sorted(set(fields) - {"artefacts"})
    ]
    if (
        not isinstance(paths, list)
        or not paths
        or not all(isinstance(path, str) and path.startswith("./") for path in paths)
    ):
        problems.append(
            Problem(
                MANIFEST, f"{where}.artefacts lists the artefact files, as ./path in the plugin"
            )
        )
        return (), problems
    outside = [
        path for path in paths if not (folder / path).resolve().is_relative_to(folder.resolve())
    ]
    problems += [
        Problem(MANIFEST, f"{where}.artefacts stays inside the plugin: {path!r}")
        for path in outside
    ]
    if len(set(paths)) != len(paths):
        problems.append(Problem(MANIFEST, f"{where}.artefacts lists a file once"))
    return (() if problems else tuple(paths)), problems


def read_manifest(folder: Path) -> tuple[PluginManifest | None, list[Problem]]:
    """The manifest in ``folder``, and everything the standard's schema finds wrong with it."""
    path = folder / MANIFEST
    if not path.is_file():
        return None, [Problem(MANIFEST, f"add {MANIFEST} at the plugin root")]
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        return None, [Problem(MANIFEST, f"is not valid JSON: {error}")]
    if problems := breaks_the_standard(MANIFEST, "plugin", record):
        return None, problems
    artefacts, problems = _artefact_paths(folder, record.get("extensions", {}).get(NAMESPACE))
    if not artefacts:
        return None, problems
    return PluginManifest(
        name=record["name"],
        version=str(record.get("version", "")),
        description=str(record.get("description", "")),
        artefacts=artefacts,
    ), []
