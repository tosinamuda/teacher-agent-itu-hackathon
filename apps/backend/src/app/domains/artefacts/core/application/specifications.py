"""Where the current specification of each content type is read from."""

from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification


class ContentSpecifications(Protocol):
    """The stored specifications; the highest revision of a kind's own specs is its current one."""

    async def current(self, db: AsyncSession, kind: str) -> ContentSpecification: ...

    async def revision(
        self, db: AsyncSession, kind: str, revision: int
    ) -> ContentSpecification: ...

    async def all_current(self, db: AsyncSession) -> list[ContentSpecification]: ...

    async def history(self, db: AsyncSession, kind: str) -> list[ContentSpecification]: ...

    async def add_revision(
        self,
        db: AsyncSession,
        specification: ContentSpecification,
        created_by: str | None,
        generator: str | None = None,
    ) -> ContentSpecification:
        """Store ``specification`` as the kind's next revision; its own number is ignored.

        A ``generator`` names the plugin it belongs to; such a revision is never the current one.
        """
        ...
