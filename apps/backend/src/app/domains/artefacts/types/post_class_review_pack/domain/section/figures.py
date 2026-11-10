"""Deterministic placement of source-grounded figures in generated sections."""

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)

from .schemas import ReviewPackBlock, ReviewPackSection


def append_grounded_figures(section: ReviewPackSection, unit: SectionGenerationUnit) -> None:
    """Replace model-authored visuals with canonical figures placed at first citation."""
    section.blocks = authored_blocks(section.blocks)
    seen: set[str] = set()
    for figure in unit.source_figures:
        identity = figure.url or figure.figure_ref or figure.source_tikz
        if not identity or identity in seen:
            continue
        seen.add(identity)
        placed = ReviewPackBlock(
            block_id=figure.figure_id,
            block_type="visual",
            lesson_objective_id=unit.lesson_objective_id,
            variant=figure.variant,
            url=figure.url,
            caption=figure.caption,
            figure_ref=figure.figure_ref,
            source_tikz=figure.source_tikz,
            source_record_id=figure.source_record_id,
        )
        position = len(section.blocks)
        if placed.figure_ref:
            for index, block in enumerate(section.blocks):
                if block.text and placed.figure_ref in block.text:
                    position = index + 1
                    break
        # Figures citing the same block share an anchor, so step past the ones already
        # placed there. Inserting each at the anchor put every new figure in front of
        # the last, and a passage citing fig-05, fig-06 and fig-07 was answered by
        # fig-07, fig-06, fig-05.
        while position < len(section.blocks) and section.blocks[position].block_type == "visual":
            position += 1
        section.blocks.insert(position, placed)


def authored_blocks(blocks: list[ReviewPackBlock]) -> list[ReviewPackBlock]:
    """Return model-authored prose blocks; figures never originate from the model."""
    return [block for block in blocks if block.block_type != "visual"]
