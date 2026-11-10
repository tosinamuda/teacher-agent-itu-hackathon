"""Concurrent offline-rating import converges instead of crashing the batch.

``import_ratings`` resolves each row's rater by display name (unique) and upserts a
rating (unique per packet+rater). Both are check-then-insert, and the loop only
caught ``EvaluationApplicationError`` — so a concurrent import (or one racing the
interactive save) tripped a unique index, raised an unhandled ``IntegrityError``,
500'd, and aborted the rest of the batch with a poisoned session.

Invariant under real concurrency: N imports of the SAME row converge — exactly one
rater, exactly one rating, no escaped error.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text

from app.domains.evaluation.application.rating_import_service import (
    OfflineRatingRow,
    RatingImportApplicationService,
)
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
)
from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
    SqlAlchemyEvaluationStore,
)
from app.domains.experiments.domain import PacketStatus

pytestmark = pytest.mark.asyncio

_N = 6


async def test_concurrent_import_same_rater_and_rating_converges(
    run_race, count_rows, session_factory
) -> None:
    # Seed one packet to import against (FK checks off — execution_db_id target
    # is irrelevant to the import path).
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        packet = EvaluationPacket(
            evaluation_packet_id="ECR-IMPORT",
            execution_db_id=uuid.uuid4(),
            packet_code="PKT-IMPORT",
            hypothesis="H1",
            status=PacketStatus.READY.value,
            primary_condition_run_id="run-x",
            condition_run_ids=["run-x"],
        )
        seed.add(packet)
        await seed.commit()
        packet_id = packet.id

    row = OfflineRatingRow(
        packet_code="PKT-IMPORT",
        rater_name="Concurrent Rater",
        overall_score=4.0,
        rubric_scores={"clarity": 4},
    )

    async def op(session, _i):
        return await RatingImportApplicationService(
            SqlAlchemyEvaluationStore(session)
        ).import_ratings(rows=[row])

    # Every import should converge (no error expected) — the dup rater/rating races
    # resolve to the winner's rows.
    out = await run_race(op, lambda _e: False, n=_N)

    assert out.others == [], f"import raised under concurrency: {out.others}"
    assert len(out.wins) == _N
    assert await count_rows(EvaluationRater, display_name="Concurrent Rater") == 1
    assert await count_rows(EvaluationRating, evaluation_packet_db_id=packet_id) == 1
