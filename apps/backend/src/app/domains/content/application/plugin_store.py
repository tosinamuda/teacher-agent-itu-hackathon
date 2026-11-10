"""Where installed plugins are recorded."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.plugins import PluginFiles, PluginRevision


class PluginStore(Protocol):
    """Every revision of every plugin. A revision is added, never edited."""

    async def latest(self, db: AsyncSession, name: str) -> PluginRevision | None: ...

    async def of_type(self, db: AsyncSession, type_slug: str) -> PluginRevision | None:
        """The latest revision of the plugin that added the type, if a plugin did.

        A plugin that only implements the type is not the one that added it.
        """
        ...

    async def all_latest(self, db: AsyncSession) -> list[PluginRevision]:
        """The latest revision of each plugin, by name."""
        ...

    async def add(
        self, db: AsyncSession, revision: PluginRevision, files: Mapping[str, str] | None = None
    ) -> PluginRevision:
        """Store ``revision`` as its plugin's next one; its own number is ignored."""
        ...

    async def files_for(
        self, db: AsyncSession, type_slug: str, spec_revision: int
    ) -> PluginFiles | None:
        """The files of the latest revision that made the spec revision; none once removed."""
        ...
