"""Skills in the ``content_skills`` table."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.skills import Skill, SkillFile
from app.domains.content.infrastructure.models import ContentSkillRecord


def _skill(row: ContentSkillRecord) -> Skill:
    return Skill(
        slug=row.slug,
        revision=row.revision,
        name=row.name,
        description=row.description,
        instructions=row.instructions,
        files=tuple(SkillFile(str(f["path"]), str(f["text"])) for f in row.files or ()),
    )


class SqlAlchemySkills:
    async def current(self, db: AsyncSession) -> list[Skill]:
        latest = (
            select(ContentSkillRecord.slug, func.max(ContentSkillRecord.revision).label("revision"))
            .group_by(ContentSkillRecord.slug)
            .subquery()
        )
        rows = await db.scalars(
            select(ContentSkillRecord)
            .join(
                latest,
                (ContentSkillRecord.slug == latest.c.slug)
                & (ContentSkillRecord.revision == latest.c.revision),
            )
            .order_by(ContentSkillRecord.slug)
        )
        return [_skill(row) for row in rows]

    async def revision(self, db: AsyncSession, slug: str, revision: int) -> Skill | None:
        row = await db.scalar(
            select(ContentSkillRecord)
            .where(ContentSkillRecord.slug == slug)
            .where(ContentSkillRecord.revision == revision)
        )
        return _skill(row) if row is not None else None

    async def latest(self, db: AsyncSession, slug: str) -> Skill | None:
        row = await db.scalar(
            select(ContentSkillRecord)
            .where(ContentSkillRecord.slug == slug)
            .order_by(ContentSkillRecord.revision.desc())
            .limit(1)
        )
        return _skill(row) if row is not None else None

    async def add(self, db: AsyncSession, skill: Skill, created_by: str | None) -> Skill:
        last = await db.scalar(
            select(func.max(ContentSkillRecord.revision)).where(
                ContentSkillRecord.slug == skill.slug
            )
        )
        stored = Skill(
            slug=skill.slug,
            revision=(last or 0) + 1,
            name=skill.name,
            description=skill.description,
            instructions=skill.instructions,
            files=skill.files,
        )
        db.add(
            ContentSkillRecord(
                slug=stored.slug,
                revision=stored.revision,
                name=stored.name,
                description=stored.description,
                instructions=stored.instructions,
                files=[{"path": f.path, "text": f.text} for f in stored.files],
                created_by=created_by,
            )
        )
        await db.flush()
        return stored
