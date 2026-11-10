"""What of a lesson plan has been written so far, for a page that waits for the rest."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.domains.content_engine.domain.lesson import LESSON_UNIT_ID, LessonUnit
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class OutlineStep:
    title: str
    minutes: int | None


@dataclass(frozen=True)
class PlanOutline:
    objectives: list[str]
    #: The introduction, then the core steps in unit order, then the evaluation.
    steps: list[OutlineStep]
    #: How many of the plan's units have a part.
    written: int
    total: int


def _step(raw: object) -> OutlineStep | None:
    if not isinstance(raw, dict):
        return None
    title = raw.get("title")
    if not isinstance(title, str) or not title.strip():
        return None
    minutes = raw.get("estimated_minutes")
    return OutlineStep(title.strip(), minutes if isinstance(minutes, int) else None)


def _objectives(part: JsonObject) -> list[JsonObject]:
    raw = part.get("lesson_objectives")
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def outline_of(units: Sequence[LessonUnit], parts: Mapping[str, JsonObject]) -> PlanOutline:
    """The objectives and steps the parts written so far set out, in the order of the plan."""
    lesson = parts.get(LESSON_UNIT_ID, {})
    steps = [_step(lesson.get("intro"))]
    objectives: list[str] = []
    for unit in units:
        if unit.unit_id == LESSON_UNIT_ID:
            continue
        for objective in _objectives(parts.get(unit.unit_id, {})):
            text = objective.get("objective")
            if isinstance(text, str) and text.strip():
                objectives.append(text.strip())
            steps.append(_step(objective.get("core_step")))
    steps.append(_step(lesson.get("evaluation")))
    return PlanOutline(
        objectives=objectives,
        steps=[step for step in steps if step is not None],
        written=sum(1 for unit in units if unit.unit_id in parts),
        total=len(units),
    )
