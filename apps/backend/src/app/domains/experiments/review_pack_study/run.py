"""What one experiment execution is run against: its identity, and its lesson."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


@dataclass(frozen=True)
class ExperimentRun:
    """Identity of one execution — what saved runs and generation-log rows correlate against."""

    execution_db_id: uuid.UUID
    execution_id: str
    experiment_id: str
    plan_version_id: str


@dataclass(frozen=True)
class LessonUnderStudy:
    """The frozen lesson content every condition generates from."""

    session_plan: SessionPlanView
    sources: LessonSources
    #: The lesson note the plan carries, as a pack that reads it records.
    grounding: JsonObject = field(default_factory=dict)
