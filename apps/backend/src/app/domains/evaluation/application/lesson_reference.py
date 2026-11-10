"""The taught lesson as a rater is shown it — built once, rendered three ways.

Taught-lesson alignment is rated against a reference sheet, and there were three
of them: the markdown packet an LLM judge reads, the worksheet PDF, and the
platform's packet drawer. They were assembled by three functions from the same
plan, and each carried a different lesson. The markdown had her previous-knowledge
line, every activity in her words, the work each step set, and her evaluation
questions; the PDF had the activities and not the rest; the drawer had step
titles. A pack's alignment score therefore depended on which surface rated it,
and the LLM passes were scored against material the human endpoint never sees.

This is the one reference. Every surface renders from it, and a test holds that
each rendering carries every item in it, so the media may differ in layout but
not in what lesson they describe.

Her evaluation questions are in it by decision. Assessment is part of how she
planned the lesson, and a rater cannot judge whether a pack's practice matches
her assessment without seeing it. The cost — that a pack can reproduce those
questions verbatim and look aligned for it — is carried by the rubric, which
says that reproduction alone does not establish alignment, and by an overlap
measure recorded beside every candidate rather than hidden from the analysis.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (
    question_as_asked,
)
from app.shared.session_plan_view import SessionPlanStepView, SessionPlanView


@dataclass(frozen=True)
class SequenceStep:
    objective: str
    activities: tuple[str, ...]
    tasks_set: tuple[str, ...]

    def as_line(self) -> str:
        """One string per step, for a surface that lists the sequence flat."""
        parts = [self.objective]
        if self.activities:
            parts.append(" — " + "; ".join(self.activities))
        for task in self.tasks_set:
            parts.append(f". Set for the students: {task}")
        return "".join(parts)


@dataclass(frozen=True)
class LessonReference:
    subject: str | None
    grade: str | None
    term: str | None
    week: int | None
    topic: str | None
    subtopic: str | None
    theme: str | None
    objectives: tuple[str, ...]
    entry_behaviour: tuple[str, ...]
    instructional_materials: tuple[str, ...]
    sequence: tuple[SequenceStep, ...]
    evaluation: tuple[str, ...]

    def items(self) -> tuple[str, ...]:
        """Every content string a rendering must carry, for the surface test."""
        return (
            *self.objectives,
            *self.entry_behaviour,
            *self.instructional_materials,
            *(s.objective for s in self.sequence),
            *(a for s in self.sequence for a in s.activities),
            *(t for s in self.sequence for t in s.tasks_set),
            *self.evaluation,
        )


def lesson_reference(plan: SessionPlanView) -> LessonReference:
    objectives = tuple(
        text for o in plan.lesson_plan_objectives if (text := (o.objective_text or "").strip())
    )
    by_id = {
        o.lesson_objective_id: (o.objective_text or "").strip() for o in plan.lesson_plan_objectives
    }
    return LessonReference(
        subject=plan.subject,
        grade=plan.grade,
        term=plan.term,
        week=plan.week,
        topic=plan.topic,
        subtopic=plan.subtopic,
        theme=plan.theme,
        objectives=objectives,
        entry_behaviour=tuple(item for item in plan.entry_behaviour if item),
        instructional_materials=tuple(item for item in plan.instructional_materials if item),
        sequence=tuple(
            SequenceStep(
                objective=by_id.get(step.lesson_objective_id or "", "")
                or (step.title or "").strip(),
                activities=tuple(_activity_phrases(step)),
                tasks_set=tuple(_practice_questions(step)),
            )
            for step in plan.steps
            if step.step_kind == "core"
        ),
        evaluation=tuple(
            question
            for step in plan.steps
            if step.step_kind == "evaluation"
            for question in _practice_questions(step)
        ),
    )


def reference_sheet(reference: LessonReference) -> dict[str, object]:
    """The payload the platform drawer and the worksheet renderers read."""
    return {
        "subject": reference.subject,
        "grade": reference.grade,
        "term": reference.term,
        "week": reference.week,
        "topic": reference.topic,
        "subtopic": reference.subtopic,
        "theme": reference.theme,
        "curriculum_objectives": list(reference.objectives),
        "entry_behaviour": list(reference.entry_behaviour),
        "lesson_sequence": [step.as_line() for step in reference.sequence],
        "instructional_materials": list(reference.instructional_materials),
        "evaluation": list(reference.evaluation),
    }


def _activity_phrases(step: SessionPlanStepView) -> list[str]:
    """Her activity lines as prose — "the teacher draws the shapes" — never coded."""
    out = []
    for activity in step.activities:
        who = str(activity.get("who") or "").strip()
        what = str(activity.get("what") or "").strip().rstrip(".")
        if who and what:
            out.append(f"the {who} {what}")
    return out


def _practice_questions(step: SessionPlanStepView) -> list[str]:
    return [
        question_as_asked(str(block.get("question")).strip())
        for block in step.blocks
        if isinstance(block, dict) and block.get("type") == "practice" and block.get("question")
    ]
