"""What a writer reads about the learner whose revision note it writes."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.application.adaptation_parameters import (
    resolve_parameters,
)
from app.domains.artefacts.types.post_class_review_pack.application.engine_learner_pack import (
    EngineLearnerPack,
    EngineLearnerPackError,
    LearnerWork,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    PERSONALISED_REVIEW_PACK_POLICY,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.content_engine.domain.draft import DraftError
from app.shared.json_types import JsonObject, JsonValue


def _section(section: ReviewPackSection) -> JsonObject:
    """The class note's section as the learner's version starts from."""
    return {
        "lesson_objective_id": section.lesson_objective_id,
        "title": section.title,
        "blocks": [
            {"kind": b.block_type, "text": b.text}
            for b in section.blocks
            if b.block_type != "visual"
        ],
        "practice": [
            {"question": p.prompt, "answer": p.answer, "worked_solution": p.worked_solution}
            for p in section.practice
        ],
    }


class LessonLearners:
    def __init__(self, packs: EngineLearnerPack) -> None:
        self._packs = packs

    async def context(self, db: AsyncSession, plan_version_id: str, student_id: str) -> JsonObject:
        work = await self._work(db, plan_version_id, student_id)
        least = PERSONALISED_REVIEW_PACK_POLICY.personalisation.min_marked_questions
        signals = work.learner.signals
        objectives: list[JsonValue] = []
        for base in work.base_sections:
            objective = base.lesson_objective_id
            state = work.learner.states.get(objective)
            objectives.append(
                {
                    "lesson_objective_id": objective,
                    "adapt": work.adapts(objective),
                    "marked_questions": work.learner.marked_questions.get(objective, 0),
                    "class_section": _section(base),
                    "learner_state": state.model_dump(mode="json") if state else None,
                    "adaptation": (
                        resolve_parameters(state).model_dump(mode="json")
                        if state and work.adapts(objective)
                        else None
                    ),
                }
            )
        return {
            "student_id": student_id,
            "class_note": {
                "artefact_id": work.class_pack.artefact_id,
                "version": work.class_pack.version,
            },
            "marked_questions_needed_to_adapt": least,
            "session_signals": signals.model_dump(mode="json") if signals else None,
            "objectives": list[JsonValue](objectives),
        }

    async def adapted(self, db: AsyncSession, plan_version_id: str, student_id: str) -> list[str]:
        return (await self._work(db, plan_version_id, student_id)).adapted_objectives()

    async def _work(self, db: AsyncSession, plan_version_id: str, student_id: str) -> LearnerWork:
        try:
            return await self._packs.work(db, plan_version_id, student_id)
        except EngineLearnerPackError as error:
            raise DraftError(str(error)) from error
