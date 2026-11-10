"""Installed plugins in the ``content_plugins`` table."""

from __future__ import annotations

import json
from collections.abc import Mapping

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.plugins import PluginFiles, PluginRevision, PluginStatus
from app.domains.content.infrastructure.models import ContentPluginRecord


def _plugin_of(row: ContentPluginRecord) -> str:
    """The manifest name in the files the row was installed with; the row's own name without."""
    try:
        manifest = json.loads((row.files or {}).get("plugin.json", ""))
        name = manifest.get("name") if isinstance(manifest, dict) else None
    except ValueError:
        name = None
    return name if isinstance(name, str) else row.name


def _revision(row: ContentPluginRecord) -> PluginRevision:
    return PluginRevision(
        name=row.name,
        revision=row.revision,
        version=row.version,
        digest=row.digest,
        type_slug=row.type_slug,
        spec_revision=row.spec_revision,
        status=PluginStatus(row.status),
        installed_by=row.installed_by,
        implements=row.implements,
        plugin=_plugin_of(row),
    )


class SqlAlchemyPlugins:
    async def latest(self, db: AsyncSession, name: str) -> PluginRevision | None:
        row = await db.scalar(
            select(ContentPluginRecord)
            .where(ContentPluginRecord.name == name)
            .order_by(ContentPluginRecord.revision.desc())
            .limit(1)
        )
        return _revision(row) if row is not None else None

    async def of_type(self, db: AsyncSession, type_slug: str) -> PluginRevision | None:
        row = await db.scalar(
            select(ContentPluginRecord)
            .where(ContentPluginRecord.type_slug == type_slug)
            .where(ContentPluginRecord.implements.is_(False))
            .limit(1)
        )
        return await self.latest(db, row.name) if row is not None else None

    async def all_latest(self, db: AsyncSession) -> list[PluginRevision]:
        newest = (
            select(ContentPluginRecord.name, func.max(ContentPluginRecord.revision).label("n"))
            .group_by(ContentPluginRecord.name)
            .subquery()
        )
        rows = await db.scalars(
            select(ContentPluginRecord)
            .join(
                newest,
                (ContentPluginRecord.name == newest.c.name)
                & (ContentPluginRecord.revision == newest.c.n),
            )
            .order_by(ContentPluginRecord.name)
        )
        return [_revision(row) for row in rows]

    async def files_for(
        self, db: AsyncSession, type_slug: str, spec_revision: int
    ) -> PluginFiles | None:
        row = await db.scalar(
            select(ContentPluginRecord)
            .where(
                ContentPluginRecord.type_slug == type_slug,
                ContentPluginRecord.spec_revision == spec_revision,
                ContentPluginRecord.status == PluginStatus.INSTALLED.value,
                ContentPluginRecord.files.is_not(None),
            )
            .order_by(ContentPluginRecord.revision.desc())
            .limit(1)
        )
        if row is None or row.files is None:
            return None
        latest = await self.latest(db, row.name)
        if latest is None or not latest.installed:
            return None
        return PluginFiles(row.name, row.revision, {str(k): str(v) for k, v in row.files.items()})

    async def add(
        self, db: AsyncSession, revision: PluginRevision, files: Mapping[str, str] | None = None
    ) -> PluginRevision:
        last = await db.scalar(
            select(func.max(ContentPluginRecord.revision)).where(
                ContentPluginRecord.name == revision.name
            )
        )
        row = ContentPluginRecord(
            name=revision.name,
            revision=(last or 0) + 1,
            version=revision.version,
            digest=revision.digest,
            type_slug=revision.type_slug,
            spec_revision=revision.spec_revision,
            status=revision.status.value,
            installed_by=revision.installed_by,
            implements=revision.implements,
            files=dict(files) if files is not None else None,
        )
        db.add(row)
        await db.flush()
        return _revision(row)
