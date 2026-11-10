"""Where the registered content types are read from and added to."""

from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.types import ContentTypeDefinition


class ContentTypes(Protocol):
    """Every registered type. A type is added, never edited or removed."""

    async def all(self, db: AsyncSession) -> list[ContentTypeDefinition]:
        """Every type, in position order."""
        ...

    async def get(self, db: AsyncSession, slug: str) -> ContentTypeDefinition | None: ...

    async def by_kind(self, db: AsyncSession, kind: str) -> ContentTypeDefinition | None: ...

    async def add(
        self, db: AsyncSession, definition: ContentTypeDefinition, created_by: str | None
    ) -> ContentTypeDefinition:
        """Store ``definition`` after every type already registered; its position is ignored."""
        ...
