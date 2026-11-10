"""Behavior contract for the experiment execution-results query."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any, cast

import pytest

from app.domains.experiments.application.results_summary_query import (
    ExperimentResultsSummaryQuery,
    ResultsSummaryReader,
)


class _ResultsReader:
    def __init__(self) -> None:
        self.execution = SimpleNamespace(
            id=uuid.uuid4(),
            execution_id="EXE-results",
            hypothesis="H1",
            attempt_number=2,
            status="succeeded",
        )
        self.run = SimpleNamespace(
            experiment_condition_run_id="ECR-c4",
            condition_code="C4",
            status="succeeded",
            student_id=None,
            artefact_plan_id="ARP-base",
            artefact_build_job_id="ABJ-base",
            error_message=None,
        )
        self.packet = SimpleNamespace(
            evaluation_packet_id="EVP-results",
            packet_code="PKT-results",
            status="ready",
            primary_condition_run_id="ECR-c4",
            experiment_focal_case_id=None,
            condition_run_ids=["ECR-c4"],
        )

    async def get_execution(self, execution_id: str) -> Any:
        return self.execution if execution_id == self.execution.execution_id else None

    async def list_condition_runs(self, execution_db_id: uuid.UUID) -> list[Any]:
        return [self.run]

    async def list_focal_cases(self, execution_db_id: uuid.UUID) -> list[Any]:
        return []

    async def list_packets(self, execution_db_id: uuid.UUID) -> list[Any]:
        return [self.packet]

    async def current_artefacts_by_condition_run(self, run_ids: list[str]) -> dict[str, Any]:
        return {"ECR-c4": SimpleNamespace(artefact_id="AT-c4")}


@pytest.mark.asyncio
async def test_results_summary_preserves_counts_statuses_and_current_artefact_ids() -> None:
    reader = _ResultsReader()

    summary = await ExperimentResultsSummaryQuery(
        cast(ResultsSummaryReader, reader)
    ).build_results_summary(execution_id="EXE-results")

    assert summary.execution_id == "EXE-results"
    assert summary.attempt_number == 2
    assert summary.condition_run_count == 1
    assert summary.focal_case_count == 0
    assert summary.packet_count == 1
    assert summary.status_counts == {"succeeded": 1}
    assert summary.condition_runs[0]["artefact_id"] == "AT-c4"
    assert summary.packets[0]["condition_run_ids"] == ["ECR-c4"]
