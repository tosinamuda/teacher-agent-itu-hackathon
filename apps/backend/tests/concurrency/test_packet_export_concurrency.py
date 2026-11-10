"""MySQL concurrency and transaction contracts for evaluation packet export."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.packet_export_service import (
    PacketExportApplicationService,
)
from app.domains.experiments.domain import (
    ConditionCode,
    ConditionRunStatus,
    ExecutionStatus,
    Hypothesis,
    PacketStatus,
)
from app.domains.experiments.infrastructure.models import (
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)

pytestmark = pytest.mark.asyncio


async def _seed_h1_export(session_factory, *, current_packets: bool) -> tuple[str, uuid.UUID]:
    tag = uuid.uuid4().hex[:8]
    async with session_factory() as session:
        await session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        execution = ExperimentExecution(
            execution_id=f"EXE-{tag}",
            experiment_db_id=uuid.uuid4(),
            hypothesis=Hypothesis.H1.value,
            attempt_number=1,
            status=ExecutionStatus.SUCCEEDED,
        )
        session.add(execution)
        await session.flush()

        runs = [
            ExperimentConditionRun(
                experiment_condition_run_id=f"RUN-{tag}-{code.value}",
                execution_db_id=execution.id,
                hypothesis=Hypothesis.H1.value,
                condition_code=code.value,
                status=ConditionRunStatus.SUCCEEDED,
            )
            for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3)
        ]
        session.add_all(runs)
        session.add_all(
            Artefact(
                artefact_id=f"ART-{tag}-{index}",
                artefact_type="post_class_review_pack",
                scope="class",
                plan_version_id=f"LPV-{tag}",
                experiment_condition_run_id=run.experiment_condition_run_id,
                manifest={},
            )
            for index, run in enumerate(runs)
        )
        if current_packets:
            session.add_all(
                EvaluationPacket(
                    evaluation_packet_id=f"EPK-{tag}-{index}",
                    execution_db_id=execution.id,
                    packet_code=f"PKT-{tag}-{index}",
                    hypothesis=Hypothesis.H1.value,
                    status=PacketStatus.READY.value,
                    primary_condition_run_id=run.experiment_condition_run_id,
                    condition_run_ids=[run.experiment_condition_run_id],
                )
                for index, run in enumerate(runs)
            )
        else:
            stale_packet = EvaluationPacket(
                evaluation_packet_id=f"EPK-{tag}-stale",
                execution_db_id=execution.id,
                packet_code=f"PKT-{tag}-stale",
                hypothesis=Hypothesis.H1.value,
                status=PacketStatus.READY.value,
                primary_condition_run_id="RUN-STALE",
                condition_run_ids=["RUN-STALE"],
            )
            session.add(stale_packet)
            await session.flush()
            rater = EvaluationRater(
                rater_id=f"EVR-{tag}",
                display_name=f"Synthetic {tag}",
                user_id=None,
            )
            session.add(rater)
            await session.flush()
            session.add(
                EvaluationRating(
                    rating_id=f"RT-{tag}",
                    evaluation_packet_db_id=stale_packet.id,
                    rater_db_id=rater.id,
                    hypothesis=Hypothesis.H1.value,
                    overall_score=4.0,
                    rubric_scores={},
                )
            )
        await session.commit()
        return execution.execution_id, execution.id


async def test_concurrent_current_exports_serialize_and_reuse_one_packet_set(
    session_factory,
    run_race,
) -> None:
    execution_id, execution_db_id = await _seed_h1_export(
        session_factory,
        current_packets=True,
    )

    async def export(session, _index):
        return await PacketExportApplicationService(
            SqlAlchemyExperimentStore(session)
        ).export_packets(execution_id=execution_id)

    outcome = await run_race(export, lambda _error: False, n=2)

    assert outcome.others == []
    assert [len(packets) for packets in outcome.wins] == [4, 4]
    async with session_factory() as check:
        packet_count = await check.scalar(
            select(func.count())
            .select_from(EvaluationPacket)
            .where(EvaluationPacket.execution_db_id == execution_db_id)
        )
    assert packet_count == 4


async def test_failed_replacement_restores_previous_packets_and_ratings(
    session_factory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    execution_id, execution_db_id = await _seed_h1_export(
        session_factory,
        current_packets=False,
    )
    monkeypatch.setattr(
        "app.domains.experiments.application.packet_export_service.new_public_id",
        lambda _prefix: "DUPLICATE-PACKET-ID",
    )

    async with session_factory() as work:
        with pytest.raises(IntegrityError):
            await PacketExportApplicationService(SqlAlchemyExperimentStore(work)).export_packets(
                execution_id=execution_id
            )

    async with session_factory() as check:
        packet_count = await check.scalar(
            select(func.count())
            .select_from(EvaluationPacket)
            .where(EvaluationPacket.execution_db_id == execution_db_id)
        )
        rating_count = await check.scalar(select(func.count()).select_from(EvaluationRating))
    assert packet_count == 1
    assert rating_count == 1


async def test_real_rating_guard_rolls_back_without_destroying_rows(session_factory) -> None:
    execution_id, execution_db_id = await _seed_h1_export(
        session_factory,
        current_packets=False,
    )
    async with session_factory() as bind_real_rater:
        await bind_real_rater.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        rating = (await bind_real_rater.execute(select(EvaluationRating))).scalars().one()
        rater = await bind_real_rater.get(EvaluationRater, rating.rater_db_id)
        assert rater is not None
        rater.user_id = uuid.uuid4()
        await bind_real_rater.commit()

    async with session_factory() as work:
        with pytest.raises(ExperimentApplicationError) as excinfo:
            await PacketExportApplicationService(SqlAlchemyExperimentStore(work)).export_packets(
                execution_id=execution_id
            )
    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == "reexport_blocked_expert_ratings_exist"

    async with session_factory() as check:
        packet_count = await check.scalar(
            select(func.count())
            .select_from(EvaluationPacket)
            .where(EvaluationPacket.execution_db_id == execution_db_id)
        )
        rating_count = await check.scalar(select(func.count()).select_from(EvaluationRating))
    assert packet_count == 1
    assert rating_count == 1
