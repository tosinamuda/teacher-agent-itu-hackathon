"""A construction lesson's worksheet has to carry its constructions.

Her note draws its figures in TikZ rather than embedding images, and the worksheet had
no branch for that: it printed the caption and stopped. On ``t3-w06`` — construct a
parallel line, a perpendicular, a bisector, a 60-degree angle — that is fourteen
drawings replaced by fourteen descriptions of drawings, on exactly the two conditions
whose treatment is that they read her note.

The drawing is compiled where TeX is installed and skipped where it is not, so these
separate what the renderer does with a drawing from whether this machine can make one.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.types.post_class_review_pack.application import manifest_adapter
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.application.worksheet_html import renderer
from app.domains.evaluation.application.worksheet_html.renderer import render_h1_worksheet_html
from app.shared.tikz_svg import tikz_available, tikz_to_svg
from experiments.h1_condition_eval.rater_packets import _manifest_steps

PICTURE = r"""\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (7,0);
  \node[below left] at (0,-0.1) {$A$};
  \node[below right] at (7,-0.1) {$B$};
\end{tikzpicture}"""
CAPTION = "The line segment $AB$, a stroke at each end."
_DRAWING_DIV = '<div class="block-figure block-figure-drawing">'


def _detail(block: dict) -> dict:
    return {
        "packet_code": "H1-TEST",
        "reference_sheet": {"subject": "Mathematics", "grade": "JSS1"},
        "objectives": [{"objective_text": "Construct a line parallel to a given line"}],
        "candidate_pack": {
            "manifest": {"steps": [{"step_id": "s1", "title": "Parallel lines", "blocks": [block]}]}
        },
        "rubric": [],
    }


def test_a_drawing_reaches_the_page(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(renderer, "tikz_to_svg", lambda _: "<svg id='drawn'></svg>")
    html = render_h1_worksheet_html(
        _detail({"type": "visual", "caption": CAPTION, "source_tikz": PICTURE})
    )
    assert _DRAWING_DIV + "<svg id='drawn'></svg>" in html
    assert "stroke at each end" in html, "the caption goes with the drawing, not instead of it"


def test_the_tikz_source_is_never_printed(monkeypatch: pytest.MonkeyPatch) -> None:
    """A learner reading ``\\draw (0,0) -- (7,0);`` has been handed the wrong thing."""
    monkeypatch.setattr(renderer, "tikz_to_svg", lambda _: "<svg id='drawn'></svg>")
    html = render_h1_worksheet_html(
        _detail({"type": "visual", "caption": CAPTION, "source_tikz": PICTURE})
    )
    assert "tikzpicture" not in html


def test_an_undrawable_figure_falls_back_to_its_caption(monkeypatch: pytest.MonkeyPatch) -> None:
    """No TeX on the machine is not a reason to render nothing where a figure was."""
    monkeypatch.setattr(renderer, "tikz_to_svg", lambda _: None)
    html = render_h1_worksheet_html(
        _detail({"type": "visual", "caption": CAPTION, "source_tikz": PICTURE})
    )
    assert "stroke at each end" in html
    # Not "no <svg>" (the caption's own $AB$ typesets to one) and not the bare class
    # name (the stylesheet is inlined into the same document).
    assert _DRAWING_DIV not in html


def test_an_image_figure_still_renders_as_an_image(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(renderer, "tikz_to_svg", lambda _: None)
    html = render_h1_worksheet_html(
        _detail({"type": "visual", "caption": CAPTION, "url": "https://example.test/fig.png"})
    )
    assert 'src="https://example.test/fig.png"' in html


def test_the_packet_builder_hands_the_drawing_on() -> None:
    """The renderer cannot draw what the packet never passed it."""
    section = {
        "section_id": "objective:lo-1",
        "title": "Parallel lines",
        "blocks": [
            {"block_type": "explanation", "text": "Slide the set square along the ruler."},
            {
                "block_type": "visual",
                "text": "",
                "caption": CAPTION,
                "figure_ref": "fig-10",
                "source_tikz": PICTURE,
            },
        ],
        "practice": [],
    }
    visual = next(b for b in _manifest_steps([section])[0]["blocks"] if b["type"] == "visual")
    assert visual["source_tikz"] == PICTURE
    assert visual["caption"] == CAPTION


def test_a_stored_pack_keeps_its_drawing_through_the_round_trip() -> None:
    """Persisting forced every figure to ``image`` and dropped the drawing with it.

    The published block shape has carried ``source_tikz`` all along; the adapter simply
    did not write it, so a pack came back from storage with a caption where a
    construction had been — and nothing downstream could ever draw it again.
    """
    section = ReviewPackSection(
        section_id="objective:lo-1",
        title="Parallel lines",
        lesson_objective_id="lo-1",
        blocks=[
            ReviewPackBlock(
                block_id="objective:lo-1:b0",
                block_type="visual",
                lesson_objective_id="lo-1",
                variant="diagram_tikz",
                caption=CAPTION,
                figure_ref="fig-10",
                source_tikz=PICTURE,
            )
        ],
    )
    manifest = manifest_adapter.sections_to_review_pack_manifest(
        sections=[section],
        artefact_id="AT-BASE",
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL,
        lesson_context=LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="Construction", lesson_objectives=[]
        ),
        created_at=datetime(2026, 8, 11, tzinfo=timezone.utc),
    )
    recovered = manifest_adapter.review_pack_manifest_to_sections(
        PostClassReviewPack.model_validate(manifest)
    )
    figure = recovered[0].blocks[0]
    assert figure.variant == "diagram_tikz"
    assert figure.figure_ref == "fig-10"
    assert figure.source_tikz == PICTURE


@pytest.mark.skipif(not tikz_available(), reason="no latex/dvisvgm on this machine")
def test_a_real_picture_compiles_to_svg() -> None:
    svg = tikz_to_svg(PICTURE)
    assert svg is not None
    assert svg.lstrip().startswith("<?xml") or svg.lstrip().startswith("<svg")
    assert "<svg" in svg


@pytest.mark.skipif(not tikz_available(), reason="no latex/dvisvgm on this machine")
def test_a_picture_that_will_not_compile_is_a_miss_not_a_crash() -> None:
    """One bad figure must cost its own drawing and nothing else in the booklet."""
    assert tikz_to_svg(r"\begin{tikzpicture} \draw (0,0) -- ; \end{tikzpicture}") is None


def test_an_empty_source_asks_tex_for_nothing() -> None:
    assert tikz_to_svg("   ") is None
