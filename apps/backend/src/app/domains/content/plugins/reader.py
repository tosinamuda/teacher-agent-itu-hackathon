"""Read a plugin folder into a plugin, or into the list of what is wrong with it."""

from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from pathlib import Path

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.artefacts.core.domain.skill_refs import SkillRefError
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.domain.skills import Skill, SkillError, split_skill_markdown
from app.domains.content.domain.types import Audience, ContentTypeDefinition, Engine
from app.domains.content.plugins.artefact import ArtefactFile, read_artefact
from app.domains.content.plugins.manifest import PluginManifest, read_manifest
from app.domains.content.plugins.plugin import Plugin
from app.domains.content.plugins.problems import Problem, Severity, errors_in
from app.domains.content.plugins.servers import ListedTools, read_servers, unused_servers
from app.domains.content.skill_seed import references_of

SKILLS_DIR = "skills"
_FOLDER = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_RESERVED = ("anthropic", "claude")
#: The longest skill name and description an Agent Skills reader accepts.
_NAME_LIMIT = 64
_DESCRIPTION_LIMIT = 1024


def _naming_faults(where: str, folder_name: str, text: str, skill: Skill) -> list[Problem]:
    """What the Agent Skills format asks of a skill's name and description, and of revision."""
    faults: list[Problem] = []
    if skill.name != folder_name:
        faults.append(
            Problem(where, f"name is {skill.name!r}; it is the folder name, {folder_name!r}")
        )
    if any(word in folder_name for word in _RESERVED):
        faults.append(Problem(where, f"the folder name holds none of {', '.join(_RESERVED)}"))
    if len(folder_name) > _NAME_LIMIT:
        faults.append(Problem(where, f"the folder name is at most {_NAME_LIMIT} letters"))
    if len(skill.description) > _DESCRIPTION_LIMIT:
        faults.append(Problem(where, f"description is at most {_DESCRIPTION_LIMIT} letters"))
    if "revision" in split_skill_markdown(folder_name, text)[0]:
        faults.append(
            Problem(where, "remove revision; installing numbers the revisions", Severity.WARNING)
        )
    return faults


def _unmentioned_references(where: str, skill: Skill) -> list[Problem]:
    """A warning for each reference file that the skill's instructions never name."""
    return [
        Problem(
            where,
            f"{file.path} is not named in the instructions, so nothing says when to read it",
            Severity.WARNING,
        )
        for file in skill.files
        if file.path not in skill.instructions
    ]


def _skill(artefact_file: str, folder: Path, name: str) -> tuple[Skill | None, list[Problem]]:
    where = f"{SKILLS_DIR}/{name}/SKILL.md"
    if not _FOLDER.match(name):
        return None, [Problem(artefact_file, f"skills names a folder of lowercase words: {name!r}")]
    path = folder / where
    if not path.is_file():
        return None, [
            Problem(where, f"add SKILL.md for the skill {name} that {artefact_file} lists")
        ]
    text = path.read_text(encoding="utf-8")
    try:
        skill = Skill.from_markdown(name, text)
        skill = replace(skill, revision=1, files=references_of(path.parent))
    except SkillError as error:
        return None, [Problem(where, str(error))]
    faults = [*_naming_faults(where, name, text, skill), *_unmentioned_references(where, skill)]
    return (None if errors_in(faults) else skill), faults


def _skills(
    artefact_file: str, folder: Path, listed: tuple[str, ...]
) -> tuple[tuple[Skill, ...], list[Problem]]:
    found: list[Skill] = []
    problems: list[Problem] = []
    for name in listed:
        skill, faults = _skill(artefact_file, folder, name)
        problems += faults
        if skill is not None:
            found.append(skill)
    return tuple(found), problems


def _unpinned_skills(folder: Path, artefacts: list[tuple[str, ArtefactFile]]) -> list[Problem]:
    """A warning for each skill folder that no artefact of the plugin lists."""
    listed = {name for _, artefact in artefacts for name in artefact.skills}
    present = {path.parent.name for path in (folder / SKILLS_DIR).glob("*/SKILL.md")}
    return [
        Problem(
            f"{SKILLS_DIR}/{name}",
            "is listed in no artefact file, so no spec pins it",
            Severity.WARNING,
        )
        for name in sorted(present - listed)
    ]


def _slug(artefact: ArtefactFile) -> str:
    return artefact.type or artefact.implements or ""


def _definition(artefact: ArtefactFile) -> ContentTypeDefinition | None:
    """The type a plugin adds; none for a plugin that implements a type that exists."""
    if artefact.type is None:
        return None
    return ContentTypeDefinition(
        slug=artefact.type,
        kind=ContentTypeDefinition.kind_for(artefact.type),
        label=artefact.label,
        audience=Audience(artefact.audience),
        engine=Engine.MCP,
        made_from_a_plan_version=artefact.made_from_a_plan_version,
        position=0,
    )


