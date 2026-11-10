"""What the app sets on a learner's part: the class note's drawings and an unwanted repair."""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.learner_part_pins import (
    drawings_of,
    pinned,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.engine_draft import (
    draft_from_part,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)

TRIANGLE = r"\begin{tikzpicture}\draw (0,0) -- (2,0) -- (1,1) -- cycle;\end{tikzpicture}"
SQUARE = r"\begin{tikzpicture}\draw (0,0) rectangle (1,1);\end{tikzpicture}"


def _base(explanation: str) -> ReviewPackSection:
    return ReviewPackSection(
        section_id="s1",
        title="Shapes",
        lesson_objective_id="lo1",
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text=explanation,
                lesson_objective_id="lo1",
            )
        ],
    )


def _state(misconception: str | None = None) -> ObjectiveLearnerState:
    return ObjectiveLearnerState.model_validate(
        {
            "lesson_objective_id": "lo1",
            "mastery_band": "reinforce",
            "misconception": misconception,
        }
    )


def test_the_class_sections_drawings_are_read_with_their_captions() -> None:
    base = _base(f"A triangle has three sides.\n\n{TRIANGLE}\n\n*A triangle ABC*\n\n{SQUARE}")

    assert drawings_of(base) == [
        {"drawing": TRIANGLE, "caption": "A triangle ABC"},
        {"drawing": SQUARE, "caption": ""},
    ]


def test_the_writers_drawings_give_way_to_the_class_sections() -> None:
    base = _base(f"A triangle has three sides.\n\n{TRIANGLE}\n\n*A triangle ABC*")
    written = {
        "explanation": f"Three sides make a triangle.\n\n{SQUARE}",
        "figures": [{"drawing": SQUARE, "caption": "something else"}],
        "title": "My own title",
    }

    kept = pinned(written, base, _state())

    assert kept["figures"] == [{"drawing": TRIANGLE, "caption": "A triangle ABC"}]
    assert SQUARE not in str(kept["explanation"])
    assert draft_from_part(kept).instructional_support.count("tikzpicture") == 2
    assert TRIANGLE in draft_from_part(kept).instructional_support


def test_a_section_with_no_drawing_gets_none() -> None:
    kept = pinned({"explanation": f"Text.\n\n{SQUARE}"}, _base("Plain text."), _state())

    assert kept["figures"] == [] and "tikzpicture" not in str(kept["explanation"])


def test_a_repair_is_kept_only_where_the_state_names_a_misconception() -> None:
    written = {"explanation": "x", "misconception_repair": "A common slip is ..."}

    assert "misconception_repair" in pinned(written, _base("x"), _state("adds denominators"))
    assert "misconception_repair" not in pinned(written, _base("x"), _state())
