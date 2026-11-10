"""Per-id experiment access authorization.

Single source of truth for the tenant-isolation rule on the experiments domain.
A teacher actor may only act on experiments whose ``teacher_workspace`` they
own. A research-manager actor may act on any (the role is cross-tenant by
design — they oversee the study).

Per-id routes in ``api/routes.py`` MUST call
``ExperimentAuthorization.load_and_authorize_experiment`` instead of
``repository.get_experiment`` directly. That is how the rule is enforced
uniformly across the read surface — adding a new per-id route without going
through this helper is the bug pattern this module exists to prevent.

Resolution of "unauthorized" to HTTP 404 (rather than 403) is intentional:
the route must not leak the existence of another tenant's row.
"""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.infrastructure.models import Experiment
from app.shared.auth import ROLE_ADMIN, Actor


class ExperimentAccessReader(Protocol):
    """Experiment identity and ownership reads used by the authorization gate."""

    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def is_workspace_owned_by_teacher(
        self,
        *,
        workspace_id: uuid.UUID,
        teacher_id: uuid.UUID,
    ) -> bool: ...


class ExperimentAuthorization:
    """Gate per-id experiment access against the caller's ``Actor``."""

    def __init__(self, repository: ExperimentAccessReader) -> None:
        self._repository = repository

    async def load_and_authorize_experiment(
        self,
        *,
        actor: Actor,
        experiment_id: str,
    ) -> Experiment:
        """Load the experiment row + verify the actor may read it.

        Raises ``ExperimentApplicationError(404, "experiment_not_found")`` for
        both genuine not-found AND not-authorized. Collapsing the two avoids
        leaking the existence of another tenant's row to an unauthorized
        caller.
        """
        experiment = await self._repository.get_experiment(experiment_id)
        if experiment is None:
            raise ExperimentApplicationError(404, "experiment_not_found")
        if await self._is_authorized(actor=actor, experiment=experiment):
            return experiment
        raise ExperimentApplicationError(404, "experiment_not_found")

    async def _is_authorized(
        self,
        *,
        actor: Actor,
        experiment: Experiment,
    ) -> bool:
        # Research-manager is intentionally cross-tenant (oversees the study).
        # Admin gets the same read-through so the per-experiment "Assign raters"
        # picker can resolve every experiment — no workspace ownership applies.
        if actor.is_research_manager or actor.role == ROLE_ADMIN:
            return True
        # An anonymous actor (no resolved teacher row) is never authorized.
        if actor.teacher_id is None:
            return False
        return await self._repository.is_workspace_owned_by_teacher(
            workspace_id=experiment.teacher_workspace_id,
            teacher_id=actor.teacher_id,
        )
