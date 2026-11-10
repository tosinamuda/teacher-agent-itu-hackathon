"""Poison-message redelivery bound on the durable tasks.

acks_late + reject_on_worker_lost redelivers a task that crashes the worker; left
unbounded, a task that crashes EVERY time loops forever and wedges the single solo
worker. The claim increments ``delivery_count`` and, past ``MAX_TASK_DELIVERIES``,
marks the row FAILED (error_category="poison") and skips — so the loop terminates.

We simulate redeliveries by claiming the same row from successive sessions without
ever finalizing it (a crashed run never reaches finalize).
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select, text

from app.domains.artefacts.types.post_class_review_pack.domain.types import (
    StudentPackGenerationStatus,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.repository import (
    StudentPackGenerationRepository,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_generation_job_service,
)
from app.domains.experiments.application.execution_lifecycle import claim_execution
from app.domains.experiments.domain.types import ExecutionStatus
from app.domains.experiments.infrastructure.execution_context import bind_execution_context
from app.domains.experiments.infrastructure.models import ExperimentExecution
from app.shared.worker_delivery import MAX_TASK_DELIVERIES

pytestmark = pytest.mark.asyncio


async def test_execution_claim_poison_bounds_after_max_deliveries(session_factory) -> None:
    execution_id = "EXE-poison"
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            ExperimentExecution(
                execution_id=execution_id,
                experiment_db_id=uuid.uuid4(),
                hypothesis="H1",
                attempt_number=1,
                status=ExecutionStatus.QUEUED,
            )
        )
        await seed.commit()

    # Up to MAX_TASK_DELIVERIES crashed redeliveries are taken over and re-run. Only the
    # first is a fresh delivery; the rest find the row RUNNING and are entitled to take it
    # over because the broker restored the message (its previous owner crashed).
    for attempt in range(1, MAX_TASK_DELIVERIES + 1):
        async with session_factory() as worker:
            claimed = await claim_execution(
                bind_execution_context(worker).store, execution_id, redelivered=attempt > 1
            )
            assert claimed is not None, f"delivery {attempt} should still run"

    # The next redelivery is poison: claim refuses it and marks the execution FAILED.
    async with session_factory() as worker:
        assert (
            await claim_execution(
                bind_execution_context(worker).store, execution_id, redelivered=True
            )
            is None
        )

    async with session_factory() as check:
        row = (
            await check.execute(
                select(ExperimentExecution).where(ExperimentExecution.execution_id == execution_id)
            )
        ).scalar_one()
        assert row.status == ExecutionStatus.FAILED
        assert row.error_category == "poison"
        assert row.delivery_count == MAX_TASK_DELIVERIES + 1


async def test_student_pack_claim_poison_bounds_after_max_deliveries(session_factory) -> None:
    jobs = build_generation_job_service()
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            StudentPackGeneration(
                generation_id="SPG-poison",
                student_id="ST-poison",
                plan_version_id="LPV-poison",
                attempt_number=1,
                status=StudentPackGenerationStatus.QUEUED,
            )
        )
        await seed.commit()

    for attempt in range(1, MAX_TASK_DELIVERIES + 1):
        async with session_factory() as worker:
            assert await jobs.claim(worker, "SPG-poison") is not None, f"delivery {attempt} runs"

    async with session_factory() as worker:
        assert await jobs.claim(worker, "SPG-poison") is None  # poison

    async with session_factory() as check:
        row = await StudentPackGenerationRepository().get(check, "SPG-poison")
        assert row is not None
        assert row.status == StudentPackGenerationStatus.FAILED
        assert row.error_category == "poison"
        assert row.delivery_count == MAX_TASK_DELIVERIES + 1
