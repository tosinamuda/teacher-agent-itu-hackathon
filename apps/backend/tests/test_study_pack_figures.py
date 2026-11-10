"""Grounded-figure cascade into the study pack (§1).

The lesson plan already embeds captioned, grounded figures as ``visual`` blocks. The
study pack carries those into textbook-grounded conditions only (C2/C3/P1) — never the
C0/C1 ablation baseline — and renders them via the published VisualBlock shape. These
tests pin: the retrieval gate on carry-over, the deterministic post-pass (strip stray
LLM visuals, splice the canonical figures, dedup), and the manifest serialization.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    sections_to_review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
    SectionGenerationUnit,
    SourceFigure,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    normalise_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.session_plan_view import SessionPlanView

FIGURE_URL = "https://example.org/figures/004.png"


def _session_plan_with_figure() -> dict:
    return {
        "subject": "Mathematics",
        "grade": "JSS1",
        "topic": "Whole Numbers",
        "subtopic": "Millions and billions",
        "lesson_plan_objectives": [
            {"lesson_objective_id": "lop01", "objective_text": "Count in millions"}
        ],
        "steps": [
            {
                "step_id": "step01",
                "step_kind": "core",
                "lesson_objective_id": "lop01",
                "title": "Counting in millions",
                "content": "Project the chart and count along.",
                "blocks": [
                    {"id": "b1", "type": "explanation", "content": "Count in ten-thousands."},
                    {
                        "id": "b2",
                        "type": "visual",
                        "variant": "image",
                        "url": FIGURE_URL,
                        "caption": "Counting chart from 99,990 to 1,000,000.",
                        "source_record_id": "ch01-b029",
                    },
                ],
            }
        ],
        "references": ["Siyavula Gr7 ch1", "NERDC JSS1 maths"],
    }


def _figures_for(code: ConditionCode) -> list[ReviewPackBlock]:
    builder = BaseReviewPackRequestBuilder()
    plan = SessionPlanView.model_validate(_session_plan_with_figure())
    request = builder.build(
        session_plan=plan,
        policy=profile_for(Hypothesis.H1, code),
        sources=LessonSources.unresolved(plan.references),
    )
    return [figure for unit in request.units for figure in unit.source_figures]


def test_figures_carried_only_for_grounded_conditions() -> None:
    # C0 (objectives only) and C1 (lesson plan, no retrieval) must stay figure-free —
    # a figure here would silently turn the ablation baseline into a partial-C2.
    assert _figures_for(ConditionCode.C0) == []
    assert _figures_for(ConditionCode.C1) == []

    # C2 (retrieval enabled) carries the lesson plan's grounded figure.
    c2_figures = _figures_for(ConditionCode.C2)
    assert len(c2_figures) == 1
    figure = c2_figures[0]
    assert figure.figure_id == "b2"
    assert figure.variant == "image"
    assert figure.url == FIGURE_URL
    assert figure.source_record_id == "ch01-b029"
    assert figure.caption and "Counting chart" in figure.caption


def test_only_grounded_visual_blocks_become_figures() -> None:
    """A figure must be a visual block with both a url and a source record.

    The step's block list is mixed lesson-plan content. Admitting anything else
    would put ungrounded material into C2/C3 under a textbook-figure label, and
    a repeated url would show the learner the same figure twice.
    """
    plan = _session_plan_with_figure()
    plan["steps"][0]["blocks"].extend(
        [
            # Carries url + record id, but is not a visual block.
            {
                "id": "b3",
                "type": "explanation",
                "content": "Read the chart.",
                "url": "https://cdn.example/not-a-figure.png",
                "source_record_id": "ch01-b030",
            },
            # Visual, but ungrounded: no source record to attribute it to.
            {
                "id": "b4",
                "type": "visual",
                "variant": "image",
                "url": "https://cdn.example/unsourced.png",
                "caption": "Unsourced sketch",
            },
            # The canonical figure again, under a different block id.
            {
                "id": "b5",
                "type": "visual",
                "variant": "image",
                "url": FIGURE_URL,
                "caption": "Duplicate of the counting chart.",
                "source_record_id": "ch01-b029",
            },
        ]
    )
    session_plan = SessionPlanView.model_validate(plan)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=session_plan,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=LessonSources.unresolved(session_plan.references),
    )
    figures = [figure for unit in request.units for figure in unit.source_figures]
    assert [figure.url for figure in figures] == [FIGURE_URL]


def testnormalise_section_strips_stray_visuals_and_splices_canonical_figures() -> None:
    unit = SectionGenerationUnit(
        unit_id="step:step01",
        lesson_objective_id="lop01",
        objective_text="Count in millions",
        source_figures=[
            SourceFigure(
                figure_id="fig1",
                variant="image",
                url=FIGURE_URL,
                caption="Counting chart",
                source_record_id="ch01-b029",
            )
        ],
    )
    section = ReviewPackSection(
        section_id="raw",
        title="Counting",
        lesson_objective_id="lop01",
        blocks=[
            ReviewPackBlock(
                block_id="t1", block_type="explanation", text="Count.", lesson_objective_id="lop01"
            ),
            # a hallucinated visual block the model should never author
            ReviewPackBlock(
                block_id="stray",
                block_type="visual",
                lesson_objective_id="lop01",
                variant="image",
                url="https://hallucinated.example/x.png",
                source_record_id="fake",
            ),
        ],
    )

    result = normalise_section(section, unit)

    visuals = [block for block in result.blocks if block.block_type == "visual"]
    assert len(visuals) == 1
    assert visuals[0].url == FIGURE_URL  # canonical figure, not the hallucinated one
    assert [b.block_type for b in result.blocks] == ["explanation", "visual"]


def test_manifest_emits_renderable_visual_block() -> None:
    section = ReviewPackSection(
        section_id="step01",
        title="Counting in millions",
        lesson_objective_id="lop01",
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="Count in ten-thousands.",
                lesson_objective_id="lop01",
            ),
            ReviewPackBlock(
                block_id="b2",
                block_type="visual",
                lesson_objective_id="lop01",
                variant="image",
                url=FIGURE_URL,
                caption="Counting chart.",
                source_record_id="ch01-b029",
            ),
        ],
    )

    # sections_to_review_pack_manifest validates a PostClassReviewPack internally — a
    # malformed visual block would raise here (the ContentBlock union requires url +
    # source_record_id for image visuals).
    manifest = sections_to_review_pack_manifest(
        sections=[section],
        artefact_id="ART-1",
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL,
        lesson_context=LessonContextForGeneration(
            subject="Mathematics",
            grade_level="JSS1",
            topic="Whole Numbers",
            lesson_objectives=["Count in millions"],
        ),
        created_at=datetime(2026, 6, 3, tzinfo=timezone.utc),
    )

    blocks = manifest["steps"][0]["blocks"]
    visuals = [block for block in blocks if block.get("type") == "visual"]
    assert len(visuals) == 1
    assert visuals[0]["variant"] == "image"
    assert visuals[0]["url"] == FIGURE_URL
    assert visuals[0]["source_record_id"] == "ch01-b029"


def test_manifest_round_trip_carries_source_refs_beside_the_prose() -> None:
    """Refs survive the round trip in a field, and never enter the text.

    They used to be appended as a "_Sources:" footer and parsed back out — the
    only channel the pack schema offered. Dropping them on the way back left a
    recovered pack citing only in prose, so re-rendering appended a SECOND
    footer, visible to raters on any pack built from an approved base. A field
    makes both the round trip and the blinding structural.
    """
    from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
        review_pack_manifest_to_sections,
    )
    from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack

    section = ReviewPackSection(
        section_id="step:s1",
        title="Rectangle area",
        lesson_objective_id="lop01",
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="Multiply the two side lengths.",
                lesson_objective_id="lop01",
                source_refs=["REF-1", "REF-2"],
            )
        ],
        source_refs=["REF-1", "REF-2"],
    )
    context = LessonContextForGeneration(
        subject="Mathematics", grade_level="JSS1", topic="Area", lesson_objectives=["lop01"]
    )
    kwargs = {
        "artefact_id": "AT-1",
        "plan_version_id": "LPV-1",
        "scope": ArtefactScope.CLASS_LEVEL,
        "lesson_context": context,
        "created_at": datetime(2026, 8, 11, tzinfo=timezone.utc),
    }
    first = sections_to_review_pack_manifest(sections=[section], **kwargs)
    recovered = review_pack_manifest_to_sections(PostClassReviewPack.model_validate(first))

    assert recovered[0].blocks[0].source_refs == ["REF-1", "REF-2"]
    assert "_Sources:" not in recovered[0].blocks[0].text
    assert recovered[0].blocks[0].text == "Multiply the two side lengths."
    # The forward direction keeps the refs out of the prose to begin with.
    assert first["steps"][0]["blocks"][0]["source_refs"] == ["REF-1", "REF-2"]
    assert "REF-" not in first["steps"][0]["blocks"][0]["content"]

    # Re-rendering the recovered pack reproduces it exactly — the property the
    # doubled footer used to break.
    second = sections_to_review_pack_manifest(sections=recovered, **kwargs)
    assert second["steps"][0]["blocks"][0] == first["steps"][0]["blocks"][0]


def test_normalise_section_stamps_identity_and_cleans_every_text_it_carries() -> None:
    r"""What an assembled section must have done to it before it is a pack section.

    Composition and repair build the section themselves, so nothing upstream has
    stamped ids or decoded the model's escapes. Blank ids collide — three
    unstamped practice items would answer to one id and no highlight could
    address them — and a literal ``\n`` pair is a paragraph break the reader
    never gets.
    """
    unit = SectionGenerationUnit(
        unit_id="step:s1", lesson_objective_id="lop01", objective_text="Find the area"
    )
    section = ReviewPackSection(
        section_id="model-authored",
        title="Area",
        lesson_objective_id="model-authored-objective",
        blocks=[
            ReviewPackBlock(
                block_id="",
                block_type="explanation",
                text=r"Area is length \n\n times width.",
                lesson_objective_id="wrong",
            ),
            ReviewPackBlock(
                block_id="",
                block_type="explanation",
                text="Second block.",
                lesson_objective_id="wrong",
            ),
        ],
        practice=[
            ReviewPackPracticeItem(prompt=r"Find \n\n the area.", answer=r"30 \n\n square cm"),
            ReviewPackPracticeItem(prompt="And this one.", answer="12"),
        ],
    )

    result = normalise_section(section, unit)

    assert result.section_id == "step:s1"
    assert result.lesson_objective_id == "lop01"
    assert all(block.lesson_objective_id == "lop01" for block in result.blocks)
    # Ids are stamped AND distinct — a shared id is what a blank one collapses to.
    block_ids = [block.block_id for block in result.blocks]
    item_ids = [item.item_id for item in result.practice]
    assert len(set(block_ids)) == len(block_ids) and all(block_ids)
    assert len(set(item_ids)) == len(item_ids) and all(item_ids)
    # Escapes are decoded in every text the section carries, practice included.
    assert r"\n\n" not in result.blocks[0].text
    assert r"\n\n" not in result.practice[0].prompt
    assert r"\n\n" not in result.practice[0].answer
