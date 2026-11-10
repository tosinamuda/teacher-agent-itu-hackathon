"""Model contract for finding learner-visible defects in one generated section."""

from typing import Literal

import dspy
from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    ReviewPackPipeline,
)

ContentDefect = Literal["grounding", "consistency", "audience"]


class ContentFinding(BaseModel):
    """One defect in a review-pack section, tied to the text that carries it."""

    model_config = ConfigDict(extra="forbid")

    defect: ContentDefect = Field(..., description="Which kind of defect this is.")
    quote: str = Field(
        ...,
        min_length=1,
        description="The exact words from the section that carry the defect, copied verbatim.",
    )
    problem: str = Field(..., min_length=1, description="What is wrong with them.")


class SectionCritique(dspy.Signature):
    """Find text in a review-pack section that must not reach a learner.

    Read the section as the 11-to-13 year old it is written for. Report a
    finding only where you can quote the exact words that carry the defect, and
    only for these three kinds:

    grounding — something stated as fact that is false or unfounded: a wrong
      definition or rule, a claim about real events or people that never
      happened, a cause or reason invented to explain the numbers, or material
      from a topic this lesson did not cover. Made-up numbers in an example or
      practice question are ordinary teaching and are NOT a defect; what must
      never be invented is an explanation OF them, or a fact about the world.
      Teaching the lesson's own topic is what the section is FOR, so standard
      definitions, explanations and extra practice belong in it whether or not
      the evidence spells them out. Anything the evidence itself states is
      settled — this class was taught it, so never report it, and never correct
      it towards a more general or more advanced formulation. Report invention,
      never elaboration.
    consistency — a statement the section's own tables, numbers or examples
      contradict, or a worked answer that does not follow from its own working.
    audience — text written for anyone other than the learner: labels naming
      the lesson's own stages or objectives, narration of what the teacher does
      in class, or any mention of where the material came from ("the source",
      "the textbook", "the evidence", "the lesson note"). A "fig-NN" citation is
      none of these: the figure it names is printed beside the text under that
      label, and the citation is how the reader finds it. Numbered steps inside
      a worked solution or instructions to the reader are how a method is taught
      and are NOT a defect.

    Work through the section to the end and report every defect you find. Report
    nothing about style, tone, length or how much of the objective is covered.
    Return an empty list when the section is clean.
    """

    setting: str = dspy.InputField(
        desc=(
            "The curriculum and country this pack is written for. Vocabulary normal in "
            "that setting is correct even where another one would say it differently."
        )
    )
    lesson_objective: str = dspy.InputField(desc="What this section is meant to teach.")
    teaching_evidence: str = dspy.InputField(
        desc="What the class was taught, as recorded by the teacher. May be empty."
    )
    section_to_review: str = dspy.InputField(desc="The section exactly as the learner reads it.")
    findings: list[ContentFinding] = dspy.OutputField(
        desc="Every defect found, each quoting the section verbatim. Empty when there are none."
    )


# The critic's instructions as Part 1's run sent them, verbatim; pipeline 2026-08-25 reads
# these. The study's fingerprint recorded their digest, and a test holds them to it.
EVALUATED_SECTION_CRITIQUE_INSTRUCTIONS = (
    "Find text in a review-pack section that must not reach a learner.\n"
    "\n"
    "Read the section as the 11-to-13 year old it is written for. Report a\n"
    "finding only where you can quote the exact words that carry the defect, and\n"
    "only for these three kinds:\n"
    "\n"
    "grounding — something stated as fact that is false or unfounded: a wrong\n"
    "  definition or rule, a claim about real events or people that never\n"
    "  happened, a cause or reason invented to explain the numbers, or material\n"
    "  from a topic this lesson did not cover. Made-up numbers in an example or\n"
    "  practice question are ordinary teaching and are NOT a defect; what must\n"
    "  never be invented is an explanation OF them, or a fact about the world.\n"
    "  Teaching the lesson's own topic is what the section is FOR, so standard\n"
    "  definitions, explanations and extra practice belong in it whether or not\n"
    "  the evidence spells them out. Anything the evidence itself states is\n"
    "  settled — this class was taught it, so never report it, and never correct\n"
    "  it towards a more general or more advanced formulation. Report invention,\n"
    "  never elaboration.\n"
    "consistency — a statement the section's own tables, numbers or examples\n"
    "  contradict, or a worked answer that does not follow from its own working.\n"
    "audience — text written for anyone other than the learner: labels naming\n"
    "  the lesson's own stages or objectives, narration of what the teacher does\n"
    '  in class, or any mention of where the material came from ("the source",\n'
    '  "the textbook", "the evidence", "the lesson note"). Numbered steps inside\n'
    "  a worked solution or instructions to the reader are how a method is taught\n"
    "  and are NOT a defect.\n"
    "\n"
    "Work through the section to the end and report every defect you find. Report\n"
    "nothing about style, tone, length or how much of the objective is covered.\n"
    "Return an empty list when the section is clean."
)


def critique_contract(pipeline: ReviewPackPipeline) -> type[dspy.Signature]:
    """The critic's contract for a pipeline version: same fields, that version's instructions."""
    if pipeline is ReviewPackPipeline.V2026_08_25:
        evaluated: type[dspy.Signature] = SectionCritique.with_instructions(
            EVALUATED_SECTION_CRITIQUE_INSTRUCTIONS
        )
        return evaluated
    return SectionCritique
