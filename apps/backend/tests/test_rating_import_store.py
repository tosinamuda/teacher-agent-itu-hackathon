"""Per-row unit-of-work behavior for offline rating imports."""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.rating_import_service import (
    OfflineRatingRow,
    RatingImportApplicationService,
)
from app.domains.evaluation.domain.records import RaterIdentity
from app.domains.evaluation.infrastructure.models import EvaluationRating


class _ImportData:
    def __init__(self) -> None:
        self.packet = SimpleNamespace(id=uuid.UUID(int=1), hypothesis="H1")
        self.raters: dict[str, RaterIdentity] = {}
        self.ratings: dict[tuple[uuid.UUID, uuid.UUID], EvaluationRating] = {}
        self.pending_raters: list[RaterIdentity] = []
        self.pending_ratings: list[EvaluationRating] = []

    async def get_packet_by_code(self, *, packet_code: str):
        return self.packet if packet_code == "PKT-1" else None

    async def rater_identity_by_name(self, *, display_name: str):
        return self.raters.get(display_name)

    async def get_rating(self, *, evaluation_packet_db_id: uuid.UUID, rater_db_id: uuid.UUID):
        return self.ratings.get((evaluation_packet_db_id, rater_db_id))

    async def stage_rater_identity(self, rater: RaterIdentity) -> RaterIdentity:
        self.pending_raters.append(rater)
        return rater

    async def stage_rating(self, rating: EvaluationRating) -> EvaluationRating:
        if rating.overall_score < 0:
            raise EvaluationApplicationError(422, "invalid_import_score")
        self.pending_ratings.append(rating)
        return rating


class _ImportStore:
    def __init__(self, persistence: _ImportData) -> None:
        self.persistence = persistence
        self.commits = 0
        self.rollbacks = 0

    @property
    def rating_imports(self) -> _ImportData:
        return self.persistence

    async def commit(self) -> None:
        for rater in self.persistence.pending_raters:
            self.persistence.raters[rater.display_name] = rater
        for rating in self.persistence.pending_ratings:
            key = (rating.evaluation_packet_db_id, rating.rater_db_id)
            self.persistence.ratings[key] = rating
        self.persistence.pending_raters.clear()
        self.persistence.pending_ratings.clear()
        self.commits += 1

    async def rollback(self) -> None:
        self.persistence.pending_raters.clear()
        self.persistence.pending_ratings.clear()
        self.rollbacks += 1


def _row(*, rater_name: str, score: float, packet_code: str = "PKT-1") -> OfflineRatingRow:
    return OfflineRatingRow(
        packet_code=packet_code,
        rater_name=rater_name,
        overall_score=score,
        rubric_scores={"criterion": score},
    )


@pytest.mark.asyncio
async def test_failed_row_rolls_back_rater_and_continues_with_next_row() -> None:
    persistence = _ImportData()
    store = _ImportStore(persistence)
    service = RatingImportApplicationService(store)

    result = await service.import_ratings(
        rows=[
            _row(rater_name="First Rater", score=4),
            _row(rater_name="Failed Rater", score=-1),
            _row(rater_name="Last Rater", score=3),
        ]
    )

    assert result.imported == 2
    assert result.updated == 0
    assert result.skipped == 1
    assert result.errors == ["row 2: invalid_import_score"]
    assert set(persistence.raters) == {"First Rater", "Last Rater"}
    assert len(persistence.ratings) == 2
    assert store.commits == 2
    assert store.rollbacks == 1


@pytest.mark.asyncio
async def test_repeated_row_reports_import_then_update() -> None:
    persistence = _ImportData()
    store = _ImportStore(persistence)
    service = RatingImportApplicationService(store)

    result = await service.import_ratings(
        rows=[
            _row(rater_name="Same Rater", score=2),
            _row(rater_name="Same Rater", score=5),
            _row(rater_name="Unknown Packet", score=4, packet_code="missing"),
        ]
    )

    assert result.imported == 1
    assert result.updated == 1
    assert result.skipped == 1
    assert result.errors == ["row 3: unknown packet_code missing"]
    assert store.commits == 2
    assert store.rollbacks == 1
