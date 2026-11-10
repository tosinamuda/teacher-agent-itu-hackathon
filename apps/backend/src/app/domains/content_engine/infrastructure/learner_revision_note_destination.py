"""Save a finished learner's revision-note draft as that learner's pending note."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.application.adaptation_limits import (
    adaptation_faults,
)
from app.domains.artefacts.types.post_class_review_pack.application.engine_learner_pack import (
    EngineLearnerPack,
    EngineLearnerPackError,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_part_pins import (
    pinned,
)
from app.domains.content.domain.generator_contract import LEARNER_ADAPTABLE
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.shared.json_types import JsonObject


class LearnerRevisionNoteDestination:
    """A learner's note is held to what adaptation may change.

    Its plugin's scripts check the rest.
    """

    def __init__(self, packs: EngineLearnerPack) -> None:
        self._packs = packs

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        faults: list[str] = []
        if draft.plan_version_id is None or draft.student_id is None:
            return faults
        try:
            work = await self._packs.work(db, draft.plan_version_id, draft.student_id)
        except EngineLearnerPackError as error:
            return [*faults, str(error)]
        bases = {s.lesson_objective_id: s for s in work.base_sections}
        for unit, part in draft.written():
            base, state = bases.get(unit.unit_id), work.learner.states.get(unit.unit_id)
            if base is not None and state is not None:
                faults += [
                    f"{unit.unit_id}: {fault}"
                    for fault in adaptation_faults(
                        pinned(part, base, state), base, state, LEARNER_ADAPTABLE
                    )
                ]
        return faults

    def preview(self, draft: Draft) -> JsonObject:
        return {"content_type": draft.type, "sections": draft.sections()}

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        if draft.plan_version_id is None or draft.student_id is None:
            raise DraftError("a learner's revision note is made from a plan version and a learner")
        if draft.saved_as is not None:
            raise DraftError("a learner's revision note is written again, not revised, here")
        written = {unit.unit_id: part for unit, part in draft.written()}
        try:
            return await self._packs.store(
                db=db,
                plan_version_id=draft.plan_version_id,
                student_id=draft.student_id,
                written=written,
                generator=generator,
            )
        except EngineLearnerPackError as error:
            raise DraftError(f"the learner's note cannot be saved yet: {error}") from error
