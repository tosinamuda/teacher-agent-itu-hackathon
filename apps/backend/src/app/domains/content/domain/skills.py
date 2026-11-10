"""Skills: know-how a writer applies, kept as data so any content type can reuse it.

A skill is written as a ``SKILL.md`` file: front matter naming it and saying when to use it,
then the instructions. It may carry reference files, markdown a writer reads when the
instructions send it there. A spec pins the skills its type is written with, each at a revision,
so content records exactly which know-how shaped it, and a type gains a skill by a new spec
revision, never by code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from pathlib import PurePosixPath

import yaml

from app.domains.artefacts.core.domain.skill_refs import SKILL_SLUG, SkillRef
from app.shared.json_types import JsonObject, JsonValue

_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
#: Where a skill's reference files sit, beside its instructions.
REFERENCES = "references"
_MAX_FILES = 20
_MAX_FILE_CHARACTERS = 20_000


class SkillError(ValueError):
    """A skill that cannot be used, or a reference to one."""


def split_skill_markdown(slug: str, text: str) -> tuple[dict[str, object], str]:
    """A ``SKILL.md`` split into its front matter mapping and its instructions."""
    found = _FRONT_MATTER.match(text.replace("\r\n", "\n"))
    if found is None:
        raise SkillError(f"{slug}: SKILL.md starts with front matter between --- lines")
    front = yaml.safe_load(found.group(1))
    if not isinstance(front, dict):
        raise SkillError(f"{slug}: the front matter is a mapping")
    return front, found.group(2).strip()


@dataclass(frozen=True)
class SkillFile:
    """One reference file of a skill: markdown at a path under ``references/``."""

    path: str
    text: str

    def __post_init__(self) -> None:
        """Refuse a file that is not markdown inside the skill's references folder."""
        parts = PurePosixPath(self.path).parts
        inside = len(parts) > 1 and parts[0] == REFERENCES and ".." not in parts
        if PurePosixPath(self.path).is_absolute() or not inside or not self.path.endswith(".md"):
            raise SkillError(f"a reference file is markdown under {REFERENCES}/: {self.path!r}")
        if not self.text.strip() or len(self.text) > _MAX_FILE_CHARACTERS:
            raise SkillError(f"{self.path} holds 1 to {_MAX_FILE_CHARACTERS} characters")


@dataclass(frozen=True)
class Skill:
    slug: str
    revision: int
    #: What a person calls it.
    name: str
    #: When a writer should use it.
    description: str
    #: The know-how itself, in markdown.
    instructions: str
    #: Reference files the instructions send a writer to.
    files: tuple[SkillFile, ...] = ()

    def __post_init__(self) -> None:
        """Refuse a skill a writer could not be told how to use."""
        if not SKILL_SLUG.match(self.slug) or len(self.slug) > 64:
            raise SkillError(f"a skill slug is lowercase words joined by hyphens: {self.slug!r}")
        if self.revision < 1:
            raise SkillError(f"{self.slug}: revisions count from 1")
        for field, value in (("name", self.name), ("description", self.description)):
            if not value.strip():
                raise SkillError(f"{self.slug}: a skill has a {field}")
        if not self.instructions.strip():
            raise SkillError(f"{self.slug}: a skill has instructions")
        paths = [file.path for file in self.files]
        if len(paths) > _MAX_FILES or len(set(paths)) != len(paths):
            raise SkillError(f"{self.slug}: at most {_MAX_FILES} reference files, each once")

    @classmethod
    def from_markdown(cls, slug: str, text: str) -> Skill:
        """A skill from a ``SKILL.md`` file: front matter, then the instructions."""
        front, instructions = split_skill_markdown(slug, text)
        revision = front.get("revision", 1)
        return cls(
            slug=slug,
            revision=revision if isinstance(revision, int) else 0,
            name=str(front.get("name", "")),
            description=str(front.get("description", "")),
            instructions=instructions,
        )

    def with_files(self, files: tuple[SkillFile, ...]) -> Skill:
        return replace(self, files=files)

    def ref(self) -> SkillRef:
        return SkillRef(self.slug, self.revision)

    def summary(self) -> JsonObject:
        """What a list of skills shows: enough to choose one."""
        return {
            "skill": self.slug,
            "revision": self.revision,
            "name": self.name,
            "description": self.description,
            "files": [file.path for file in self.files],
        }

    def document(self) -> JsonObject:
        """The skill whole, as a harness that loads it itself is given it."""
        files: list[JsonValue] = [{"path": f.path, "text": f.text} for f in self.files]
        return {**self.summary(), "instructions": self.instructions, "files": files}

    def for_writer(self) -> JsonObject:
        """The skill as a writer is given it."""
        return {"name": self.name, "use_when": self.description, "instructions": self.instructions}
