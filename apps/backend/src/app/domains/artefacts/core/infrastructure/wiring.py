"""Composition root for the artefacts cluster.

The use cases below take their collaborators; this is the one module that knows
which adapter satisfies each. HTTP routes, jobs and the synthetic
teacher all build through here, so none of them constructs a repository itself
and none of them decides differently from the others.
"""

from __future__ import annotations

from app.domains.artefacts.core.application.build_jobs import ArtefactLifecycleManager
from app.domains.artefacts.core.application.service import ArtefactApplicationService
from app.domains.artefacts.core.infrastructure.artefact_store import ArtefactStore
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository


def build_artefact_service() -> ArtefactApplicationService:
    """Read/approve/export over artefacts; approving a class pack releases its learners."""
    # Imported here, not at module level: the review-pack wiring builds on this module.
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
        build_learner_pack_gate,
    )

    repository = ArtefactRepository()
    return ArtefactApplicationService(
        repository,
        ArtefactStore(),
        approvals=repository,
        after_approval=build_learner_pack_gate(),
    )


def build_lifecycle_manager() -> ArtefactLifecycleManager:
    """The artefact lifecycle the review-pack routes drive."""
    return ArtefactLifecycleManager(build_artefact_service())
