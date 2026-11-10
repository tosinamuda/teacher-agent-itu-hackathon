"""Item 1: the execution-row lock serializes ops-vs-worker status transitions.

The ops panel (redispatch/cancel) and the worker (claim + terminal write) mutate the same
execution row from DIFFERENT processes. Without a FOR UPDATE lock + a status guard, a
cancel could be lost to (or clobbered by) the worker's terminal SUCCEEDED, a redispatch
could race the worker, and a crashed RUNNING was unrecoverable.

Uses independent committing sessions (one per "process": seeder, worker, ops, rival) so
the commits + rollbacks the production code performs behave exactly as they do live; the
LLM/generation itself is never invoked (we drive _claim/_finalize + ops directly).
"""

from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest
from sqlalchemy import text

from app.domains.experiments.application import execution_lifecycle
from app.domains.experiments.application.condition_retry import retry_failed_condition
from app.domains.experiments.application.create_execution import create_execution
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.domain.types import (
    ConditionedInputsMissingError,
    ExecutionStatus,
    Hypothesis,
)
from app.domains.experiments.infrastructure.execution_context import bind_execution_context
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.infra.jobs.kinds import RUN_CONDITIONED_EXECUTION
from app.infra.jobs.models import Job, JobState
from app.infra.jobs.queue import JobQueue

pytestmark = pytest.mark.asyncio


class _StaleAttemptRepository(ExperimentRepository):
    """Replays an attempt number read before a concurrent winner committed."""

    def __init__(self, session: Any, attempt_number: int) -> None:
        super().__init__(session)
        self._attempt_number = attempt_number

    async def next_attempt_number(
        self,
        *,
        experiment_db_id: uuid.UUID,
        hypothesis: Hypothesis,
    ) -> int:
        del experiment_db_id, hypothesis
        return self._attempt_number


class _StaleAttemptStore:
    """The launch unit of work over a session whose attempt number is already stale."""

    def __init__(self, session: Any, attempt_number: int) -> None:
        self._session = session
        self._repository = _StaleAttemptRepository(session, attempt_number)

    @property
    def executions(self) -> _StaleAttemptRepository:
        return self._repository

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


async def test_stale_attempt_conflict_rolls_back_as_generation_in_progress(
    session_factory, count_rows
) -> None:
    experiment_db_id = uuid.uuid4()
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            Experiment(
                id=experiment_db_id,
                experiment_id="EXP-ATTEMPT-RACE",
                experiment_code="ATTEMPT-RACE-001",
                investigation_db_id=uuid.uuid4(),
                teacher_workspace_id=uuid.uuid4(),
            )
        )
        await seed.commit()

    async with session_factory() as winner, session_factory() as loser:
        winner_attempt = await ExperimentRepository(winner).next_attempt_number(
            experiment_db_id=experiment_db_id,
            hypothesis=Hypothesis.H1,
        )
        loser_attempt = await ExperimentRepository(loser).next_attempt_number(
            experiment_db_id=experiment_db_id,
            hypothesis=Hypothesis.H1,
        )
        assert winner_attempt == loser_attempt == 1

        await create_execution(
            _StaleAttemptStore(winner, winner_attempt),
            experiment_db_id=experiment_db_id,
            hypothesis=Hypothesis.H1,
            runtime_snapshot=None,
        )
        await winner.commit()

        with pytest.raises(ExperimentApplicationError) as raised:
            await create_execution(
                _StaleAttemptStore(loser, loser_attempt),
                experiment_db_id=experiment_db_id,
                hypothesis=Hypothesis.H1,
                runtime_snapshot=None,
            )

        assert raised.value.status_code == 409
        assert raised.value.detail == "generation_already_in_progress"
        assert await loser.scalar(text("SELECT 1")) == 1

    assert await count_rows(ExperimentExecution, experiment_db_id=experiment_db_id) == 1


