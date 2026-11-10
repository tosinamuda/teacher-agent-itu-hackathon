"""Generate objective-indexed MCQ diagnostic items with tagged distractors.

Each item carries a difficulty and, for every wrong option, a misconception
code — so a student selecting a distractor reveals that misconception. This is
the evidence instrument behind objective-indexed learner state: answers give
mastery (band), the chosen distractors give misconceptions; a separate survey
adds the emotive signals (confidence, perceived difficulty).
"""

from __future__ import annotations

import logging
from typing import Literal

import dspy
from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.infra.dspy_lm import build_dspy_lm


class DiagnosticMCQItem(BaseModel):
    """One multiple-choice diagnostic item with tagged distractors."""

    model_config = ConfigDict(extra="forbid")

    stem: str = Field(..., min_length=1)
    options: dict[str, str] = Field(..., description="Option key (A-D) -> text.")
    correct_option: str = Field(..., min_length=1)
    distractor_misconceptions: dict[str, str] = Field(
        default_factory=dict,
        description="Wrong option key -> short snake_case misconception code.",
    )
    difficulty: Literal["easy", "medium", "hard"]


class DiagnosticItemSet(BaseModel):
    """The set of items generated for one objective."""

    model_config = ConfigDict(extra="forbid")

    items: list[DiagnosticMCQItem] = Field(default_factory=list)


class GenerateDiagnosticItemsSignature(dspy.Signature):
    """Write the class-test items artefact_spec describes, for ONE lesson objective.

    Follow every requirement in artefact_spec exactly.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(desc="The brief to follow exactly.")
    objective_text: str = dspy.InputField(desc="The lesson objective to assess.")
    subject: str = dspy.InputField(desc="Subject, e.g. Mathematics.")
    grade: str = dspy.InputField(desc="Grade, e.g. JSS1.")
    topic: str = dspy.InputField(desc="Lesson topic for context.")
    item_count: int = dspy.InputField(desc="How many items to write for this objective.")
    output: DiagnosticItemSet = dspy.OutputField(desc="The MCQ items with tagged distractors.")


class DiagnosticItemGenerator:
    """LLM generator for objective-scoped MCQ diagnostic items."""

    def __init__(self) -> None:
        self.lm = build_dspy_lm()
        self.predict = dspy.ChainOfThought(GenerateDiagnosticItemsSignature)
        self.logger = logging.getLogger(__name__)

    async def generate(
        self,
        *,
        brief: ArtefactSpec,
        objective_text: str,
        subject: str,
        grade: str,
        topic: str,
        item_count: int = 2,
        draw: int = 0,
    ) -> list[DiagnosticMCQItem]:
        """The items of one draw; draw 0 is the cached one, each later draw a fresh sample."""
        config = {"rollout_id": draw} if draw else {}
        with dspy.settings.context(lm=self.lm):
            result = await self.predict.acall(
                artefact_spec=brief,
                objective_text=objective_text,
                subject=subject,
                grade=grade,
                topic=topic,
                item_count=item_count,
                config=config,
            )
        return list(result.output.items)
