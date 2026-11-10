"""Which C1 call missed which key, and what in the plan explains the miss.

``cohort_audit`` reports delivery as a ratio per lesson: ``student_tasks 4/17``
says how much of the manipulation arrived and never says where. This reports the
same delivery per **core step**, because the step is the unit a researcher can
carry to a source page and settle.

Delivery is read off the rendered prompt, as it is there — a projection drops a
value it has nothing to put in, so absent and withheld are indistinguishable once
rendered, and only the message says which arrived. The explanation for a miss is
then counted from the plan, so the page states a mechanism rather than a guess.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.session_plan_view import SessionPlanStepView, SessionPlanView
from scripts.prompt_snapshots.arms import _UncallableLM
from scripts.prompt_snapshots.cohort_audit import CONTEXT_FIELDS, MANIPULATION_KEYS, frozen_lessons
from scripts.prompt_snapshots.note_tasks import NoteTask, task_lines
from scripts.prompt_snapshots.rendered import field_blocks, json_value

CORE = "core"
EVALUATION = "evaluation"


def _no_events(step: SessionPlanStepView, _: SessionPlanView) -> str:
    if not step.activities:
        return "the step records no teacher or student activity, so there is nothing to code"
    count = len(step.activities)
    return (
        f"its {count} recorded {'activity' if count == 1 else 'activities'} coded to no Gagné event"
    )


def _no_tasks(step: SessionPlanStepView, _: SessionPlanView) -> str:
    """Both routes failed, so the reason names both."""
    kinds = Counter(str(block.get("type") or "untyped") for block in step.blocks)
    written = ", ".join(f"{count}x {kind}" for kind, count in sorted(kinds.items()))
    student = [
        str(activity.get("what") or "")
        for activity in step.activities
        if str(activity.get("who") or "") == "student"
    ]
    column = (
        f"her Student Activity is {', '.join(repr(a) for a in student)}, which is reception"
        if student
        else "the step records no student activity"
    )
    return (
        f"no block on this step is typed practice "
        f"({written or 'the step has no blocks'}), and {column}"
    )


def _assessed_objectives(plan: SessionPlanView) -> list[str]:
    """The objectives her evaluation questions actually name."""
    return sorted(
        {
            str(block.get("lesson_objective_id") or "")
            for step in plan.steps
            if step.step_kind == EVALUATION
            for block in step.blocks
            if block.get("question") and block.get("lesson_objective_id")
        }
    )


def _no_assessment(step: SessionPlanStepView, plan: SessionPlanView) -> str:
    if not any(other.step_kind == EVALUATION for other in plan.steps):
        return "the lesson has no evaluation step at all"
    named = ", ".join(_assessed_objectives(plan)) or "no objective"
    return f"her evaluation questions name {named}, not this step's {step.lesson_objective_id}"


_WHY_MISSING = {
    "lesson_context.entry_behaviour": lambda step, plan: "the plan records no previous knowledge",
    "lesson_context.instructional_materials": lambda step, plan: (
        "the plan records no instructional materials"
    ),
    "unit_context.current_step": lambda step, plan: "the condition withholds lesson sequence",
    "unit_context.instructional_events": _no_events,
    "unit_context.student_tasks": _no_tasks,
    "unit_context.assessment_points": _no_assessment,
}


@dataclass(frozen=True)
class MissingKey:
    """One key that did not reach one call, and the mechanism behind it."""

    key: str
    reason: str

    @property
    def short(self) -> str:
        return self.key.split(".")[-1]


@dataclass(frozen=True)
class StepDelivery:
    """One core step — which is exactly one C1 call — and what it carried."""

    position: int
    step_id: str
    title: str
    objective_id: str
    objective_text: str
    delivered: tuple[str, ...]
    missing: tuple[MissingKey, ...]
    tasks: tuple[NoteTask, ...]

    @property
    def complete(self) -> bool:
        return not self.missing


@dataclass(frozen=True)
class LessonDelivery:
    """One lesson's calls, in the order the generator makes them."""

    lesson: str
    topic: str
    subtopic: str
    term: str
    week: str
    evaluation_steps: int
    steps: tuple[StepDelivery, ...]

    def carried(self, key: str) -> int:
        return sum(1 for step in self.steps if key in step.delivered)


def _rendered_keys(plan: SessionPlanView) -> dict[str, set[str]]:
    """Per step id, the manipulation keys present in the prompt C1 actually sends."""
    request = BaseReviewPackRequestBuilder().build(
        session_plan=plan,
        policy=profile_for(Hypothesis.H1, ConditionCode.C1).generation_policy(),
        sources=LessonSources.unresolved(plan.references),
    )
    generator = GenerateSection(lm=_UncallableLM())
    present: dict[str, set[str]] = {}
    for unit in request.units:
        blocks = field_blocks(generator.prepared_call(request=request, unit=unit))
        carried: set[str] = set()
        for field in CONTEXT_FIELDS:
            value = json_value(blocks[field]) if field in blocks else {}
            if isinstance(value, dict):
                carried.update(f"{field}.{key}" for key in value)
        present[str(unit.source_step_id)] = carried
    return present


def _step_delivery(
    position: int, step: SessionPlanStepView, plan: SessionPlanView, carried: set[str]
) -> StepDelivery:
    objectives = {
        o.lesson_objective_id: o.objective_text or "" for o in plan.lesson_plan_objectives
    }
    objective_id = step.lesson_objective_id or ""
    return StepDelivery(
        position=position,
        step_id=step.step_id,
        title=step.title or "",
        objective_id=objective_id,
        objective_text=objectives.get(objective_id, ""),
        delivered=tuple(key for key in MANIPULATION_KEYS if key in carried),
        missing=tuple(
            MissingKey(key=key, reason=_WHY_MISSING[key](step, plan))
            for key in MANIPULATION_KEYS
            if key not in carried
        ),
        tasks=tuple(task_lines(step.note or "")),
    )


def lesson_delivery(lesson: str, plan: SessionPlanView) -> LessonDelivery:
    """Every C1 call this lesson makes, with what reached it."""
    carried = _rendered_keys(plan)
    core = [step for step in plan.steps if step.step_kind == CORE]
    return LessonDelivery(
        lesson=lesson,
        topic=plan.topic or "",
        subtopic=plan.subtopic or "",
        term=plan.term or "",
        week=str(plan.week or ""),
        evaluation_steps=sum(1 for step in plan.steps if step.step_kind == EVALUATION),
        steps=tuple(
            _step_delivery(position, step, plan, carried.get(step.step_id, set()))
            for position, step in enumerate(core, start=1)
        ),
    )


def cohort_delivery() -> list[LessonDelivery]:
    """The frozen eval set, lesson by lesson, in its recorded order."""
    return [lesson_delivery(lesson, plan) for lesson, plan in frozen_lessons().items()]
