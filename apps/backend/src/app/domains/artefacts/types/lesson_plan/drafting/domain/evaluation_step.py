from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    PlannerContentBlock,
    PlannerPlanStep,
    PracticeBlock,
)


def build_evaluation_step(
    assessment_by_objective: dict[str, AssessmentItem],
    *,
    step_id: str = "step-evaluation",
    title: str = "Evaluation",
    content: str = "Check mastery of the lesson objectives.",
    estimated_minutes: int = 10,
) -> PlannerPlanStep:
    """Assemble the evaluation step deterministically from the curated assessment items.

    The evaluation step is a no-latitude transcription of the per-objective
    ``AssessmentItem``s the planner already produced (reused from a textbook exercise
    in ``manual_linkage`` mode, or LLM-designed at planning time in ``curriculum_only``
    mode). Letting the LLM re-author it adds no value and is the source of the
    "evaluation steps require at least one practice block" crash when the model drops
    the items. We build it here — no LLM — so the step is always valid and always
    grounded in the curated content.

    One ``PracticeBlock`` is emitted per assessment item, in objective order. The dict
    key is used as the ``lesson_objective_id`` fallback when the item itself omits it
    (the evaluation invariant requires every practice block to carry a lesson objective).
    An objective whose item has neither is skipped — the existing soft
    ``missing_evaluation_coverage`` check then surfaces it on refine rather than crashing.

    Raises ``ValueError`` only if no usable assessment item exists at all (the evaluation
    invariant requires at least one practice block); in practice every objective gets an
    item from the planner, so this is a defensive guard.
    """
    blocks: list[PlannerContentBlock] = []
    for index, (objective_id, item) in enumerate(assessment_by_objective.items(), start=1):
        lesson_objective_id = (item.lesson_objective_id or objective_id or "").strip()
        if not lesson_objective_id:
            continue
        blocks.append(
            PracticeBlock(
                id=f"eval-practice-{index}",
                type="practice",
                question=item.question,
                answer=item.expected_answer,
                lesson_objective_id=lesson_objective_id,
            )
        )

    if not blocks:
        raise ValueError(
            "cannot build evaluation step: no assessment item carries a lesson objective"
        )

    # Constructed via ``model_validate`` so the CANONICAL field names are used —
    # the LM-facing aliases (``step_role`` etc.) exist only for the model boundary,
    # and the synthesized __init__ signature knows only the aliases.
    return PlannerPlanStep.model_validate(
        {
            "step_id": step_id,
            "step_kind": "evaluation",
            "title": title,
            "content": content,
            "estimated_minutes": estimated_minutes,
            "blocks": blocks,
        }
    )
