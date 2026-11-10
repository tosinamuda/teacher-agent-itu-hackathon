"""A valid artefact plugin folder to break one way at a time."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.plugins.manifest import NAMESPACE
from app.domains.content.plugins.plugin import Plugin
from app.domains.content.plugins.problems import Problem
from app.domains.content.plugins.reader import read_plugins
from app.domains.content.plugins.standard import MCP_SCHEMA, PLUGIN_SCHEMA
from tests.content_engine_support import PARTS

SKILL_MD = """---
name: checking-worked-answers
description: Use for any worked example.
---
Work every example line by line.
"""


ARTEFACT_PATH = f"./{NAMESPACE}/artefact.json"


def read_plugin(folder: Path, name: str | None = None) -> tuple[Plugin | None, list[Problem]]:
    """One artefact of the folder, the named one or else the first; none when it is refused."""
    plugins, problems = read_plugins(folder)
    return next((plugin for plugin in plugins if name in (None, plugin.name)), None), problems


def artefact_record(type_slug: str = "worked-examples") -> dict[str, object]:
    return {
        "type": type_slug,
        "label": "Worked examples",
        "audience": "learner",
        "spec": {
            "material": "worked examples for one step of the lesson",
            "audience": "{reader} revising at home",
            "levels": ["class_level"],
            "requirements": ["Show every step of the working."],
            "unit": "plan_step",
            "parts": PARTS,
        },
        "skills": ["checking-worked-answers"],
        "servers": {"maths": ["solve"]},
    }


def mcp_record() -> dict[str, object]:
    server = {
        "type": "streamable-http",
        "url": "https://tools.example.org/mcp",
        "headers": {"Authorization": "Bearer ${MATHS_TOKEN}"},
    }
    return {"$schema": MCP_SCHEMA, "mcpServers": {"maths": server}}


def write_plugin(
    folder: Path, name: str = "worked-examples", type_slug: str = "worked-examples"
) -> Path:
    """A plugin that validates, at ``folder``."""
    folder.mkdir(parents=True, exist_ok=True)
    manifest = {
        "$schema": PLUGIN_SCHEMA,
        "name": name,
        "version": "1.0.0",
        "description": "x",
        "extensions": {NAMESPACE: {"artefacts": [ARTEFACT_PATH]}},
    }
    (folder / "plugin.json").write_text(json.dumps(manifest))
    artefact = folder / ARTEFACT_PATH.removeprefix("./")
    artefact.parent.mkdir(parents=True, exist_ok=True)
    artefact.write_text(json.dumps(artefact_record(type_slug)))
    (folder / "mcp.json").write_text(json.dumps(mcp_record()))
    skill = folder / "skills" / "checking-worked-answers"
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(SKILL_MD)
    return folder


def rewrite(path: Path, change: Callable[[dict[str, Any]], None]) -> None:
    """Load the JSON file, let ``change`` edit it, and save it."""
    record = json.loads(path.read_text())
    change(record)
    path.write_text(json.dumps(record))


def rewrite_artefact(
    folder: Path, change: Callable[[dict[str, Any]], None], name: str | None = None
) -> None:
    """Edit the plugin's artefact file: the one of the named artefact, else the only one."""
    path = ARTEFACT_PATH if name is None else f"./{NAMESPACE}/{name}.json"
    rewrite(folder / path.removeprefix("./"), change)


SPEC_FIELDS = (
    "material", "audience", "levels", "structure", "requirements", "adaptable",
    "unit", "parts", "lesson_parts",
)  # fmt: skip


def implementing_plan(folder: Path, own: ContentSpecification, **spec: Any) -> Path:
    """A plugin folder that implements the lesson plan with the plan's own shape."""
    write_plugin(folder, "plan-writer", "unused")
    record = own.to_record()

    def change(artefact: dict[str, Any]) -> None:
        for key in ("type", "label", "audience"):
            del artefact[key]
        artefact["implements"] = "lesson-plan"
        artefact["spec"] = {**{k: record[k] for k in SPEC_FIELDS if record[k] is not None}, **spec}
        artefact["servers"] = {}

    rewrite_artefact(folder, change)
    (folder / "mcp.json").unlink()
    return folder
