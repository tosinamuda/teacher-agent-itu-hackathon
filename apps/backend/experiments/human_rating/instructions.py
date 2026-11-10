"""What a rater is told, in the words of the Research Assistant Guide.

Nothing here says how a material was produced, names a condition, or hints that one
material is expected to score higher than another. Raters learn that after the study.
"""

from __future__ import annotations

from app.domains.evaluation.domain.study_instrument import COMPARISON, SCALE, Criterion

from .forms import CHOSEN, comparison_example, criteria_reference, rubric_matrix

STUDY_LINE = (
    "This research evaluates mathematics revision materials intended for students to use "
    "after completing a classroom lesson."
)

H1_STEPS: tuple[str, ...] = (
    "Read the lesson page to see what the lesson taught and in what order.",
    "Read the revision material pages straight through once. Together they are the "
    "complete revision material, in its own order.",
    "Then take the learning objectives one at a time. Read what the teacher taught for "
    "that objective, then the revision material page for it.",
    "On the scoring page that follows, give three independent scores using the criteria "
    "printed there, and add any comment that explains a score.",
    "Repeat for every learning objective. There is no overall score for the whole material.",
    "Add any general comments on the last page. Your scores stay where you gave them.",
)

H2_STEPS: tuple[str, ...] = (
    "Read the lesson page to see what the lesson taught and in what order.",
    "Take the learning objectives the student has class work for, one at a time. For each, "
    "read what the teacher taught, then the student's class work, then Material A's "
    "section and Material B's section.",
    "Score Material A independently on the three criteria, then Material B independently on "
    "the same three criteria. A and B may receive identical scores.",
    "Do not choose a winner between A and B, and do not assume that one must score higher.",
    "The complete Material A and Material B follow the rated objectives, for context. They "
    "include sections the student has no class work for, which are not rated.",
    "Add any general comments on the last page. Your scores stay where you gave them.",
)

#: The same reading, ending in one comparison rather than two independent scores.
H2_COMPARISON_STEPS: tuple[str, ...] = (
    "Read the lesson page to see what the lesson taught and in what order.",
    "Take the learning objectives the student has class work for, one at a time. For each, "
    "read what the teacher taught, then the student's class work.",
    "Then read Material A and Material B, which are set out side by side on one page. Read "
    "both of them before you decide anything.",
    f"On the comparison page, write {CHOSEN} in one box on each of the three rows, and "
    "nothing in the other four: which material is stronger on that criterion, and by how much.",
    "\u201cAbout the same\u201d is a real answer. Both materials can be good, or both weak, on "
    "a criterion \u2014 mark the middle whenever neither is clearly ahead.",
    "The complete Material A and Material B follow the compared objectives, for context. "
    "They include sections the student has no class work for, which are not compared.",
    "Add any general comments on the last page. Your marks stay where you made them.",
)

DO: tuple[str, ...] = (
    "Use the supplied rating criteria.",
    "Make your own professional judgement.",
    "Complete every required field.",
    "Use the information provided in each Evaluation Set.",
)

DO_NOT: tuple[str, ...] = (
    "Discuss your ratings with other raters.",
    "Look for a preferred answer.",
    "Allow another person's judgement to influence yours.",
    "Ask the research assistant what score to give.",
)


def scale_line() -> str:
    scale = "; ".join(f"**{score}** — {meaning}" for score, meaning in SCALE)
    return f"**The scale.** Each criterion is scored 1 to 5, independently: {scale}."


def comparison_scale_line() -> str:
    points = ", ".join(f"*{point}*" for point in COMPARISON)
    return (
        "**The scale.** Each criterion is marked once, on a five-point row: "
        f"{points}. You are not scoring either material on its own."
    )


def comparison_instructions_page(criteria: tuple[Criterion, ...]) -> list[str]:
    """What to do and what each criterion asks, on the one page after the cover."""
    lines = ["## Instructions", "", "**What to do.**", ""]
    lines += [f"{i}. {step}" for i, step in enumerate(H2_COMPARISON_STEPS, start=1)]
    lines += ["", comparison_scale_line(), ""]
    lines += ["**What an answered row looks like.** The three shown are illustrations only.", ""]
    lines += comparison_example()
    lines += ["**The criteria.**", ""]
    lines += criteria_reference(criteria)
    guidance = [
        f"- *{n}. {c.name}.* " + " ".join(c.notes)
        for n, c in enumerate(criteria, start=1)
        if c.notes
    ]
    if guidance:
        lines += ["**Guidance.**", "", *guidance, ""]
    return lines


def instructions_page(steps: tuple[str, ...], criteria: tuple[Criterion, ...]) -> list[str]:
    """What to do, the scale, and the whole instrument, on the one page after the cover."""
    lines = ["## Instructions", "", "**What to do.**", ""]
    lines += [f"{i}. {step}" for i, step in enumerate(steps, start=1)]
    lines += ["", scale_line(), ""]
    lines += ["**The criteria.** Give each criterion the score whose description fits best:", ""]
    lines += rubric_matrix(criteria)
    guidance = [
        f"- *{n}. {c.name}.* " + " ".join(c.notes)
        for n, c in enumerate(criteria, start=1)
        if c.notes
    ]
    if guidance:
        lines += ["**Guidance.**", "", *guidance, ""]
    return lines


def general_instructions_markdown(rater_number: int) -> str:
    lines = [
        "# General instructions for raters",
        "",
        f"**Rater {rater_number}**",
        "",
        "Thank you for participating in this research. " + STUDY_LINE,
        "",
        "## Part 1: Class revision material evaluation",
        "",
        "You will evaluate revision materials intended for a mathematics class. For each "
        "Evaluation Set:",
        "",
    ]
    lines += [f"{i}. {step}" for i, step in enumerate(H1_STEPS, start=1)]
    lines += [
        "",
        "Evaluate each material independently.",
        "",
        "## Part 2: Student-specific revision material evaluation",
        "",
        "You will compare two revision materials for an individual student. Each Evaluation "
        "Set contains the student's marked class work, Material A, and Material B, set out "
        "side by side. For each Evaluation Set:",
        "",
    ]
    lines += [f"{i}. {step}" for i, step in enumerate(H2_COMPARISON_STEPS, start=1)]
    lines += ["", "## Please", ""] + [f"- {item}" for item in DO]
    lines += ["", "## Please do not", ""] + [f"- {item}" for item in DO_NOT]
    lines += [
        "",
        "**There is no preferred score or expected result.**",
        "",
        "If you are unsure where to enter a response, ask the research assistant for assistance.",
        "",
    ]
    return "\n".join(lines)
