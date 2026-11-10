"""The learner attempts before checking, and the worksheet's shape is what enforces it.

``artefact_spec`` has always required "answers at the end, so the learner attempts first
and then checks". While a practice question and its answer were one paragraph of model
prose, nothing could enforce it and the model put the answer directly under its own
question in 9 of 12 lesson/condition cells — three blinded judges marked packs down for
defeating self-testing (issue #163). A practice item now carries its answer as a field,
so placement belongs to the renderer, and this is what says the renderer does it.
"""

from __future__ import annotations

import pytest

from app.domains.evaluation.application.worksheet_html.renderer import render_h1_worksheet_html
from tests.worksheet_pdf_support import worksheet_text

DETAIL = {
    "packet_code": "H1-TEST",
    "reference_sheet": {"subject": "Mathematics", "grade": "JSS1"},
    "objectives": [{"objective_text": "Find the area of rectangles"}],
    "candidate_pack": {
        "manifest": {
            "steps": [
                {
                    "step_id": "s1",
                    "title": "Working out area",
                    "blocks": [
                        {"type": "explanation", "content": "Area = length x breadth."},
                        {
                            "type": "practice",
                            "id": "s1:p0",
                            "question": "Find the area of an 8 cm by 4 cm rectangle.",
                            "answer": "32 square centimetres\n\n8 x 4 = 32",
                        },
                    ],
                }
            ]
        }
    },
    "rubric": [],
}


def test_the_answer_is_not_printed_beside_its_own_question() -> None:
    html = render_h1_worksheet_html(DETAIL)
    question = html.index("8 cm by 4 cm")
    heading = html.index("Check your work")
    answer = html.index("32 square centimetres")
    assert question < heading < answer, "the answer must follow the activities, not sit in them"
    assert "Answer:</strong>" not in html


def test_a_worked_solution_waits_with_the_answer() -> None:
    """It shows the method, so beside the question it gives the attempt away.

    The adapter folds it into the answer rather than into ``hints``: a hint scaffolds an
    attempt and is shown with the question; a worked solution is checking support.
    """
    html = render_h1_worksheet_html(DETAIL)
    assert html.index("8 x 4 = 32") > html.index("Check your work")
    assert "Hints:" not in html


def test_a_worksheet_with_no_practice_has_no_answer_page() -> None:
    detail = {
        **DETAIL,
        "candidate_pack": {
            "manifest": {
                "steps": [
                    {
                        "step_id": "s1",
                        "title": "Working out area",
                        "blocks": [{"type": "explanation", "content": "Area = length x breadth."}],
                    }
                ]
            }
        },
    }
    assert "Check your work" not in render_h1_worksheet_html(detail)


def test_display_math_that_runs_on_from_prose_still_typesets() -> None:
    r"""Markdown reads ``text\n\[…\]`` as one paragraph, so arithmatex never marks it.

    The reader then gets a raw ``\[P = 6 \times 4\text{ cm}\]`` beside formulas that
    rendered cleanly — a blinded judge found exactly that in an answer key, which is the
    self-check material a learner has no way to correct (issue #131). The fix is to give
    the block the blank line markdown needs, not to widen a regex over the output.
    """
    from app.domains.evaluation.application.worksheet_html.renderer import _render_markdown

    run_on = "A hexagon has 6 equal sides. If each is 4 cm, then\n\\[P = 6 \\times 4 = 24.\\]"
    html = str(_render_markdown(run_on))
    assert "\\[" not in html and "\\times" not in html, "raw LaTeX reached the reader"
    assert "<svg" in html

    # A blank line already there must not become two, and inline math is untouched.
    spaced = "A hexagon has 6 equal sides.\n\n\\[P = 6 \\times 4 = 24.\\]"
    assert "\\[" not in str(_render_markdown(spaced))
    assert "<svg" in str(_render_markdown("Inline \\(\\pi \\approx 3.14\\) works."))


CONSTRUCTION_DETAIL = {
    "packet_code": "H1-TEST",
    "reference_sheet": {"subject": "Mathematics", "grade": "JSS1"},
    "objectives": [{"objective_text": "Construct a line parallel to a given line"}],
    "candidate_pack": {
        "manifest": {
            "steps": [
                {
                    "step_id": "s1",
                    "title": "How to Construct Parallel Lines",
                    "blocks": [
                        {
                            "type": "practice",
                            "id": "s1:p0",
                            "question": "Construct a line parallel to the given slanted line.",
                            "answer": (
                                "1. Draw a short horizontal base line AB.\n"
                                "2. Place the set-square on AB.\n"
                                "3. Mark a point C on the given slanted line."
                            ),
                        },
                        {
                            "type": "practice",
                            "id": "s1:p1",
                            "question": "Which tool keeps the two lines the same distance apart?",
                            "answer": "A set-square slid along a ruler.",
                        },
                    ],
                }
            ]
        }
    },
    "rubric": [],
}


@pytest.fixture(scope="module")
def construction_worksheet() -> str:
    """The worksheet as a reader gets it, whitespace flattened.

    The list markers are the stylesheet's, not the markup's — the HTML carries an
    ``<ol>`` inside an ``<ol>`` either way — so only the rendered page shows the
    numbering a learner reads.
    """
    return worksheet_text(CONSTRUCTION_DETAIL)


def test_a_multi_step_answer_reads_as_sub_steps_under_its_number(
    construction_worksheet: str,
) -> None:
    """A construction answer is a numbered list of its own, and markdown restarts it
    at 1 inside the answer key's numbering. Both runs are decimal, so the page opened
    "1. 1. Draw a short horizontal base line AB." with nothing to say which number was
    the question's. The outer number is the only tie back to the question, so the inner
    list is what gives way.
    """
    answers = construction_worksheet[construction_worksheet.index("Check your work") :]
    assert "1. a. Draw a short horizontal base line AB." in answers
    assert "b. Place the set-square on AB." in answers
    assert "c. Mark a point C on the given slanted line." in answers
    assert "1. 1." not in answers


def test_the_sub_steps_do_not_consume_the_next_answer_number(
    construction_worksheet: str,
) -> None:
    """Splicing the steps into the answer key's own list would read just as cleanly
    and silently renumber: the second answer becomes 4 and stops finding question 2.
    """
    questions, answers = construction_worksheet.split("Check your work")
    assert "1. Construct a line parallel" in questions
    assert "2. Which tool keeps" in questions
    assert "2. A set-square slid along a ruler." in answers
