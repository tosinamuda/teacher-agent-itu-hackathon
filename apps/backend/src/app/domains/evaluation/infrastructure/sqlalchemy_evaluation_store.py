"""SQLAlchemy-backed evaluation rating units of work."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.evaluation.application.assignment_ports import (
    Assignments,
    ExperimentAssignmentScopes,
)
from app.domains.evaluation.application.audit_ports import (
    AuditItems,
    AuditRatings,
)
from app.domains.evaluation.application.identity_ports import RaterIdentities
from app.domains.evaluation.application.rating_ports import (
    RatingImports,
    SubmittedRatings,
)
from app.domains.evaluation.infrastructure.repository import EvaluationRepository


class SqlAlchemyEvaluationStore:
    """One request-bound session exposed through evaluation role capabilities."""

    def __init__(
        self,
        session: AsyncSession,
        *,
        assignment_scopes: ExperimentAssignmentScopes | None = None,
    ) -> None:
        self._session = session
        self._repository = EvaluationRepository(session)
        self._assignment_scopes = assignment_scopes

    @property
    def ratings(self) -> SubmittedRatings:
        return self._repository

    @property
    def rating_imports(self) -> RatingImports:
        return self._repository

    @property
    def rater_identities(self) -> RaterIdentities:
        return self._repository

    @property
    def assignments(self) -> Assignments:
        return self._repository

    @property
    def assignment_scopes(self) -> ExperimentAssignmentScopes:
        if self._assignment_scopes is None:
            raise RuntimeError("assignment scopes were not composed for this store")
        return self._assignment_scopes

    @property
    def audit_builds(self) -> AuditItems:
        return self._repository

    @property
    def audit_ratings(self) -> AuditRatings:
        return self._repository

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
