"""Shared helpers for the synthetic (dry-run) evaluators.

The synthetic source-auditor and the synthetic packet-rater are independent entry
points but share two pieces of plumbing: resolving a persistent ``EvaluationRater``
row by display name, and loading an experiment's executions (or signalling that the
experiment is absent). Both live here so neither evaluator copies the other.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Protocol

from app.domains.evaluation.application.identity_ports import RaterRegistrationStore
from app.domains.evaluation.application.rater_identity import ensure_synthetic_rater
from app.domains.evaluation.domain.records import RaterIdentity
from app.domains.experiments.infrastructure.models import Experiment

if TYPE_CHECKING:
    from app.domains.experiments.infrastructure.models import ExperimentExecution


class SyntheticExperimentReader(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...


async def get_or_create_rater(
    store: RaterRegistrationStore,
    display_name: str,
) -> RaterIdentity:
    """Ensure the synthetic rater with this display name exists, and return it.

    Each rater is its own atomic unit of work (a committed get-or-create on reference data),
    NOT part of the caller's batch transaction. That matters because ``synthetic_rater`` builds
    several raters in a dict comprehension: if they shared one transaction, a unique-conflict on
    a later persona would force a rollback that also discarded the raters already added for
    earlier personas. Committing each one independently makes that impossible — and is safe for
    the callers, which both resolve their raters *before* doing any of their own writes
    (``expire_on_commit=False`` keeps their already-loaded rows usable across the commit).
    """
    return await ensure_synthetic_rater(store, display_name=display_name)


async def load_experiment_executions(
    experiment_id: str,
    *,
    repository: SyntheticExperimentReader,
) -> list[ExperimentExecution] | None:
    """Return the executions for an experiment, or ``None`` if the experiment does not exist."""
    experiment = await repository.get_experiment(experiment_id)
    if experiment is None:
        return None
    return list(await repository.list_executions_for_experiment(experiment.id))
