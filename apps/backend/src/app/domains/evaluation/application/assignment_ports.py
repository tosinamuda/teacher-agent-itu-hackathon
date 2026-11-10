"""Role-specific stores and provider capabilities for assignment commands."""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.evaluation.domain.records import AssignmentRecord, RaterIdentity
from app.domains.evaluation.infrastructure.models import EvaluationAuditItem, RaterAssignment
from app.domains.experiments.application.evaluation_scope import (
    EvaluationBundleScope,
    EvaluationExperimentScope,
)


class ExperimentAssignmentScopes(Protocol):
    async def evaluation_scope(self, *, experiment_id: str) -> EvaluationExperimentScope | None: ...

    async def evaluation_scope_for_execution(
        self, *, execution_id: uuid.UUID
    ) -> EvaluationExperimentScope | None: ...

    async def lock_evaluation_scope(self, *, experiment_db_id: uuid.UUID) -> None: ...

    async def lesson_period_exists(self, *, lesson_period_id: uuid.UUID) -> bool: ...

    async def lesson_period_title(self, *, lesson_period_id: uuid.UUID) -> str | None: ...

    async def focal_case_belongs_to_experiment(
        self,
        *,
        experiment_db_id: uuid.UUID,
        focal_case_id: str,
    ) -> bool: ...

    async def evaluation_bundle_scope(
        self, *, experiment_id: str
    ) -> EvaluationBundleScope | None: ...


class Assignments(Protocol):
    async def rater_identity(self, *, rater_id: str) -> RaterIdentity | None: ...

    async def assignment_record(
        self,
        *,
        experiment_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
    ) -> AssignmentRecord | None: ...

    async def assignment_count(
        self,
        *,
        experiment_db_id: uuid.UUID,
        hypothesis: str,
        scope_id: str,
        exclude_adjudicators: bool = False,
        adjudicators_only: bool = False,
    ) -> int: ...

    async def stage_assignment_record(self, assignment: AssignmentRecord) -> AssignmentRecord: ...

    async def audit_assignment_target(self, *, audit_item_id: str) -> uuid.UUID | None: ...

    async def audit_item_ids_for_executions(
        self, *, execution_ids: tuple[uuid.UUID, ...]
    ) -> tuple[str, ...]: ...


class AssignmentStore(Protocol):
    @property
    def assignments(self) -> Assignments: ...

    @property
    def assignment_scopes(self) -> ExperimentAssignmentScopes: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class AssignmentViewData(Protocol):
    """Read model used by assignment administration and rater queues."""

    async def list_audit_items_for_executions(
        self, *, execution_db_ids: list[uuid.UUID]
    ) -> list[EvaluationAuditItem]: ...

    async def list_assignments_for_experiment(
        self, *, experiment_db_id: uuid.UUID
    ) -> list[RaterAssignment]: ...

    async def list_rater_identities(self) -> list[RaterIdentity]: ...

    async def list_assignments_for_rater(
        self, *, rater_db_id: uuid.UUID
    ) -> list[RaterAssignment]: ...
