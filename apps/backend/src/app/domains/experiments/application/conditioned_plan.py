"""The frozen lesson plan a conditioned experiment generates from, with its lesson note."""

from dataclasses import dataclass
from typing import Protocol

from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    ApprovedLessonNote,
    Grounding,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.experiments.domain.types import ConditionedInputsMissingError
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class SessionPlanReader(Protocol):
    """Read the frozen authored plan used by a conditioned execution, and its note."""

    async def get_plan_version(self, plan_version_id: str) -> PlanVersion | None: ...

    async def approved_lesson_note(self, plan_version_id: str) -> ApprovedLessonNote | None: ...


@dataclass(frozen=True)
class ConditionedPlan:
    """The plan as the conditions read it: each step carrying its section of the lesson note."""

    session_plan: SessionPlanView
    #: What a pack that reads the note records of it, as every revision note does.
    grounding: JsonObject


async def validated_session_plan(
    experiments: SessionPlanReader,
    plan_version_id: str,
) -> ConditionedPlan:
    """The authored plan with the lesson's approved note, or its stable worker failure reason."""
    plan_version = await experiments.get_plan_version(plan_version_id)
    if plan_version is None:
        raise ConditionedInputsMissingError("plan_version_not_found")
    note = await experiments.approved_lesson_note(plan_version_id)
    grounding = Grounding(ExpertSources.LESSON_NOTE if note else ExpertSources.TEXTBOOK, note)
    try:
        return ConditionedPlan(
            session_plan=grounding.plan(plan_version.session_plan or {}),
            grounding=grounding.refs(),
        )
    except ValidationError as exc:
        raise ConditionedInputsMissingError("plan_version_session_plan_missing") from exc
