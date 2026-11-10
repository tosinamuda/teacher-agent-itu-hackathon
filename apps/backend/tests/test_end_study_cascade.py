"""Regression: ending a study ends all its member experiments (P6).

``end_investigation`` previously flipped only the investigation row to ENDED, leaving
member experiments ``lifecycle_status='active'``. Confirmed intent: ending a study
ends its experiments. This pins the cascade — members ENDED + stamped who/when, in
one transaction — and that it never touches experiments in OTHER studies.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text

from app.domains.experiments.application.investigation_service import (
    end_investigation,
)
from app.domains.experiments.domain.types import (
    ExperimentLifecycleStatus,
    InvestigationStatus,
)
from app.domains.experiments.infrastructure.models import Experiment, Investigation
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)

pytestmark = pytest.mark.asyncio


def _experiment(investigation_db_id: uuid.UUID, tag: str) -> Experiment:
    # teacher_workspace_id FK target is irrelevant to the cascade (FK checks off).
    return Experiment(
        experiment_id=f"EXP-{tag}",
        experiment_code=f"CODE-{tag}",
        investigation_db_id=investigation_db_id,
        teacher_workspace_id=uuid.uuid4(),
    )


async def test_end_study_cascades_to_member_experiments(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    investigation = Investigation(
        investigation_id="INV-CASCADE",
        investigation_code="INVC-1",
        title="Cascade study",
        status=InvestigationStatus.ACTIVE,
    )
    db.add(investigation)
    await db.flush()

    member_one = _experiment(investigation.id, "M1")
    member_two = _experiment(investigation.id, "M2")
    other_study = _experiment(uuid.uuid4(), "CTRL")  # belongs to a different study
    db.add_all([member_one, member_two, other_study])
    await db.flush()

    result = await end_investigation(
        SqlAlchemyExperimentStore(db),
        investigation_id="INV-CASCADE",
        ended_by="researcher",
    )

    assert result.status == InvestigationStatus.ENDED
    for member in (member_one, member_two):
        assert member.lifecycle_status == ExperimentLifecycleStatus.ENDED
        assert member.ended_by == "researcher"
        assert member.ended_at is not None
    # A different study's experiment is untouched.
    assert other_study.lifecycle_status == ExperimentLifecycleStatus.ACTIVE
    assert other_study.ended_at is None
