"""Diagnostic reviser — one focused, well-formed edit per human-feedback turn.

Runs ``ReviseDiagnosticSignature`` over the full MCQ item set, then
deterministically drops malformed items (no answer key in options) and preserves
objective coverage, so a wording tweak can never silently drop an objective or
break an item's answer key / distractor tags. Each LM call is tagged for the generation log.
This is the unit the HITL ``DiagnosticRevisionExecutor`` calls; it speaks only in
``DiagnosticItemForRevision`` and never touches the DB.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

import dspy
from pydantic import BaseModel, ConfigDict, Field

from app.domains.assessments.domain.option_order import placed
from app.domains.generation_log.application.recorder import log_context
from app.infra.dspy_lm import build_dspy_lm

logger = logging.getLogger(__name__)


class DiagnosticItemForRevision(BaseModel):
    """One MCQ item as seen by the reviser (item_id preserves identity)."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(default="", description="Preserve for kept/edited items; empty for new.")
    lesson_objective_id: str
    stem: str
    options: dict[str, str]
    correct_option: str
    distractor_misconceptions: dict[str, str] = Field(default_factory=dict)
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class ReviseDiagnosticSignature(dspy.Signature):
    """Apply ONE teacher instruction to an existing JSS1 MCQ diagnostic, minimally.

    You are an expert teacher revising a colleague's objective-indexed multiple-choice
    diagnostic in response to a single piece of feedback. Rules:
    - Apply EXACTLY the requested change and nothing else. Preserve every other item
      verbatim, INCLUDING its item_id, so unchanged items stay stable. Set item_id to
      an empty string ONLY for a brand-new item you add.
    - Keep objective coverage: every lesson_objective_id present in current_items must
      still have at least one item unless the instruction explicitly removes it.
    - Every item must stay well-formed: exactly four options keyed "A"-"D"; a
      correct_option that is one of the option keys; and for EACH wrong option a short
      snake_case misconception code in distractor_misconceptions naming the error a
      student picking it likely holds. Keep numbers grade-appropriate for JSS1.
    - If a highlighted part is given (an item_id / objective), scope the change to it;
      if it is empty, the instruction applies to the whole diagnostic.
    - Output the COMPLETE revised item set (not a diff).
    """

    objectives = dspy.InputField(
        desc="lesson_objective_id -> objective_text for the objectives this diagnostic covers."
    )
    current_items: list[DiagnosticItemForRevision] = dspy.InputField(
        desc="The full current MCQ diagnostic to revise."
    )
    highlighted_part = dspy.InputField(
        desc="The item/objective the teacher highlighted; empty for a whole-diagnostic change."
    )
    revision_instruction = dspy.InputField(desc="The teacher's free-text change request.")
    conversation_summary = dspy.InputField(
        desc="Summary of earlier revision turns (empty on the first turn)."
    )

    revised_items: list[DiagnosticItemForRevision] = dspy.OutputField(
        desc="The complete revised diagnostic — same items/objectives, focused change applied."
    )
    change_summary: str = dspy.OutputField(
        desc="One short sentence describing what you changed (for the chat history)."
    )


@dataclass(frozen=True)
class DiagnosticRevisionResult:
    """The outcome of one diagnostic revision turn."""

    items: list[DiagnosticItemForRevision]
    change_summary: str


def _well_formed(item: DiagnosticItemForRevision) -> bool:
    return (
        bool(item.stem.strip()) and len(item.options) >= 2 and item.correct_option in item.options
    )


def _clean(item: DiagnosticItemForRevision) -> DiagnosticItemForRevision:
    """Keep only distractor codes that name a real wrong option, and place the answer."""
    codes = {
        key: code
        for key, code in item.distractor_misconceptions.items()
        if key in item.options and key != item.correct_option
    }
    options = placed(item.options, item.correct_option, codes, stem=item.stem)
    item.options = options.options
    item.correct_option = options.correct_option
    item.distractor_misconceptions = options.misconceptions
    return item


def _preserve_coverage(
    *,
    original: list[DiagnosticItemForRevision],
    revised: list[DiagnosticItemForRevision],
) -> list[DiagnosticItemForRevision]:
    """Drop malformed revised items; restore an objective's originals if the model.

    dropped every item for it, so a turn can never lose objective coverage.
    """
    kept = [_clean(item) for item in revised if _well_formed(item)]
    covered = {item.lesson_objective_id for item in kept}
    originals_by_objective: dict[str, list[DiagnosticItemForRevision]] = {}
    for item in original:
        originals_by_objective.setdefault(item.lesson_objective_id, []).append(item)
    out = list(kept)
    for objective, items in originals_by_objective.items():
        if objective and objective not in covered:
            out.extend(items)
    return out or original


class DiagnosticReviser:
    """Produce a new, well-formed MCQ item set from the diagnostic + one instruction."""

    def __init__(self) -> None:
        self.lm = build_dspy_lm()
        self.revise_module = dspy.ChainOfThought(ReviseDiagnosticSignature)

    async def revise(
        self,
        *,
        current_items: list[DiagnosticItemForRevision],
        objectives: dict[str, str],
        highlighted_part: str,
        instruction: str,
        conversation_summary: str,
        correlation_id: str,
        thread_id: str,
    ) -> DiagnosticRevisionResult:
        with log_context(
            kind="diagnostic_revision",
            correlation_id=correlation_id,
            thread_id=thread_id,
        ):
            with dspy.settings.context(lm=self.lm):
                result = await self.revise_module.acall(
                    objectives=objectives,
                    current_items=current_items,
                    highlighted_part=highlighted_part or "(none — whole-diagnostic instruction)",
                    revision_instruction=instruction,
                    conversation_summary=conversation_summary or "(first turn)",
                )
        revised = list(getattr(result, "revised_items", None) or [])
        items = _preserve_coverage(original=current_items, revised=revised)
        summary = str(getattr(result, "change_summary", "") or "Revised the diagnostic.")
        logger.info("diagnostic revision produced %s item(s)", len(items))
        return DiagnosticRevisionResult(items=items, change_summary=summary)
