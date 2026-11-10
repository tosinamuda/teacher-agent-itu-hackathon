"""A slide deck as a PowerPoint file: one slide for each slide of the deck, notes included.

Points and notes keep their words as editable text, with the maths written in symbols
(``60 cm × 8,315 steps``). A drawing is compiled from its TikZ and placed as a picture.
"""

from __future__ import annotations

import io
import logging
import math
import re
from dataclasses import dataclass

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.presentation import Presentation as PresentationFile
from pptx.slide import Slide as PptxSlide
from pptx.text.text import _Paragraph
from pptx.util import Emu, Length, Pt

from app.domains.content_engine.files.slide_deck.layout import EMU_PER_POINT, SlideLayout
from app.shared.json_types import JsonObject, JsonValue
from app.shared.latex_plain import plain_maths
from app.shared.native_libs import ensure_native_lib_path
from app.shared.tikz_svg import tikz_to_svg

logger = logging.getLogger(__name__)

_MARKDOWN_MARKS = re.compile(r"\*\*|__|`|^#{1,6}\s*", re.MULTILINE)
_LIST_MARK = re.compile(r"^\s*[-*]\s+", re.MULTILINE)
_DRAWING_MISSING = (
    "(A drawing belongs on this slide but could not be placed here: see it in the app.)"
)


@dataclass(frozen=True)
class DeckSlide:
    title: str
    points: list[str]
    figure: str | None
    notes: str
    #: A cover slide shows the lesson's objectives under its title and subtitle.
    objectives: tuple[str, ...] = ()
    cover: bool = False


def _rows(value: JsonValue | None) -> list[JsonObject]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _text(value: JsonValue | None) -> str:
    return value.strip() if isinstance(value, str) else ""


def _cover(content: JsonObject) -> DeckSlide | None:
    """The deck's cover slide, which the app set when it saved the deck; older decks have none."""
    cover = content.get("cover")
    if not isinstance(cover, dict) or not (title := _text(cover.get("title"))):
        return None
    subtitle = _text(cover.get("subtitle"))
    listed = cover.get("objectives")
    objectives = (
        tuple(o for item in listed or [] if (o := _text(item))) if isinstance(listed, list) else ()
    )
    return DeckSlide(title, [subtitle] if subtitle else [], None, "", objectives, cover=True)


def deck_slides(content: JsonObject) -> list[DeckSlide]:
    """The cover, then every slide of a stored deck in the order shown, step after step."""
    cover = _cover(content)
    return [
        *([cover] if cover else []),
        *(
            DeckSlide(
                title=_text(slide.get("title")),
                points=[
                    p for entry in _rows(slide.get("points")) if (p := _text(entry.get("point")))
                ],
                figure=_text(slide.get("figure")) or None,
                notes=_text(slide.get("speaker_notes")),
            )
            for section in _rows(content.get("sections"))
            for slide in _rows(_part(section).get("slides"))
        ),
    ]


def _part(section: JsonObject) -> JsonObject:
    part = section.get("part")
    return part if isinstance(part, dict) else {}


def _spoken(markdown: str) -> str:
    """Notes as plain text: the markdown marks and the maths markup taken out."""
    return plain_maths(_LIST_MARK.sub("• ", _MARKDOWN_MARKS.sub("", markdown)))


def _figure_png(source: str, layout: SlideLayout) -> bytes | None:
    """The drawing as a picture, or ``None`` where it cannot be drawn here."""
    svg = tikz_to_svg(source)
    if svg is None:
        return None
    ensure_native_lib_path()
    import cairosvg  # noqa: PLC0415  # needs the native libraries path set first

    try:
        png: bytes = cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            output_width=layout.figure_pixels,
            background_color="white",
        )
    except Exception:  # noqa: BLE001  # cairosvg raises many types; the slide keeps its words
        logger.warning("a slide's drawing could not be turned into a picture")
        return None
    return png


