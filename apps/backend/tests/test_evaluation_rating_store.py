"""Transaction ownership for interactive H1/H2 rating submission."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any, cast

import pytest

from app.domains.evaluation.application.constants import H1_RUBRIC
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.application.rating_commands import (
    H1RatingSubmission,
    RatingCommandDependencies,
    RatingConflictError,
    RatingExperiments,
    submit_h1_rating,
)
from app.domains.evaluation.domain.records import RatingRecord
from app.domains.evaluation.infrastructure.models import RaterAssignment
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
)
from app.shared.experiment_enums import Hypothesis
from tests.evaluation_collaborators import EvaluationStoreDouble, NoPackArtefacts

_RATER_DB_ID = uuid.UUID(int=1)
_PACKET_DB_ID = uuid.UUID(int=2)
_EXECUTION_DB_ID = uuid.UUID(int=3)
_EXPERIMENT_DB_ID = uuid.UUID(int=4)
_LESSON_PERIOD_ID = uuid.UUID(int=5)


class _RatingData:
    def __init__(self, *, conflict: bool = False) -> None:
        self.conflict = conflict
        self.staged: list[RatingRecord] = []
        self.rater = SimpleNamespace(id=_RATER_DB_ID, rater_id="EVR-1")
        self.packet = SimpleNamespace(
            id=_PACKET_DB_ID,
            evaluation_packet_id="EVP-1",
            packet_code="PKT-1",
            hypothesis=Hypothesis.H1.value,
            execution_db_id=_EXECUTION_DB_ID,
            experiment_focal_case_id=None,
        )
        self.assignment = RaterAssignment(
            assignment_id="RAS-1",
            experiment_db_id=_EXPERIMENT_DB_ID,
            rater_db_id=_RATER_DB_ID,
            hypothesis=Hypothesis.H1.value,
            scope_id=str(_LESSON_PERIOD_ID),
            is_adjudicator=False,
        )

    async def get_rater(self, *, rater_id: str) -> Any:
        return self.rater if rater_id == self.rater.rater_id else None

    async def get_rater_by_user_id(self, *, user_id: uuid.UUID) -> None:
        return None

    async def get_packet(self, *, evaluation_packet_id: str) -> Any:
        return self.packet if evaluation_packet_id == self.packet.evaluation_packet_id else None

    async def get_rating(
        self, *, evaluation_packet_db_id: uuid.UUID, rater_db_id: uuid.UUID
    ) -> None:
        return None

    async def find(self, *, evaluation_packet_db_id: uuid.UUID, rater_db_id: uuid.UUID) -> None:
        return None

    async def list_assignments_for_rater(self, *, rater_db_id: uuid.UUID) -> list[RaterAssignment]:
        return [self.assignment] if rater_db_id == _RATER_DB_ID else []

    async def stage(self, rating: RatingRecord) -> RatingRecord:
        if self.conflict:
            raise RatingConflictError
        self.staged.append(rating)
        return rating


class _ExperimentData:
    async def get_execution_by_db_id(self, execution_db_id: uuid.UUID) -> Any:
        if execution_db_id != _EXECUTION_DB_ID:
            return None
        return SimpleNamespace(experiment_db_id=_EXPERIMENT_DB_ID)

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Any:
        if experiment_db_id != _EXPERIMENT_DB_ID:
            return None
        return SimpleNamespace(id=_EXPERIMENT_DB_ID, lesson_period_id=_LESSON_PERIOD_ID)


def _dependencies(
    persistence: _RatingData,
) -> tuple[RatingCommandDependencies, EvaluationStoreDouble]:
    experiments = cast(RatingExperiments, _ExperimentData())
    store = EvaluationStoreDouble(persistence)
    dependencies = RatingCommandDependencies(
        store=store,
        experiments=experiments,
        experiment_context=ExperimentContextApplicationService(experiments),
        artefacts=cast(PackArtefactsPort, NoPackArtefacts()),
    )
    return dependencies, store


def _valid_h1_scores() -> dict[str, int]:
    return {str(criterion["criterion_id"]): 4 for criterion in H1_RUBRIC}


@pytest.mark.asyncio
async def test_valid_submission_stages_then_commits_exactly_once() -> None:
    persistence = _RatingData()
    dependencies, store = _dependencies(persistence)

    result = await submit_h1_rating(
        dependencies=dependencies,
        evaluation_packet_id="EVP-1",
        rater_id="EVR-1",
        submission=H1RatingSubmission(rubric_scores=_valid_h1_scores(), notes=None),
    )

    assert len(persistence.staged) == 1
    assert store.commits == 1
    assert store.rollbacks == 0
    assert result["evaluation_packet_id"] == "EVP-1"


@pytest.mark.asyncio
async def test_failed_validation_stages_and_commits_nothing() -> None:
    persistence = _RatingData()
    dependencies, store = _dependencies(persistence)

    with pytest.raises(EvaluationApplicationError) as error:
        await submit_h1_rating(
            dependencies=dependencies,
            evaluation_packet_id="EVP-1",
            rater_id="EVR-1",
            submission=H1RatingSubmission(rubric_scores={}, notes=None),
        )

    assert error.value.detail == "h1_rubric_dimensions_incomplete"
    assert persistence.staged == []
    assert store.commits == 0
    assert store.rollbacks == 0


@pytest.mark.asyncio
async def test_unique_conflict_rolls_back_and_preserves_h1_lock_response() -> None:
    persistence = _RatingData(conflict=True)
    dependencies, store = _dependencies(persistence)

    with pytest.raises(EvaluationApplicationError) as error:
        await submit_h1_rating(
            dependencies=dependencies,
            evaluation_packet_id="EVP-1",
            rater_id="EVR-1",
            submission=H1RatingSubmission(rubric_scores=_valid_h1_scores(), notes=None),
        )

    assert error.value.status_code == 409
    assert error.value.detail == "h1_rating_locked"
    assert store.commits == 0
    assert store.rollbacks == 1
