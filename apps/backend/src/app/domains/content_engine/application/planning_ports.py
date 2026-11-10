"""The lesson-plan side a plan draft is saved through, as the port its adapter implements."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class PlanLesson:
    """A lesson period, as a writer of its plan needs it."""

    session_id: str
    #: Subject, grade, term, week, topic, subtopic and the lesson's length in minutes.
    facts: JsonObject
    #: The curriculum objectives a lesson objective maps to, with their IDs.
    curriculum_objectives: list[JsonObject]
    #: The curriculum's notes for the lesson and the textbook records its objectives link to.
    grounding: JsonObject = field(default_factory=dict)


@dataclass(frozen=True)
class PlanRecord:
    """A lesson's plan as it stands, split into the parts a draft of it is written in."""

    plan_id: str
    #: The lesson period the plan is for.
    session_id: str
    #: The version the plan is at now.
    version_id: str
    #: The lesson's own part, and each curriculum objective's part by its ID.
    lesson: JsonObject
    sections: dict[str, JsonObject]
    #: Its lesson's study has concluded, so it can be read and never changed.
    concluded: bool = False


class PlanRefusedError(ValueError):
    """The plan cannot be saved yet; ``issues`` says why, by check."""

    def __init__(self, issues: JsonObject) -> None:
        super().__init__(str(issues))
        self.issues = issues


class Planning(Protocol):
    """The lesson, the checks a plan must pass, and saving it as the teacher's plan."""

    async def lesson(self, db: AsyncSession, session_id: str) -> PlanLesson | None: ...

    async def current(self, db: AsyncSession, plan_id: str) -> PlanRecord | None:
        """The plan as it stands, to reopen it as a draft."""
        ...

    async def issues(
        self, db: AsyncSession, session_id: str, content: JsonObject, *, strict: bool
    ) -> JsonObject:
        """What stops ``content`` being saved as the lesson's plan; empty when nothing does.

        A plan the app writes is ``strict``ly held to the lesson-plan spec's requirements; a
        teacher's own document is saved as it is.
        """
        ...

    async def save(
        self,
        db: AsyncSession,
        session_id: str,
        content: JsonObject,
        author: str | None,
        *,
        source_type: str,
        generator: JsonObject,
    ) -> str:
        """Save ``content`` as a new draft plan version of ``source_type``, made by ``generator``.

        Returns its ID.
        """
        ...

    async def revise(
        self,
        db: AsyncSession,
        plan_id: str,
        session_id: str,
        content: JsonObject,
        *,
        generator: JsonObject,
    ) -> str:
        """Save ``content`` as the next draft version of the plan. Returns its ID."""
        ...
