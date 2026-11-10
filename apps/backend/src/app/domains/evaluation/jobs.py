"""The evaluation jobs: synthetic rating, synthetic teacher review, and the loop of both.

Browser-triggered and multi-call (one judge call per packet x persona), so each runs as a
best-effort job reporting progress on the experiment's channel.
"""

from __future__ import annotations

import logging

from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def synthetic_rate(experiment_id: str, personas: list[str] | None = None) -> None:
    from app.domains.evaluation.application.synthetic_rater import rate_experiment
    from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
        SqlAlchemyEvaluationStore,
    )
    from app.domains.experiments.application.synthetic_progress import (
        publish_synthetic_progress,
    )

    def on_progress(event: dict) -> None:
        publish_synthetic_progress(experiment_id, {**event, "flow": "ratings"})

    async with AsyncSessionLocal() as db:
        try:
            await rate_experiment(
                db,
                identity_store=SqlAlchemyEvaluationStore(db),
                experiment_id=experiment_id,
                personas=personas,
                on_progress=on_progress,
            )
        except Exception:  # noqa: BLE001 - best-effort; never crash the worker
            logger.exception("synthetic rating failed: experiment=%s", experiment_id)
            on_progress({"type": "error", "phase": "ratings", "message": "synthetic rating failed"})


async def synthetic_teacher(experiment_id: str, max_rounds: int = 2) -> None:
    from app.domains.evaluation.application.synthetic_teacher import review_experiment
    from app.domains.experiments.application.synthetic_progress import (
        publish_synthetic_progress,
    )

    def on_progress(event: dict) -> None:
        publish_synthetic_progress(experiment_id, {**event, "flow": "teacher_review"})

    async with AsyncSessionLocal() as db:
        try:
            await review_experiment(
                db, experiment_id=experiment_id, max_rounds=max_rounds, on_progress=on_progress
            )
        except Exception:  # noqa: BLE001 - best-effort; never crash the worker
            logger.exception("synthetic teacher review failed: experiment=%s", experiment_id)
            on_progress(
                {"type": "error", "phase": "teacher_review", "message": "synthetic teacher failed"}
            )


async def synthetic_loop(
    experiment_id: str, max_rounds: int = 2, personas: list[str] | None = None
) -> None:
    from app.domains.evaluation.application.synthetic_loop import run_synthetic_loop
    from app.domains.evaluation.infrastructure.sqlalchemy_evaluation_store import (
        SqlAlchemyEvaluationStore,
    )
    from app.domains.experiments.application.synthetic_progress import (
        publish_synthetic_progress,
    )
    from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
        SqlAlchemyExperimentStore,
    )

    def on_progress(event: dict) -> None:
        publish_synthetic_progress(experiment_id, {"flow": event.get("phase", "loop"), **event})

    async with AsyncSessionLocal() as db:
        try:
            await run_synthetic_loop(
                db,
                identity_store=SqlAlchemyEvaluationStore(db),
                packet_export_store=SqlAlchemyExperimentStore(db),
                experiment_id=experiment_id,
                max_rounds=max_rounds,
                personas=personas,
                on_progress=on_progress,
            )
        except Exception:  # noqa: BLE001 - best-effort; never crash the worker
            logger.exception("synthetic loop failed: experiment=%s", experiment_id)
            on_progress({"type": "error", "phase": "loop", "message": "synthetic loop failed"})
