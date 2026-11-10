"""Resolve and publish progress for one conditioned experiment execution."""

from __future__ import annotations

import logging
import uuid
from typing import Protocol

from app.domains.experiments.application.synthetic_progress import publish_synthetic_progress
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.domains.experiments.review_pack_study.progress import ProgressSink
from app.shared.json_types import JsonObject

logger = logging.getLogger(__name__)


class ExecutionProgressReader(Protocol):
    """Resolve the public experiment identity used by progress subscribers."""

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...


async def progress_publisher(
    experiments: ExecutionProgressReader,
    execution: ExperimentExecution,
) -> ProgressSink:
    """Publish live generation progress, or discard it when its experiment vanished."""
    experiment = await experiments.get_experiment_by_db_id(execution.experiment_db_id)
    if experiment is None:
        logger.warning(
            "execution %s has no experiment row; publishing no progress",
            execution.execution_id,
        )
        return discard_progress

    def publish(event: JsonObject) -> None:
        publish_synthetic_progress(experiment.experiment_id, {**event, "flow": "generation"})

    return publish


def discard_progress(event: JsonObject) -> None:
    """Drop progress nobody can be subscribed to."""
