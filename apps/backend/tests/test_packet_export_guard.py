"""Regression: re-export must protect REAL expert ratings, not synthetic dry-run ones.

A re-export replaces the stale packet set and cascades the delete to the packets'
ratings. Synthetic dry-run raters have ``user_id IS NULL`` (disposable); real
onboarded raters have ``user_id`` set, and their ratings must never be silently
destroyed. ``count_real_ratings_for_packets`` is the guard that distinguishes them
(``export_packets`` raises 409 when it returns > 0). Runs against the MySQL test DB.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text

from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
)
from app.domains.experiments.domain import PacketStatus
from app.domains.experiments.infrastructure.repository import ExperimentRepository

pytestmark = pytest.mark.asyncio


def _rater(*, real: bool) -> EvaluationRater:
    tag = uuid.uuid4().hex[:8]
    return EvaluationRater(
        rater_id=f"EVR-{tag}",
        display_name=f"{'real' if real else 'syn'}-{tag}",
        user_id=uuid.uuid4() if real else None,  # real raters are bound to a user
    )


async def _rating(db, packet: EvaluationPacket, rater: EvaluationRater) -> None:
    db.add(rater)
    await db.flush()
    db.add(
        EvaluationRating(
            rating_id=f"RT-{uuid.uuid4().hex[:8]}",
            evaluation_packet_db_id=packet.id,
            rater_db_id=rater.id,
            hypothesis="H1",
            overall_score=4.0,
            rubric_scores={},
        )
    )
    await db.flush()


async def _seed_packet(db) -> EvaluationPacket:
    # FK checks off: execution_db_id's target is irrelevant to the guard query.
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    packet = EvaluationPacket(
        evaluation_packet_id=f"ECR-{uuid.uuid4().hex[:8]}",
        execution_db_id=uuid.uuid4(),
        packet_code=f"PKT-{uuid.uuid4().hex[:8]}",
        hypothesis="H1",
        status=PacketStatus.READY.value,
        primary_condition_run_id="run-x",
        condition_run_ids=["run-x"],
    )
    db.add(packet)
    await db.flush()
    return packet


async def test_guard_counts_only_real_rater_ratings(db) -> None:
    packet = await _seed_packet(db)
    await _rating(db, packet, _rater(real=True))
    await _rating(db, packet, _rater(real=False))  # synthetic — must be ignored

    count = await ExperimentRepository(db).count_real_ratings_for_packets(packet_ids=[packet.id])
    assert count == 1


async def test_guard_zero_when_only_synthetic(db) -> None:
    packet = await _seed_packet(db)
    await _rating(db, packet, _rater(real=False))

    count = await ExperimentRepository(db).count_real_ratings_for_packets(packet_ids=[packet.id])
    assert count == 0  # disposable dry-run ratings → re-export stays allowed
