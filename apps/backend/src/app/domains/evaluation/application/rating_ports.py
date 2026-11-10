"""Role stores for interactive and imported rating persistence."""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.evaluation.domain.records import RaterIdentity, RatingRecord
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
    RaterAssignment,
)


class SubmittedRatings(Protocol):
    """Persistence capabilities required to submit an interactive rating."""

    async def get_rater(self, *, rater_id: str) -> EvaluationRater | None: ...

    async def get_rater_by_user_id(self, *, user_id: uuid.UUID) -> EvaluationRater | None: ...

    async def get_packet(self, *, evaluation_packet_id: str) -> EvaluationPacket | None: ...

    async def get_rating(
        self,
        *,
        evaluation_packet_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> EvaluationRating | None: ...

    async def find(
        self,
        *,
        evaluation_packet_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> RatingRecord | None: ...

    async def list_assignments_for_rater(
        self, *, rater_db_id: uuid.UUID
    ) -> list[RaterAssignment]: ...

    async def stage_rating(self, rating: EvaluationRating) -> EvaluationRating: ...

    async def stage(self, rating: RatingRecord) -> RatingRecord: ...


class RatingImports(Protocol):
    """Persistence capabilities required to import one offline rating row."""

    async def get_packet_by_code(self, *, packet_code: str) -> EvaluationPacket | None: ...

    async def rater_identity_by_name(self, *, display_name: str) -> RaterIdentity | None: ...

    async def stage_rater_identity(self, identity: RaterIdentity) -> RaterIdentity: ...

    async def get_rating(
        self,
        *,
        evaluation_packet_db_id: uuid.UUID,
        rater_db_id: uuid.UUID,
    ) -> EvaluationRating | None: ...

    async def stage_rating(self, rating: EvaluationRating) -> EvaluationRating: ...


class RatingSubmissionStore(Protocol):
    """One open transaction for an interactive rating submission."""

    @property
    def ratings(self) -> SubmittedRatings: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class RatingImportStore(Protocol):
    """One open transaction reused as one explicit unit of work per import row."""

    @property
    def rating_imports(self) -> RatingImports: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
