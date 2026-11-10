"""The lesson as the teacher planned it, for a human rater.

Two views of one plan. The *common* reference is the whole lesson once per set. The
*objective-linked* reference is the part of the plan that treats one objective — its
step, the teacher's and learners' activities, the work set in class and the evaluation
questions that assess it — so a rater scoring that objective is not searching a long
plan for the relevant lines. The protocol asks for both.

Everything is in the teacher's words. The vocabulary is "teacher-planned": nothing here
claims to know what happened in the room.
"""

from __future__ import annotations

import re
from typing import Any

from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    question_as_asked,
)

from .forms import step_table
from .layout import RULE
from .sources import typesettable


def objectives(plan: dict[str, Any]) -> list[tuple[str, str]]:
    return [(o["lesson_objective_id"], o["objective_text"]) for o in plan["lesson_plan_objectives"]]


def lesson_reference_rows(plan: dict[str, Any]) -> list[tuple[str, str | list[str]]]:
    """The cover's key–value table: what the lesson is, and what it set out to teach."""
    return [
        ("Subject", _text(plan.get("subject"))),
        ("Class", _text(plan.get("grade"))),
        ("Term", _text(plan.get("term"))),
        ("Week", _text(plan.get("week"))),
        ("Topic", _text(plan.get("topic"))),
        ("Subtopic", _text(plan.get("subtopic"))),
        (
            "Curriculum target",
            [o["objective_text"] for o in plan.get("curriculum_objectives") or []],
        ),
    ]


def material_header(plan: dict[str, Any]) -> list[str]:
    """What a material is about, at the head of the material: topic, class, subject, week."""
    return [
        f"**Topic:** {_text(plan.get('topic'))} — {_text(plan.get('subtopic'))}  ",
        f"**Class:** {_text(plan.get('grade'))} · **Subject:** {_text(plan.get('subject'))} · "
        f"**Term:** {_text(plan.get('term'))} · **Week:** {_text(plan.get('week'))}",
        "",
        RULE,
        "",
    ]


def _text(value: Any) -> str:
    return str(value) if value not in (None, "") else "—"


def lesson_at_a_glance(plan: dict[str, Any]) -> list[str]:
    """The lesson's shape: what came before it, what it used, and the order of its steps.

    Only what the per-objective blocks cannot give. The narration, the activities and the
    evaluation questions live beside the material they are judged against, not here.
    """
    lines = []
    if plan.get("entry_behaviour"):
        lines += [
            "**Previous knowledge.** Students had been taught: "
            + "; ".join(item.rstrip(".") for item in plan["entry_behaviour"])
            + ".",
            "",
        ]
    if plan.get("instructional_materials"):
        lines += [
            "**Instructional materials.** " + "; ".join(plan["instructional_materials"]),
            "",
        ]
    numbers = {oid: n for n, (oid, _) in enumerate(objectives(plan), start=1)}
    texts = dict(objectives(plan))
    rows = [
        (
            str(step["title"]).strip(),
            _what_happened(step),
            f"Objective {numbers[step['lesson_objective_id']]}: "
            f"{texts[step['lesson_objective_id']]}",
        )
        for step in _core_steps(plan)
        if step.get("lesson_objective_id") in numbers
    ]
    return lines + ["**The lesson in order.**", "", *step_table(rows)]


#: A step titled only "Step 1" or "Step II" says nothing on its own.
_BARE_TITLE = re.compile(r"^Step\s+[0-9IVXivx]+\s*[—–-]?\s*", re.I)


def _what_happened(step: dict[str, Any]) -> str:
    """What the step was about: the teacher's own title where it says something, else what
    the teacher did in it."""
    topic = _BARE_TITLE.sub("", str(step.get("title") or "")).strip()
    if topic:
        return topic
    narration = _narration(step).strip()
    return re.split(r"(?<=[.!?])\s", narration)[0] if narration else "—"


def taught_for_objective(plan: dict[str, Any], objective_id: str) -> list[str]:
    """Everything the teacher intended and taught for one objective, in one block.

    The plan says what was meant to happen and the teacher's note says what was taught in
    it; a rater judging emphasis, methods, representations or examples needs both, and
    needs them here rather than in two places.
    """
    lines = []
    curriculum = next(
        (
            o.get("curriculum_objective_text")
            for o in plan["lesson_plan_objectives"]
            if o["lesson_objective_id"] == objective_id
        ),
        None,
    )
    if curriculum:
        lines += [f"*Curriculum target:* {curriculum}", ""]
    steps = [s for s in _core_steps(plan) if s.get("lesson_objective_id") == objective_id]
    if not steps:
        lines += ["*The plan has no step dedicated to this objective.*", ""]
    for step in steps:
        lines += [f"*In the lesson — {step['title']}.* {_narration(step)}", ""]
        activities = step.get("activities") or []
        if activities:
            lines += [f"- The {a['who']} {a['what'].rstrip('.')}." for a in activities] + [""]
        note = (step.get("note") or "").strip()
        if note:
            lines += [
                "*What the teacher's note taught here:*",
                "",
                typesettable(note),
                "",
            ]
        tasks = _tasks(step)
        if tasks:
            # Not a list: a task's own text often carries its numbering, and a numbered
            # line inside a bullet renders as an empty bullet over a nested list.
            lines += ["*Work set in class:*", ""]
            for task in tasks:
                lines += [typesettable(task), ""]
    questions = [q for oid, q in _evaluation_items(plan) if oid == objective_id]
    if questions:
        lines += ["*Evaluation questions for this objective:*", ""]
        lines += [f"{i}. {typesettable(_indent(q))}" for i, q in enumerate(questions, 1)] + [""]
    return lines


def _core_steps(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [s for s in plan["steps"] if s.get("step_kind") == "core"]


def _narration(step: dict[str, Any]) -> str:
    return " ".join(str(step.get("content") or "").split())


def _tasks(step: dict[str, Any]) -> list[str]:
    return [
        question_as_asked(str(b["question"]).strip())
        for b in step.get("blocks") or []
        if b.get("type") == "practice" and b.get("question")
    ]


def _evaluation_items(plan: dict[str, Any]) -> list[tuple[str, str]]:
    return [
        (str(b.get("lesson_objective_id") or ""), question_as_asked(str(b["question"]).strip()))
        for s in plan["steps"]
        if s.get("step_kind") == "evaluation"
        for b in s.get("blocks") or []
        if b.get("type") == "practice" and b.get("question")
    ]


def _indent(text: str) -> str:
    """A multi-line item stays inside its list entry when rendered."""
    return text.replace("\n", "\n   ")
