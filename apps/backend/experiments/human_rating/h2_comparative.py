"""One Part 2 Evaluation Set under the comparative instrument.

An objective runs over four pages: what the teacher taught, the student's class work,
the two materials set side by side, and the comparison. The side-by-side page is the
point of this variant. A rater who reads one material and then the other weighs the
second against a memory of the first, which means weighing it against a private standard
that does not hold steady; read in columns, the comparison is made by looking.

The comparison pages are cut landscape, where a column is wider than the drawings in it,
so nothing is shrunk to be set beside anything else. Which of A and B is which is fixed
by the assignment and appears in the researcher's key, never here.
"""

from __future__ import annotations

from typing import Any

from app.domains.evaluation.domain.study_instrument import H2_CRITERIA

from . import material, reference
from .cover import cover
from .forms import class_work_table, closing_comments, comparison_body, guide, side_by_side
from .h2_document import PART_TITLE, class_work_page
from .instructions import comparison_instructions_page
from .layout import LANDSCAPE, PAGE_BREAK, PORTRAIT, shaped_page, titled_page
from .mapping import H2Assignment
from .sources import Materials, ObjectiveEvidence

WELCOME = (
    "You will see two revision materials, Material A and Material B, prepared for one "
    "student after the lesson below, together with the student's marked class work. The "
    "table below shows what that class work demonstrated, objective by objective. For each "
    "compared objective you read what the teacher taught, then the student's class work, "
    "then the two materials side by side, and mark which one is stronger on each criterion. "
    "Neither material is expected to win, and “about the same” is a real answer."
)


def _class_work_rows(
    rated: list[str], evidence: list[ObjectiveEvidence]
) -> list[tuple[str, str, str]]:
    return [
        (text, item.summary, item.recorded_misconception or "—")
        for text, item in zip(rated, evidence, strict=True)
    ]


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
            f"the {len(evidence)} objectives the student has class work for, four pages each",
            "Closing comments",
            "The complete Material A and Material B, for context",
        ],
        extra=[
            "### The student's class work, objective by objective",
            "",
            "Only the objectives the student has marked class work for are compared. Each is "
            "shown in full on a page of its own before the two materials.",
            "",
            *class_work_table(_class_work_rows(rated, evidence)),
        ],
    )
    lines += [PAGE_BREAK, ""] + comparison_instructions_page(H2_CRITERIA)
    lines += titled_page("The lesson")
    lines += guide(
        "Read this to see what the lesson taught and in what order. Nothing is compared here."
    )
    lines += reference.lesson_at_a_glance(plan)

    for index, item in enumerate(evidence, start=1):
        text = titles.get(item.objective_id, item.objective_id)
        label = f"Objective {index} of {len(evidence)}"
        taught = f"{label} — what the teacher taught"
        lines += titled_page(taught) if index == 1 else shaped_page(taught, PORTRAIT)
        lines += [f"**Learning objective.** {text}", ""]
        lines += guide(
            "Read this page, then the student's class work on the page after it. Nothing is "
            "compared here."
        )
        lines += reference.taught_for_objective(plan, item.objective_id)

        lines += titled_page(f"{label} — the student's class work")
        lines += class_work_page(item, text, assignment.learner_card_id)

        lines += shaped_page(f"{label} — the two materials", LANDSCAPE)
        lines += [
            f"**Learning objective.** {text}  ",
            f"**Topic.** {plan.get('topic')} — {plan.get('subtopic')}",
            "",
        ]
        lines += guide(
            "Read both columns before you decide anything. The comparison page follows "
            "this material."
        )
        lines += side_by_side(
            _rows(a_by, b_by, item.objective_id),
            (f"Material A *({assignment.a_id})*", f"Material B *({assignment.b_id})*"),
            tag=str(index),
        )

        lines += titled_page(f"{label} — your comparison")
        lines += comparison_body(
            H2_CRITERIA,
            tag=str(index),
            objective=text,
            subject=(
                "Material A and Material B for this objective, side by side on the page "
                "before this one."
            ),
        )

    lines += shaped_page("Closing comments", PORTRAIT)
    lines += closing_comments(
        f"You should have made {len(rated) * len(H2_CRITERIA)} marks in all: one on each of "
        f"the {len(H2_CRITERIA)} criteria, for each of the {len(rated)} compared objectives.",
        given="Your marks are on the comparison pages",
    )
    for label, sections, ident in (
        ("A", a_sections, assignment.a_id),
        ("B", b_sections, assignment.b_id),
    ):
        lines += titled_page(f"The complete Material {label} *({ident})*")
        lines += guide(
            "For context only. You have already compared the objectives the student has "
            "class work for; the rest are not compared."
        )
        lines += reference.material_header(plan)
        lines += material.whole(sections, level=3)
        lines.append("")
    return "\n".join(lines)


def _rows(
    a_by: dict[str, list], b_by: dict[str, list], objective_id: str
) -> list[tuple[list[str], list[str]]]:
    """The two materials for one objective, part against corresponding part."""
    left, right = _parts(a_by, objective_id, "A"), _parts(b_by, objective_id, "B")
    height = max(len(left), len(right))
    pad = [[] for _ in range(height)]
    return list(zip((left + pad)[:height], (right + pad)[:height], strict=True))


def _parts(grouped: dict[str, list], objective_id: str, name: str) -> list[list[str]]:
    sections = grouped.get(objective_id) or []
    if not sections:
        return [[f"*Material {name} has no section for this objective.*"]]
    return [part for section in sections for part in material.parts(section)]
