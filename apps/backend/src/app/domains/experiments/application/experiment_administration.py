"""Transactional commands for experiment administration."""

from __future__ import annotations

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_administration_store import (
    ExperimentAdministrationStore,
)
from app.domains.experiments.application.experiment_context_service import (
    list_focal_learner_candidates,
)
from app.domains.experiments.domain import ExperimentLifecycleStatus
from app.domains.experiments.domain.records import ExperimentAdministrationRecord
from app.shared.time import utc_now


async def _experiment_or_error(
    store: ExperimentAdministrationStore,
    experiment_id: str,
) -> ExperimentAdministrationRecord:
    experiment = await store.experiments.get_experiment(experiment_id)
    if experiment is None:
        raise ExperimentApplicationError(404, "experiment_not_found")
    return experiment


async def end_experiment(
    store: ExperimentAdministrationStore,
    *,
    experiment_id: str,
    ended_by: str | None,
) -> ExperimentAdministrationRecord:
    """End one experiment as a single application-owned transaction."""
    try:
        experiment = await _experiment_or_error(store, experiment_id)
        experiment.lifecycle_status = ExperimentLifecycleStatus.ENDED
        experiment.ended_at = utc_now()
        experiment.ended_by = ended_by
        await store.experiments.stage_experiment(experiment)
        if experiment.plan_version_id:
            await store.lesson_conclusions.conclude_where_no_experiment_is_active(
                [experiment.plan_version_id]
            )
        await store.commit()
        return experiment
    except BaseException:
        await store.rollback()
        raise


async def set_sandbox(
    store: ExperimentAdministrationStore,
    *,
    experiment_id: str,
    is_sandbox: bool,
) -> ExperimentAdministrationRecord:
    """Set an experiment's sandbox flag in one explicit transaction."""
    try:
        experiment = await _experiment_or_error(store, experiment_id)
        experiment.is_sandbox = is_sandbox
        await store.experiments.stage_experiment(experiment)
        await store.commit()
        return experiment
    except BaseException:
        await store.rollback()
        raise


async def update_focal_learners(
    store: ExperimentAdministrationStore,
    *,
    experiment_id: str,
    learner_ids: list[str],
) -> ExperimentAdministrationRecord:
    """Validate and replace focal learners in one explicit transaction."""
    try:
        experiment = await _experiment_or_error(store, experiment_id)
        normalized_ids = list(dict.fromkeys(learner_ids))
        candidates = await list_focal_learner_candidates(
            store.experiment_context,
            experiment=experiment,
        )
        candidate_map = {candidate.learner.student_id: candidate for candidate in candidates}

        if not normalized_ids:
            raise ExperimentApplicationError(422, "focal_learners_required")
        for learner_id in normalized_ids:
            candidate = candidate_map.get(learner_id)
            if candidate is None:
                raise ExperimentApplicationError(409, "focal_learner_not_in_workspace_class")
            if candidate.diagnostic is None:
                raise ExperimentApplicationError(409, "focal_learner_evidence_missing")

        experiment.focal_learner_ids = normalized_ids
        await store.experiments.stage_experiment(experiment)
        await store.commit()
        return experiment
    except BaseException:
        await store.rollback()
        raise
