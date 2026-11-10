"""The skill library: every skill's revisions, and the skills a spec is written with."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.skill_refs import SkillRef
from app.domains.content.application.errors import ContentError
from app.domains.content.domain.skills import Skill


class SkillStore(Protocol):
    """Every revision of every skill. A revision is added, never edited."""

    async def current(self, db: AsyncSession) -> list[Skill]:
        """The latest revision of each skill, by slug."""
        ...

    async def revision(self, db: AsyncSession, slug: str, revision: int) -> Skill | None: ...

    async def latest(self, db: AsyncSession, slug: str) -> Skill | None: ...

    async def add(self, db: AsyncSession, skill: Skill, created_by: str | None) -> Skill:
        """Store ``skill`` as its slug's next revision; its own revision is ignored."""
        ...


class SkillLibrary:
    def __init__(self, store: SkillStore) -> None:
        self._store = store

    async def skills(self, db: AsyncSession) -> list[Skill]:
        return await self._store.current(db)

    async def find(self, db: AsyncSession, slug: str) -> Skill | None:
        """The latest revision of the skill, or nothing when the slug is new."""
        return await self._store.latest(db, slug)

    async def skill(self, db: AsyncSession, slug: str) -> Skill:
        found = await self._store.latest(db, slug)
        if found is None:
            raise ContentError(404, f"unknown_skill:{slug}")
        return found

    async def at(self, db: AsyncSession, slug: str, revision: int | None) -> Skill:
        """The skill at ``revision``, or at its latest when none is given."""
        if revision is None:
            return await self.skill(db, slug)
        found = await self._store.revision(db, slug, revision)
        if found is None:
            raise ContentError(404, f"unknown_skill_revision:{slug}@{revision}")
        return found

    async def pinned(self, db: AsyncSession, refs: Sequence[SkillRef]) -> list[Skill]:
        """The skills ``refs`` pin, each at its revision; refused if one is not stored."""
        found: list[Skill] = []
        for ref in refs:
            skill = await self._store.revision(db, ref.slug, ref.revision)
            if skill is None:
                raise ContentError(422, f"unknown_skill_revision:{ref.slug}@{ref.revision}")
            found.append(skill)
        return found

    async def add(self, db: AsyncSession, skill: Skill, created_by: str | None) -> Skill:
        """Store ``skill`` as the next revision of its slug."""
        return await self._store.add(db, skill, created_by)
