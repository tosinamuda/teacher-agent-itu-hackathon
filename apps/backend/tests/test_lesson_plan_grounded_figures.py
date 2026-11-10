"""Deterministic embedding of grounded source figures as image VisualBlocks.

The drafter reproduces source *tables* as LaTeX explanation blocks but rarely emits the
source's image figures (counting charts, diagrams), so a step ends up telling the teacher
to "project the counting chart" while no chart renders. ``normalize_step_content`` now
attaches those grounded figures deterministically. These tests pin: the blocks are built,
deduped, skip incomplete assets, only attach when grounding is present, and validate
against the strict published ``VisualBlock`` schema.
"""

from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    build_grounded_figure_blocks,
    normalize_step_content,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import VisualBlock


def _grounded(url: str, record_id: str = "ch01-b035", caption: str = "") -> dict[str, str]:
    return {
        "url": url,
        "caption": caption,
        "source_record_id": record_id,
        "source_html_path": "dataset/textbook/html/Chapter 01.html",
        "source_anchor_id": "counting-up-to-one-billion",
    }


def test_grounded_figure_block_numbers_and_prefixes_caption() -> None:
    cap1 = "A counting chart from 10,000,000 to 1,000,000,000 in ten-millions."
    cap2 = "The final stretch from 999,990,100 to 1,000,000,000."
    figures = build_grounded_figure_blocks(
        [],
        grounded_images=[
            _grounded("https://x/007.png", caption=cap1),
            _grounded("https://x/008.png", caption=cap2),
        ],
        step_id="step01",
    )
    # captions are numbered (Figure 1/2) in placement order and prefixed with the source caption
    assert figures[0]["caption"] == f"Figure 1: {cap1}"
    assert figures[1]["caption"] == f"Figure 2: {cap2}"
    # an empty source caption still gets a stable figure number (no dangling reference)
    plain = build_grounded_figure_blocks(
        [], grounded_images=[_grounded("https://x/009.png")], step_id="step01"
    )
    assert plain[0]["caption"] == "Figure 1"


def test_build_grounded_figure_blocks_emits_valid_image_blocks() -> None:
    figures = build_grounded_figure_blocks(
        [],
        grounded_images=[_grounded("https://x/007.png"), _grounded("https://x/008.png")],
        step_id="step01",
    )

    assert [f["url"] for f in figures] == ["https://x/007.png", "https://x/008.png"]
    assert [f["id"] for f in figures] == ["step01-figure-1", "step01-figure-2"]
    # Every emitted block satisfies the strict published schema (image validator included).
    for figure in figures:
        block = VisualBlock.model_validate(figure)
        assert block.variant == "image"
        assert block.source_record_id == "ch01-b035"


def test_build_grounded_figure_blocks_dedupes_against_existing_and_skips_incomplete() -> None:
    existing = [
        {"id": "b1", "type": "explanation", "content": "..."},
        {"id": "b2", "type": "visual", "variant": "image", "url": "https://x/007.png"},
    ]
    figures = build_grounded_figure_blocks(
        existing,
        grounded_images=[
            _grounded("https://x/007.png"),  # already present -> skipped
            _grounded("https://x/008.png"),  # new -> kept
            {"url": "", "source_record_id": "ch01-b035"},  # no url -> skipped
            {"url": "https://x/009.png", "source_record_id": ""},  # no record -> skipped
        ],
        step_id="step01",
    )
    assert [f["url"] for f in figures] == ["https://x/008.png"]


def test_normalize_step_content_appends_figures_only_when_grounded() -> None:
    def _step() -> dict:
        return {
            "step_id": "step01",
            "step_kind": "core",
            "content": "Explain the concept of a million.",
            "blocks": [{"id": "b1", "type": "explanation", "content": "table + counting list"}],
        }

    grounded = [_grounded("https://x/007.png")]
    appended = normalize_step_content(_step(), grounded_images=grounded)
    types = [b["type"] for b in appended["blocks"]]
    assert types == ["explanation", "visual"]
    assert appended["blocks"][1]["url"] == "https://x/007.png"
    # adding a visual doesn't change a core step's instructional type
    assert appended["instructional_type"] == "explain_only"

    # No grounding (global steps pass [], re-normalization passes None) -> no figures added.
    assert [b["type"] for b in normalize_step_content(_step(), grounded_images=[])["blocks"]] == [
        "explanation"
    ]
    assert [b["type"] for b in normalize_step_content(_step(), grounded_images=None)["blocks"]] == [
        "explanation"
    ]
