"""The teacher's production review queue excludes experiment-produced packs.

An experiment's own plan_version shares the lesson_period with production, so it
resolves as teacher-owned; without a partition, experiment H2 P1 packs (LEARNER
scope, PENDING) would leak into ``/teacher/pack-reviews``. The queue therefore
filters to artefacts with no ``experiment_condition_run_id`` (production only).

This asserts the filter is present in the compiled query — the codebase favours
this over standing up the full experiment→execution→condition-run→artefact FK
chain for a single predicate; the end-to-end behaviour is covered by the live
multi-persona check.
"""

from __future__ import annotations

from typing import Any

import pytest

from app.domains.artefacts.core.domain.types import (
    DEFAULT_ARTEFACT_TYPE,
    ArtefactReviewStatus,
)
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository


class _CapturingResult:
    def scalars(self) -> Any:
        class _Scalars:
            def all(self) -> list[Any]:
                return []

        return _Scalars()


class _CapturingDB:
    """Records the statement passed to ``execute`` so we can inspect the SQL."""

    def __init__(self) -> None:
        self.stmt: Any = None

    async def execute(self, stmt: Any) -> _CapturingResult:
        self.stmt = stmt
        return _CapturingResult()


@pytest.mark.asyncio
async def test_pending_learner_queue_excludes_experiment_packs() -> None:
    db = _CapturingDB()
    await ArtefactRepository().list_pending_learner_artefacts(
        db,  # type: ignore[arg-type]
        artefact_type=DEFAULT_ARTEFACT_TYPE,
        plan_version_id=None,
        limit=100,
    )
    sql = str(db.stmt.compile())
    # The production queue must constrain to non-experiment artefacts.
    assert "experiment_condition_run_id IS NULL" in sql
    # Sanity: it's still the pending learner-level query.
    assert "review_status" in sql
    assert "scope" in sql


@pytest.mark.asyncio
async def test_the_learner_queue_can_list_approved_packs() -> None:
    db = _CapturingDB()
    await ArtefactRepository().list_pending_learner_artefacts(
        db,  # type: ignore[arg-type]
        artefact_type=DEFAULT_ARTEFACT_TYPE,
        plan_version_id=None,
        limit=100,
        review_status=ArtefactReviewStatus.APPROVED,
    )
    assert db.stmt.compile().params["review_status_1"] == "approved"
