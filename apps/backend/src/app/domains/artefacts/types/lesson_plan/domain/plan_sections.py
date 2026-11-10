"""A lesson plan written in sections: one for the lesson, one for each curriculum objective.

Each curriculum objective's section holds the lesson objectives that teach it, each with its
core step and the questions that check it at the end. Putting the sections together makes
the plan: every ID, and every link between an objective and the steps that teach and check
it, comes from where a part sits, so a writer never types one. A check on the plan names
the section and the place in it that a finding is about. Splitting a plan gives its sections
back, so a plan that exists can be reopened to be revised.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from app.shared.json_types import JsonObject, JsonValue

#: The fields of the lesson's own part that the plan carries as they are.
LESSON_FIELDS = (
    "theme",
    "entry_behaviour",
    "instructional_materials",
    "misconceptions",
    "references",
    "assessments",
)
_STEP_FIELDS = ("title", "content", "estimated_minutes", "activities")
_OBJECTIVE_FIELDS = ("kc_type", "kc_focus", "source_form", "target_form")

LESSON_SECTION = "lesson"


@dataclass(frozen=True)
class ObjectiveSection:
    """One curriculum objective's section: its ID, its text, and its part so far."""

    curriculum_objective_id: str
    objective_text: str
    part: JsonObject


@dataclass
class PlanPlaces:
    """Where each part of the plan was written: a section, and a path inside its part."""

    steps: dict[str, tuple[str, str, str]] = field(default_factory=dict)
    blocks: dict[tuple[str, int], tuple[str, str]] = field(default_factory=dict)
    objectives: dict[str, tuple[str, str]] = field(default_factory=dict)

    def locate(self, path: Sequence[object]) -> str:
        """The section and place a path into the plan points at."""
        head, rest = (str(path[0]), list(path[1:])) if path else ("", [])
        if head == "steps" and rest and (step := self.steps.get(str(rest[0]))):
            step_id, section, where = step
            rest = rest[1:]
            if len(rest) > 1 and rest[0] == "blocks" and str(rest[1]).isdigit():
                block = self.blocks.get((step_id, int(str(rest[1]))))
                if block is not None:
                    (section, where), rest = block, rest[2:]
            return _place(section, where, rest)
        if head == "lesson_plan_objectives":
            place = self.objectives.get(str(rest[0])) if rest else None
            if place is None:
                return "the curriculum objective parts, at lesson_objectives"
            return _place(*place, rest[1:])
        return _place(LESSON_SECTION, "", [head, *rest] if head else [])


def _place(section: str, where: str, rest: Sequence[object]) -> str:
    inside = ".".join(part for part in (where, *(str(r) for r in rest)) if part)
    return f"the {section} part, at {inside}" if inside else f"the {section} part"


@dataclass(frozen=True)
class AssembledPlan:
    content: JsonObject
    places: PlanPlaces


def _activity(activity: JsonObject) -> JsonObject:
    """An activity as the plan holds it: only a student's says whether it sets work."""
    if activity.get("who") == "teacher":
        return {name: value for name, value in activity.items() if name != "sets_work"}
    return activity


def _object(value: JsonValue) -> JsonObject:
    return value if isinstance(value, dict) else {}


def _objects(value: JsonValue) -> list[JsonObject]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


