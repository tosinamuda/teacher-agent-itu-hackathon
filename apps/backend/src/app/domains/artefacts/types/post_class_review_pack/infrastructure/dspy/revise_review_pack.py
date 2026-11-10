"""Apply focused teacher feedback while preserving pack coverage and identity."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.generation_log.application.recorder import log_context

from .contracts.revise_review_pack import ApplyReviewPackFeedback
from .prompt_projection import prompt_lesson

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReviewPackRevisionResult:
    """The outcome of one review-pack revision turn."""

    sections: list[ReviewPackSection]
    change_summary: str


def _preserve_coverage(
    *,
    original: list[ReviewPackSection],
    revised: list[ReviewPackSection],
) -> list[ReviewPackSection]:
    """Force the revised pack back onto the original objective set + identity.

    Takes the model's revised section per objective when it exists and is
    non-empty, otherwise keeps the original — so a turn can change content but can
    never drop an objective or change a section's stable ids.
    """
    revised_by_objective: dict[str, ReviewPackSection] = {}
    for section in revised:
        if section.lesson_objective_id and section.blocks:
            revised_by_objective.setdefault(section.lesson_objective_id, section)

    out: list[ReviewPackSection] = []
    for base in original:
        candidate = revised_by_objective.get(base.lesson_objective_id)
        if candidate is None:
            out.append(base)
            continue
        candidate.section_id = base.section_id
        candidate.lesson_objective_id = base.lesson_objective_id
        for block_index, block in enumerate(candidate.blocks):
            block.lesson_objective_id = base.lesson_objective_id
            if not block.block_id:
                block.block_id = f"{base.section_id}:b{block_index}"
        out.append(candidate)
    return out


class ReviseReviewPack(dspy.Module):
    """Produce a coverage-preserving pack from one teacher instruction."""

    def __init__(self, *, lm: dspy.BaseLM) -> None:
        super().__init__()
        self.lm = lm
        self.apply_feedback = dspy.ChainOfThought(ApplyReviewPackFeedback)

    async def aforward(
        self,
        *,
        current_sections: list[ReviewPackSection],
        lesson_context: LessonContextForGeneration,
        highlighted_part: str,
        instruction: str,
        conversation_summary: str,
        correlation_id: str,
        thread_id: str,
    ) -> ReviewPackRevisionResult:
        with log_context(
            kind="study_pack_revision",
            correlation_id=correlation_id,
            thread_id=thread_id,
        ):
            with dspy.settings.context(lm=self.lm):
                result = await self.apply_feedback.acall(
                    lesson_context=prompt_lesson(lesson_context),
                    current_sections=current_sections,
                    highlighted_part=highlighted_part or "(none — whole-pack instruction)",
                    revision_instruction=instruction,
                    conversation_summary=conversation_summary or "(first turn)",
                )
        revised = list(getattr(result, "revised_sections", None) or [])
        sections = _preserve_coverage(original=current_sections, revised=revised)
        summary = str(getattr(result, "change_summary", "") or "Revised the study pack.")
        logger.info("review-pack revision produced %s section(s)", len(sections))
        return ReviewPackRevisionResult(sections=sections, change_summary=summary)

    async def revise(
        self,
        *,
        current_sections: list[ReviewPackSection],
        lesson_context: LessonContextForGeneration,
        highlighted_part: str,
        instruction: str,
        conversation_summary: str,
        correlation_id: str,
        thread_id: str,
    ) -> ReviewPackRevisionResult:
        revised: ReviewPackRevisionResult = await self.acall(
            current_sections=current_sections,
            lesson_context=lesson_context,
            highlighted_part=highlighted_part,
            instruction=instruction,
            conversation_summary=conversation_summary,
            correlation_id=correlation_id,
            thread_id=thread_id,
        )
        return revised
