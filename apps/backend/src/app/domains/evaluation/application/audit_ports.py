"""Role stores for audit-item construction and audit-rating submission."""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.evaluation.domain.records import (
    AuditItemRecord,
    AuditRatingRecord,
    RaterIdentity,
)
from app.domains.evaluation.infrastructure.models import (
    EvaluationAuditItem,
    EvaluationAuditRating,
    EvaluationRater,
    RaterAssignment,
)


class AuditItems(Protocol):
    async def count_audit_items_for_execution(self, *, execution_db_id: uuid.UUID) -> int: ...

    async def stage_audit_items(
        self, items: tuple[AuditItemRecord, ...]
    ) -> tuple[AuditItemRecord, ...]: ...


class AuditItemBuildStore(Protocol):
    @property
    def audit_builds(self) -> AuditItems: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class AuditRatings(Protocol):
    async def audit_item_record(self, *, audit_item_id: str) -> AuditItemRecord | None: ...

    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None: ...

    async def audit_item_is_assigned(
        self, *, audit_item_id: str, rater_db_id: uuid.UUID
    ) -> bool: ...

    async def audit_rating_record(
        self,
        *,
        audit_item_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> AuditRatingRecord | None: ...

    async def stage_audit_rating(self, rating: AuditRatingRecord) -> AuditRatingRecord: ...


class AuditRatingStore(Protocol):
    @property
    def audit_ratings(self) -> AuditRatings: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class AuditPresentationData(Protocol):
    """Read model needed to render audit queues, details, and exports."""

    async def get_rater(self, *, rater_id: str) -> EvaluationRater | None: ...

    async def list_assignments_for_rater(
        self, *, rater_db_id: uuid.UUID
    ) -> list[RaterAssignment]: ...

    async def list_audit_items(self) -> list[EvaluationAuditItem]: ...

    async def list_audit_items_for_executions(
        self, *, execution_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditItem]: ...

    async def get_audit_item(self, *, audit_item_id: str) -> EvaluationAuditItem | None: ...

    async def get_audit_rating(
        self, *, audit_item_db_id: uuid.UUID, rater_db_id: uuid.UUID
    ) -> EvaluationAuditRating | None: ...

    async def list_audit_ratings_for_items(
        self, *, audit_item_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditRating]: ...
