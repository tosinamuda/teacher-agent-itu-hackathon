"""The C4 base pack is the teacher-validated C4 condition-run artefact.

These tests lock the single-source-of-truth contract the experiment teacher flow
depends on: the base pack the teacher reviews + approves IS the C4 condition-run
artefact (the PENDING pack H1 forks from C3). Approving that artefact — and only
that artefact — flips the C4-ready signal that gates H2.

Regression guard for the disconnect where a freestanding ``post_class_review_pack``
base pack was reviewed while the readiness gate watched a different artefact.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

import pytest

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.experiments.application.c4_base_pack import (
    c4_pack_approved,
    current_c4_artefact,
)


class _FakeRepo:
    """Minimal repo: one H1 execution with the given condition runs + their packs."""

    def __init__(self, runs: list[Any], artefact_by_run: dict[str, Any]) -> None:
        self._execution = SimpleNamespace(id=uuid.uuid4(), hypothesis="H1")
        self._runs = runs
        self._artefact_by_run = artefact_by_run

    async def list_executions_for_experiment(self, experiment_db_id: uuid.UUID):
        return [self._execution]

    async def list_condition_runs(self, execution_db_id: uuid.UUID):
        return self._runs

    async def current_artefact_for_condition_run(self, run_id: str):
        return self._artefact_by_run.get(run_id)


def _run(code: str, run_id: str) -> SimpleNamespace:
    return SimpleNamespace(condition_code=code, experiment_condition_run_id=run_id)


def _artefact(artefact_id: str, status: ArtefactReviewStatus) -> SimpleNamespace:
    return SimpleNamespace(artefact_id=artefact_id, review_status=status)


_EXPERIMENT = SimpleNamespace(id=uuid.uuid4())


@pytest.mark.asyncio
async def test_no_c4_run_means_no_base_pack() -> None:
    """Before H1 forks C4, there is no base pack and the gate is closed."""
    repo = _FakeRepo(runs=[_run("C3", "ECR-c3")], artefact_by_run={})

    assert await current_c4_artefact(experiments=repo, experiment=_EXPERIMENT) is None
    assert await c4_pack_approved(experiments=repo, experiment=_EXPERIMENT) is False


@pytest.mark.asyncio
async def test_pending_c4_pack_is_resolvable_but_not_approved() -> None:
    """The PENDING C4 pack is the base pack to review — present, not yet approved."""
    pending = _artefact("AT-c4", ArtefactReviewStatus.PENDING)
    repo = _FakeRepo(
        runs=[_run("C3", "ECR-c3"), _run("C4", "ECR-c4")],
        artefact_by_run={"ECR-c4": pending},
    )

    assert await current_c4_artefact(experiments=repo, experiment=_EXPERIMENT) is pending
    assert await c4_pack_approved(experiments=repo, experiment=_EXPERIMENT) is False


@pytest.mark.asyncio
async def test_approving_the_c4_pack_opens_the_gate() -> None:
    """Approving the C4 condition-run artefact — and it alone — flips the gate."""
    approved = _artefact("AT-c4", ArtefactReviewStatus.APPROVED)
    repo = _FakeRepo(
        runs=[_run("C3", "ECR-c3"), _run("C4", "ECR-c4")],
        artefact_by_run={"ECR-c4": approved},
    )

    assert await current_c4_artefact(experiments=repo, experiment=_EXPERIMENT) is approved
    assert await c4_pack_approved(experiments=repo, experiment=_EXPERIMENT) is True


@pytest.mark.asyncio
async def test_approved_c3_does_not_satisfy_the_c4_gate() -> None:
    """An auto-approved C3 pack must NOT open the C4 teacher gate (the old bug)."""
    repo = _FakeRepo(
        runs=[_run("C3", "ECR-c3"), _run("C4", "ECR-c4")],
        artefact_by_run={
            "ECR-c3": _artefact("AT-c3", ArtefactReviewStatus.APPROVED),
            "ECR-c4": _artefact("AT-c4", ArtefactReviewStatus.PENDING),
        },
    )

    # The gate reads the C4 run only — C3's approval is irrelevant.
    assert await c4_pack_approved(experiments=repo, experiment=_EXPERIMENT) is False
    resolved = await current_c4_artefact(experiments=repo, experiment=_EXPERIMENT)
    assert resolved is not None and resolved.artefact_id == "AT-c4"
