"""A stored slide deck as a PowerPoint file, laid out as ``powerpoint.json`` says."""

from __future__ import annotations

from functools import cache

from app.domains.content_engine.files.builder import BuiltFile, FileRefusedError
from app.domains.content_engine.files.slide_deck.build import build_pptx, deck_slides
from app.domains.content_engine.files.slide_deck.layout import SlideLayout, load_layout
from app.shared.json_types import JsonObject

PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


@cache
def _layout() -> SlideLayout:
    return load_layout()


def build_slide_deck_file(content: JsonObject) -> BuiltFile:
    """The deck's PowerPoint file; ``FileRefusedError`` when the deck has no slide."""
    slides = deck_slides(content)
    if not slides:
        raise FileRefusedError("slide_deck_is_empty")
    return BuiltFile("pptx", PPTX, build_pptx(slides, _layout()))
