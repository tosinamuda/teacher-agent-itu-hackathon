"""v2 LM-facing models + personalisation signature (evidence-rich variant).

These are EXPERIMENT-ONLY contracts. Field names are chosen for the LM (clean,
self-describing), mirroring how production handles LM-facing naming. If v2 wins
the comparison, the production port goes through the real request schema +
``SectionPersonalisation`` with proper aliases — not by importing
from here.
"""

from __future__ import annotations

import dspy
from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    GenerationPolicyContext,
    LessonContextForGeneration,
    SourceEvidenceItem,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)


class AnswerEvidenceItem(BaseModel):
    """One diagnostic question the learner got wrong, with the chosen distractor."""

    model_config = ConfigDict(extra="forbid")

    question: str
    options: dict[str, str] = Field(default_factory=dict)
    correct_option: str
    student_choice: str
    chosen_option_misconception: str | None = Field(
        default=None,
        description="The misconception the chosen distractor was authored to reveal.",
    )


class ObjectiveLearnerEvidence(BaseModel):
    """v2 learner state: the distilled card PLUS the raw answer evidence."""

    model_config = ConfigDict(extra="forbid")

    lesson_objective_id: str
    status: str = Field(description="remediate | reinforce | extend")
    mastery_score: float | None = None
    confidence_score: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Self-reported: 1 (not sure at all) to 5 (very sure they can do this alone).",
    )
    difficulty_score: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Self-reported: 1 (very easy) to 5 (very difficult).",
    )
    misconception: str | None = Field(
        default=None, description="The diagnosed misconception, in plain words."
    )
    evidence_items: list[AnswerEvidenceItem] = Field(
        default_factory=list,
        description=(
            "The questions this learner missed for this objective, with their chosen options."
        ),
    )


class SessionSignals(BaseModel):
    """Session-level survey signals, asked once for the whole lesson."""

    model_config = ConfigDict(extra="forbid")

    interest_score: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="1 (not interested in the topic) to 5 (very interested).",
    )
    end_of_lesson_feeling: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="1 (very confused at the end of the lesson) to 5 (very good).",
    )


class PersonaliseReviewPackSectionV2Signature(dspy.Signature):
    """Personalise an approved base study-pack section for one focal learner.

    The lesson objective MUST be preserved. Adapt depth, scaffolding and examples
    to the learner's objective-indexed state (remediate / reinforce / extend).
    Use the answer evidence to target the SPECIFIC misconception the learner
    showed: address why their chosen option is tempting but wrong, phrased
    gently (never "you chose B, so you are wrong" — instead "a common slip
    here is ..."). Calibrate support to the self-reports: low confidence or
    high difficulty -> more worked support and hints; high confidence with
    high mastery -> less redundancy, more challenge. Session signals set tone
    and length: low interest -> shorter, more direct sections; a low
    end-of-lesson feeling -> reduce cognitive load and reassure. Keep grounding
    in the provided evidence and its source_refs.
    """

    policy: GenerationPolicyContext = dspy.InputField(desc="Personalisation + preservation policy.")
    lesson_context: LessonContextForGeneration = dspy.InputField()
    base_section: ReviewPackSection = dspy.InputField(desc="Approved base section.")
    learner_state: ObjectiveLearnerEvidence = dspy.InputField(
        desc="Objective-indexed learner state with per-question answer evidence."
    )
    session_signals: SessionSignals = dspy.InputField(
        desc="Session-level interest + end-of-lesson feeling (tone/depth modifiers)."
    )
    source_evidence: list[SourceEvidenceItem] = dspy.InputField()
    output: ReviewPackSection = dspy.OutputField(
        desc=(
            "Personalised section preserving the same lesson objective. Return ALL "
            "content blocks (adapt each block's text to the learner; never return an "
            "empty blocks list)."
        )
    )
