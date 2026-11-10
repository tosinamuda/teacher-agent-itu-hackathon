"""The repair step's output contract as Part 1's run sent it: pipeline 2026-08-25 only.

The current ``DraftBlock`` tells the model its text is markdown and never HTML; the Part 1
run predates that sentence, and a repair turn renders the output schema in full. These are
the models as they stood at 5b43e968 — same names, fields and descriptions — so the schema
2026-08-25 sends is the one Part 1's run sent. A repaired section is read back into the
current models.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    AuthoredBlockType,
    DraftPractice,
)


class DraftBlock(BaseModel):
    """One model-authored prose block, without record identity or provenance."""

    model_config = ConfigDict(extra="forbid")

    block_type: AuthoredBlockType = Field(description="What this block is for the reader.")
    text: str = Field(description="The block, written for the reader.")


class RevisedSection(BaseModel):
    """A finished section as the model reworks it, without persisted record fields."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(description="The reader-facing section title.")
    blocks: list[DraftBlock] = Field(
        description="The instructional blocks, in the order the reader meets them."
    )
    practice: list[DraftPractice] = Field(
        default_factory=list,
        description="What the learner does, each with the answer they check against.",
    )
