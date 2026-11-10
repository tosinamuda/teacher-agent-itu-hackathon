"""One number per practice item, and it is the renderer's.

Practice prompts arrive already numbered, copied out of the numbered task lists in the
teacher's note, and the worksheet renders each into an ordered list. The two schemes
stacked and the page opened "1. 1. Simplify 4n + 3n x 10.".

That was not cosmetic. Across the 288 blinded dimension-scores of `c0c3-worksheet`,
twenty flagged it — C0 1, C1 2, C2 8, C3 9 — because 51% of C2's and 56% of C3's prompts
carry their own number against 17% of C0's and 18% of C1's: the grounded arms copy her
task lists, so the arms whose treatment *is* reading her note were the arms penalised for
reading it, on the clarity dimension. A rating-instrument confound, directional against
the treatment, so what the numbering does is a claim the suite has to hold.
"""

from __future__ import annotations

import pytest

from app.domains.evaluation.application.worksheet_html.lesson_plan_renderer import (
    render_lesson_plan_html,
)
from app.shared.item_numbering import under_supplied_number
from tests.worksheet_pdf_support import worksheet_text


def _detail(*blocks: dict[str, object]) -> dict[str, object]:
    return {
        "packet_code": "H1-TEST",
        "reference_sheet": {"subject": "Mathematics", "grade": "JSS1"},
        "objectives": [{"objective_text": "Simplify algebraic expressions"}],
        "candidate_pack": {
            "manifest": {
                "steps": [{"step_id": "s1", "title": "Order of operations", "blocks": list(blocks)}]
            }
        },
        "rubric": [],
    }


def _practice(question: str, answer: str) -> dict[str, object]:
    return {"type": "practice", "question": question, "answer": answer}


NUMBERED_PROMPTS = _detail(
    _practice("1. Simplify 4n + 3n x 10.", "34n"),
    _practice("2. Simplify 32 + 8x / 2.", "32 + 4x"),
    _practice("3. Simplify 3 x 5x + 4x / 2.", "17x"),
)


@pytest.fixture(scope="module")
def numbered_prompts_worksheet() -> str:
    """The page a learner reads, whitespace flattened.

    The markers are the stylesheet's rather than the markup's — the HTML holds an
    ``<ol>`` inside an ``<ol>`` whichever way this goes — so only the rendered page
    shows the numbering.
    """
    return worksheet_text(NUMBERED_PROMPTS)


def test_a_prompt_that_arrives_numbered_is_numbered_once(
    numbered_prompts_worksheet: str,
) -> None:
    questions = numbered_prompts_worksheet.split("Check your work")[0]
    assert "1. Simplify 4n + 3n x 10." in questions
    assert "2. Simplify 32 + 8x / 2." in questions
    assert "3. Simplify 3 x 5x + 4x / 2." in questions


def test_the_prompt_s_own_number_is_gone_rather_than_relettered(
    numbered_prompts_worksheet: str,
) -> None:
    """Rendering the inner list at a second level makes it "1. a. Simplify …", which
    reads as a sub-step of a question that has none. A copy of the item's number is not
    a sub-step, so it comes off instead of changing marker.
    """
    questions = numbered_prompts_worksheet.split("Check your work")[0]
    assert "1. 1." not in questions
    assert "1. a. Simplify" not in questions


def test_the_answer_key_still_keys_off_the_question_numbers(
    numbered_prompts_worksheet: str,
) -> None:
    """The outer number is the only tie between an answer and its question."""
    answers = numbered_prompts_worksheet[numbered_prompts_worksheet.index("Check your work") :]
    assert "1. 34n" in answers
    assert "2. 32 + 4x" in answers
    assert "3. 17x" in answers


def test_letter_parts_of_one_question_are_left_alone() -> None:
    """``(a)``/``(b)`` split a single question rather than numbering several, so they
    are not a duplicate of anything and the renderer must not touch them.
    """
    text = worksheet_text(
        _detail(
            _practice("(a) Simplify (12a - 7) + (4 - 5a).", "7a - 3"),
            _practice("(b) Simplify (8x - 2y) - (9x - 4y).", "-x + 2y"),
        )
    )
    questions = text.split("Check your work")[0]
    assert "1. (a) Simplify (12a - 7) + (4 - 5a)." in questions
    assert "2. (b) Simplify (8x - 2y) - (9x - 4y)." in questions


