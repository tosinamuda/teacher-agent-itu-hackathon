"""Save a finished revision-note draft as the lesson's class revision note."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.application.engine_base_pack import (
    EngineBasePackError,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_engine_base_pack,
)
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.shared.json_types import JsonObject


class RevisionNoteDestination:
    """The class note is stored as the pipeline's is, and its plugin's scripts check it.

    A learner's note is made from it and the teacher reviews it exactly as they would the
    pipeline's.
    """

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """What the pack's structural checks find in the finished parts, for the writer to mend."""
        if draft.plan_version_id is None:
            return []
        written = {unit.unit_id: part for unit, part in draft.written()}
        return await build_engine_base_pack().faults(db, draft.plan_version_id, written)

    def preview(self, draft: Draft) -> JsonObject:
        return {"content_type": draft.type, "sections": draft.sections()}

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        if draft.plan_version_id is None:
            raise DraftError("a revision note is made from a plan version")
        if draft.saved_as is not None:
            raise DraftError("a revision note is revised in its chat, not drafted again")
        written = {unit.unit_id: part for unit, part in draft.written()}
        try:
            stored = await build_engine_base_pack().store(
                db=db,
                plan_version_id=draft.plan_version_id,
                written=written,
                generator=generator,
            )
        except EngineBasePackError as error:
            raise DraftError(f"the revision note cannot be saved yet: {error}") from error
        return stored
