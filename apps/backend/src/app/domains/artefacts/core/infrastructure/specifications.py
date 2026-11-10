"""Specifications in the ``content_specifications`` table."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.core.infrastructure.models import ContentSpecificationRecord


class ContentSpecificationNotSeededError(LookupError):
    """No revision of a kind is stored: the specification seed has not run."""


def _specification(row: ContentSpecificationRecord) -> ContentSpecification:
    return ContentSpecification.from_record(
        {
            "kind": row.kind,
            "revision": row.revision,
            "material": row.material,
            "audience": row.audience,
            "levels": row.levels,
            "structure": row.structure,
            "requirements": row.requirements,
            "adaptable": row.adaptable,
            "unit": row.unit,
            "parts": row.parts,
            "lesson_parts": row.lesson_parts,
            "skills": row.skills,
            "mcp": row.mcp,
        }
    )


class SqlAlchemyContentSpecifications:
    """Reads the highest revision of each kind among the type's own specs.

    A spec that belongs to a plugin's generator takes a revision number of the kind but is never
    its current one; it is read by its number.
    """

    async def current(self, db: AsyncSession, kind: str) -> ContentSpecification:
        row = (
            await db.execute(
                select(ContentSpecificationRecord)
                .where(ContentSpecificationRecord.kind == kind)
                .where(ContentSpecificationRecord.generator.is_(None))
                .order_by(ContentSpecificationRecord.revision.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if row is None:
            raise ContentSpecificationNotSeededError(f"content_specification_not_seeded:{kind}")
        return _specification(row)

    async def revision(self, db: AsyncSession, kind: str, revision: int) -> ContentSpecification:
        row = (
            await db.execute(
                select(ContentSpecificationRecord)
                .where(ContentSpecificationRecord.kind == kind)
                .where(ContentSpecificationRecord.revision == revision)
            )
        ).scalar_one_or_none()
        if row is None:
            raise LookupError(f"content_specification_not_found:{kind}:{revision}")
        return _specification(row)

    async def all_current(self, db: AsyncSession) -> list[ContentSpecification]:
        latest = (
            select(
                ContentSpecificationRecord.kind,
                func.max(ContentSpecificationRecord.revision).label("revision"),
            )
            .where(ContentSpecificationRecord.generator.is_(None))
            .group_by(ContentSpecificationRecord.kind)
            .subquery()
        )
        rows = (
            await db.execute(
                select(ContentSpecificationRecord)
                .join(
                    latest,
                    (ContentSpecificationRecord.kind == latest.c.kind)
                    & (ContentSpecificationRecord.revision == latest.c.revision),
                )
                .order_by(ContentSpecificationRecord.kind)
            )
        ).scalars()
        return [_specification(row) for row in rows]

    async def history(self, db: AsyncSession, kind: str) -> list[ContentSpecification]:
        rows = (
            await db.execute(
                select(ContentSpecificationRecord)
                .where(ContentSpecificationRecord.kind == kind)
                .where(ContentSpecificationRecord.generator.is_(None))
                .order_by(ContentSpecificationRecord.revision)
            )
        ).scalars()
        return [_specification(row) for row in rows]

    async def add_revision(
        self,
        db: AsyncSession,
        specification: ContentSpecification,
        created_by: str | None,
        generator: str | None = None,
    ) -> ContentSpecification:
        latest = (
            await db.execute(
                select(func.max(ContentSpecificationRecord.revision)).where(
                    ContentSpecificationRecord.kind == specification.kind
                )
            )
        ).scalar_one_or_none()
        record = {**specification.to_record(), "revision": (latest or 0) + 1}
        db.add(ContentSpecificationRecord(**record, generator=generator, created_by=created_by))
        await db.commit()
        return ContentSpecification.from_record(record)
