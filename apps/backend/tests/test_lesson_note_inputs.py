"""The note writer sees the plan's own questions, and a note never shows a written-out newline."""

from __future__ import annotations

from app.domains.artefacts.lesson_note.application.draft import note_inputs
from app.domains.artefacts.lesson_note.domain.note import ClassQuestion, NoteStepDraft
from app.shared.session_plan_view import SessionPlanView


def test_each_step_is_written_with_the_questions_the_plan_sets_in_it() -> None:
    plan = SessionPlanView.model_validate(
        {
            "lesson_plan_objectives": [],
            "steps": [
                {
                    "step_id": "evaluation",
                    "step_kind": "evaluation",
                    "title": "Evaluation",
                    "content": "Check mastery.",
                    "blocks": [
                        {
                            "id": "q1",
                            "type": "practice",
                            "question": "Convert 22/5.",
                            "answer": "4 2/5",
                        },
                        {"id": "e1", "type": "explanation", "content": "Not a question."},
                    ],
                }
            ],
        }
    )

    _, (step,) = note_inputs(plan)

    assert [(q.question, q.expected_answer) for q in step.questions] == [("Convert 22/5.", "4 2/5")]


def test_a_written_out_newline_breaks_the_line_and_a_command_in_maths_is_kept() -> None:
    draft = NoteStepDraft(
        title="Compare",
        teaching_points=["Compare."],
        board_summary=r"one.\n2. two $x \neq y$ $$\nu$$",
    )

    assert "one.\n2. two $x \\neq y$ $$\\nu$$" in draft.as_markdown()


def test_a_drafted_note_renders_without_written_out_newlines() -> None:
    draft = NoteStepDraft(
        title="Convert",
        teaching_points=["Divide."],
        board_summary=r"1. Divide.\n2. Keep the remainder.",
    )

    assert "1. Divide.\n2. Keep the remainder." in draft.as_markdown()


def test_a_textbook_exercise_and_its_working_stand_as_blocks_of_their_own() -> None:
    """Set in a list item, the working's lines and display maths broke out of it."""
    answer = (
        "1. $\\frac{30}{7}$\n\n            Parts in one whole: 7\n\n"
        "            $$\n\\begin{array}{r}\n4\\newline\n7 \\enclose{longdiv}{30}\n\\end{array}\n$$"
    )
    draft = NoteStepDraft(
        title="Evaluate",
        teaching_points=["Check."],
        class_questions=[
            ClassQuestion(question="Express as a mixed number.", expected_answer=answer)
        ],
        board_summary="Divide.",
    )

    assert (
        "#### Questions for the class\n\n**Question 1.**\n\nExpress as a mixed number.\n\n"
        f"*Expected answer:*\n\n{answer}\n\n#### On the board"
    ) in draft.as_markdown()


def test_a_point_s_own_list_marker_does_not_start_a_list_inside_its_bullet() -> None:
    draft = NoteStepDraft(
        title="Convert",
        teaching_points=["1. Divide the numerator.", "   • A proper fraction is less than one."],
        board_summary="Divide.",
    )

    assert "- 1\\. Divide the numerator.\n- A proper fraction is less than one." in (
        draft.as_markdown()
    )
