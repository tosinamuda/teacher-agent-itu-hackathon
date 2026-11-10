"""Schemas for model-authored drafts and persisted review-pack sections."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

BlockType = Literal["explanation", "worked_example", "misconception_repair", "visual"]
AuthoredBlockType = Literal["explanation", "worked_example"]
#: How a misconception repair opens in the stored note, which keeps every prose block as an
#: explanation and tells them apart by what they open with.
MISCONCEPTION_LABEL = "**A common slip**\n\n"


class ReviewPackBlock(BaseModel):
    """One learner-facing block within a generated section."""

    model_config = ConfigDict(extra="forbid")

    block_id: str
    block_type: BlockType = Field(
        description=(
            "Do not author 'visual' blocks — figure blocks are attached "
            "automatically from the lesson plan and any you write are discarded."
        )
    )
    text: str = ""
    lesson_objective_id: str
    source_refs: list[str] = Field(default_factory=list)
    variant: Literal["image", "diagram_tikz"] | None = None
    url: str | None = None
    caption: str | None = None
    figure_ref: str | None = None
    source_tikz: str | None = None
    source_record_id: str | None = None


class ReviewPackPracticeItem(BaseModel):
    """One thing the learner does, and what they check it against."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = ""
    prompt: str = Field(description="The question, as the learner reads it.")
    answer: str = Field(description="What the learner checks against, after attempting.")
    worked_solution: str | None = Field(
        default=None,
        description="The steps to the answer, where the answer alone will not do.",
    )


#: The practice fields the model writes and a learner reads. Everything that cleans,
#: measures or renders a practice item walks this rather than its own list.
WRITTEN_PRACTICE_FIELDS = ("prompt", "answer", "worked_solution")


class ReviewPackSection(BaseModel):
    """A generated or personalised review-pack section for one objective."""

    model_config = ConfigDict(extra="forbid")

    section_id: str
    title: str
    lesson_objective_id: str
    blocks: list[ReviewPackBlock]
    practice: list[ReviewPackPracticeItem] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class DraftBlock(BaseModel):
    """One model-authored prose block, without record identity or provenance."""

    model_config = ConfigDict(extra="forbid")

    block_type: AuthoredBlockType = Field(description="What this block is for the reader.")
    text: str = Field(
        description=(
            "The block, written for the reader. Markdown only — **bold**, *italic*, "
            "- lists, $LaTeX$. NEVER HTML: every reader-facing surface XML-escapes the "
            "text before converting the markdown, so a <strong> tag is shown to the "
            "reader as the literal characters <strong>."
        )
    )


class DraftPractice(BaseModel):
    """One model-authored practice item, without its persisted id."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(description="The question, as the learner reads it.")
    answer: str = Field(description="What the learner checks against, after attempting.")
    worked_solution: str | None = Field(
        default=None,
        description="The steps to the answer, where the answer alone will not do.",
    )


class DraftSection(BaseModel):
    """A section as the model writes it from an objective and its allowed context."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(description="The reader-facing section title.")
    instructional_support: str = Field(
        description=(
            "The principle, relationship, rule or representation the learner needs to "
            "review this objective. Concise and relational — not a summary of the topic."
        )
    )
    worked_examples: list[DraftBlock] = Field(
        description=(
            "One or more worked or modelled examples: the problem, then its solution "
            "worked through, demonstrating the knowledge or procedure being taught."
        )
    )
    practice: list[DraftPractice] = Field(
        description="What the learner does, each with the answer they check against."
    )


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
