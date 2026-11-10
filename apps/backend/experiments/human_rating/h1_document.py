"""One Part 1 Evaluation Set: the lesson, then every objective taught, read and scored.

An objective is three pages, each titled by the objective it belongs to and by the job of
that page. What the teacher taught comes first, the revision material for that objective
stands alone on the page after it, and the scores go on the page after that. The material
is printed once: its sections are the objectives' sections, in the order the material
itself sets, so those pages read straight through are the whole material. Nothing names
the condition or the draw; the set id is the only identifier, and it is the external one.
"""

from __future__ import annotations

from typing import Any

from app.domains.evaluation.domain.study_instrument import H1_CRITERIA

from . import material, reference
from .cover import cover
from .forms import closing_comments, guide, scoring_body
from .instructions import H1_STEPS, instructions_page
from .layout import PAGE_BREAK, titled_page
from .mapping import H1Assignment

PART_TITLE = "Part 1 — Class revision material evaluation"
WELCOME = (
    "You will see one revision material prepared for a mathematics class after the lesson "
    "below. Each learning objective is taken in turn over three pages: what the teacher "
    "taught for it, the part of the revision material that addresses it, and your scores. "
    "Score every objective on its own; there is no overall score for the whole material, "
    "and you are not asked how the material was made."
)


def markdown(assignment: H1Assignment, plan: dict[str, Any], sections: list[dict[str, Any]]) -> str:
    grouped = material.by_objective(sections)
    objectives = reference.objectives(plan)
    total = len(objectives)
    lines = cover(
        external_id=assignment.external_id,
        part_title=PART_TITLE,
        rater_number=assignment.rater_number,
        plan=plan,
        welcome=WELCOME,
        contents=[
            "Instructions and criteria",
            "The lesson",
            f"the {total} learning objectives, each taught, read and scored over three pages",
            "Closing comments",
        ],
    )
    lines += [PAGE_BREAK, ""] + instructions_page(H1_STEPS, H1_CRITERIA)
    lines += titled_page("The lesson")
    lines += guide(
        "Read this to see what the lesson taught and in what order. Nothing is scored here."
    )
    lines += reference.lesson_at_a_glance(plan)
    for index, (objective_id, text) in enumerate(objectives, start=1):
        label = f"Objective {index} of {total}"
        lines += titled_page(f"{label} — what the teacher taught")
        lines += [f"**Learning objective.** {text}", ""]
        lines += guide(
            "Read this page, then the revision material for this objective on the next page."
        )
        lines += reference.taught_for_objective(plan, objective_id)
        lines += titled_page(f"{label} — the revision material")
        lines += [
            f"**Learning objective.** {text}  ",
            f"**Topic.** {plan.get('topic')} — {plan.get('subtopic')}",
            "",
        ]
        lines += guide(
            "This is the part of the revision material that addresses this objective. "
            "Score it on the next page."
        )
        for section in grouped.get(objective_id, []):
            lines += material.one(section, level=3)
        if not grouped.get(objective_id):
            lines += ["*The material has no section for this objective.*", ""]
        titles = [str(s.get("title") or "").strip() for s in grouped.get(objective_id, [])]
        named = ", ".join(f"\u201c{t}\u201d" for t in titles if t)
        lines += titled_page(f"{label} — your scores")
        lines += scoring_body(
            H1_CRITERIA,
            ("Your",),
            tag=str(index),
            objective=text,
            subject=(
                f"The revision material's section for this objective, {named}, on the page "
                "before this one."
                if named
                else "The revision material, which has no section for this objective."
            ),
            instruction=(
                "Score the revision material's section for this objective only, using the "
                "descriptions below."
            ),
        )
    lines += titled_page("Closing comments")
    lines += closing_comments(
        f"You should have given {total * len(H1_CRITERIA)} scores in all: "
        f"{len(H1_CRITERIA)} criteria for each of the {total} learning objectives."
    )
    return "\n".join(lines)