async def _seed(
    session_factory: Any, status: ExecutionStatus, *, with_partial: bool = False
) -> str:
    execution_id = f"EXE-{uuid.uuid4().hex[:8]}"
    execution_db_id = uuid.uuid4()
    async with session_factory() as s:
        await s.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        await s.execute(
            text(
                "INSERT INTO experiment_executions "
                "(id, execution_id, experiment_db_id, hypothesis, attempt_number, status) "
                "VALUES (:id, :eid, :exp, :hyp, 1, :st)"
            ),
            {
                "id": execution_db_id.hex,
                "eid": execution_id,
                "exp": execution_db_id.hex,  # FK off; value is irrelevant to these tests
                "hyp": Hypothesis.H1.value,
                "st": status.value,
            },
        )
        if with_partial:
            s.add(
                ExperimentConditionRun(
                    experiment_condition_run_id=f"RUN-{uuid.uuid4().hex[:8]}",
                    execution_db_id=execution_db_id,
                    hypothesis=Hypothesis.H1.value,
                    condition_code="C0",
                    status="failed",
                )
            )
        await s.commit()
    return execution_id


async def _status(session_factory: Any, execution_id: str) -> ExecutionStatus | None:
    async with session_factory() as s:
        execution = await ExperimentRepository(s).get_execution(execution_id)
        return execution.status if execution is not None else None


async def _partial_count(session_factory: Any, count_rows: Any, execution_id: str) -> int:
    # Resolve the db id, then count its condition runs.
    async with session_factory() as s:
        db_id = await s.scalar(
            text("SELECT experiment_db_id FROM experiment_executions WHERE execution_id=:e"),
            {"e": execution_id},
        )
    return await count_rows(ExperimentConditionRun, execution_db_id=uuid.UUID(db_id))


# --- worker claim (re-entrancy + double-dispatch guard) ---


async def test_claim_skips_terminal_execution(session_factory) -> None:
    execution_id = await _seed(session_factory, ExecutionStatus.SUCCEEDED)
    async with session_factory() as s:
        store = bind_execution_context(s).store
        assert (
            await execution_lifecycle.claim_execution(store, execution_id, redelivered=False)
            is None
        )
    assert await _status(session_factory, execution_id) == ExecutionStatus.SUCCEEDED


async def test_claim_flips_queued_to_running_and_clears_partial(
    session_factory, count_rows
) -> None:
    execution_id = await _seed(session_factory, ExecutionStatus.QUEUED, with_partial=True)
    async with session_factory() as s:
        claimed = await execution_lifecycle.claim_execution(
            bind_execution_context(s).store, execution_id, redelivered=False
        )
        assert claimed is not None and claimed.status == ExecutionStatus.RUNNING
    assert await _status(session_factory, execution_id) == ExecutionStatus.RUNNING
    # The stale condition run was cleared at claim so the re-run can't duplicate it.
    assert await _partial_count(session_factory, count_rows, execution_id) == 0


async def test_a_fresh_delivery_never_takes_over_a_running_execution(
    session_factory, count_rows
) -> None:
    # A second dispatch of a still-RUNNING execution must NOT claim it: claiming clears the
    # generated output, so two workers generating at once lose each other's condition runs
    # and the survivor finalizes SUCCEEDED with nothing recorded. Only a redelivery may take
    # over, because the broker restores a message only once its owner is gone.
    execution_id = await _seed(session_factory, ExecutionStatus.RUNNING, with_partial=True)
    async with session_factory() as s:
        assert (
            await execution_lifecycle.claim_execution(
                bind_execution_context(s).store, execution_id, redelivered=False
            )
            is None
        )
    assert await _partial_count(session_factory, count_rows, execution_id) == 1  # left alone


async def test_a_redelivery_takes_over_a_running_execution(session_factory, count_rows) -> None:
    # The other half of the rule: the previous owner crashed (acks_late + reject_on_worker_lost
    # redelivered the message), so the row is RUNNING with nobody behind it. Taking it over is
    # what recovers a SIGKILLed worker's execution instead of stranding it.
    execution_id = await _seed(session_factory, ExecutionStatus.RUNNING, with_partial=True)
    async with session_factory() as s:
        claimed = await execution_lifecycle.claim_execution(
            bind_execution_context(s).store, execution_id, redelivered=True
        )
        assert claimed is not None
    assert await _status(session_factory, execution_id) == ExecutionStatus.RUNNING
    assert await _partial_count(session_factory, count_rows, execution_id) == 0  # cleared


# --- worker terminal-write guard ---


