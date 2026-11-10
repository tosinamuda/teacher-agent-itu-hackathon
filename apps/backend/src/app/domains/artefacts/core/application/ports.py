"""Ports for the artefacts core application layer.

The read/approve/export use cases depend on these Protocols rather than on
``ArtefactRepository`` and ``ArtefactStore``, so wiring stays in a composition
root and a test substitutes a fake without a database.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)

if TYPE_CHECKING:
    from app.domains.artefacts.core.infrastructure.models import Artefact
    from app.shared.json_types import JsonObject


class ArtefactReadPort(Protocol):
    """The persisted artefacts the core use cases read."""

    async def get_artefact(self, db: AsyncSession, artefact_id: str) -> Artefact | None: ...

    async def get_artefact_for_update(
        self, db: AsyncSession, artefact_id: str
    ) -> Artefact | None: ...

    async def get_latest_artefact_for_plan_version(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        scope: ArtefactScope,
        plan_version_id: str,
    ) -> Artefact | None: ...

    async def list_artefacts_for_student(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        student_id: str,
        limit: int,
        review_status: str | None = None,
    ) -> list[Artefact]: ...

    async def list_pending_learner_artefacts(
        self,
        db: AsyncSession,
        *,
        artefact_type: ArtefactType,
        plan_version_id: str | None,
        limit: int,
        owned_plan_version_ids: Sequence[str] | None = None,
        review_status: ArtefactReviewStatus = ArtefactReviewStatus.PENDING,
    ) -> list[Artefact]: ...


@dataclass(frozen=True)
class Approval:
    """One teacher approval of one version of a content item."""

    approval_id: str
    approved_version: int
    approved_by: str | None
    approved_at: datetime


class ApprovalFollowUp(Protocol):
    """What a content type does once one of its items is approved, after the approval commits."""

    async def after_approval(self, db: AsyncSession, artefact: Artefact) -> None: ...


class ContentApprovals(Protocol):
    """Every approval of a content item, kept with the version it approved."""

    def record_approval(
        self, db: AsyncSession, *, artefact_id: str, approved_version: int, approved_by: str | None
    ) -> None: ...

    async def list_approvals(self, db: AsyncSession, artefact_id: str) -> list[Approval]: ...


class ReviewPackExportPort(Protocol):
    """Writing a review pack out for download."""

    def export_review_pack(self, artefact_id: str, manifest: JsonObject) -> JsonObject: ...
