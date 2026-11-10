"""The lesson a writer builds from: its units, and what it may read about each.

A writer reads the plan's own fields and the lesson's approved note, never a note a teacher
left on a plan step: only an approved note is ever read as the lesson's note.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.domains.artefacts.core.domain.parts import Unit
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView

LESSON_UNIT_ID = "lesson"
#: The subjects whose working lines are calculations, by the name they are taught under.
FORMULA_SUBJECTS = frozenset({"mathematics", "further mathematics"})


class LessonUnitsError(ValueError):
    """The lesson has none of the units a spec is written for."""


@dataclass(frozen=True)
class LessonUnit:
    """One thing a part covers, and which kind of unit it is."""

    unit_id: str
    label: str
    unit: Unit


@dataclass(frozen=True)
class LessonFrame:
    """What a draft's units come from: the lesson, and its plan once it has one."""

    title: str
    grade: str
    #: The lesson's curriculum objectives: ``curriculum_objective_id`` and ``objective_text``.
    curriculum_objectives: Sequence[Mapping[str, object]]
    plan: SessionPlanView | None = None
    subject: str = ""

    @property
    def formulas(self) -> bool:
        """Whether the lesson's working is calculation, so each working line is a formula.

        A lesson that names no subject is taken as mathematics, which is what the app was built
        for.
        """
        return not self.subject or self.subject.casefold() in FORMULA_SUBJECTS

    @classmethod
    def of_plan(cls, plan: SessionPlanView) -> LessonFrame:
        return cls(
            title=plan.title or plan.topic or "The lesson",
            grade=plan.grade or "",
            curriculum_objectives=plan.curriculum_objectives,
            plan=plan,
            subject=plan.subject or "",
        )


def _units_of(frame: LessonFrame, unit: Unit) -> tuple[LessonUnit, ...]:
    if unit is Unit.LESSON:
        return (LessonUnit(LESSON_UNIT_ID, frame.title, unit),)
    if unit is Unit.CURRICULUM_OBJECTIVE:
        return tuple(
            LessonUnit(str(o.get("curriculum_objective_id")), str(o.get("objective_text")), unit)
            for o in frame.curriculum_objectives
            if o.get("curriculum_objective_id")
        )
    plan = frame.plan
    if plan is None:
        raise LessonUnitsError(f"a {unit.value.replace('_', ' ')} needs the lesson's plan")
    if unit is Unit.LESSON_OBJECTIVE:
        return tuple(
            LessonUnit(objective.lesson_objective_id, objective.objective_text or "", unit)
            for objective in plan.lesson_plan_objectives
        )
    return tuple(LessonUnit(s.step_id, s.title or s.step_kind, unit) for s in plan.steps)


def lesson_units(frame: LessonFrame, spec: ContentSpecification) -> tuple[LessonUnit, ...]:
    """The units a part is written for, in order: the lesson's own part first, if any."""
    if spec.unit is None:
        raise LessonUnitsError(f"{spec.kind} has no part schema, so it is not drafted")
    units = _units_of(frame, spec.unit)
    if not units:
        raise LessonUnitsError(
            f"the lesson has no {spec.unit.value.replace('_', ' ')}s to write for"
        )
    own = _units_of(frame, Unit.LESSON) if spec.lesson_parts is not None else ()
    ids = [unit.unit_id for unit in (*own, *units)]
    if len(set(ids)) != len(ids):
        raise LessonUnitsError(f"the lesson's units share IDs: {', '.join(ids)}")
    return (*own, *units)


def lesson_material(plan: SessionPlanView, note_sections: Mapping[str, str]) -> JsonObject:
    """Everything a writer may read about a planned lesson, keyed the way units are."""
    objectives = {
        objective.lesson_objective_id: objective.objective_text or ""
        for objective in plan.lesson_plan_objectives
    }
    return {
        "subject": plan.subject or "",
        "grade": plan.grade or "",
        "topic": plan.topic or "",
        "subtopic": plan.subtopic or "",
        "title": plan.title or "",
        "entry_behaviour": list(plan.entry_behaviour),
        "instructional_materials": list(plan.instructional_materials),
        "misconceptions": list(plan.misconceptions),
        "objectives": [
            {"lesson_objective_id": objective_id, "objective": text}
            for objective_id, text in objectives.items()
        ],
        "steps": [
            {
                "step_id": step.step_id,
                "step_kind": step.step_kind,
                "kc_type": step.kc_type,
                "instructional_type": step.instructional_type,
                "lesson_objective_id": step.lesson_objective_id,
                "objective": objectives.get(step.lesson_objective_id or "", ""),
                "title": step.title or "",
                "content": step.content or "",
                "activities": list(step.activities),
                "blocks": [
                    {k: v for k, v in block.items() if k not in ("id", "source_refs")}
                    for block in step.blocks
                ],
                "lesson_note": note_sections.get(step.step_id, ""),
            }
            for step in plan.steps
        ],
        "has_approved_lesson_note": bool(note_sections),
    }