async def test_finalize_discards_committed_runs_when_no_longer_running(
    session_factory, count_rows
) -> None:
    # run_h1/run_h2 COMMIT condition runs DURING generation, so a stale finalize must actually
    # CLEAR them — not just roll back the status flip — or they orphan under the cancelled
    # execution and stay visible/exportable. Seed a committed condition run to prove the clear.
    execution_id = await _seed(session_factory, ExecutionStatus.RUNNING, with_partial=True)
    # A concurrent cancel committed FAILED while the worker was generating.
    async with session_factory() as s:
        await s.execute(
            text(
                "UPDATE experiment_executions SET status='failed', error_category='cancelled' "
                "WHERE execution_id=:e"
            ),
            {"e": execution_id},
        )
        await s.commit()
    # The worker tries to write SUCCEEDED — must detect status != RUNNING and discard.
    async with session_factory() as s:
        await execution_lifecycle.finalize_execution(
            bind_execution_context(s).store,
            execution_id,
            status=ExecutionStatus.SUCCEEDED,
        )
    assert (
        await _status(session_factory, execution_id) == ExecutionStatus.FAILED
    )  # cancel preserved
    assert await _partial_count(session_factory, count_rows, execution_id) == 0  # orphans cleared


async def test_clear_execution_generation_handles_h2_focal_case_fk(
    session_factory, count_rows
) -> None:
    # An H2 condition run carries focal_case_db_id → experiment_focal_cases.id (no ON DELETE
    # cascade). clear MUST delete the condition run before the focal case it references, or it
    # FK-violates (errno 1451). Runs with FK checks ON (a fresh session), so a wrong order crashes.
    execution_id = await _seed(session_factory, ExecutionStatus.FAILED)
    async with session_factory() as s:
        db_id = await s.scalar(
            text("SELECT experiment_db_id FROM experiment_executions WHERE execution_id=:e"),
            {"e": execution_id},
        )
        await s.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        focal_id = uuid.uuid4().hex
        await s.execute(
            text(
                "INSERT INTO experiment_focal_cases "
                "(id, experiment_focal_case_id, execution_db_id, student_id, focal_case_type, "
                "learner_state_snapshot, created_at) "
                "VALUES (:id, :fid, :exec, 'ST-X', 'median', '{}', NOW())"
            ),
            {"id": focal_id, "fid": f"FC-{focal_id[:8]}", "exec": db_id},
        )
        s.add(
            ExperimentConditionRun(
                experiment_condition_run_id=f"RUN-{focal_id[:8]}",
                execution_db_id=uuid.UUID(db_id),
                hypothesis=Hypothesis.H2.value,
                condition_code="P1",
                status="succeeded",
                focal_case_db_id=uuid.UUID(focal_id),
            )
        )
        await s.commit()

    async with session_factory() as s:
        await ExperimentRepository(s).clear_execution_generation(uuid.UUID(db_id))
        await s.commit()

    assert await _partial_count(session_factory, count_rows, execution_id) == 0  # run gone
    async with session_factory() as s:
        focal_left = await s.scalar(
            text("SELECT COUNT(*) FROM experiment_focal_cases WHERE execution_db_id=:e"),
            {"e": db_id},
        )
    assert focal_left == 0  # focal case gone, no FK crash


async def test_finalize_writes_terminal_when_still_running(session_factory) -> None:
    execution_id = await _seed(session_factory, ExecutionStatus.RUNNING)
    async with session_factory() as s:
        await execution_lifecycle.finalize_execution(
            bind_execution_context(s).store,
            execution_id,
            status=ExecutionStatus.SUCCEEDED,
        )
    assert await _status(session_factory, execution_id) == ExecutionStatus.SUCCEEDED


# --- ops cancel / redispatch status guard ---


async def test_ops_cancel_is_noop_on_terminal_execution(session_factory) -> None:
    from app.domains.ops.application import execution_ops

    execution_id = await _seed(session_factory, ExecutionStatus.SUCCEEDED)
    async with session_factory() as s:
        result = await execution_ops.cancel(s, execution_id)
    assert result["ok"] is True and result["status"] == ExecutionStatus.SUCCEEDED.value
    assert await _status(session_factory, execution_id) == ExecutionStatus.SUCCEEDED  # not flipped