def test_an_answer_that_opens_with_a_decimal_keeps_its_digits() -> None:
    """ "25.12 cm" opens with digits and a dot and is an answer, not an enumerator —
    reading it as one would silently delete the answer the learner checks against.
    """
    circle = _practice("Find the circumference of a 4 cm circle.", "25.12 cm")
    text = worksheet_text(_detail(circle))
    answers = text[text.index("Check your work") :]
    assert "1. 25.12 cm" in answers


def test_a_run_of_sub_steps_written_as_one_paragraph_reads_as_a_list() -> None:
    """A construction answer is a list to a reader and one item to markdown, which
    numbers the first step and leaves the rest trailing inside it: "1. a. Draw line PQ.
    2. Place the compass at P." — two schemes again, in the self-check material a
    learner has no way to correct.
    """
    text = worksheet_text(
        _detail(
            _practice(
                "Construct a 60 degree angle at P.",
                "1. Draw line PQ. 2. Place the compass at P, draw an arc cutting PQ at R. "
                "3. Keep the width and draw an arc from R meeting the first at S.",
            )
        )
    )
    answers = text[text.index("Check your work") :]
    assert "1. a. Draw line PQ." in answers
    assert "b. Place the compass at P, draw an arc cutting PQ at R." in answers
    assert "c. Keep the width and draw an arc from R meeting the first at S." in answers
    assert "1. a. Draw line PQ. 2." not in answers


def test_a_surface_that_supplies_no_number_keeps_the_item_s_own() -> None:
    """The lesson plan labels each item "PRACTICE" instead of numbering it, so there is
    nothing for the prompt's number to duplicate and dropping it would lose the
    teacher's numbering outright. Only a caller that numbers may take a number away.
    """
    html = render_lesson_plan_html(
        {
            "topic": "Algebra",
            "steps": [
                {
                    "title": "Order of operations",
                    "blocks": [{"type": "practice", "question": "1. Simplify 4n + 3n x 10."}],
                }
            ],
        },
        plan_label="PLAN-1",
    )
    # The number survives as the list markdown made of it, which is what prints it.
    assert "<ol> <li>Simplify 4n + 3n x 10.</li> </ol>" in " ".join(html.split())


# --- the discriminators, directly ------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1. Simplify 4n + 3n x 10.", "Simplify 4n + 3n x 10."),
        ("2) Simplify 32 + 8x / 2.", "Simplify 32 + 8x / 2."),
        # Sentence-final and mid-sentence figures are not a successor, so the leading
        # number is still the item's own. Both shapes are in the field data.
        (
            "4. Your class read 3, 5, 2, 4, 5, 3, 4. What is one purpose of a table?",
            "Your class read 3, 5, 2, 4, 5, 3, 4. What is one purpose of a table?",
        ),
        # Sub-parts of the item survive the item's number coming off.
        (
            "1. A pen costs h naira.\n   (a) Find the cost of a crayon.",
            "A pen costs h naira.\n   (a) Find the cost of a crayon.",
        ),
    ],
)
def test_a_lone_leading_enumerator_is_the_item_s_own_number(text: str, expected: str) -> None:
    assert under_supplied_number(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "(a) Simplify (12a - 7) + (4 - 5a).",
        "25.12 cm",
        "3.5 cm",
        "Simplify 4n + 3n x 10.",
        # Already one step per line: the run is a list and needs no rearranging.
        "1. Draw AB.\n2. Place the set-square on AB.\n3. Mark a point C.",
    ],
)
def test_text_carrying_no_duplicate_number_is_returned_unchanged(text: str) -> None:
    assert under_supplied_number(text) == text


def test_a_run_of_steps_is_broken_onto_its_own_lines() -> None:
    assert under_supplied_number("1. Draw PQ. 2. Place the compass at P. 3. Draw an arc.") == (
        "1. Draw PQ.\n2. Place the compass at P.\n3. Draw an arc."
    )


def test_the_run_ends_where_the_numbering_does() -> None:
    """A figure that does not continue the run is prose, so the break stops before it."""
    assert under_supplied_number("1. Draw PQ. 2. Mark R. Repeat 5. times if needed.") == (
        "1. Draw PQ.\n2. Mark R. Repeat 5. times if needed."
    )


def test_a_run_written_with_parentheses_still_becomes_a_list() -> None:
    """Markdown reads only the dotted form as a list, so a run written "1) … 2) …" got
    no list, no second level, and the stylesheet had nothing to letter — leaving
    "1. 1) Place ruler along XY." on the answer page of three of the 72 packs.
    """
    text = worksheet_text(
        _detail(
            _practice(
                "Draw a line parallel to XY, 3 cm away.",
                "1) Place ruler along XY. 2) Position the set square against the ruler. "
                "3) Measure 3 cm and mark a point.",
            )
        )
    )
    answers = text[text.index("Check your work") :]
    assert "1. a. Place ruler along XY." in answers
    assert "b. Position the set square against the ruler." in answers
    assert "1) " not in answers


