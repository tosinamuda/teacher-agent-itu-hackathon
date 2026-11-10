"""Render generated sections as a PostClassReviewPack manifest.

The rater UI loads a packet's pack from ``artefacts.manifest`` (a
``PostClassReviewPack``) via the condition run's ``artefact_id``. Materialising
generated output into that shape lets the existing evaluation flow display packs
unchanged.
"""

from __future__ import annotations

import re
from datetime import datetime

from pydantic import TypeAdapter

from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    ContentBlock,
    ExplanationBlock,
    PracticeBlock,
    VisualBlock,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    MISCONCEPTION_LABEL,
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import (
    PostClassReviewPack,
    ReviewPackStep,
)
from app.shared.json_types import JsonObject


def review_pack_manifest_to_sections(pack: PostClassReviewPack) -> list[ReviewPackSection]:
    """Recover spec sections from a stored PostClassReviewPack manifest.

    Inverse of ``sections_to_review_pack_manifest`` — for example, to reuse a
    cached base during personalisation. Takes a typed ``PostClassReviewPack`` so the caller owns
    validation at the boundary (one ``model_validate`` per read, not per
    consumer); the body just walks the typed models — no per-field
    ``dict.get()``/cast guessing.
    """
    return [_section_from_step(step) for step in pack.steps]


def _section_from_step(step: ReviewPackStep) -> ReviewPackSection:
    """One stored step back into the section it was rendered from."""
    objective_id = step.lesson_objective_id or step.step_id or ""
    blocks: list[ReviewPackBlock] = []
    practice: list[ReviewPackPracticeItem] = []
    for index, block in enumerate(step.blocks):
        block_id = block.id or f"{step.step_id}:b{index}"
        # Practice is a first-class item on the section, not a block: read back
        # as an explanation it would come home empty, and the revision turn
        # writes the recovered pack back in place — so every question and answer
        # in the stored pack would be gone after one turn.
        if isinstance(block, PracticeBlock):
            practice.append(_recover_practice(block, block_id))
        else:
            blocks.append(_recover_block(block, block_id, objective_id))
    return ReviewPackSection(
        section_id=step.step_id or objective_id,
        title=step.title or "",
        lesson_objective_id=objective_id,
        blocks=blocks,
        practice=practice,
        source_refs=list(dict.fromkeys(ref for item in blocks for ref in item.source_refs)),
    )


def _recover_practice(block: PracticeBlock, block_id: str) -> ReviewPackPracticeItem:
    return ReviewPackPracticeItem(item_id=block_id, prompt=block.question, answer=block.answer)


def _recover_block(block: ContentBlock, block_id: str, objective_id: str) -> ReviewPackBlock:
    if isinstance(block, VisualBlock):
        return ReviewPackBlock(
            block_id=block_id,
            block_type="visual",
            lesson_objective_id=objective_id,
            # Her note's figures are drawings, not images, and the round trip forced
            # every one of them to "image" and dropped the drawing with it — so a
            # stored pack came back with a caption where a construction had been.
            variant=block.variant if block.variant in ("image", "diagram_tikz") else "image",
            url=((block.url or "").strip() or None),
            caption=((block.caption or "").strip() or None),
            figure_ref=((block.figure_ref or "").strip() or None),
            source_tikz=((block.source_tikz or "").strip() or None),
            source_record_id=((block.source_record_id or "").strip() or None),
        )
    explanation = block if isinstance(block, ExplanationBlock) else None
    # The field is authoritative; the trailer is how packs stored before it
    # carried their refs, so it is still read back.
    text, trailing = _split_source_trailer(explanation.content if explanation else "")
    return ReviewPackBlock(
        block_id=block_id,
        block_type="misconception_repair"
        if text.startswith(MISCONCEPTION_LABEL)
        else "explanation",
        text=text,
        lesson_objective_id=objective_id,
        source_refs=(list(explanation.source_refs) if explanation else []) or trailing,
    )


_BLOCK_LABELS = {
    "misconception_repair": MISCONCEPTION_LABEL,
    "worked_example": "**Worked example**\n\n",
    "practice": "**Practice**\n\n",
    "reflection": "**Reflection**\n\n",
}


# The trailer ``_block_markdown`` appends. Recovering it on the way back keeps
# the round trip lossless: without this a recovered pack carries its refs only
# as prose, and re-rendering appends a second trailer.
_SOURCES_TRAILER = re.compile(r"\n\n_Sources: ([^_\n]+)_[ \t]*$")


def _split_source_trailer(content: str) -> tuple[str, list[str]]:
    """The block's text without the appended sources line, and the refs it named."""
    match = _SOURCES_TRAILER.search(content)
    if not match:
        return content, []
    refs = [ref.strip() for ref in match.group(1).split(",") if ref.strip()]
    return content[: match.start()], refs