class _Assembly:
    """One pass that builds the plan and records where each piece came from."""

    def __init__(self) -> None:
        self.places = PlanPlaces()
        self.objectives: list[JsonObject] = []
        self.core_steps: list[JsonObject] = []
        self.checks: list[tuple[JsonObject, str, str]] = []

    def step(
        self, step_id: str, kind: str, source: JsonObject, section: str, where: str
    ) -> JsonObject:
        step: JsonObject = {"step_id": step_id, "step_kind": kind}
        step |= {name: source[name] for name in _STEP_FIELDS if name in source}
        step["activities"] = [_activity(item) for item in _objects(source.get("activities"))]
        step["blocks"] = [
            self.block(step_id, index, entry, section, f"{where}.blocks.{index}")
            for index, entry in enumerate(_objects(source.get("blocks")))
        ]
        self.places.steps[step_id] = (step_id, section, where)
        return step

    def block(
        self, step_id: str, index: int, entry: JsonObject, section: str, where: str
    ) -> JsonObject:
        self.places.blocks[(step_id, index)] = (section, where)
        fields = {name: value for name, value in entry.items() if name != "kind"}
        return {"id": f"{step_id}-b{index + 1}", "type": entry.get("kind"), **fields}

    def objective(self, section: ObjectiveSection, index: int, entry: JsonObject) -> None:
        number = len(self.objectives) + 1
        objective_id, where = f"lo{number}", f"lesson_objectives.{index}"
        objective: JsonObject = {
            "lesson_objective_id": objective_id,
            "objective_order": number,
            "curriculum_objective_id": section.curriculum_objective_id,
            "curriculum_objective_text": section.objective_text,
        }
        if "objective" in entry:
            objective["objective_text"] = entry["objective"]
        objective |= {name: entry[name] for name in _OBJECTIVE_FIELDS if name in entry}
        self.objectives.append(objective)
        self.places.objectives[objective_id] = (section.curriculum_objective_id, where)
        self.places.objectives[str(number - 1)] = (section.curriculum_objective_id, where)
        self.core(objective, _object(entry.get("core_step")), section, where)
        for position, question in enumerate(_objects(entry.get("check_questions"))):
            self.checks.append(
                (
                    {**question, "lesson_objective_id": objective_id},
                    section.curriculum_objective_id,
                    f"{where}.check_questions.{position}",
                )
            )

    def core(
        self, objective: JsonObject, source: JsonObject, section: ObjectiveSection, where: str
    ) -> None:
        step_id = f"core{len(self.core_steps) + 1}"
        step = self.step(
            step_id, "core", source, section.curriculum_objective_id, f"{where}.core_step"
        )
        step["lesson_objective_id"] = objective["lesson_objective_id"]
        step["kc_type"] = objective.get("kc_type")
        step["instructional_type"] = instructional_type(step["blocks"])
        self.core_steps.append(step)

    def evaluation(self, source: JsonObject) -> JsonObject:
        step = self.step("evaluation", "evaluation", source, LESSON_SECTION, "evaluation")
        step["instructional_type"] = "check"
        step["blocks"] = [
            self.block("evaluation", index, {"kind": "practice", **question}, section, where)
            for index, (question, section, where) in enumerate(self.checks)
        ]
        return step


def instructional_type(blocks: JsonValue) -> str:
    """How a core step teaches, as its blocks show it."""
    kinds = {block.get("type") for block in _objects(blocks)}
    if "worked_example" in kinds:
        return "explain_example_practice"
    return "explain_practice" if "practice" in kinds else "explain_only"


def assemble_plan(lesson: JsonObject | None, sections: Sequence[ObjectiveSection]) -> AssembledPlan:
    """The plan the sections written so far make, and where each part of it was written."""
    assembly = _Assembly()
    for section in sections:
        for index, entry in enumerate(_objects(section.part.get("lesson_objectives"))):
            assembly.objective(section, index, entry)
    steps: list[JsonObject] = []
    content: JsonObject = {"lesson_plan_objectives": [*assembly.objectives]}
    if lesson is not None:
        content |= {name: lesson[name] for name in LESSON_FIELDS if name in lesson}
        steps.append(
            assembly.step("intro", "intro", _object(lesson.get("intro")), LESSON_SECTION, "intro")
        )
    steps.extend(assembly.core_steps)
    if lesson is not None:
        steps.append(assembly.evaluation(_object(lesson.get("evaluation"))))
    content["steps"] = [*steps]
    for index, step in enumerate(steps):
        assembly.places.steps[str(index)] = assembly.places.steps[str(step["step_id"])]
    return AssembledPlan(content, assembly.places)


def issue_lines(issues: JsonObject, places: PlanPlaces) -> list[str]:
    """Each finding of a check on the plan, said as where in which section it is."""
    lines: list[str] = []
    for check, found in issues.items():
        entries = found if isinstance(found, list) else [found]
        lines.extend(_line(check, entry, places) for entry in entries)
    return list(dict.fromkeys(lines))


def _line(check: str, entry: JsonValue, places: PlanPlaces) -> str:
    if isinstance(entry, dict):
        path = entry.get("path")
        if isinstance(path, list):
            return f"{places.locate(path)}: {entry.get('message')}"
        return f"{check}: {entry}"
    text = str(entry)
    dotted, colon, message = text.partition(": ")
    if colon and " " not in dotted:
        return f"{places.locate(dotted.split('.'))}: {message}"
    return f"{check}: {text}"


_ENTRY_FIELDS = ("objective_text", *_OBJECTIVE_FIELDS)
#: The kinds of block a part is written with; a plan may hold others, such as a figure.
PART_BLOCK_KINDS = ("explanation", "worked_example", "practice")
#: What a stored block carries that a part does not hold: its identity, and where it is grounded.
_BLOCK_ONLY = ("id", "type", "kind", "source_refs", "lesson_objective_id")


def _clean(value: JsonValue) -> JsonValue:
    """The value without the empty fields a part leaves out, where it is a list or a mapping."""
    if isinstance(value, dict):
        kept = {name: _clean(item) for name, item in value.items()}
        return {name: item for name, item in kept.items() if item not in (None, "", [], {})}
    if isinstance(value, list):
        return [_clean(item) for item in value]
    return value


