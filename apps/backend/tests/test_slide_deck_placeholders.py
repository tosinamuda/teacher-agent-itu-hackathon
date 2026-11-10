"""A slide whose drawing says it is unfinished is sent back."""

from __future__ import annotations

import pytest

from app.domains.content_engine.rules.slide_deck.placeholders import placeholder_drawings
from tests.slide_deck_support import deck, slide

PLACEHOLDER = (
    "\\begin{tikzpicture}\n% Exact TikZ code from lesson note\n\\draw (0,0) rectangle (10,5);\n"
    "% ... (full drawing omitted for brevity)\n\\end{tikzpicture}"
)
DRAWN = (
    "\\begin{tikzpicture}\n\\draw (0,0) -- (10,0);\n"
    "\\foreach \\x in {0,...,10} \\draw (\\x,0) -- (\\x,0.2);\n\\end{tikzpicture}"
)


def _with_figure(figure: str) -> dict[str, object]:
    return {**slide("See the chart"), "figure": figure}


def test_a_drawing_that_says_it_is_omitted_for_brevity_goes_back() -> None:
    issues = placeholder_drawings(deck(step01=[slide("Intro"), _with_figure(PLACEHOLDER)]))

    assert len(issues) == 1
    assert issues[0].startswith("step01: slide 2 draws a placeholder")


@pytest.mark.parametrize("comment", ["% placeholder", "% TODO draw this", "% to be completed"])
def test_other_comments_that_say_the_drawing_is_unfinished_go_back_too(comment: str) -> None:
    figure = f"\\begin{{tikzpicture}}\n{comment}\n\\draw (0,0) -- (1,1);\n\\end{{tikzpicture}}"

    assert len(placeholder_drawings(deck(step01=[_with_figure(figure)]))) == 1


def test_a_finished_drawing_and_a_slide_with_none_have_no_fault() -> None:
    assert placeholder_drawings(deck(step01=[_with_figure(DRAWN), slide("No drawing")])) == []
