"""The API sends every moment with its UTC offset.

MySQL's DATETIME reads back naive. Sent without an offset, a browser reads the time as
its own local time, and a page two hours east of UTC says an action a minute old
happened two hours ago.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.domains.experiments.api.schemas import ExperimentExecutionResponse
from app.domains.experiments.api.workflow_schemas import WorkflowItemResponse
from app.domains.experiments.domain.types import ExecutionStatus, Hypothesis


def _execution(moment: datetime) -> ExperimentExecutionResponse:
    return ExperimentExecutionResponse(
        execution_id="ex-1",
        experiment_id="exp-1",
        hypothesis=Hypothesis.H1,
        attempt_number=1,
        status=ExecutionStatus.SUCCEEDED,
        created_at=moment,
        updated_at=moment,
    )


def test_a_stored_moment_is_sent_as_utc() -> None:
    body = WorkflowItemResponse(
        id="h1", label="H1", status="done", timestamp=datetime(2026, 9, 27, 14, 5)
    ).model_dump(mode="json")

    assert body["timestamp"] == "2026-09-27T14:05:00Z"


def test_a_moment_with_an_offset_keeps_it() -> None:
    cest = timezone(timedelta(hours=2))
    body = WorkflowItemResponse(
        id="h1", label="H1", status="done", timestamp=datetime(2026, 9, 27, 16, 5, tzinfo=cest)
    ).model_dump(mode="json")

    assert body["timestamp"] == "2026-09-27T16:05:00+02:00"


def test_an_execution_is_sent_as_utc() -> None:
    body = _execution(datetime(2026, 9, 27, 14, 5)).model_dump(mode="json")

    assert body["created_at"] == body["updated_at"] == "2026-09-27T14:05:00Z"