def _specification(
    artefact_file: str,
    artefact: ArtefactFile,
    skills: tuple[Skill, ...],
    servers: tuple[McpServerRef, ...],
) -> tuple[ContentTypeDefinition | None, ContentSpecification | None, list[Problem]]:
    """The type and spec the artefact file describes, refused as the API would refuse them."""
    try:
        definition = _definition(artefact)
        kind = definition.kind if definition else ContentTypeDefinition.kind_for(_slug(artefact))
        record = {
            **artefact.spec,
            "kind": kind,
            "revision": 1,
            "skills": [skill.ref().to_record() for skill in skills],
            "mcp": [server.to_record() for server in servers],
        }
        spec = ContentSpecification.from_record(record)
        if definition is not None:
            definition.check(spec)
    except (KeyError, TypeError, ValueError, SkillRefError) as error:
        return None, None, [Problem(artefact_file, f"spec: {error}")]
    return definition, spec, []


def _names(
    manifest: PluginManifest, artefacts: list[tuple[str, ArtefactFile]]
) -> tuple[list[str], list[Problem]]:
    """The name each artefact installs under: its own, or the plugin's when it is the only one."""
    names = [artefact.name or manifest.name for _, artefact in artefacts]
    problems = [
        Problem(file, "name tells this artefact from the plugin's others")
        for file, artefact in artefacts
        if artefact.name is None and len(manifest.artefacts) > 1
    ]
    problems += [
        Problem(file, f"name {name!r} is used by another artefact of the plugin")
        for (file, _), name in zip(artefacts, names, strict=True)
        if names.count(name) > 1
    ]
    return names, problems


def _files_for(
    files: dict[str, str], manifest: PluginManifest, own: ArtefactFile, own_file: str
) -> dict[str, str]:
    """The folder's files that one artefact uses: not another's skills, nor another's file."""
    others = {path.removeprefix("./") for path in manifest.artefacts} - {own_file}
    return {
        path: text
        for path, text in files.items()
        if path not in others
        and not (path.startswith(f"{SKILLS_DIR}/") and path.split("/")[1] not in own.skills)
    }


def read_plugins(folder: Path) -> tuple[list[Plugin], list[Problem]]:
    """The plugins in ``folder``, one for each artefact, and every problem found.

    No plugin is returned when any problem is an error: a folder installs whole or not at all.
    """
    manifest, problems = read_manifest(folder)
    if manifest is None:
        return [], problems
    artefacts: list[tuple[str, ArtefactFile]] = []
    for path in manifest.artefacts:
        artefact, more = read_artefact(folder, path)
        problems += more
        if artefact is not None:
            artefacts.append((path.removeprefix("./"), artefact))
    names, more = _names(manifest, artefacts)
    files, faults = read_files(folder)
    problems += more + faults + _unpinned_skills(folder, artefacts)
    plugins: list[Plugin] = []
    for (file, artefact), name in zip(artefacts, names, strict=True):
        skills, more = _skills(file, folder, artefact.skills)
        servers, faults = read_servers(
            folder,
            ListedTools(artefact.servers, artefact.checks, artefact.adds, artefact.files),
            file,
        )
        definition, spec, found = _specification(file, artefact, skills, servers)
        problems += more + faults + found
        if spec is not None:
            own = _files_for(files, manifest, artefact, file)
            plugins.append(
                Plugin(manifest, name, definition, artefact.implements, spec, skills, servers, own)
            )
    linked = {server.name for plugin in plugins for server in plugin.servers}
    problems = list(dict.fromkeys([*problems, *unused_servers(folder, linked)]))
    if errors_in(problems) or len(plugins) != len(manifest.artefacts):
        return [], problems
    return plugins, problems


def _plugin_paths(folder: Path) -> list[Path]:
    """The files a plugin is made of: every file outside a hidden folder or a bytecode cache."""
    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file()
        and not any(
            part.startswith(".") or part == "__pycache__" for part in path.relative_to(folder).parts
        )
    )


def read_files(folder: Path) -> tuple[dict[str, str], list[Problem]]:
    """The text of every file of the plugin by its path, and a problem for each file not text."""
    files: dict[str, str] = {}
    problems: list[Problem] = []
    for path in _plugin_paths(folder):
        where = path.relative_to(folder).as_posix()
        try:
            files[where] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(Problem(where, "is not text; a plugin holds text files only"))
    return files, problems


def folder_digest(folder: Path) -> str:
    """A hash of every file in ``folder`` by path and content, so equal folders hash equal."""
    digest = hashlib.sha256()
    for path in _plugin_paths(folder):
        digest.update(path.relative_to(folder).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()
