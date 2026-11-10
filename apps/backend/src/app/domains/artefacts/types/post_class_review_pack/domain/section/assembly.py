"""Pure assembly of model drafts into persisted review-pack sections."""

from collections.abc import Sequence
from typing import NamedTuple

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.shared.llm_markup import reader_ready

from .figures import append_grounded_figures
from .schemas import (
    BlockType,
    DraftBlock,
    DraftPractice,
    DraftSection,
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
    RevisedSection,
)


class AuthoredBlock(NamedTuple):
    """A block of prose an engine writer wrote, of any stored kind but a figure.

    ``DraftBlock`` is the pipeline's schema and stays as it is: it has two kinds. A learner's
    note also has a misconception repair, which only the engine writes.
    """

    block_type: BlockType
    text: str


def clean_model_text(text: str) -> str:
    r"""What the model wrote, as a reader can be shown it.

    Decoding the transport's escapes is half of it. The other half is markup the
    model never supplied: `Perimeter = 4 \times side` is stored exactly as written
    and reaches the page with the backslash showing, because only delimited maths
    is typeset. See :func:`~app.shared.llm_markup.reader_ready`.
    """
    return reader_ready(text)


def section_from_draft(draft: DraftSection, unit: SectionGenerationUnit) -> ReviewPackSection:
    """Build a stored section from a model draft and the unit's identity."""
    stream: list[DraftBlock] = []
    if draft.instructional_support.strip():
        stream.append(DraftBlock(block_type="explanation", text=draft.instructional_support))
    stream.extend(draft.worked_examples)
    return assemble_section(title=draft.title, blocks=stream, practice=draft.practice, unit=unit)


def section_from_revision(
    revised: RevisedSection, unit: SectionGenerationUnit
) -> ReviewPackSection:
    """Build a stored section from a rewritten section and the unit's identity."""
    return assemble_section(
        title=revised.title, blocks=revised.blocks, practice=revised.practice, unit=unit
    )


def assemble_section(
    *,
    title: str,
    blocks: Sequence[DraftBlock | AuthoredBlock],
    practice: Sequence[DraftPractice],
    unit: SectionGenerationUnit,
) -> ReviewPackSection:
    """Apply identity, provenance, figures, and text cleanup to model-authored content.

    The single place a section acquires an id, and the single place the model's
    writing is made reader-ready — every entry point assembles through here, so no
    path can store text a reader cannot be shown.
    """
    refs = [item.source_ref for item in unit.source_evidence if item.source_ref]
    section = ReviewPackSection(
        section_id=unit.unit_id,
        title=title,
        lesson_objective_id=unit.lesson_objective_id,
        blocks=[
            ReviewPackBlock(
                block_id=f"{unit.unit_id}:b{index}",
                block_type=block.block_type,
                text=clean_model_text(block.text),
                lesson_objective_id=unit.lesson_objective_id,
                source_refs=list(refs),
            )
            for index, block in enumerate(blocks)
        ],
        practice=[
            ReviewPackPracticeItem(
                item_id=f"{unit.unit_id}:p{index}",
                prompt=clean_model_text(item.prompt),
                answer=clean_model_text(item.answer),
                worked_solution=(
                    clean_model_text(item.worked_solution) if item.worked_solution else None
                ),
            )
            for index, item in enumerate(practice)
        ],
    )
    append_grounded_figures(section, unit)
    return section


def normalise_section(section: ReviewPackSection, unit: SectionGenerationUnit) -> ReviewPackSection:
    """Rebuild a finished section so identity and provenance come only from its unit."""
    return assemble_section(
        title=section.title,
        blocks=[
            AuthoredBlock(block.block_type, block.text)
            for block in section.blocks
            if block.block_type != "visual"
        ],
        practice=[
            DraftPractice(
                prompt=item.prompt,
                answer=item.answer,
                worked_solution=item.worked_solution,
            )
            for item in section.practice
        ],
        unit=unit,
    )
