"""A drawing's own measurements must survive the stripping of its source.

TikZ is replaced before the model reads a note, and on `t3-w02` seven of fourteen
drawings label their dimensions where the prose never repeats them — so stripping
deleted the only statement of what Examples 4, 5 and 10 measure. A blind auditor
recorded 4.9 as "appearing for the first time inside the solution"; it was on her
drawing all along.
"""

from __future__ import annotations

import json

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    drawings_as_references,
    drawn_labels,
)
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

CASES = {c["lesson"]: c for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}


def _model_sees(lesson: str) -> str:
    return "\n".join(
        drawings_as_references(step.get("note") or "", step["step_id"])
        for step in CASES[lesson]["plan"]["steps"]
    )


@pytest.mark.parametrize(
    ("lesson", "measurement"),
    [
        ("t3-w02", "4.9 cm"),  # Example 10, the composite shape
        ("t3-w02", "5.2cm"),  # Example 6, the regular hexagon — written without a space
        ("t3-w02", "15cm"),  # Example 1, the square
        # The prism's triangular face. Her working gives the numbers bare —
        # "$\\frac{1}{2} \\times 5 \\times 3$" — and only fig-03 carries their unit.
        ("t3-w05", "3 m"),
    ],
)
def test_dimensions_reach_the_model(lesson: str, measurement: str) -> None:
    assert measurement in _model_sees(lesson)


@pytest.mark.parametrize(
    "term", ["Diameter", "Radius", "Chord", "Circumference", "Segment", "Sector", "Tangent"]
)
def test_the_circle_vocabulary_reaches_the_model(term: str) -> None:
    """An audit recorded these as "never defined"; they are labelled on her figure."""
    assert term in _model_sees("t3-w02")


def test_style_declarations_are_not_writing() -> None:
    """``every node/.style={font=\\small}`` is a directive, not text on the page."""
    assert "font=" not in _model_sees("t3-w05")


def test_the_drawing_source_itself_never_does() -> None:
    for lesson in CASES:
        seen = _model_sees(lesson)
        assert "tikzpicture" not in seen
        assert "\\draw" not in seen


def test_an_unlabelled_drawing_reads_as_one() -> None:
    """ "attached as unlabelled" was read as the drawing's NAME by a blind auditor."""
    seen = _model_sees("t3-w02")
    assert "as unlabelled" not in seen
    assert "here, unlabelled" in seen


def test_only_written_text_is_lifted() -> None:
    tikz = r"\begin{tikzpicture}\draw (0,0) -- (2.4,0); \node at (1.2,0) {1 cm};\end{tikzpicture}"
    # (0,0) and (2.4,0) are coordinates, not things written on the drawing.
    assert drawn_labels(tikz) == ["1 cm"]


def test_a_label_hung_off_a_path_is_lifted() -> None:
    """`t3-w04` names "face", "vertex" and "edge" this way — the lesson's whole point."""
    tikz = (
        r"\draw (4.3,2.4)--(8.5,2.4) node[right] {face};"
        r"\draw (7.6,1.6)--(8.5,1.6) node[right] {vertex};"
    )
    assert drawn_labels(tikz) == ["face", "vertex"]


def test_repeated_labels_are_reported_once() -> None:
    tikz = r"\node {5.2 cm}; \node {5.2 cm}; \node {5.2 cm};"
    assert drawn_labels(tikz) == ["5.2 cm"]
