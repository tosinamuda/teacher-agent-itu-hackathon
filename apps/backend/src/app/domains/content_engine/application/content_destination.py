"""Save a finished draft as content made from a plan version, pending the teacher's review."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import (
    ContentSpecification,
    specification_ref,
)
from app.domains.content_engine.application.drafting_ports import ContentStore
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.shared.json_types import JsonObject

#: What a finished draft must satisfy to be saved, as the lines it still needs to fix.
Check = Callable[[AsyncSession, Draft], Awaitable[list[str]]]
#: The fields a type's plugin adds to its saved content, such as a deck's cover.
Additions = Callable[[Draft, ContentSpecification], Awaitable[JsonObject]]


class ContentDestination:
    """Engine types: the draft's sections are the content, stored as they were written."""

    def __init__(self, content: ContentStore, additions: Additions | None = None) -> None:
        """``additions`` are the fields the draft's plugin adds when the content is saved."""
        self._content = content
        self._additions = additions

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """An engine type is checked by its plugin's scripts alone."""
        return []

    def preview(self, draft: Draft) -> JsonObject:
        return {"content_type": draft.type, "sections": draft.sections()}

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        if draft.plan_version_id is None:
            raise DraftError(f"{draft.type} is made from a plan version")
        manifest: JsonObject = {
            "content_type": draft.type,
            "plan_version_id": draft.plan_version_id,
            "unit": draft.unit.value,
            "sections": draft.sections(),
        }
        if self._additions is not None:
            manifest = {**manifest, **await self._additions(draft, spec)}
        if draft.saved_as is not None:
            await self._content.replace(db, draft.saved_as, manifest)
            return draft.saved_as
        return await self._content.add(
            db,
            kind=draft.kind,
            plan_version_id=draft.plan_version_id,
            manifest=manifest,
            refs={
                **specification_ref(spec),
                "origin": "generated",
                "generator": generator,
                "engine": {"draft_id": draft.draft_id},
            },
        )
