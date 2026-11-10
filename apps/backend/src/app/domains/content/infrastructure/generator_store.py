"""Generators in the ``content_type_generators`` table."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.generators import (
    GeneratorBinding,
    GeneratorKind,
    GeneratorStatus,
    SchemaSource,
)
from app.domains.content.domain.types import Level
from app.domains.content.infrastructure.models import ContentTypeGeneratorRecord


def _binding(row: ContentTypeGeneratorRecord) -> GeneratorBinding:
    return GeneratorBinding(
        type_slug=row.type_slug,
        level=Level(row.level),
        harness=GeneratorKind(row.harness),
        schema=SchemaSource(row.schema_source),
        ref=row.ref,
        status=GeneratorStatus(row.status),
        spec_revision=row.spec_revision,
    )


class SqlAlchemyGeneratorBindings:
    async def of(self, db: AsyncSession, slug: str, level: Level) -> list[GeneratorBinding]:
        rows = await db.execute(
            select(ContentTypeGeneratorRecord)
            .where(ContentTypeGeneratorRecord.type_slug == slug)
            .where(ContentTypeGeneratorRecord.level == level.value)
            .order_by(ContentTypeGeneratorRecord.ref.desc())
        )
        return [_binding(row) for row in rows.scalars()]

    async def add(self, db: AsyncSession, binding: GeneratorBinding, by: str | None) -> None:
        db.add(
            ContentTypeGeneratorRecord(
                type_slug=binding.type_slug,
                level=binding.level.value,
                harness=binding.harness.value,
                schema_source=binding.schema.value,
                ref=binding.ref,
                spec_revision=binding.spec_revision,
                status=GeneratorStatus.AVAILABLE.value,
                changed_by=by,
            )
        )
        await db.flush()

    async def set_spec_revision(
        self, db: AsyncSession, binding: GeneratorBinding, spec_revision: int, by: str | None
    ) -> None:
        row = await self._row(db, binding)
        row.spec_revision = spec_revision
        if row.status == GeneratorStatus.RETIRED.value:
            row.status = GeneratorStatus.AVAILABLE.value
        self._changed(row, by)
        await db.flush()

    async def set_default(
        self, db: AsyncSession, binding: GeneratorBinding, by: str | None
    ) -> None:
        rows = await db.scalars(
            select(ContentTypeGeneratorRecord)
            .where(ContentTypeGeneratorRecord.type_slug == binding.type_slug)
            .where(ContentTypeGeneratorRecord.level == binding.level.value)
            .where(ContentTypeGeneratorRecord.status == GeneratorStatus.DEFAULT.value)
        )
        for old in rows:
            old.status = GeneratorStatus.AVAILABLE.value
            old.default_key = None
            self._changed(old, by)
        await db.flush()
        row = await self._row(db, binding)
        row.status = GeneratorStatus.DEFAULT.value
        row.default_key = f"{binding.type_slug}:{binding.level.value}"
        self._changed(row, by)
        await db.flush()

    async def retire(self, db: AsyncSession, binding: GeneratorBinding, by: str | None) -> None:
        row = await self._row(db, binding)
        row.status = GeneratorStatus.RETIRED.value
        self._changed(row, by)
        await db.flush()

    async def _row(self, db: AsyncSession, binding: GeneratorBinding) -> ContentTypeGeneratorRecord:
        return (
            await db.execute(
                select(ContentTypeGeneratorRecord)
                .where(ContentTypeGeneratorRecord.type_slug == binding.type_slug)
                .where(ContentTypeGeneratorRecord.level == binding.level.value)
                .where(ContentTypeGeneratorRecord.harness == binding.harness.value)
                .where(ContentTypeGeneratorRecord.ref == binding.ref)
            )
        ).scalar_one()

    @staticmethod
    def _changed(row: ContentTypeGeneratorRecord, by: str | None) -> None:
        row.changed_by = by
        row.changed_at = datetime.now(timezone.utc)
