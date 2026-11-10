"""Read the skills shipped beside this module, one folder per skill.

A folder's ``SKILL.md`` is the skill's current revision, with the markdown files under its
``references/`` as its reference files. ``revisions/<n>.md`` keeps each earlier revision as it
was, so a spec that pins one can still be built on a new database.
"""

from __future__ import annotations

from functools import cache
from pathlib import Path

from app.domains.content.domain.skills import REFERENCES, Skill, SkillError, SkillFile

SKILLS_PATH = Path(__file__).with_name("skills")


def _earlier(folder: Path) -> list[Skill]:
    earlier = []
    for file in (folder / "revisions").glob("*.md"):
        skill = Skill.from_markdown(folder.name, file.read_text(encoding="utf-8"))
        if file.stem != str(skill.revision):
            raise SkillError(f"{folder.name}: {file.name} holds revision {skill.revision}")
        earlier.append(skill)
    return sorted(earlier, key=lambda skill: skill.revision)


def references_of(folder: Path) -> tuple[SkillFile, ...]:
    """The markdown files under a skill folder's ``references/``, by path."""
    files = sorted((folder / REFERENCES).rglob("*.md"))
    return tuple(
        SkillFile(file.relative_to(folder).as_posix(), file.read_text(encoding="utf-8"))
        for file in files
    )


def read_skills(root: Path) -> tuple[Skill, ...]:
    """Every revision of every skill under ``root``, by slug and then revision."""
    shipped: list[Skill] = []
    for folder in sorted(root.iterdir()):
        if (folder / "SKILL.md").is_file():
            text = (folder / "SKILL.md").read_text("utf-8")
            current = Skill.from_markdown(folder.name, text).with_files(references_of(folder))
            earlier = _earlier(folder)
            if any(skill.revision >= current.revision for skill in earlier):
                raise SkillError(f"{folder.name}: SKILL.md is the latest revision")
            shipped.extend([*earlier, current])
    return tuple(shipped)


@cache
def seed_skills() -> tuple[Skill, ...]:
    """Every shipped revision of every skill."""
    return read_skills(SKILLS_PATH)
