"""Transactional command for binding an experiment's lesson-plan version."""

from __future__ import annotations

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_authoring_store import (
    ExperimentAuthoringStore,
)
from app.domains.experiments.domain.records import ExperimentPlanBindingRecord


async def bind_experiment_plan_version(
    store: ExperimentAuthoringStore,
    *,
    experiment_id: str,
    plan_version_id: str,
    expected_plan_id: str | None = None,
    target_not_found_detail: str = "plan_version_not_found",
) -> ExperimentPlanBindingRecord:
    """Validate, stage, and commit one experiment plan-version binding."""
    authoring = store.experiment_authoring
    try:
        experiment = await authoring.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")

        target = await authoring.get_plan_version_plan(plan_version_id=plan_version_id)
        if target is None:
            raise ExperimentApplicationError(404, target_not_found_detail)
        _, plan = target
        if plan.lesson_period_id != experiment.lesson_period_id:
            raise ExperimentApplicationError(409, "plan_version_belongs_to_other_lesson")
        if expected_plan_id is not None and plan.plan_id != expected_plan_id:
            raise ExperimentApplicationError(409, "accepted_version_belongs_to_other_plan")

        experiment.plan_version_id = plan_version_id
        await authoring.stage_plan_binding(experiment)
        await store.commit()
        return experiment
    except BaseException:
        await store.rollback()
        raise
