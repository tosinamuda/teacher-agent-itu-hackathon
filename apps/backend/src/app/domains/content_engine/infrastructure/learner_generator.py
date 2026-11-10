"""Write one learner's revision note with the content engine, for the job that makes it."""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.application.engine_learner_pack import (
    EngineLearnerPack,
)
from app.domains.content.domain.generators import GeneratorBinding
from app.domains.content_engine.domain.draft import DraftError
from app.domains.content_engine.infrastructure.chat import HeldTap
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.learner_context import LessonLearners
from app.domains.content_engine.infrastructure.tap import tapping

REVISION_NOTE = "revision-note"


class EngineLearnerGenerator:
    def __init__(self, engine: Engine, packs: EngineLearnerPack, learners: LessonLearners) -> None:
        self._engine = engine
        self._packs = packs
        self._learners = learners

    async def generate(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str,
        student_id: str,
        binding: GeneratorBinding,
    ) -> str:
        """The id of the learner's pending note.

        When the learner has too little marked work to adapt any objective, the note is the class
        note as it stands and no agent runs.
        """
        try:
            adapted = await self._learners.adapted(db, plan_version_id, student_id)
        except DraftError as error:
            raise LookupError(str(error)) from error
        if not adapted:
            return await self._packs.store(
                db=db,
                plan_version_id=plan_version_id,
                student_id=student_id,
                written={},
                generator=binding.provenance(),
            )
        request = Request(
            type=REVISION_NOTE,
            plan_version_id=plan_version_id,
            student_id=student_id,
            generator=binding.ref,
        )
        with tapping(HeldTap()):
            built = await self._engine.build_kept(request, key=f"learner-{uuid.uuid4().hex}")
        await db.commit()
        return built.saved_as
