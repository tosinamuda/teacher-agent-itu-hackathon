"""How a slide deck is laid out as a PowerPoint file: what the deck's plugin says, as lengths."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Length, Pt

from app.shared.json_types import JsonObject, JsonValue

#: The file beside this one that says how slides are laid out.
LAYOUT_FILE = "powerpoint.json"
EMU_PER_POINT = 12700
_HEX_COLOUR = re.compile(r"[0-9A-Fa-f]{6}")


class LayoutError(ValueError):
    """The layout file is missing or does not say what a PowerPoint file needs."""


@dataclass(frozen=True)
class SlideLayout:
    """Sizes and colours of a deck's slides; each list of text sizes runs largest first."""

    slide_width: Length
    slide_height: Length
    margin: Length
    accent_bar: Length
    title_top: Length
    title_height: Length
    title_sizes: tuple[int, ...]
    body_top: Length
    body_height: Length
    point_sizes: tuple[int, ...]
    point_gap: int
    wide_ratio: float
    wide_figure_min: Length
    wide_figure_max: Length
    body_width_beside_figure: Length
    figure_left: Length
    figure_box_width: Length
    figure_pixels: int
    cover_title_top: Length
    cover_title_height: Length
    cover_title_sizes: tuple[int, ...]
    cover_subtitle_top: Length
    cover_subtitle_height: Length
    cover_subtitle_size: Length
    cover_objectives_top: Length
    cover_objectives_height: Length
    cover_objectives_size: Length
    character_width: float
    bold_character_width: float
    line_height: float
    text_inset: int
    fill_share: float
    ink: RGBColor
    accent: RGBColor
    on_accent: RGBColor

    @property
    def full_width(self) -> Length:
        """The width between the margins."""
        return Emu(self.slide_width - 2 * self.margin)

    @property
    def figure_box(self) -> tuple[Length, Length]:
        """The room a drawing beside the points may take."""
        return (self.figure_box_width, self.body_height)


def _group(source: JsonObject, name: str) -> JsonObject:
    group = source.get(name)
    if not isinstance(group, dict):
        raise LayoutError(f"the layout has no '{name}'")
    return group


def _number(group: JsonObject, name: str) -> float:
    value = group.get(name)
    if isinstance(value, bool) or not isinstance(value, int | float) or value <= 0:
        raise LayoutError(f"'{name}' must be a number above zero")
    return float(value)


def _sizes(group: JsonObject, name: str) -> tuple[int, ...]:
    value: JsonValue | None = group.get(name)
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(s, int) and not isinstance(s, bool) and s > 0 for s in value)
    ):
        raise LayoutError(f"'{name}' must list the text sizes, in points")
    sizes = tuple(int(s) for s in value if isinstance(s, int))
    if list(sizes) != sorted(sizes, reverse=True):
        raise LayoutError(f"'{name}' must list the sizes largest first")
    return sizes


def _colour(group: JsonObject, name: str) -> RGBColor:
    value = group.get(name)
    if not isinstance(value, str) or _HEX_COLOUR.fullmatch(value) is None:
        raise LayoutError(f"'{name}' must be a colour of six hexadecimal digits")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def _inches(group: JsonObject, name: str) -> Length:
    return Inches(_number(group, name))


def parse_layout(source: JsonObject) -> SlideLayout:
    """The layout a plugin's file says; ``LayoutError`` where it leaves something out."""
    slide, title, body = _group(source, "slide"), _group(source, "title"), _group(source, "body")
    figure, cover = _group(source, "figure"), _group(source, "cover")
    fit, colours = _group(source, "fit"), _group(source, "colours")
    return SlideLayout(
        slide_width=_inches(slide, "width_in"),
        slide_height=_inches(slide, "height_in"),
        margin=_inches(slide, "margin_in"),
        accent_bar=_inches(slide, "accent_bar_in"),
        title_top=_inches(title, "top_in"),
        title_height=_inches(title, "height_in"),
        title_sizes=_sizes(title, "sizes_pt"),
        body_top=_inches(body, "top_in"),
        body_height=_inches(body, "height_in"),
        point_sizes=_sizes(body, "sizes_pt"),
        point_gap=int(_number(body, "point_gap_pt")),
        wide_ratio=_number(figure, "wide_ratio"),
        wide_figure_min=_inches(figure, "wide_min_in"),
        wide_figure_max=_inches(figure, "wide_max_in"),
        body_width_beside_figure=_inches(figure, "body_width_beside_in"),
        figure_left=_inches(figure, "left_in"),
        figure_box_width=_inches(figure, "box_width_in"),
        figure_pixels=int(_number(figure, "pixels")),
        cover_title_top=_inches(cover, "title_top_in"),
        cover_title_height=_inches(cover, "title_height_in"),
        cover_title_sizes=_sizes(cover, "title_sizes_pt"),
        cover_subtitle_top=_inches(cover, "subtitle_top_in"),
        cover_subtitle_height=_inches(cover, "subtitle_height_in"),
        cover_subtitle_size=Pt(_number(cover, "subtitle_size_pt")),
        cover_objectives_top=_inches(cover, "objectives_top_in"),
        cover_objectives_height=_inches(cover, "objectives_height_in"),
        cover_objectives_size=Pt(_number(cover, "objectives_size_pt")),
        character_width=_number(fit, "character_width_em"),
        bold_character_width=_number(fit, "bold_character_width_em"),
        line_height=_number(fit, "line_height"),
        text_inset=int(_number(fit, "text_inset_pt")),
        fill_share=_number(fit, "fill_share"),
        ink=_colour(colours, "ink"),
        accent=_colour(colours, "accent"),
        on_accent=_colour(colours, "on_accent"),
    )


def load_layout() -> SlideLayout:
    """The layout in ``powerpoint.json`` beside this file."""
    try:
        source = json.loads((Path(__file__).parent / LAYOUT_FILE).read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LayoutError(f"{LAYOUT_FILE} cannot be read: {error}") from error
    if not isinstance(source, dict):
        raise LayoutError(f"{LAYOUT_FILE} must be an object")
    return parse_layout(source)
