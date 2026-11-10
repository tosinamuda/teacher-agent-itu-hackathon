"""A lesson plan as the study's lesson document, and the rules every such document keeps.

The study's lessons were written as XML documents valid against ``lesson.rng``; that is the
lesson-plan input the evaluation generated from. A plan made in the app is held to the same
grammar and the same reference rules by projecting it into that document, so the everyday
path and the evaluation read plans of one specification.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import cache
from pathlib import Path
from typing import Any

from lxml import etree

GRAMMAR_PATH = Path(__file__).with_name("lesson.rng")


@cache
def _grammar() -> etree.RelaxNG:
    return etree.RelaxNG(etree.parse(str(GRAMMAR_PATH)))


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _set(element: etree._Element, name: str, value: Any) -> None:
    if value is not None and _text(value) != "":
        element.set(name, _text(value))


def _items(parent: etree._Element, tag: str, values: Iterable[Any]) -> None:
    items = [_text(value) for value in values if _text(value)]
    if items:
        holder = etree.SubElement(parent, tag)
        for item in items:
            etree.SubElement(holder, "item").text = item


def _activities(parent: etree._Element, activities: Iterable[Mapping[str, Any]]) -> None:
    listed = list(activities)
    if not listed:
        return
    holder = etree.SubElement(parent, "activities")
    for activity in listed:
        element = etree.SubElement(holder, "activity", who=_text(activity.get("who")))
        if activity.get("sets_work") is not None:
            element.set("sets-work", "true" if activity["sets_work"] else "false")
        element.text = _text(activity.get("what"))


def _questions(parent: etree._Element, step_id: str, blocks: Iterable[Mapping[str, Any]]) -> None:
    practice = [block for block in blocks if block.get("type") == "practice"]
    if not practice:
        return
    holder = etree.SubElement(parent, "questions")
    for block in practice:
        # A plan names a question within the lesson; the document, within its step.
        local = _text(block.get("id")).removeprefix(f"{step_id}:")
        question = etree.SubElement(holder, "question", id=local)
        _set(question, "objective", block.get("lesson_objective_id"))
        question.text = _text(block.get("question"))


def _step(parent: etree._Element, step: Mapping[str, Any]) -> None:
    element = etree.SubElement(
        parent, "step", id=_text(step.get("step_id")), kind=_text(step.get("step_kind"))
    )
    _set(element, "objective", step.get("lesson_objective_id"))
    _set(element, "minutes", step.get("estimated_minutes"))
    _set(element, "title", step.get("title"))
    _set(element, "instructional-type", step.get("instructional_type"))
    if _text(step.get("content")):
        etree.SubElement(element, "plan-content").text = _text(step.get("content"))
    _activities(element, step.get("activities") or [])
    if step.get("step_kind") == "evaluation":
        _questions(element, _text(step.get("step_id")), step.get("blocks") or [])


def as_document(plan: Mapping[str, Any]) -> etree._Element:
    """The plan as a lesson document. A step's lesson note is its own record, so none is here."""
    root = etree.Element("lesson")
    for name, key in (
        ("id", "plan_id"),
        ("plan-id", "plan_id"),
        ("session-id", "session_id"),
        ("subject", "subject"),
        ("track", "track"),
        ("grade", "grade"),
        ("term", "term"),
        ("week", "week"),
        ("topic", "topic"),
        ("subtopic", "subtopic"),
    ):
        root.set(name, _text(plan.get(key)))
    curriculum = etree.SubElement(root, "curriculum")
    for objective in plan.get("curriculum_objectives") or []:
        etree.SubElement(
            curriculum, "objective", id=_text(objective.get("curriculum_objective_id"))
        ).text = _text(objective.get("objective_text"))
    objectives = etree.SubElement(root, "objectives")
    for objective in plan.get("lesson_plan_objectives") or []:
        element = etree.SubElement(
            objectives,
            "objective",
            id=_text(objective.get("lesson_objective_id")),
            curriculum=_text(objective.get("curriculum_objective_id")),
        )
        _set(element, "kc-type", objective.get("kc_type"))
        element.text = _text(objective.get("objective_text"))
    _items(root, "entry-behaviour", plan.get("entry_behaviour") or [])
    _items(root, "materials", plan.get("instructional_materials") or [])
    _items(root, "references", plan.get("references") or [])
    for step in plan.get("steps") or []:
        _step(root, step)
    return root


def _declared(root: etree._Element, path: str) -> set[str]:
    return {element.get("id", "") for element in root.iterfind(path)}


def _reference_violations(root: etree._Element) -> list[str]:
    """Every id points at something declared, and nothing is declared twice."""
    curriculum = _declared(root, "curriculum/objective")
    objectives = _declared(root, "objectives/objective")
    found: list[str] = []
    for objective in root.iterfind("objectives/objective"):
        if objective.get("curriculum") not in curriculum:
            found.append(
                f"{objective.get('id')}: curriculum objective "
                f"{objective.get('curriculum')!r} is not declared"
            )
    seen: set[str] = set()
    for step in root.iterfind("step"):
        step_id = step.get("id", "")
        if step.get("kind") == "core" and not step.get("objective"):
            found.append(f"{step_id}: a core step must name the objective it teaches")
        if step.get("objective") and step.get("objective") not in objectives:
            found.append(f"{step_id}: objective {step.get('objective')!r} is not declared")
        inside = (*step.iterfind("note/section"), *step.iterfind("questions/question"))
        # A section's or question's id is its step's own, so it is unique within the step.
        for declared_id in (step_id, *(f"{step_id}:{e.get('id', '')}" for e in inside)):
            if declared_id in seen:
                found.append(f"{declared_id}: declared twice")
            seen.add(declared_id)
        for question in step.iterfind("questions/question"):
            if question.get("objective") and question.get("objective") not in objectives:
                found.append(
                    f"{question.get('id')}: objective {question.get('objective')!r} is not declared"
                )
    return found


def violations(root: etree._Element) -> list[str]:
    """Where a lesson document breaks its grammar or its references; empty when it keeps both."""
    grammar = _grammar()
    if not grammar.validate(etree.ElementTree(root)):
        return [f"{GRAMMAR_PATH.name}: {error.message}" for error in grammar.error_log]
    return _reference_violations(root)
