"""Derive per-distractor misconception codes for an MCQ item (FD-03).

The teacher hand-enters classwork (FD-02) without misconception tags; this infers,
for each WRONG option, a short snake_case code naming the error a student who picks
it likely holds — the same representation the LLM diagnostic generator emits, so the
derived tags feed scoring/learner-state/P1 identically. The teacher reviews/edits the
suggestions before they persist.
"""

from __future__ import annotations

import logging

import dspy
from pydantic import BaseModel, ConfigDict, Field

from app.infra.dspy_lm import build_dspy_lm


class DerivedMisconceptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    option_misconceptions: dict[str, str] = Field(
        default_factory=dict,
        description="Wrong option key -> short snake_case misconception code.",
    )


class DeriveMisconceptionsSignature(dspy.Signature):
    """Tag each WRONG option of a multiple-choice maths item with the misconception it reveals.

    Given the question, its options, and which option is correct, name — for EACH
    wrong option — a short snake_case code for the specific error a student who picks
    it likely holds (e.g. "area_perimeter_confusion"). Tag ONLY the wrong options,
    never the correct one. Keep each code specific to the maths error, not generic
    ("wrong_answer"). Do not add commentary outside the schema.
    """

    stem: str = dspy.InputField(desc="The question stem.")
    options: dict[str, str] = dspy.InputField(desc="Option key (A-D) -> text.")
    correct_option: str = dspy.InputField(desc="The correct option key.")
    objective_text: str = dspy.InputField(desc="The lesson objective the item assesses (context).")
    output: DerivedMisconceptions = dspy.OutputField(desc="Wrong-option key -> misconception code.")


def valid_misconceptions(
    raw: dict[str, str] | None, options: dict[str, str], correct_option: str
) -> dict[str, str]:
    """Keep only wrong options that exist and carry a non-empty code.

    Mirrors the diagnostic generator's filter so a derived map never tags the correct
    answer or an option that isn't on the item.
    """
    return {
        key: code.strip()
        for key, code in (raw or {}).items()
        if key in options and key != correct_option and isinstance(code, str) and code.strip()
    }


class MisconceptionDeriver:
    def __init__(self) -> None:
        self.lm = build_dspy_lm()
        self.predict = dspy.ChainOfThought(DeriveMisconceptionsSignature)
        self.logger = logging.getLogger(__name__)

    async def derive(
        self,
        *,
        stem: str,
        options: dict[str, str],
        correct_option: str,
        objective_text: str = "",
    ) -> dict[str, str]:
        with dspy.settings.context(lm=self.lm):
            result = await self.predict.acall(
                stem=stem,
                options=options,
                correct_option=correct_option,
                objective_text=objective_text,
            )
        return valid_misconceptions(result.output.option_misconceptions, options, correct_option)
