"""What the note-task probe may and may not conclude.

The probe exists to stop a count standing in for a reading: it finds task-shaped
lines in a teacher's note and reports what the note does with each one next. The
distinction it draws — solved on the page, drawn at the next stage, or neither —
is the whole value, so these pin it.
"""

from __future__ import annotations

from scripts.prompt_snapshots.note_tasks import Disposition, paragraphs, task_lines


def test_a_solution_outranks_a_figure_wherever_both_follow() -> None:
    """Her worked examples put the figure first and solve underneath it.

    Taking whichever came first read `Calculate the volume of the prism below.`
    — a fully worked example on t3-w05 — as a construction stage.
    """
    note = (
        "Calculate the volume of the prism below.\n\n"
        "**fig-03.** A triangular prism lying on its rectangular face.\n\n"
        "Solution:\n\n"
        "Area of triangular face = 7.5m^2\n"
    )
    (found,) = task_lines(note)
    assert found.disposition is Disposition.WORKED
    assert found.followed_by == "Solution:"


def test_a_stage_drawing_marks_a_construction_she_performed() -> None:
    note = (
        "1. Draw a line AB mark a point Q on the line.\n\n"
        "**fig-07.** A plain line with a stroke at each end.\n\n"
        "2. Place the edge of the set square on line AB.\n\n"
        "**fig-08.** Line AB with the set square standing on it.\n"
    )
    assert [found.disposition for found in task_lines(note)] == [
        Disposition.DEMONSTRATED,
        Disposition.DEMONSTRATED,
    ]


def test_a_line_with_neither_stays_open_for_the_source_page() -> None:
    note = "Find the cost of a pencil.\n\nThe class then copied the table.\n"
    (found,) = task_lines(note)
    assert found.disposition is Disposition.OPEN


def test_an_enumerator_or_bold_marker_does_not_hide_the_verb() -> None:
    note = (
        "(a) Find the cost of a pencil\n\n**Solution**\n\n"
        "2. Draw a line AB\n\n**fig-01.** A line.\n"
    )
    assert [found.disposition for found in task_lines(note)] == [
        Disposition.WORKED,
        Disposition.DEMONSTRATED,
    ]


def test_prose_that_merely_mentions_a_verb_is_not_a_task() -> None:
    """The verb has to open the line. `We can find …` is exposition."""
    assert task_lines("We can find the cost by writing it as an equation.\n\nSolution:\n") == []


def test_drawing_source_and_review_markup_leave_before_the_probe_reads() -> None:
    note = (
        "Draw a line segment AB.\n\n"
        "\\begin{center}\n\\begin{tikzpicture}\n\\draw (0,0) -- (7,0);\n"
        "\\end{tikzpicture}\n\\end{center}\n\n"
        "<!-- transcriber: the arc is faint here -->\n\n"
        "**fig-13.** The line AB with a stroke at each end.\n"
    )
    assert "tikzpicture" not in " ".join(paragraphs(note))
    assert "transcriber" not in " ".join(paragraphs(note))
    (found,) = task_lines(note)
    assert found.disposition is Disposition.DEMONSTRATED
