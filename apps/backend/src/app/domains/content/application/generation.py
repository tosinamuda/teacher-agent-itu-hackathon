"""Generating one type of content from a frozen plan version."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.types import Level


@dataclass(frozen=True)
class GenerationChoices:
    """What a request may choose about how content is generated.

    ``pipeline`` names the type's generator by its ref: a revision note's version by date, a
    plugin's name, or ``builtin`` for the original program; the default when unset. ``sources``
    names the expert content a revision note is grounded in, and no other type takes it.
    """

    pipeline: str | None = None
    sources: str | None = None
    #: What the teacher asked for in their own words, for an engine type's first draft.
    instructions: str | None = None


class ContentGenerator(Protocol):
    """Generates content of a type and returns the new item's ID.

    ``type`` is the slug asked for: the engine builds every engine type, so it needs it.
    """

    def check(self, level: Level, choices: GenerationChoices) -> None:
        """Refuse, before any generation, what this type is never made as."""
        ...

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        type: str,
        level: Level,
        choices: GenerationChoices,
    ) -> str: ...
