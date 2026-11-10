"""A leak in a practice answer is a leak.

The run metric read block text alone, and the practice is where the maths sits:
across ``c0c3-prism-objective`` the practice fields carried 36 of the 152 figure
citations and every ``\\(…\\)`` in an answer, and none of it was counted.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from experiments.h1_condition_eval.measurements import pack_metrics, reader_facing_text


def _section(
    *, text: str = "", caption: str | None = None, answer: str = "a", worked: str | None = None
) -> ReviewPackSection:
    blocks = [
        ReviewPackBlock(
            block_id="b0", block_type="explanation", text=text, lesson_objective_id="lo"
        )
    ]
    if caption is not None:
        blocks.append(
            ReviewPackBlock(
                block_id="b1",
                block_type="visual",
                lesson_objective_id="lo",
                variant="image",
                caption=caption,
                figure_ref="fig-01",
            )
        )
    return ReviewPackSection(
        section_id="s",
        title="t",
        lesson_objective_id="lo",
        blocks=blocks,
        practice=[
            ReviewPackPracticeItem(item_id="p0", prompt="q", answer=answer, worked_solution=worked)
        ],
    )


def test_every_reader_facing_field_is_read() -> None:
    section = _section(text="T", caption="C", answer="A", worked="W")
    assert reader_facing_text([section]).split("\n") == ["T", "C", "q", "A", "W"]


def test_html_in_a_practice_answer_is_counted() -> None:
    metrics = pack_metrics([_section(answer="<strong>10x</strong>")])
    assert metrics["html_markers"] == 2


def test_a_bare_command_in_a_worked_solution_is_counted() -> None:
    metrics = pack_metrics([_section(worked=r"4 \times 5 = 20")])
    assert metrics["raw_latex_markers"] == 1


def test_clean_text_scores_zero_on_both() -> None:
    metrics = pack_metrics([_section(text="Perimeter is $4s$.", caption="A square.")])
    assert metrics["html_markers"] == 0
    assert metrics["raw_latex_markers"] == 0
