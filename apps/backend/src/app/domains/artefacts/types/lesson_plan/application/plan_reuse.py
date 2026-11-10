"""Bring a lesson plan that already exists into another lesson.

A reused plan keeps its content: the steps, the blocks and the wording of its objectives. Two
things change. The names a plan was written with before the field renames are read the way the
plan model reads a stored plan. And each lesson objective is pointed at a curriculum objective of
the lesson it now sits in, which this module maps.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.application.errors import PlanValidationError
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    normalize_session_plan_payload,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    READING_A_STORED_PLAN,
    SessionPlan,
)
from app.shared.json_types import JsonObject, JsonValue


class SavedPlan(Protocol):
    """A plan that was saved: the response the API sends carries these and more."""

    plan_id: str
    version_id: str


@dataclass(frozen=True)
class ReuseSource:
    """A saved plan version, as another lesson can reuse it."""

    session_plan: JsonObject
    version_id: str
    lesson_period_id: uuid.UUID


@dataclass(frozen=True)
class ReusedPlan:
    #: The saved plan; ``None`` while a lesson objective still has no curriculum objective.
    plan: SavedPlan | None
    #: The lesson objectives that still need one.
    unmapped: list[JsonObject]
    #: The curriculum objectives of the lesson, to choose from.
    choices: list[JsonObject]


@dataclass(frozen=True)
class MappedPlan:
    #: The plan with each lesson objective pointed at a curriculum objective where one is known.
    content: JsonObject
    #: The lesson objectives still without one: ``lesson_objective_id`` and ``objective_text``.
    unmapped: list[JsonObject]


def canonical_content(source: JsonObject) -> JsonObject:
    """``source`` with the field names the plan model writes, such as ``kc_type``."""
    try:
        plan = SessionPlan.model_validate(
            normalize_session_plan_payload(source), context=READING_A_STORED_PLAN
        )
    except ValidationError as error:
        messages = [str(found.get("msg", found)) for found in error.errors()]
        raise PlanValidationError({"plan": messages}) from None
    return plan.model_dump(mode="json", exclude_none=True)


def map_curriculum(
    content: JsonObject,
    curriculum: Sequence[JsonObject],
    chosen: Mapping[str, str],
) -> MappedPlan:
    """Point each lesson objective at one of the lesson's curriculum objectives.

    An objective takes, in order: the curriculum objective chosen for it, the one it already
    names when the lesson has it, and the lesson's only curriculum objective. Any other objective
    is left unmapped for the caller to ask about.
    """
    targets = {
        str(found["curriculum_objective_id"]): found
        for found in curriculum
        if found.get("curriculum_objective_id")
    }
    only = next(iter(targets.values())) if len(targets) == 1 else None
    objectives: list[JsonValue] = []
    unmapped: list[JsonObject] = []
    for objective in _objectives_of(content):
        lesson_objective_id = str(objective.get("lesson_objective_id") or "")
        target = (
            targets.get(chosen.get(lesson_objective_id, ""))
            or targets.get(str(objective.get("curriculum_objective_id") or ""))
            or only
        )
        if target is None:
            unmapped.append(
                {
                    "lesson_objective_id": lesson_objective_id,
                    "objective_text": str(objective.get("objective_text") or ""),
                }
            )
            objectives.append(objective)
            continue
        objectives.append(
            {
                **objective,
                "curriculum_objective_id": target["curriculum_objective_id"],
                "curriculum_objective_text": target.get("objective_text"),
            }
        )
    return MappedPlan({**content, "lesson_plan_objectives": objectives}, unmapped)


def _objectives_of(content: JsonObject) -> list[JsonObject]:
    found = content.get("lesson_plan_objectives")
    return [item for item in found if isinstance(item, dict)] if isinstance(found, list) else []