def _block_markdown(block: ReviewPackBlock) -> str:
    # The generated text often already opens with its own heading
    # (``**Worked Example**`` / ``### …``). Only prepend the generic kind label
    # when it doesn't, so the two don't stack into a duplicate header.
    if block.block_type == "misconception_repair":
        return (
            block.text
            if block.text.startswith(MISCONCEPTION_LABEL)
            else (f"{MISCONCEPTION_LABEL}{block.text}")
        )
    stripped = block.text.lstrip()
    has_own_heading = stripped.startswith(("#", "**"))
    label = "" if has_own_heading else _BLOCK_LABELS.get(block.block_type, "")
    return f"{label}{block.text}"


def _explanation_block(block: ReviewPackBlock, section_id: str, index: int) -> JsonObject:
    # Map every text spec block to an ExplanationBlock (always valid + renderable);
    # the original block_type is preserved as a markdown label and in the raw
    # generated_pack for research.
    return {
        "id": block.block_id or f"{section_id}:b{index}",
        "type": "explanation",
        "content": _block_markdown(block),
        "source_refs": list(block.source_refs),
    }


def _visual_block(block: ReviewPackBlock, section_id: str, index: int) -> JsonObject:
    # Grounded figure carried from the lesson plan — emit the published VisualBlock shape
    # the shared frontend renderer dispatches on (type="visual", variant="image"), which
    # ReviewPackStep validates via the ContentBlock union.
    return {
        "id": block.block_id or f"{section_id}:b{index}",
        "type": "visual",
        "variant": block.variant or "image",
        "url": block.url,
        "caption": block.caption,
        # The label the prose points at, and the drawing itself. Without them a
        # diagram_tikz figure stores as a caption and can never be drawn again.
        "figure_ref": block.figure_ref,
        "source_tikz": block.source_tikz,
        "source_record_id": block.source_record_id,
    }


_CONTENT_BLOCK: TypeAdapter[ContentBlock] = TypeAdapter(ContentBlock)


def _manifest_block(block: ReviewPackBlock, section_id: str, index: int) -> ContentBlock:
    raw = (
        _visual_block(block, section_id, index)
        if block.block_type == "visual"
        else _explanation_block(block, section_id, index)
    )
    return _CONTENT_BLOCK.validate_python(raw)


def _practice_block(
    item: ReviewPackPracticeItem, section: ReviewPackSection, index: int
) -> ContentBlock:
    """One practice item as a manifest block, question and answer still apart.

    The answer travels with its question so nothing can lose the pairing; WHERE it is
    shown is the renderer's decision, and the renderer puts it after the activities.
    """
    # The working goes with the ANSWER, not into ``hints``. A hint scaffolds an attempt
    # and is shown beside the question; a worked solution shows the method and would give
    # it away before the learner has tried. Both are checking support, so both wait.
    answer = item.answer
    if item.worked_solution:
        answer = f"{answer}\n\n{item.worked_solution}"
    return _CONTENT_BLOCK.validate_python(
        {
            # Indexed like its siblings: without it every unstamped item in a
            # section shares one id, and anything addressing a block by id —
            # a revision highlight, the editing reviser's unique match, the
            # rater UI's keys — cannot tell three questions apart.
            "id": item.item_id or f"{section.section_id}:p{index}",
            "type": "practice",
            "question": item.prompt,
            "answer": answer,
            "lesson_objective_id": section.lesson_objective_id or None,
        }
    )


def sections_to_review_pack_manifest(
    *,
    sections: list[ReviewPackSection],
    artefact_id: str,
    plan_version_id: str,
    scope: ArtefactScope,
    lesson_context: LessonContextForGeneration,
    created_at: datetime,
    lesson_plan_objectives: list[JsonObject] | None = None,
    student_id: str | None = None,
    personalisation_bands: dict[str, str] | None = None,
) -> JsonObject:
    """Build a validated PostClassReviewPack manifest dict from spec sections."""
    bands = personalisation_bands or {}
    steps = [
        ReviewPackStep(
            step_id=section.section_id,
            step_kind="core",
            type="review",
            title=section.title,
            blocks=[
                *(
                    _manifest_block(block, section.section_id, index)
                    for index, block in enumerate(section.blocks)
                ),
                *(
                    _practice_block(item, section, index)
                    for index, item in enumerate(section.practice)
                ),
            ],
            status="generated",
            lesson_objective_id=section.lesson_objective_id,
            personalisation_band=bands.get(section.lesson_objective_id),
        )
        for section in sections
    ]
    pack = PostClassReviewPack(
        artefact_id=artefact_id,
        artefact_type=ArtefactType.POST_CLASS_REVIEW_PACK,
        scope=scope,
        plan_version_id=plan_version_id,
        created_at=created_at,
        subject=lesson_context.subject or None,
        grade=lesson_context.grade_level or None,
        topic=lesson_context.topic or None,
        subtopic=lesson_context.subtopic,
        term=lesson_context.term,
        week=lesson_context.week,
        theme=lesson_context.curriculum_scope,
        lesson_plan_objectives=lesson_plan_objectives or [],
        steps=steps,
        student_id=student_id,
    )
    return pack.to_json_object()