def _part_block(block: JsonObject) -> JsonObject:
    """A plan's block as a part writes it: its kind, and the fields a part holds."""
    fields = {name: value for name, value in block.items() if name not in _BLOCK_ONLY}
    return {"kind": block.get("type"), **fields}


def _part_blocks(step: JsonObject) -> list[JsonValue]:
    return [
        _part_block(block)
        for block in _objects(step.get("blocks"))
        if block.get("type") in PART_BLOCK_KINDS
    ]


def _activities(step: JsonObject) -> list[JsonValue]:
    """A step's activities in order; an older plan's lists are the teacher's, then the students'."""
    if "activities" in step:
        return step["activities"] if isinstance(step["activities"], list) else []
    return [
        {"who": who, "what": text}
        for who in ("teacher", "student")
        for text in _strings(step.get(f"{who}_activities"))
    ]


def _strings(value: JsonValue) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _part_step(step: JsonObject, *, with_blocks: bool) -> JsonObject:
    part = {name: step[name] for name in _STEP_FIELDS if name in step}
    part["activities"] = _activities(step)
    if with_blocks:
        part["blocks"] = _part_blocks(step)
    return _object(_clean(part))


def _check_questions(evaluation: JsonObject, objective_id: str) -> list[JsonValue]:
    return [
        {name: value for name, value in _part_block(block).items() if name != "kind"}
        for block in _objects(evaluation.get("blocks"))
        if block.get("lesson_objective_id") == objective_id
    ]


def split_plan(plan: JsonObject) -> tuple[JsonObject, dict[str, JsonObject]]:
    """A plan's lesson part, and each curriculum objective's part by its ID.

    The inverse of ``assemble_plan``. A step the plan lacks leaves its part out, and a
    curriculum objective that no lesson objective teaches has an empty list of them.
    """
    steps = _objects(plan.get("steps"))
    by_kind = {str(step.get("step_kind")): step for step in steps}
    core = {
        step.get("lesson_objective_id"): step for step in steps if step.get("step_kind") == "core"
    }
    evaluation = by_kind.get("evaluation", {})
    lesson: JsonObject = _object(
        _clean({name: plan[name] for name in LESSON_FIELDS if name in plan})
    )
    if "intro" in by_kind:
        lesson["intro"] = _part_step(by_kind["intro"], with_blocks=True)
    if evaluation:
        lesson["evaluation"] = _part_step(evaluation, with_blocks=False)
    entries: dict[str, list[JsonValue]] = {
        str(objective.get("curriculum_objective_id")): []
        for objective in _objects(plan.get("curriculum_objectives"))
    }
    for objective in _objects(plan.get("lesson_plan_objectives")):
        objective_id = str(objective.get("lesson_objective_id"))
        entry: JsonObject = {name: objective[name] for name in _ENTRY_FIELDS if name in objective}
        entry["objective"] = entry.pop("objective_text", "")
        entry["core_step"] = _part_step(core.get(objective_id, {}), with_blocks=True)
        entry["check_questions"] = _check_questions(evaluation, objective_id)
        entry = _object(_clean(entry))
        entries.setdefault(str(objective.get("curriculum_objective_id")), []).append(entry)
    return lesson, {unit: {"lesson_objectives": found} for unit, found in entries.items()}


def _step_key(step: JsonObject, core_ordinal: int) -> str | None:
    kind = step.get("step_kind")
    return "intro" if kind == "intro" else f"core{core_ordinal}" if kind == "core" else None


def _figures_by_step(plan: JsonObject) -> dict[str, list[tuple[int, JsonObject]]]:
    found: dict[str, list[tuple[int, JsonObject]]] = {}
    cores = 0
    for step in _objects(plan.get("steps")):
        cores += step.get("step_kind") == "core"
        key = _step_key(step, cores)
        blocks = _objects(step.get("blocks"))
        if key is not None:
            found[key] = [
                (index, block)
                for index, block in enumerate(blocks)
                if block.get("type") == "visual"
            ]
    return found


def carry_figures(previous: JsonObject, revised: JsonObject) -> JsonObject:
    """The revised plan with the figures of the plan it revises, each back where it was.

    A part holds only explanations, worked examples and practice, so a figure is not written or
    rewritten in a revision. It stays in its step, at its place among the blocks, and goes with
    the step if the revision drops it.
    """
    figures = _figures_by_step(previous)
    steps: list[JsonValue] = []
    cores = 0
    for step in _objects(revised.get("steps")):
        cores += step.get("step_kind") == "core"
        blocks: list[JsonValue] = [*_objects(step.get("blocks"))]
        for index, figure in figures.get(_step_key(step, cores) or "", []):
            blocks.insert(min(index, len(blocks)), figure)
        steps.append({**step, "blocks": blocks})
    return {**revised, "steps": steps}