def _is_wide(png: bytes, layout: SlideLayout) -> bool:
    width, height = Image.open(io.BytesIO(png)).size
    return width >= layout.wide_ratio * height


def _place_picture(
    slide: PptxSlide, png: bytes, left: Length, top: Length, box: tuple[Length, Length]
) -> None:
    """The picture as large as the box allows, centred in it."""
    picture = slide.shapes.add_picture(io.BytesIO(png), left, top)
    width_box, height_box = box
    scale = min(width_box / picture.width, height_box / picture.height)
    picture.width, picture.height = (
        Emu(int(picture.width * scale)),
        Emu(int(picture.height * scale)),
    )
    picture.left = Emu(left + (width_box - picture.width) // 2)
    picture.top = Emu(top + (height_box - picture.height) // 2)


def _text_height(points: list[str], width: Length, size: int, layout: SlideLayout) -> float:
    """The height, in points, that the points take at ``size`` in a box of ``width``."""
    usable_width = width / EMU_PER_POINT - layout.text_inset
    per_line = max(1, int(usable_width / (layout.character_width * size)))
    lines = sum(max(1, math.ceil(len(plain_maths(point)) / per_line)) for point in points)
    return lines * size * layout.line_height + len(points) * layout.point_gap


def _point_size(points: list[str], width: Length, height: Length, layout: SlideLayout) -> Length:
    """The largest size at which the points fit their box: a sparse slide reads large."""
    for size in layout.point_sizes:
        if _text_height(points, width, size, layout) <= layout.fill_share * height / EMU_PER_POINT:
            return Pt(size)
    return Pt(layout.point_sizes[-1])


def _style(paragraph: _Paragraph, size: Length, colour: RGBColor, bold: bool | None = None) -> None:
    """Size, colour and weight set on the runs, which a slide program honours."""
    for run in paragraph.runs:
        run.font.size, run.font.color.rgb = size, colour
        if bold is not None:
            run.font.bold = bold


def _title_size(text: str, layout: SlideLayout) -> Length:
    """The largest size at which the title fits on one line, so it never runs into the points."""
    usable = layout.full_width / EMU_PER_POINT - layout.text_inset
    shown = len(plain_maths(text))
    for size in layout.title_sizes:
        if shown * layout.bold_character_width * size <= usable:
            return Pt(size)
    return Pt(layout.title_sizes[-1])


def _cover_title_size(text: str, layout: SlideLayout) -> Length:
    """The largest size at which the cover title, over as many lines as it needs, fits its box."""
    usable = layout.full_width / EMU_PER_POINT - layout.text_inset
    shown = len(plain_maths(text))
    for size in layout.cover_title_sizes:
        lines = math.ceil(shown * layout.bold_character_width * size / usable)
        if lines * size * layout.line_height <= layout.cover_title_height / EMU_PER_POINT:
            return Pt(size)
    return Pt(layout.cover_title_sizes[-1])


def _write_points(
    slide: PptxSlide, points: list[str], width: Length, height: Length, layout: SlideLayout
) -> None:
    body = slide.placeholders[1]
    body.left, body.top, body.width, body.height = layout.margin, layout.body_top, width, height
    frame = body.text_frame
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    size = _point_size(points, width, height, layout)
    for index, point in enumerate(points):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = plain_maths(point)
        _style(paragraph, size, layout.ink)
        paragraph.space_after = Pt(layout.point_gap)
    if not points:
        body._element.getparent().remove(body._element)


def _write_title(
    slide: PptxSlide,
    text: str,
    top: Length,
    size: Length,
    height: Length,
    layout: SlideLayout,
    colour: RGBColor,
) -> None:
    title = slide.shapes.title
    if title is None:
        return
    title.left, title.top = layout.margin, top
    title.width, title.height = layout.full_width, height
    title.text = plain_maths(text)
    title.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    heading = title.text_frame.paragraphs[0]
    heading.alignment = PP_ALIGN.LEFT
    _style(heading, size, colour, bold=True)


def _accent_bar(slide: PptxSlide, layout: SlideLayout) -> None:
    """The deck's one mark: a band down the left edge of every content slide."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Emu(0), Emu(0), layout.accent_bar, layout.slide_height
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = layout.accent
    bar.line.fill.background()


def _add_cover(deck: PresentationFile, content: DeckSlide, layout: SlideLayout) -> None:
    """The title slide: the lesson's title, its subject line, and what the class will learn."""
    slide = deck.slides.add_slide(deck.slide_layouts[0])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = layout.accent
    _write_title(
        slide,
        content.title,
        layout.cover_title_top,
        _cover_title_size(content.title, layout),
        layout.cover_title_height,
        layout,
        layout.on_accent,
    )
    subtitle = slide.placeholders[1]
    subtitle.left, subtitle.top = layout.margin, layout.cover_subtitle_top
    subtitle.width, subtitle.height = layout.full_width, layout.cover_subtitle_height
    subtitle.text_frame.text = " ".join(content.points)
    line = subtitle.text_frame.paragraphs[0]
    line.alignment = PP_ALIGN.LEFT
    _style(line, layout.cover_subtitle_size, layout.on_accent)
    if content.objectives:
        box = slide.shapes.add_textbox(
            layout.margin,
            layout.cover_objectives_top,
            layout.full_width,
            layout.cover_objectives_height,
        )
        box.text_frame.word_wrap = True
        for index, objective in enumerate(content.objectives):
            paragraph = (
                box.text_frame.paragraphs[0] if index == 0 else box.text_frame.add_paragraph()
            )
            paragraph.text = plain_maths(objective)
            _style(paragraph, layout.cover_objectives_size, layout.on_accent)


def _add_figure_slide(
    slide: PptxSlide, content: DeckSlide, png: bytes, layout: SlideLayout
) -> None:
    """The points and the drawing, where the drawing's shape says: below them, or beside them."""
    if not _is_wide(png, layout):
        _write_points(
            slide, content.points, layout.body_width_beside_figure, layout.body_height, layout
        )
        _place_picture(slide, png, layout.figure_left, layout.body_top, layout.figure_box)
        return
    needed = Emu(
        int(
            _text_height(content.points, layout.full_width, layout.point_sizes[-1], layout)
            * EMU_PER_POINT
        )
    )
    figure_height = Emu(
        min(layout.wide_figure_max, max(layout.wide_figure_min, layout.body_height - needed))
    )
    points_height = Emu(layout.body_height - figure_height)
    _write_points(slide, content.points, layout.full_width, points_height, layout)
    _place_picture(
        slide,
        png,
        layout.margin,
        Emu(layout.body_top + points_height),
        (layout.full_width, figure_height),
    )


def _add_slide(deck: PresentationFile, content: DeckSlide, layout: SlideLayout) -> None:
    if content.cover:
        _add_cover(deck, content, layout)
        return
    slide = deck.slides.add_slide(deck.slide_layouts[1])
    _accent_bar(slide, layout)
    _write_title(
        slide,
        content.title,
        layout.title_top,
        _title_size(content.title, layout),
        layout.title_height,
        layout,
        layout.ink,
    )
    png = _figure_png(content.figure, layout) if content.figure else None
    if png is not None:
        _add_figure_slide(slide, content, png, layout)
    else:
        _write_points(slide, content.points, layout.full_width, layout.body_height, layout)
    notes = _spoken(content.notes)
    if content.figure and png is None:
        notes = f"{notes}\n\n{_DRAWING_MISSING}".strip()
    slide.notes_slide.notes_text_frame.text = notes


def build_pptx(slides: list[DeckSlide], layout: SlideLayout) -> bytes:
    """The deck as the bytes of a ``.pptx`` file, laid out as ``layout`` says."""
    deck = Presentation()
    deck.slide_width, deck.slide_height = layout.slide_width, layout.slide_height
    for slide in slides:
        _add_slide(deck, slide, layout)
    out = io.BytesIO()
    deck.save(out)
    return out.getvalue()
