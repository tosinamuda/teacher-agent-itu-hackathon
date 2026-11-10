"""Content types in the ``content_types`` table."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.types import Audience, ContentTypeDefinition, Engine
from app.domains.content.infrastructure.models import ContentTypeRecord


def _definition(row: ContentTypeRecord) -> ContentTypeDefinition:
    return ContentTypeDefinition(
        slug=row.slug,
        kind=row.kind,
        label=row.label,
        audience=Audience(row.audience),
        engine=Engine(row.engine),
        made_from_a_plan_version=row.made_from_a_plan_version,
        position=row.position,
    )


class SqlAlchemyContentTypes:
    async def all(self, db: AsyncSession) -> list[ContentTypeDefinition]:
        rows = await db.execute(select(ContentTypeRecord).order_by(ContentTypeRecord.position))
        return [_definition(row) for row in rows.scalars()]

    async def get(self, db: AsyncSession, slug: str) -> ContentTypeDefinition | None:
        row = await db.scalar(select(ContentTypeRecord).where(ContentTypeRecord.slug == slug))
        return _definition(row) if row is not None else None

    async def by_kind(self, db: AsyncSession, kind: str) -> ContentTypeDefinition | None:
        row = await db.scalar(select(ContentTypeRecord).where(ContentTypeRecord.kind == kind))
        return _definition(row) if row is not None else None

    async def add(
        self, db: AsyncSession, definition: ContentTypeDefinition, created_by: str | None
    ) -> ContentTypeDefinition:
        last = await db.scalar(select(func.max(ContentTypeRecord.position)))
        record = ContentTypeRecord(
            slug=definition.slug,
            kind=definition.kind,
            label=definition.label,
            audience=definition.audience.value,
            engine=definition.engine.value,
            made_from_a_plan_version=definition.made_from_a_plan_version,
            position=(last or 0) + 1,
            created_by=created_by,
        )
        db.add(record)
        await db.flush()
        return _definition(record)
