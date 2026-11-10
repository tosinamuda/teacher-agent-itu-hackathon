"""A run's workspace: the folder a harness starts in, with the skills it is to find there.

A harness looks for its project's skills in the folder it is started in, as ``SKILL.md`` files
under ``.agents/skills/<name>/``. The engine's skills are already that format, pinned by a
type's spec at a revision, so a run reads the pinned revisions from the engine's server, writes
them and their reference files into a folder of its own, and starts the harness there. The
harness then loads a skill when the model asks for it, where the brief would have carried the
text of every skill in every call.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from mcp import Client

from app.domains.content.domain.skills import SkillFile, split_skill_markdown
from app.domains.content_engine.infrastructure.engine import resource_json
from app.domains.content_engine.infrastructure.harness.plugin_skills import plugin_skill_files
from app.shared.json_types import JsonObject

#: Where OpenCode and DeepSeek Harness look for a project's skills, from the folder they start in.
SKILLS_DIR = Path(".agents") / "skills"
#: The longest skill name and description an Agent Skills reader accepts.
_DESCRIPTION_LIMIT = 1024


class SkillError(ValueError):
    """A pinned skill that a harness would not accept as a skill file."""


@dataclass(frozen=True)
class WorkspaceSkill:
    """One pinned skill as a ``SKILL.md`` file."""

    slug: str
    description: str
    instructions: str
    files: tuple[SkillFile, ...] = ()
    #: The skill folder's files as a plugin holds them, by path, to copy as they are.
    copied: Mapping[str, str] = field(default_factory=dict)

    @property
    def has_references(self) -> bool:
        """Whether the skill has files beyond its instructions for a writer to read."""
        return bool(self.files) or any(path != "SKILL.md" for path in self.copied)

    def document(self) -> str:
        """The file: front matter naming the skill and saying when to use it, then the text.

        The values are written as JSON strings, which YAML reads as they are. A skill copied
        from a plugin is the plugin's own file.
        """
        if not self.description.strip() or len(self.description) > _DESCRIPTION_LIMIT:
            raise SkillError(
                f"{self.slug} needs a description of 1 to {_DESCRIPTION_LIMIT} letters"
            )
        if "SKILL.md" in self.copied:
            return self.copied["SKILL.md"]
        name, description = json.dumps(self.slug), json.dumps(self.description)
        return (
            f"---\nname: {name}\ndescription: {description}\n---\n\n{self.instructions.strip()}\n"
        )


def _copied(name: str, files: Mapping[str, str]) -> WorkspaceSkill:
    front, instructions = split_skill_markdown(name, files["SKILL.md"])
    return WorkspaceSkill(name, str(front.get("description", "")), instructions, copied=files)


async def pinned_skills(client: Client, draft: JsonObject) -> list[WorkspaceSkill]:
    """The skills the draft's type pins: the plugin's own folders, else each skill's revision."""
    if (from_plugin := await plugin_skill_files(client, draft)) is not None:
        return [_copied(name, files) for name, files in from_plugin.items()]
    pinned = draft.get("pinned_skills")
    found: list[WorkspaceSkill] = []
    for ref in pinned if isinstance(pinned, list) else []:
        if not isinstance(ref, dict):
            raise SkillError(f"a pinned skill names a skill and a revision: {ref!r}")
        skill = await resource_json(client, f"skill://{ref['skill']}?revision={ref['revision']}")
        files = skill.get("files")
        found.append(
            WorkspaceSkill(
                str(ref["skill"]),
                str(skill["description"]),
                str(skill["instructions"]),
                tuple(
                    SkillFile(str(file["path"]), str(file["text"]))
                    for file in files
                    if isinstance(file, dict)
                )
                if isinstance(files, list)
                else (),
            )
        )
    return found


def without_skills(draft: JsonObject) -> JsonObject:
    """The draft with its brief's skills left out, for a harness that finds them itself."""
    brief = draft.get("brief")
    if not isinstance(brief, dict):
        return draft
    return {**draft, "brief": {name: value for name, value in brief.items() if name != "skills"}}


def write_skills(workspace: Path, skills: Sequence[WorkspaceSkill]) -> None:
    """Write each skill to ``workspace``'s skills folder."""
    for skill in skills:
        folder = workspace / SKILLS_DIR / skill.slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(skill.document(), encoding="utf-8")
        for path, text in skill.copied.items():
            target = folder / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        for file in skill.files:
            target = folder / file.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(file.text, encoding="utf-8")


def _digest(skill: WorkspaceSkill) -> str:
    kept = (f"{path}\n{text}" for path, text in sorted(skill.copied.items()))
    whole = [skill.document(), *(f"{file.path}\n{file.text}" for file in skill.files), *kept]
    return hashlib.sha256(json.dumps(whole).encode()).hexdigest()


def manifest(skills: Sequence[WorkspaceSkill]) -> JsonObject:
    """What a run's workspace held, to record with it: each skill file's hash, and one for all."""
    files = {skill.slug: _digest(skill) for skill in skills}
    overall = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {"skills": dict(sorted(files.items())), "sha256": overall}
