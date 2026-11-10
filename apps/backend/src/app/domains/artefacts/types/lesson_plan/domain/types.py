from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum

from app.shared.json_types import JsonObject


class PlanVersionStatus(str, Enum):
    """Lifecycle of a ``PlanVersion`` row: draft until a teacher approves it.

    A draft the teacher discards is ``rejected``; an approved version taken back is
    ``withdrawn``. Both stay in the plan's history with their reason, and neither is a version
    that content is made from.
    """

    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

    @property
    def is_live(self) -> bool:
        """A draft being worked on, or the approved version content is made from."""
        return self in (PlanVersionStatus.DRAFT, PlanVersionStatus.APPROVED)


@dataclass
class SessionContext:
    session_id: str
    subject: str
    track: str
    grade: str
    term: str
    week: int
    day_index: int
    topic: str
    subtopic: str
    duration_minutes: int
    session_objectives: list[str]
    general_objectives: list[str]
    reference_materials: list[JsonObject]
    theme: str = ""
    performance_objectives: list[str] = field(default_factory=list)
    teacher_activities: list[str] = field(default_factory=list)
    student_activities: list[str] = field(default_factory=list)
    instructional_materials: list[str] = field(default_factory=list)
    evaluation_guide: list[str] = field(default_factory=list)
    textbook_references: list[JsonObject] = field(default_factory=list)
    grounding_mode: str = "manual_linkage"
    # Per-AO curated planning rows (roles, assessments) for the authoritative
    # curated path; populated only when grounding_mode == "manual_linkage".
    curated_objectives: list[JsonObject] = field(default_factory=list)
    entry_behaviour: list[str] = field(default_factory=list)
    average_age: int | None = None
    # The lesson_period this session context will be persisted against. Set by
    # the day-row builder (path 2). Path 1 (curriculum-side ClassSession) leaves
    # this None; ``persist_plan_version`` requires it to be non-None — the P5.7
    # canonical lesson chain attaches every lesson_plan to a real lesson_period.
    lesson_period_id: uuid.UUID | None = None
    #: The subtopic the lesson teaches, whose performance objectives are the lesson's curriculum.
    subtopic_id: str = ""


@dataclass
class PlanVersionInfo:
    plan_id: str
    version_id: str
    status: str