def test_a_surface_without_a_stylesheet_letters_the_run_itself() -> None:
    """The worksheet's second level is the stylesheet's doing. Plain markdown has none,
    so a run left in decimals would stack on the supplied number all over again.
    """
    assert under_supplied_number(
        "1. Draw PQ. 2. Place the compass at P. 3. Draw an arc.", letter_sub_steps=True
    ) == ("a. Draw PQ.\nb. Place the compass at P.\nc. Draw an arc.")


def test_the_blinded_markdown_packet_reads_the_way_the_worksheet_does() -> None:
    """A judge reads one candidate on two surfaces, and they have to say the same thing.

    The packet numbers its own practice list, so it carries the confound the worksheet
    carried: the prompt's number stacking on the one the list supplies.
    """
    from experiments.h1_condition_eval.rater_packets import _candidate

    packet = "\n".join(
        _candidate(
            [
                {
                    "title": "Constructions",
                    "blocks": [],
                    "practice": [
                        {
                            "prompt": "1. Simplify 4n + 3n x 10.",
                            "answer": "34n",
                        },
                        {
                            "prompt": "2. Construct a 60 degree angle at P.",
                            "answer": "1. Draw line PQ. 2. Place the compass at P.",
                        },
                    ],
                }
            ]
        )
    )
    questions, answers = packet.split("## Check your work")
    assert "1. Simplify 4n + 3n x 10." in questions
    assert "2. Construct a 60 degree angle at P." in questions
    assert "1. 34n" in answers
    assert "2. a. Draw line PQ." in answers
    assert "   b. Place the compass at P." in answers
    assert "1. 1." not in packet and "2. 2." not in packet


def test_an_answer_keeps_the_labels_its_question_used() -> None:
    r"""An answer is marked without seeing its question, and can contradict it.

    Nine items in the judged run — all C0, all t3-w09 — asked "1. Which student…
    2. What is the total… 3. …" and answered "a. Hannah / b. 54 / c. 10.8". Nothing
    was wrong with either half alone; a learner just had to count to pair them.
    """
    from app.shared.item_numbering import marks_a_numbered_run
    from experiments.h1_condition_eval.rater_packets import _numbered_here

    question = (
        "Answer the following questions:\n"
        "1. Which student collected the most marbles?\n"
        "2. What is the total?\n"
        "3. What is the mean?"
    )
    assert marks_a_numbered_run(question)

    answer = "1. Hannah\n2. 54\n3. 10.8"
    following = _numbered_here(answer, like=question)
    assert "1. Hannah" in following
    assert "a. Hannah" not in following

    # A question with no parts of its own still letters, which is what keeps a
    # construction's steps off the item numbering the packet supplies.
    steps = "1. Draw line PQ.\n2. Place compass at P.\n3. Draw the arc."
    assert "a. Draw line PQ." in _numbered_here(steps, like="Construct a 60 degree angle.")


def test_the_reference_sheet_shows_a_figure_as_a_reference_not_as_tikz() -> None:
    r"""The half of the packet that is her plan, which no treatment reached.

    Every fix so far applied to the candidate pack. The reference sheet beside it is
    built straight from her plan, so a question she illustrated arrived as
    ``\begin{tikzpicture}`` — nine commands on t3-w02, read by every judge of that
    lesson across both passes, where a figure belongs.
    """
    import json

    from app.domains.evaluation.application.lesson_reference import lesson_reference
    from app.shared.llm_markup import count_bare_math
    from app.shared.session_plan_view import SessionPlanView
    from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
    from experiments.h1_condition_eval.rater_packets import _plan_reference

    plans = {c["lesson"]: c["plan"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}

    def sheet_for(plan: dict) -> str:
        return "\n".join(_plan_reference(lesson_reference(SessionPlanView.model_validate(plan))))

    for lesson, plan in plans.items():
        sheet = sheet_for(plan)
        assert count_bare_math(sheet) == 0, lesson
        assert "tikzpicture" not in sheet, lesson

    illustrated = sheet_for(plans["t3-w02"])
    assert "[the figure is not included here, marked 1cm, 5cm, 9cm]" in illustrated
