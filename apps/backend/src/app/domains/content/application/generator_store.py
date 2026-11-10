"""Where the generators of each content type are read from."""

from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.generators import GeneratorBinding
from app.domains.content.domain.types import Level


class GeneratorBindings(Protocol):
    """The generators registered for a type at a level."""

    async def of(self, db: AsyncSession, slug: str, level: Level) -> list[GeneratorBinding]: ...

    async def add(self, db: AsyncSession, binding: GeneratorBinding, by: str | None) -> None:
        """Register a generator that is available, never the default."""
        ...

    async def set_spec_revision(
        self, db: AsyncSession, binding: GeneratorBinding, spec_revision: int, by: str | None
    ) -> None: ...

    async def set_default(
        self, db: AsyncSession, binding: GeneratorBinding, by: str | None
    ) -> None:
        """Make the generator the type's default at its level, and the old default available."""
        ...

    async def retire(self, db: AsyncSession, binding: GeneratorBinding, by: str | None) -> None: ...
