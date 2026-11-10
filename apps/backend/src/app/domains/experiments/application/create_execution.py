"""Create the execution row one generation attempt is tracked by."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.launch_ports import ExecutionLaunchStore
from app.domains.experiments.domain import ExecutionStatus, Hypothesis
from app.domains.experiments.infrastructure.models import ExperimentExecution
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.time import utc_now


async def create_execution(
    store: ExecutionLaunchStore,
    *,
    experiment_db_id: UUID,
    hypothesis: Hypothesis,
    runtime_snapshot: JsonObject | None,
) -> ExperimentExecution:
    """Stage a CREATED execution row under the next attempt number."""
    attempt_number = await store.executions.next_attempt_number(
        experiment_db_id=experiment_db_id, hypothesis=hypothesis
    )
    try:
        return await store.executions.stage_execution(
            ExperimentExecution(
                execution_id=new_public_id(PublicIdPrefix.EXPERIMENT_EXECUTION),
                experiment_db_id=experiment_db_id,
                hypothesis=hypothesis.value,
                attempt_number=attempt_number,
                status=ExecutionStatus.CREATED,
                runtime_snapshot=runtime_snapshot,
                error_message=None,
                created_at=utc_now(),
                updated_at=utc_now(),
            ),
        )
    except IntegrityError as exc:
        # A concurrent create won the (experiment, hypothesis, attempt) race — the
        # in-flight check and the unique constraint disagree only under that race.
        # Treat the loser as "already in progress" (its 409), not a duplicate
        # attempt or a 500.
        await store.rollback()
        raise ExperimentApplicationError(409, "generation_already_in_progress") from exc
