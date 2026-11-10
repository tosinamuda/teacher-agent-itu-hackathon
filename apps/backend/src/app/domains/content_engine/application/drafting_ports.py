"""What drafting reads and writes, as the ports its adapters implement."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content_engine.domain.draft import Draft
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class Drafts(Protocol):
    def new_id(self) -> str: ...

    async def add(self, db: AsyncSession, draft: Draft) -> None: ...

    async def get(self, db: AsyncSession, draft_id: str, *, for_update: bool) -> Draft | None: ...

    async def save(self, db: AsyncSession, draft: Draft) -> None: ...


class Lessons(Protocol):
    async def plan(self, db: AsyncSession, plan_version_id: str) -> SessionPlanView | None: ...

    async def approved_note_sections(
        self, db: AsyncSession, plan_version_id: str
    ) -> dict[str, str]:
        """The lesson's approved note, by plan step; empty when none is approved."""
        ...

    async def concluded(self, db: AsyncSession, plan_version_id: str) -> bool: ...


@dataclass(frozen=True)
class StoredContent:
    content_id: str
    kind: str
    plan_version_id: str
    manifest: JsonObject
    spec_revision: int | None
    #: The lesson period, for content made from a lesson rather than from a plan version.
    session_id: str | None = None


class ContentReader(Protocol):
    async def get(self, db: AsyncSession, content_id: str) -> StoredContent | None: ...


class ContentStore(ContentReader, Protocol):
    async def add(
        self,
        db: AsyncSession,
        *,
        kind: str,
        plan_version_id: str,
        manifest: JsonObject,
        refs: JsonObject,
    ) -> str:
        """Store new content, pending review. Returns its ID."""
        ...

    async def replace(self, db: AsyncSession, content_id: str, manifest: JsonObject) -> None:
        """Store a revised version, pending review again; text that changed nothing is not one."""
        ...


class Drawings(Protocol):
    async def problem(self, source: str) -> str | None:
        """Why a drawing will not draw; ``None`` when it draws."""
        ...


class Learners(Protocol):
    """What a writer may read about one learner: the class note to adapt and their state."""

    async def context(self, db: AsyncSession, plan_version_id: str, student_id: str) -> JsonObject:
        """Raise ``DraftError`` when the learner has no work for the lesson or no note to adapt."""
        ...

    async def adapted(self, db: AsyncSession, plan_version_id: str, student_id: str) -> list[str]:
        """The objectives the learner has enough marked work to adapt the class note for."""
        ...


class Destination(Protocol):
    """Where a type's finished draft is saved, and what stops it being saved there."""

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """What stops the finished draft being saved; empty when nothing does."""
        ...

    def preview(self, draft: Draft) -> JsonObject:
        """What the draft would save as, from the parts written so far."""
        ...

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        """Save the finished draft, recording its generator. Returns what it is saved as."""
        ...
