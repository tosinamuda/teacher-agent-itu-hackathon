"""Where lesson notes are read from and written to, named as ports."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.lesson_note.domain.note import LessonNote
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class StoredLessonNote(Protocol):
    """A persisted lesson note as the routes read it."""

    artefact_id: str
    artefact_type: str
    scope: str
    plan_version_id: str
    manifest: JsonObject
    artefact_refs: JsonObject | None
    review_status: ArtefactReviewStatus
    reviewed_at: datetime | None
    created_at: datetime
    version: int


class LessonNotes(Protocol):
    """Plans to write notes for, and the notes written for them."""

    async def plan(self, db: AsyncSession, plan_version_id: str) -> SessionPlanView | None: ...

    async def add(
        self, db: AsyncSession, note: LessonNote, artefact_refs: JsonObject
    ) -> StoredLessonNote: ...

    async def latest(self, db: AsyncSession, plan_version_id: str) -> StoredLessonNote | None: ...

    async def get(self, db: AsyncSession, artefact_id: str) -> StoredLessonNote | None: ...

    async def get_for_update(
        self, db: AsyncSession, artefact_id: str
    ) -> StoredLessonNote | None: ...
