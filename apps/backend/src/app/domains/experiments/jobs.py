"""The experiments job a teacher starts: drafting the experiment's own plan."""

from __future__ import annotations

from app.db.session import AsyncSessionLocal
from app.domains.content.infrastructure.wiring import build_plan_generator
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_authoring import bind_experiment_plan_version
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)
from app.shared.json_types import JsonObject


async def draft_experiment_plan(experiment_id: str) -> JsonObject:
    """Draft the experiment's own plan on its lesson and bind it; say which version it is."""
    async with AsyncSessionLocal() as db:
        experiment = await ExperimentRepository(db).get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if experiment.lesson_period_id is None:
            raise ExperimentApplicationError(409, "experiment_lesson_missing")
        drafted = await build_plan_generator().draft(
            db, session_id=str(experiment.lesson_period_id), for_teacher=None
        )
        await bind_experiment_plan_version(
            SqlAlchemyExperimentStore(db),
            experiment_id=experiment_id,
            plan_version_id=drafted.version_id,
        )
    return {"experiment_id": experiment_id, "plan_version_id": drafted.version_id}
