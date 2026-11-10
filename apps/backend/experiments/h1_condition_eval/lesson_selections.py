"""What each surface selects from a canonical lesson document.

The migration table in ``LESSON-SCHEMA.md``, executable. Every function here replaces a
parse with a selection: the same answer today's code reaches by regex, reached instead
by asking the document what it declared. ``tests/test_lesson_document.py`` holds them to
that — each selection must equal the parsing path on the frozen lesson.

What is left of the regexes is deliberate. ``question_as_asked`` still runs: turning
drawing source into a readable reference is *rendering*, and it stays. What goes is the
structural guessing — which block is work, which activity performs, where a figure is,
which region a line number falls in.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    question_as_asked,
    work_the_step_sets,
)
from experiments.h1_condition_eval.lesson_document import Lesson, Section, Step


def set_work(step: Step) -> tuple[Section, ...]:
    """``//set-work`` — the regions she headed as work for the students."""
    return tuple(section for section in step.sections if section.role == "set-work")


def student_tasks(step: Step) -> list[str]:
    """The work this step sets: its set-work regions, else the activities that set work.

    Still a fallback rather than an addition, for the reason it always was — where a
    step has both, the activity is a label for the questions beside it. What changed is
    that ``sets-work`` is now declared on the activity, so the Gagne coder is never
    consulted to decide a study input; it proposes at authoring time and the file
    records what a reader concluded.
    """
    written = [question_as_asked(section.body) for section in set_work(step) if section.body]
    return written or work_the_step_sets(
        [
            {"who": activity.who, "what": activity.what, "sets_work": activity.sets_work}
            for activity in step.activities
        ]
    )


def assessment_points(lesson: Lesson) -> dict[str, list[str]]:
    """``//question[@objective]`` grouped by the objective each question checks."""
    points: dict[str, list[str]] = {}
    for step in lesson.steps:
        for question in step.questions:
            if question.objective:
                points.setdefault(question.objective, []).append(question_as_asked(question.text))
    return points


def figures(lesson: Lesson) -> list[tuple[str, str | None, str | None]]:
    """``//figure`` — (step, label, the caption the note is required to carry).

    A caption is not optional and not guessed by position: the document declares the
    label, validation refuses a label the region does not carry, and the caption is the
    line the note writes under it.
    """
    found: list[tuple[str, str | None, str | None]] = []
    for step in lesson.steps:
        for section in step.sections:
            for label in section.figures:
                found.append((step.id, label, _caption(section.body, label) if label else None))
    return found


def _caption(body: str, label: str) -> str:
    """The lines she wrote under a figure label, up to the blank line that ends them."""
    lines = body.splitlines()
    at = next(i for i, line in enumerate(lines) if line.startswith(f"**{label}.**"))
    caption = [lines[at].removeprefix(f"**{label}.**")]
    for line in lines[at + 1 :]:
        if not line.strip():
            break
        caption.append(line)
    return " ".join(" ".join(caption).split())


def region(lesson: Lesson, section_id: str) -> str:
    """One addressable region of a note — what ``read_document`` should take.

    Today that tool addresses lines, and a line number over a markdown blob moves the
    moment anyone edits a word above it. A section id does not move.
    """
    for step in lesson.steps:
        for section in step.sections:
            if section.id == section_id:
                return section.body
    raise KeyError(section_id)


def documents(lesson: Lesson) -> list[tuple[str, str, str]]:
    """What ``list_documents`` should offer: every region, addressed and titled."""
    return [
        (section.id, section.heading or step.title, section.role)
        for step in lesson.steps
        for section in step.sections
    ]
