"""The artefact file: what kind of material the plugin adds."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.domains.content.plugins.problems import Problem

_KEYS = frozenset(
    {
        "name",
        "type",
        "implements",
        "label",
        "audience",
        "made_from_a_plan_version",
        "spec",
        "skills",
        "servers",
        "checks",
        "adds",
        "files",
    }
)


@dataclass(frozen=True)
class ArtefactFile:
    #: What the plugin calls this artefact when it makes more than one; the plugin's own name
    #: otherwise.
    name: str | None
    #: The slug of the type the plugin adds; none when it implements a type instead.
    type: str | None
    #: The slug of the existing type the plugin adds a generator to.
    implements: str | None
    label: str
    audience: str
    made_from_a_plan_version: bool
    #: The spec fields, as ``content_specifications`` stores them, without skills and servers.
    spec: dict[str, object]
    #: Names of the plugin's skill folders, in the order the spec pins them.
    skills: tuple[str, ...]
    #: The tools of each server in ``mcp.json`` the writer may use.
    servers: dict[str, list[str]]
    #: The tools of each server in ``mcp.json`` the app calls to check a draft.
    checks: dict[str, list[str]]
    #: The tools of each server in ``mcp.json`` the app calls when it saves a draft.
    adds: dict[str, list[str]]
    #: The tools of each server in ``mcp.json`` the app calls to make a file of saved content.
    files: dict[str, list[str]]


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _strings(value: object) -> list[str] | None:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return [str(item) for item in value]
    return None


def _tools(value: object) -> dict[str, list[str]] | None:
    if not isinstance(value, dict):
        return None
    found: dict[str, list[str]] = {}
    for name, tools in value.items():
        listed = _strings(tools)
        if listed is None:
            return None
        found[str(name)] = listed
    return found


def _object(value: object) -> dict[str, object] | None:
    return {str(key): item for key, item in value.items()} if isinstance(value, dict) else None


def _what_it_adds(file: str, record: dict[str, object]) -> list[Problem]:
    """A plugin adds a type, or implements one that exists, and says so with one field."""
    if "implements" in record:
        extra = sorted({"type", "label", "audience", "made_from_a_plan_version"} & set(record))
        found = [
            Problem(file, f"{key} is not a field of a plugin that implements a type")
            for key in extra
        ]
        if _text(record["implements"]) is None:
            found.append(Problem(file, "implements is the slug of a type that exists"))
        return found
    return [
        Problem(file, f"{field} is a non-empty string")
        for field in ("type", "label", "audience")
        if _text(record.get(field)) is None
    ]


def read_artefact(folder: Path, relative: str) -> tuple[ArtefactFile | None, list[Problem]]:
    """The artefact file at ``relative`` in ``folder``, and everything wrong with it."""
    file = relative.removeprefix("./")
    path = folder / file
    if not path.is_file():
        return None, [Problem(file, "add the file that says what the plugin makes")]
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        return None, [Problem(file, f"is not valid JSON: {error}")]
    if not isinstance(record, dict):
        return None, [Problem(file, "is a JSON object")]
    return _artefact(file, {str(key): value for key, value in record.items()})


def _artefact(file: str, record: dict[str, object]) -> tuple[ArtefactFile | None, list[Problem]]:
    problems = [Problem(file, f"{key} is not a field here") for key in sorted(set(record) - _KEYS)]
    problems += _what_it_adds(file, record)
    text = {
        field: _text(record.get(field))
        for field in ("name", "type", "implements", "label", "audience")
    }
    if "name" in record and text["name"] is None:
        problems.append(Problem(file, "name is a non-empty string"))
    skills, servers = _strings(record.get("skills", [])), _tools(record.get("servers", {}))
    checks, adds = _tools(record.get("checks", {})), _tools(record.get("adds", {}))
    files = _tools(record.get("files", {}))
    spec = _object(record.get("spec"))
    if skills is None:
        problems.append(Problem(file, "skills lists the names of the plugin's skills"))
    if servers is None:
        problems.append(Problem(file, "servers maps each server to the list of its tools"))
    if checks is None:
        problems.append(Problem(file, "checks maps each server to the list of its check tools"))
    if adds is None:
        problems.append(Problem(file, "adds maps each server to the list of its adding tools"))
    if files is None:
        problems.append(Problem(file, "files maps each server to the list of its file tools"))
    if spec is None:
        problems.append(Problem(file, "spec is an object holding the type's spec"))
    if (
        problems
        or skills is None
        or servers is None
        or checks is None
        or adds is None
        or files is None
        or spec is None
    ):
        return None, problems
    return ArtefactFile(
        name=text["name"],
        type=text["type"],
        implements=text["implements"],
        label=text["label"] or "",
        audience=text["audience"] or "",
        made_from_a_plan_version=bool(record.get("made_from_a_plan_version", True)),
        spec=spec,
        skills=tuple(skills),
        servers=servers,
        checks=checks,
        adds=adds,
        files=files,
    ), []
