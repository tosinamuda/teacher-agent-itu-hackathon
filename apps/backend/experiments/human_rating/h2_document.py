"""One Part 2 Evaluation Set: the lesson, then each objective the student has class work for.

An objective runs over five titled pages: what the teacher taught, the student's class
work as the teacher marked it, Material A's section, Material B's section, and the scores.
Only objectives the student has class work for are rated. Which of A and B is which is
fixed by the assignment and appears in the researcher's key, never here.
"""

from __future__ import annotations

from typing import Any

from app.domains.evaluation.domain.study_instrument import H2_CRITERIA

from . import material, reference
from .cover import cover
from .forms import (
    class_work_table,
    closing_comments,
    guide,
    marked_question,
    scoring_body,
)
from .instructions import H2_STEPS, instructions_page
from .layout import PAGE_BREAK, titled_page
from .mapping import H2Assignment
from .sources import Materials, ObjectiveEvidence

PART_TITLE = "Part 2 — Student-specific revision material evaluation"
WELCOME = (
    "You will see two revision materials, Material A and Material B, prepared for one "
    "student after the lesson below, together with the student's marked class work. The "
    "table below shows what that class work demonstrated, objective by objective. For each "
    "rated objective you read what the teacher taught, then the student's class work, then "
    "each material's section, and score the two materials independently. You are not asked "
    "to pick a winner, and neither material is expected to score higher."
)


def class_work_page(evidence: ObjectiveEvidence, objective_text: str, record_id: str) -> list[str]:
    """What the student did for one objective, as the teacher marked it."""
    lines = [
        f"**Learning objective.** {objective_text}  ",
        f"**Class work record.** {record_id}",
        "",
        *guide("Read what this student did for this objective. Nothing is scored on this page."),
        f"**Result on the marked class work.** {evidence.summary}.",
        "",
    ]
    if evidence.recorded_misconception:
        lines += [f"**What the class work showed.** {evidence.recorded_misconception}", ""]
    for number, response in enumerate(evidence.responses, start=1):
        lines += marked_question(
            number,
            question=response.question,
            wrote="<br/>".join((response.working or "").splitlines()),
            expected=response.expected,
            result=response.result,
            interpretation=response.interpretation,
        )
    return lines


def markdown(
    assignment: H2Assignment,
    plan: dict[str, Any],
    materials: Materials,
    evidence: list[ObjectiveEvidence],
) -> str:
    a_sections = materials.p0 if assignment.a == "P0" else materials.p1
    b_sections = materials.p0 if assignment.b == "P0" else materials.p1
    a_by, b_by = material.by_objective(a_sections), material.by_objective(b_sections)
    order = [objective_id for objective_id, _ in reference.objectives(plan)]
    titles = dict(reference.objectives(plan))
    evidence = sorted(evidence, key=lambda item: order.index(item.objective_id))
    rated = [titles.get(item.objective_id, item.objective_id) for item in evidence]
    lines = cover(
        external_id=assignment.external_id,
        part_title=PART_TITLE,
        rater_number=assignment.rater_number,
        plan=plan,
        welcome=WELCOME,
        contents=[
            "Instructions and criteria",
            "The lesson",
            f"the {len(evidence)} objectives the student has class work for, five pages each",
            "Closing comments",
            "The complete Material A and Material B, for context",
        ],
        extra=[
            "### The student's class work, objective by objective",
            "",
            "Only the objectives the student has marked class work for are rated. Each is "
            "shown in full on a page of its own before its scores.",
            "",
            *class_work_table(
                [
                    (text, item.summary, item.recorded_misconception or "—")
                    for text, item in zip(rated, evidence, strict=True)
                ]
            ),
        ],
    )
    lines += [PAGE_BREAK, ""] + instructions_page(H2_STEPS, H2_CRITERIA)
    lines += titled_page("The lesson")
    lines += guide(
        "Read this to see what the lesson taught and in what order. Nothing is scored here."
    )
    lines += reference.lesson_at_a_glance(plan)
    for index, item in enumerate(evidence, start=1):
        text = titles.get(item.objective_id, item.objective_id)
        label = f"Objective {index} of {len(evidence)}"
        lines += titled_page(f"{label} — what the teacher taught")
        lines += [f"**Learning objective.** {text}", ""]
        lines += guide(
            "Read this page, then the student's class work on the page after it. Nothing is "
            "scored here."
        )
        lines += reference.taught_for_objective(plan, item.objective_id)
        lines += titled_page(f"{label} — the student's class work")
        lines += class_work_page(item, text, assignment.learner_card_id)
        for name, grouped, ident in (
            ("A", a_by, assignment.a_id),
            ("B", b_by, assignment.b_id),
        ):
            lines += titled_page(f"{label} — Material {name}")
            lines += [
                f"**Learning objective.** {text}  ",
                f"**Topic.** {plan.get('topic')} — {plan.get('subtopic')} *({ident})*",
                "",
            ]
            lines += guide(
                f"This is Material {name}'s section for this objective. Score it with the "
                "other material on the scoring page."
            )
            for section in grouped.get(item.objective_id, []):
                lines += material.one(section, level=3)
            if not grouped.get(item.objective_id):
                lines += [f"*Material {name} has no section for this objective.*", ""]
        named = " and ".join(
            f"Material {name}\u2019s section"
            for name, grouped in (("A", a_by), ("B", b_by))
            if grouped.get(item.objective_id)
        )
        lines += titled_page(f"{label} — your scores")
        lines += scoring_body(
            H2_CRITERIA,
            ("Material A", "Material B"),
            tag=str(index),
            objective=text,
            subject=(
                f"{named} for this objective, on the pages before this one."
                if named
                else "Neither material has a section for this objective."
            ),
            instruction=(
                "Score each material's section for this objective independently, using the "
                "descriptions below."
            ),
        )
    lines += titled_page("Closing comments")
    lines += closing_comments(
        f"You should have given {len(rated) * len(H2_CRITERIA) * 2} scores in all: "
        f"{len(H2_CRITERIA)} criteria for each of Material A and Material B, "
        f"for each of the {len(rated)} rated objectives."
    )
    for label, sections, ident in (
        ("A", a_sections, assignment.a_id),
        ("B", b_sections, assignment.b_id),
    ):
        lines += titled_page(f"The complete Material {label} *({ident})*")
        lines += guide(
            "For context only. You have already scored the sections the student has class "
            "work for; the rest are not rated."
        )
        lines += reference.material_header(plan)
        lines += material.whole(sections, level=3)
        lines.append("")
    return "\n".join(lines)
