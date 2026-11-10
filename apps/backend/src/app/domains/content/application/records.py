"""Content as stored, and where it and a class test's questions are read from."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.domain.types import Level
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class ContentRecord:
    """A stored content item, without its body."""

    content_id: str
    #: The slug of its registered type.
    type: str
    #: The artefact kind it is stored as.
    kind: str
    level: Level
    plan_version_id: str
    student_id: str | None
    version: int
    review_status: str
    created_at: datetime | None
    #: The specification revision and pipeline version it was generated with, where recorded.
    provenance: JsonObject
    manifest: JsonObject
    #: Its lesson's study has concluded, so it can be read and never changed.
    read_only: bool = False
    #: Why the teacher rejected it or withdrew it.
    review_reason: str | None = None
    #: The checks it passed and the passages it cites, as recorded when it was written.
    review: JsonObject | None = None


@dataclass(frozen=True)
class ContentItem:
    """A content item with its body, as a reader sees it."""

    record: ContentRecord
    content: JsonObject


class ContentRecords(Protocol):
    """The stored content."""

    async def get(self, db: AsyncSession, content_id: str) -> ContentRecord | None: ...

    async def find(
        self,
        db: AsyncSession,
        *,
        plan_version_id: str | None,
        type: str | None,
        level: Level | None,
        student_id: str | None,
    ) -> list[ContentRecord]: ...

    async def plan_refusal(self, db: AsyncSession, plan_version_id: str) -> str | None:
        """Why content may not be made from this plan version, or none when it may.

        Content is made from the newest approved version of a plan: a draft, a closed version, or
        one a newer approved version has taken over is refused.
        """
        ...

    async def mark_changed(self, db: AsyncSession, content_id: str) -> None:
        """Record that the content changed: a new version, back to pending review."""
        ...

    async def record_generator(
        self, db: AsyncSession, content_id: str, generator: JsonObject
    ) -> None:
        """Record which generator made the item, unless an earlier generation already did."""
        ...

    async def concluded(self, db: AsyncSession, plan_version_id: str) -> bool:
        """Whether the lesson's study has concluded, leaving its record read-only."""
        ...

    async def class_pack_awaits_its_experiment(
        self, db: AsyncSession, plan_version_id: str
    ) -> bool:
        """Whether the lesson's class revision note is still to come from its running experiment.

        The class pack of a lesson an experiment runs on is that experiment's C4 pack; until
        it exists, a pack made any other way would be a second one the lesson never uses.
        """
        ...

    async def has_class_revision_note(self, db: AsyncSession, plan_version_id: str) -> bool:
        """Whether the lesson already has a class revision note, approved or pending."""
        ...

    async def class_test_answered(self, db: AsyncSession, plan_version_id: str) -> bool:
        """Whether any student has answered the lesson's class test."""
        ...


class ClassTestQuestions(Protocol):
    """A class test's questions, read from the rows grading uses."""

    async def content(self, db: AsyncSession, plan_version_id: str) -> JsonObject: ...