async def test_ops_cancel_fails_a_running_execution_and_clears_its_runs(
    session_factory, count_rows
) -> None:
    from app.domains.ops.application import execution_ops

    # A RUNNING execution whose generation already committed condition runs (the real shape:
    # run_h1/run_h2 commit incrementally). cancel must flip to FAILED AND clear the committed
    # runs, so a cancelled execution leaves no orphans (not just the status).
    execution_id = await _seed(session_factory, ExecutionStatus.RUNNING, with_partial=True)
    async with session_factory() as s:
        await JobQueue(s).submit(RUN_CONDITIONED_EXECUTION, execution_id, subject=execution_id)
    async with session_factory() as s:
        result = await execution_ops.cancel(s, execution_id)
    assert result["status"] == ExecutionStatus.FAILED.value
    assert len(result["cancelled_job_ids"]) == 1
    assert await _status(session_factory, execution_id) == ExecutionStatus.FAILED
    assert await _partial_count(session_factory, count_rows, execution_id) == 0  # runs cleared
    assert await count_rows(Job, subject=execution_id, state=JobState.CANCELLED) == 1


async def test_ops_redispatch_clears_and_requeues(session_factory, count_rows) -> None:
    from app.domains.ops.application import execution_ops

    execution_id = await _seed(session_factory, ExecutionStatus.FAILED, with_partial=True)
    async with session_factory() as s:
        await JobQueue(s).submit(RUN_CONDITIONED_EXECUTION, execution_id, subject=execution_id)
    async with session_factory() as s:
        result = await execution_ops.redispatch(s, execution_id)
    assert result["status"] == ExecutionStatus.QUEUED.value
    assert await _status(session_factory, execution_id) == ExecutionStatus.QUEUED
    assert await _partial_count(session_factory, count_rows, execution_id) == 0  # cleared
    # The old job is cancelled and a fresh one queued, in the same commit.
    assert await count_rows(Job, subject=execution_id, state=JobState.CANCELLED) == 1
    assert await count_rows(Job, subject=execution_id, state=JobState.QUEUED) == 1


async def test_get_execution_for_update_returns_fresh_status(session_factory) -> None:
    # populate_existing: a cached RUNNING object must reflect the DB's current status on the
    # next locked read in the SAME session (the worker's finalize guard relies on this).
    execution_id = await _seed(session_factory, ExecutionStatus.RUNNING)
    async with session_factory() as worker:
        repo = ExperimentRepository(worker)
        cached = await repo.get_execution_for_update(execution_id)
        assert cached is not None and cached.status == ExecutionStatus.RUNNING
        await worker.commit()  # release the lock so the rival can update
        async with session_factory() as rival:
            await rival.execute(
                text("UPDATE experiment_executions SET status='failed' WHERE execution_id=:e"),
                {"e": execution_id},
            )
            await rival.commit()
        refreshed = await repo.get_execution_for_update(execution_id)
        assert refreshed is not None and refreshed.status == ExecutionStatus.FAILED


# --- retry path serializes on the execution lock (vs ops redispatch) ---


async def test_retry_serializes_against_a_concurrent_lock_holder(session_factory) -> None:
    # retry_failed_condition must take the execution FOR UPDATE lock so its
    # delete+reinsert can't interleave with an ops redispatch's clear + re-run on the SAME
    # execution (which would duplicate (execution_db_id, condition_code) rows — there's no DB
    # unique on that pair). Prove retry takes the lock: while a rival (the redispatch / the
    # worker) holds it, retry can't proceed; once released it does — then fails on the unseeded
    # experiment, which proves it got PAST the lock rather than skipping it (the old plain-read
    # retry would NOT have blocked).
    # retry_failed_condition opens the APP engine (AsyncSessionLocal) on this loop; dispose its
    # pool afterwards so a pooled connection can't leak into a later test's own event loop (the
    # run_in_worker loop-safety test), mirroring run_in_worker's per-task dispose.
    from app.db.session import engine

    execution_id = await _seed(session_factory, ExecutionStatus.FAILED)
    try:
        async with session_factory() as holder:
            locked = await ExperimentRepository(holder).get_execution_for_update(execution_id)
            assert locked is not None  # rival holds the row lock in an open transaction

            task = asyncio.create_task(retry_failed_condition(execution_id, "C0"))
            await asyncio.sleep(1.0)
            assert not task.done()  # blocked on the lock (the fix); a plain read would not block

            await holder.rollback()  # release the lock

        # Past the lock now → fails on the unseeded experiment/plan (got past the lock).
        with pytest.raises(ConditionedInputsMissingError):
            await asyncio.wait_for(task, timeout=15)
    finally:
        await engine.dispose()
