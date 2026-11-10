"""Build evaluation services in tests without repeating their collaborator list.

The services take every collaborator as a required argument, so a test that
exercises one lane still has to name the others. These builders supply inert
stand-ins for the lanes under test, and the real thing where behaviour depends
on it.
"""

from __future__ import annotations

from typing import Any, cast

from app.domains.evaluation.application.audit_ports import (
    AuditItems,
    AuditPresentationData,
    AuditRatings,
)
from app.domains.evaluation.application.audit_presenter import (
    AuditPresentationExperiments,
    AuditPresenter,
)
from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.application.rating_ports import (
    RatingImports,
    SubmittedRatings,
)


class NoPackArtefacts:
    """A packs port that finds nothing — for lanes that never resolve a pack."""

    async def get_plan(self, artefact_plan_id: str) -> None:
        return None

    async def current_artefact_for_condition_run(self, run_id: str) -> None:
        return None


class EvaluationStoreDouble:
    """In-memory transaction boundary over one fake evaluation persistence object."""

    def __init__(self, persistence: Any) -> None:
        self._persistence = persistence
        self.commits = 0
        self.rollbacks = 0

    @property
    def ratings(self) -> SubmittedRatings:
        return cast(SubmittedRatings, self._persistence)

    @property
    def rating_imports(self) -> RatingImports:
        return cast(RatingImports, self._persistence)

    @property
    def audit_builds(self) -> AuditItems:
        return cast(AuditItems, self._persistence)

    @property
    def audit_ratings(self) -> AuditRatings:
        return cast(AuditRatings, self._persistence)

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1


def audit_service(
    *,
    repository: AuditPresentationData,
    experiments: AuditPresentationExperiments,
    artefacts: PackArtefactsPort | None = None,
) -> AuditPresenter:
    """The source-grounding audit lane."""
    return AuditPresenter(
        repository,
        experiment_repository=experiments,
    )
