"""A stored slide deck becomes a PowerPoint file with its words, its notes and its drawing."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.presentation import Presentation as PresentationFile

from app.domains.content_engine.files.slide_deck import layout as layout_module
from app.domains.content_engine.files.slide_deck.build import build_pptx, deck_slides
from app.domains.content_engine.files.slide_deck.layout import (
    LAYOUT_FILE,
    LayoutError,
    SlideLayout,
    parse_layout,
)
from app.shared.json_types import JsonObject
from app.shared.tikz_svg import tikz_available

LAYOUT_SOURCE = json.loads((Path(layout_module.__file__).parent / LAYOUT_FILE).read_text())
LAYOUT: SlideLayout = parse_layout(LAYOUT_SOURCE)
FIGURE = r"\begin{tikzpicture}\draw (0,0) rectangle (3,1);\end{tikzpicture}"

DECK: JsonObject = {
    "content_type": "slide-deck",
    "sections": [
        {
            "label": "Recall",
            "unit_id": "intro",
            "part": {
                "slides": [
                    {
                        "title": "Learning goal",
                        "points": [{"point": "Estimate a distance from steps"}],
                        "speaker_notes": "**Ask:** why estimate?\n- Listen\n- Note answers",
                    }
                ]
            },
        },
        {
            "label": "Core",
            "unit_id": "core1",
            "part": {
                "slides": [
                    {
                        "title": "Worked example",
                        "points": [
                            {"point": r"$60\text{ cm} \times 8{,}000 = 480{,}000\text{ cm}$"},
                            {"point": r"$480{,}000 \div 100 = 4{,}800$ m"},
                        ],
                        "figure": FIGURE,
                        "speaker_notes": r"Say: $60 \times 8{,}000$.",
                    },
                    {"title": "Question", "points": [], "speaker_notes": "Ask it."},
                ]
            },
        },
    ],
}


def test_a_deck_with_a_cover_starts_with_a_title_slide_that_lists_the_objectives() -> None:
    covered: JsonObject = {
        **DECK,
        "cover": {
            "title": "Estimating distances",
            "subtitle": "Mathematics · JSS1",
            "objectives": ["Estimate a distance from steps", "Convert cm to km"],
        },
    }

    cover = deck_slides(covered)[0]
    slide = list(_opened(covered).slides)[0]
    shown = [shape.text_frame.text for shape in slide.shapes if shape.has_text_frame]

    assert (cover.title, cover.points) == ("Estimating distances", ["Mathematics · JSS1"])
    assert slide.slide_layout.name == "Title Slide"
    assert shown == [
        "Estimating distances",
        "Mathematics · JSS1",
        "Estimate a distance from steps\nConvert cm to km",
    ]
    assert len(deck_slides(covered)) == len(deck_slides(DECK)) + 1


def test_the_slides_of_a_deck_are_read_step_after_step() -> None:
    slides = deck_slides(DECK)

    assert [slide.title for slide in slides] == ["Learning goal", "Worked example", "Question"]
    assert slides[1].figure == FIGURE and slides[0].figure is None
    assert slides[2].points == []


def _opened(deck: JsonObject, layout: SlideLayout = LAYOUT) -> PresentationFile:
    return Presentation(io.BytesIO(build_pptx(deck_slides(deck), layout)))


def test_each_slide_has_its_title_its_points_and_its_notes_as_text() -> None:
    deck = _opened(DECK)

    slides = list(deck.slides)
    assert len(slides) == 3
    assert slides[0].shapes.title.text == "Learning goal"
    assert slides[1].placeholders[1].text_frame.text.splitlines() == [
        "60 cm × 8,000 = 480,000 cm",
        "480,000 ÷ 100 = 4,800 m",
    ]
    assert (
        slides[0].notes_slide.notes_text_frame.text
        == "Ask: why estimate?\n• Listen\n• Note answers"
    )
    assert slides[1].notes_slide.notes_text_frame.text.startswith("Say: 60 × 8,000")


def test_a_slide_without_points_has_no_empty_body_box() -> None:
    slide = list(_opened(DECK).slides)[2]

    assert [shape.name for shape in slide.placeholders] == [slide.shapes.title.name]


def _with_figure(figure: str) -> JsonObject:
    slide: JsonObject = {
        "title": "Picture",
        "points": [{"point": "Look"}],
        "figure": figure,
        "speaker_notes": "Point at the picture and say what it shows.",
    }
    return {"sections": [{"unit_id": "s", "part": {"slides": [slide]}}]}


@pytest.mark.skipif(not tikz_available(), reason="TeX and dvisvgm are not installed")
def test_a_drawing_that_is_not_wide_is_placed_beside_the_points() -> None:
    square = r"\begin{tikzpicture}\draw (0,0) rectangle (2,2);\end{tikzpicture}"
    slide = list(_opened(_with_figure(square)).slides)[0]

    pictures = [shape for shape in slide.shapes if shape.shape_type == 13]
    assert len(pictures) == 1
    assert pictures[0].left > slide.placeholders[1].left + slide.placeholders[1].width


@pytest.mark.skipif(not tikz_available(), reason="TeX and dvisvgm are not installed")
def test_a_wide_drawing_such_as_a_number_line_takes_the_width_below_the_points() -> None:
    line = r"\begin{tikzpicture}\draw (0,0) -- (10,0);\node at (10,-0.3) {10};\end{tikzpicture}"
    deck = _opened(_with_figure(line))
    slide = list(deck.slides)[0]
    points = slide.placeholders[1]

    picture = next(shape for shape in slide.shapes if shape.shape_type == 13)
    assert picture.top >= points.top + points.height
    assert picture.width > 0.8 * deck.slide_width


def test_a_drawing_that_cannot_be_placed_leaves_a_line_in_the_notes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.domains.content_engine.files.slide_deck.build.tikz_to_svg", lambda _: None
    )

    slide = list(_opened(DECK).slides)[1]

    assert "could not be placed" in slide.notes_slide.notes_text_frame.text
    assert not [s for s in slide.shapes if s.shape_type == 13]


@pytest.mark.skipif(not tikz_available(), reason="TeX and dvisvgm are not installed")
def test_a_wide_drawing_leaves_the_points_the_room_that_a_long_example_needs() -> None:
    line = r"\begin{tikzpicture}\draw (0,0) -- (10,0);\node at (10,-0.3) {10};\end{tikzpicture}"
    problem = " ".join(["A student takes steps to the market and then home."] * 3)
    slide: JsonObject = {
        "title": "Worked example",
        "points": [{"point": point} for point in (problem, "a", "b", "c", "d")],
        "figure": line,
        "speaker_notes": "Walk through each line of the working.",
    }
    deck = _opened({"sections": [{"unit_id": "s", "part": {"slides": [slide]}}]})
    shown = list(deck.slides)[0]
    points = shown.placeholders[1]
    picture = next(shape for shape in shown.shapes if shape.shape_type == 13)

    sparse = _opened(_with_figure(line)).slides[0]

    assert picture.top >= points.top + points.height
    assert picture.top + picture.height <= points.top + 5.7 * 914400 + 1
    assert points.height > sparse.placeholders[1].height


def _body_sizes(points: list[str]) -> set[float]:
    slide_json: JsonObject = {
        "title": "A worked example",
        "points": [{"point": point} for point in points],
        "speaker_notes": "Work it with the class, line by line.",
    }
    content: JsonObject = {"sections": [{"unit_id": "s", "part": {"slides": [slide_json]}}]}
    body = list(_opened(content).slides)[0].placeholders[1]
    assert body.text_frame.auto_size == MSO_AUTO_SIZE.NONE
    return {run.font.size.pt for paragraph in body.text_frame.paragraphs for run in paragraph.runs}


def test_a_rule_of_five_lines_and_a_worked_example_are_set_at_a_size_the_back_can_read() -> None:
    rule = [
        "Convert the step length from cm to m by dividing by 100.",
        "Multiply the step length in metres by the total number of steps.",
        "That gives the distance in metres.",
        "Convert the distance from m to km by dividing by 1,000.",
        "Round the final kilometre value to a convenient whole number.",
    ]
    example = [
        "A student's steps are 75 cm long. He takes 9,200 steps to the park. "
        "Estimate the distance to the park (nearest kilometre).",
        r"$0.75\text{ m}=\frac{75\text{ cm}}{100}$",
        r"$0.75\text{ m}\times 9{,}200 = 6{,}900\text{ m}$",
        r"$6{,}900\text{ m}=6.9\text{ km}$",
        r"$6.9\text{ km}\approx 7\text{ km}$",
    ]

    assert _body_sizes(rule) == {32.0}
    assert _body_sizes(example) == {36.0}


def _title_pt(title: str) -> float:
    slide_json: JsonObject = {
        "title": title,
        "points": [{"point": "Look"}],
        "speaker_notes": "Say what the slide shows.",
    }
    content: JsonObject = {"sections": [{"unit_id": "s", "part": {"slides": [slide_json]}}]}
    run = list(_opened(content).slides)[0].shapes.title.text_frame.paragraphs[0].runs[0]
    return float(run.font.size.pt)


def test_a_long_title_is_set_smaller_so_it_stays_on_one_line() -> None:
    assert _title_pt("Worked example 1") == 40.0
    assert _title_pt("Rounding the Stadium Distance on a Number Line") == 32.0


def test_a_long_cover_title_is_set_smaller_so_it_stays_above_the_subtitle() -> None:
    def cover_pt(title: str) -> float:
        content: JsonObject = {"cover": {"title": title, "subtitle": "Mathematics"}, "sections": []}
        run = list(_opened(content).slides)[0].shapes.title.text_frame.paragraphs[0].runs[0]
        return float(run.font.size.pt)

    assert cover_pt("Estimation") == 60.0
    assert cover_pt("Multiplications and Divisions of Fractions") == 44.0


def test_a_layout_that_sets_other_sizes_and_colours_changes_the_file() -> None:
    other = {
        **LAYOUT_SOURCE,
        "title": {**LAYOUT_SOURCE["title"], "sizes_pt": [24]},
        "colours": {**LAYOUT_SOURCE["colours"], "ink": "112233"},
    }
    slide = list(_opened(DECK, parse_layout(other)).slides)[1]

    title_run = slide.shapes.title.text_frame.paragraphs[0].runs[0]
    body_run = slide.placeholders[1].text_frame.paragraphs[0].runs[0]
    assert title_run.font.size.pt == 24.0
    assert str(body_run.font.color.rgb) == "112233"


@pytest.mark.parametrize(
    ("change", "told"),
    [
        ({"title": None}, "no 'title'"),
        ({"body": {"top_in": 1.5}}, "'height_in'"),
        ({"title": {"top_in": 0.3, "height_in": 1, "sizes_pt": [28, 40]}}, "largest first"),
        ({"title": {"top_in": 0.3, "height_in": 1, "sizes_pt": []}}, "text sizes"),
        ({"colours": {"ink": "red", "accent": "A8481A", "on_accent": "FFFFFF"}}, "'ink'"),
        ({"fit": {**LAYOUT_SOURCE["fit"], "fill_share": 0}}, "above zero"),
    ],
)
def test_a_layout_that_leaves_out_or_misstates_a_value_is_refused(
    change: dict[str, object], told: str
) -> None:
    source = {k: v for k, v in {**LAYOUT_SOURCE, **change}.items() if v is not None}

    with pytest.raises(LayoutError, match=told):
        parse_layout(source)
