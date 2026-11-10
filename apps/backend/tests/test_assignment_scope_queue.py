"""Rater queues are scoped to ``rater_assignments`` (Phase H enforcement).

An assigned rater sees only the packets / audit items assigned to them; an
unassigned rater gets an empty queue. The rating-write paths reject a rater
scoring work they were never assigned (defense in depth). These run against
in-memory fakes — no DB — mirroring ``test_rater_assignment_service``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any, cast

import pytest

from app.domains.evaluation.application.assignment_scope import AssignmentScope
from app.domains.evaluation.application.audit_commands import (
    AuditRatingSubmission,
    submit_audit_rating,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.peer_ports import PackArtefactsPort
from app.domains.evaluation.application.rating_commands import (
    H2RatingSubmission,
    RatingCommandDependencies,
    RatingExperiments,
    submit_h2_rating,
)
from app.domains.evaluation.infrastructure.models import RaterAssignment
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
    ExperimentContextReader,
)
from app.shared.experiment_enums import Hypothesis
from tests.evaluation_collaborators import EvaluationStoreDouble, NoPackArtefacts
from tests.evaluation_collaborators import (
    audit_service as build_audit_service,
)

_LESSON_A = uuid.UUID(int=101)
_LESSON_B = uuid.UUID(int=102)
_EXP_A_DB_ID = uuid.UUID(int=1)
_EXP_B_DB_ID = uuid.UUID(int=2)
_EXEC_A_DB_ID = uuid.UUID(int=11)
_EXEC_B_DB_ID = uuid.UUID(int=12)


def _rater(rater_id: str = "EVR-1") -> Any:
    return SimpleNamespace(id=uuid.UUID(int=hash(rater_id) & 0xFFFFFFFF), rater_id=rater_id)


def _h1_packet(*, code: str, execution_db_id: uuid.UUID) -> Any:
    """An H1 packet — its scope is the experiment's lesson period (via execution)."""
    return SimpleNamespace(
        evaluation_packet_id=f"EVP-{code}",
        packet_code=code,
        hypothesis="H1",
        execution_db_id=execution_db_id,
        experiment_focal_case_id=None,
    )


def _h2_packet(*, code: str, focal_case_id: str) -> Any:
    return SimpleNamespace(
        evaluation_packet_id=f"EVP-{code}",
        packet_code=code,
        hypothesis="H2",
        execution_db_id=_EXEC_A_DB_ID,
        experiment_focal_case_id=focal_case_id,
    )


def _assignment(*, rater_db_id: uuid.UUID, hypothesis: str, scope_id: str) -> RaterAssignment:
    return RaterAssignment(
        assignment_id=f"RAS-{hypothesis}-{scope_id}",
        experiment_db_id=_EXP_A_DB_ID,
        rater_db_id=rater_db_id,
        hypothesis=hypothesis,
        scope_id=scope_id,
        is_adjudicator=False,
    )


@dataclass
class _FakeEvaluationRepository:
    raters: dict[str, Any] = field(default_factory=dict)
    assignments: list[RaterAssignment] = field(default_factory=list)
    packets: list[Any] = field(default_factory=list)
    audit_items: list[Any] = field(default_factory=list)
    audit_ratings: list[Any] = field(default_factory=list)
    saved_audit_ratings: list[Any] = field(default_factory=list)

    async def get_rater(self, *, rater_id):
        return self.raters.get(rater_id)

    async def list_assignments_for_rater(self, *, rater_db_id):
        return [row for row in self.assignments if row.rater_db_id == rater_db_id]

    async def list_packets(self, *, hypothesis):
        return [p for p in self.packets if p.hypothesis == hypothesis]

    async def get_packet(self, *, evaluation_packet_id):
        return next(
            (p for p in self.packets if p.evaluation_packet_id == evaluation_packet_id), None
        )

    async def list_audit_items(self):
        return list(self.audit_items)

    async def list_audit_ratings_for_items(self, *, audit_item_db_ids):
        return [r for r in self.audit_ratings if r.audit_item_db_id in set(audit_item_db_ids)]

    async def get_audit_item(self, *, audit_item_id):
        return next((i for i in self.audit_items if i.audit_item_id == audit_item_id), None)

    async def audit_item_record(self, *, audit_item_id):
        return await self.get_audit_item(audit_item_id=audit_item_id)

    async def rater_identity(self, *, rater_id):
        return self.raters.get(rater_id)

    async def audit_item_is_assigned(self, *, audit_item_id, rater_db_id):
        return any(
            row.rater_db_id == rater_db_id
            and row.hypothesis == "audit"
            and row.scope_id == audit_item_id
            for row in self.assignments
        )

    async def get_audit_rating(self, *, audit_item_db_id, rater_db_id):
        return next(
            (
                r
                for r in self.audit_ratings
                if r.audit_item_db_id == audit_item_db_id and r.rater_db_id == rater_db_id
            ),
            None,
        )


@dataclass
class _FakeExperimentRepository:
    executions_by_db_id: dict[uuid.UUID, Any] = field(default_factory=dict)
    experiments_by_db_id: dict[uuid.UUID, Any] = field(default_factory=dict)

    async def get_execution_by_db_id(self, execution_db_id):
        return self.executions_by_db_id.get(execution_db_id)

    async def get_experiment_by_db_id(self, experiment_db_id):
        return self.experiments_by_db_id.get(experiment_db_id)


def _experiment_repo_two_lessons() -> _FakeExperimentRepository:
    """Execution A → lesson A's experiment, execution B → lesson B's experiment."""
    return _FakeExperimentRepository(
        executions_by_db_id={
            _EXEC_A_DB_ID: SimpleNamespace(experiment_db_id=_EXP_A_DB_ID),
            _EXEC_B_DB_ID: SimpleNamespace(experiment_db_id=_EXP_B_DB_ID),
        },
        experiments_by_db_id={
            _EXP_A_DB_ID: SimpleNamespace(id=_EXP_A_DB_ID, lesson_period_id=_LESSON_A),
            _EXP_B_DB_ID: SimpleNamespace(id=_EXP_B_DB_ID, lesson_period_id=_LESSON_B),
        },
    )


# ===== H1 queue scoping (via AssignmentScope.filter_assigned_packets) =====


@pytest.mark.asyncio
async def test_h1_assigned_rater_sees_only_assigned_lesson_packets() -> None:
    rater = _rater()
    scope = AssignmentScope(
        repository=_FakeEvaluationRepository(
            assignments=[
                _assignment(rater_db_id=rater.id, hypothesis="H1", scope_id=str(_LESSON_A)),
            ],
        ),
        experiment_repository=_experiment_repo_two_lessons(),
    )
    packets = [
        _h1_packet(code="A-C0", execution_db_id=_EXEC_A_DB_ID),
        _h1_packet(code="A-C1", execution_db_id=_EXEC_A_DB_ID),
        _h1_packet(code="B-C0", execution_db_id=_EXEC_B_DB_ID),
    ]
    kept = await scope.filter_assigned_packets(
        packets=packets, hypothesis=Hypothesis.H1, rater_db_id=rater.id
    )
    assert [p.packet_code for p in kept] == ["A-C0", "A-C1"]


@pytest.mark.asyncio
async def test_h1_unassigned_rater_sees_empty_queue() -> None:
    rater = _rater()
    scope = AssignmentScope(
        repository=_FakeEvaluationRepository(assignments=[]),
        experiment_repository=_experiment_repo_two_lessons(),
    )
    packets = [_h1_packet(code="A-C0", execution_db_id=_EXEC_A_DB_ID)]
    kept = await scope.filter_assigned_packets(
        packets=packets, hypothesis=Hypothesis.H1, rater_db_id=rater.id
    )
    assert kept == []


# ===== H2 queue scoping =====


@pytest.mark.asyncio
async def test_h2_assigned_rater_sees_only_assigned_focal_case_packets() -> None:
    rater = _rater()
    scope = AssignmentScope(
        repository=_FakeEvaluationRepository(
            assignments=[
                _assignment(rater_db_id=rater.id, hypothesis="H2", scope_id="EFC-1"),
            ],
        ),
        experiment_repository=_FakeExperimentRepository(),
    )
    packets = [
        _h2_packet(code="P0-1", focal_case_id="EFC-1"),
        _h2_packet(code="P1-1", focal_case_id="EFC-1"),
        _h2_packet(code="P0-2", focal_case_id="EFC-2"),
    ]
    kept = await scope.filter_assigned_packets(
        packets=packets, hypothesis=Hypothesis.H2, rater_db_id=rater.id
    )
    assert [p.packet_code for p in kept] == ["P0-1", "P1-1"]


@pytest.mark.asyncio
async def test_h2_unassigned_rater_sees_empty_queue() -> None:
    rater = _rater()
    scope = AssignmentScope(
        repository=_FakeEvaluationRepository(assignments=[]),
        experiment_repository=_FakeExperimentRepository(),
    )
    packets = [_h2_packet(code="P0-1", focal_case_id="EFC-1")]
    kept = await scope.filter_assigned_packets(
        packets=packets, hypothesis=Hypothesis.H2, rater_db_id=rater.id
    )
    assert kept == []


# ===== Audit queue scoping (end-to-end through AuditPresenter) =====


def _audit_item(*, audit_item_id: str) -> Any:
    return SimpleNamespace(
        id=uuid.UUID(int=hash(audit_item_id) & 0xFFFFFFFF),
        audit_item_id=audit_item_id,
        condition_code="C2",
        lesson_objective_id="lop01",
        objective_text="Common multiples",
        source_ref="REF-1",
        status="ready",
    )


@pytest.mark.asyncio
async def test_audit_assigned_rater_sees_only_assigned_items() -> None:
    rater = _rater("EVR-audit")
    repo = _FakeEvaluationRepository(
        raters={rater.rater_id: rater},
        assignments=[
            _assignment(rater_db_id=rater.id, hypothesis="audit", scope_id="SGA-1"),
        ],
        audit_items=[_audit_item(audit_item_id="SGA-1"), _audit_item(audit_item_id="SGA-2")],
    )
    service = build_audit_service(repository=repo, experiments=_FakeExperimentRepository())
    queue = await service.list_audit_queue(rater_id=rater.rater_id)
    assert [item["audit_item_id"] for item in queue] == ["SGA-1"]


@pytest.mark.asyncio
async def test_audit_unassigned_rater_sees_empty_queue() -> None:
    rater = _rater("EVR-audit")
    repo = _FakeEvaluationRepository(
        raters={rater.rater_id: rater},
        assignments=[],
        audit_items=[_audit_item(audit_item_id="SGA-1"), _audit_item(audit_item_id="SGA-2")],
    )
    service = build_audit_service(repository=repo, experiments=_FakeExperimentRepository())
    queue = await service.list_audit_queue(rater_id=rater.rater_id)
    assert queue == []


# ===== Defense in depth: rating-write paths reject unassigned scopes =====


@pytest.mark.asyncio
async def test_save_h2_rating_rejects_unassigned_packet() -> None:
    rater = _rater()
    repo = _FakeEvaluationRepository(
        raters={rater.rater_id: rater},
        assignments=[],  # rater holds no H2 assignment
        packets=[_h2_packet(code="P0-1", focal_case_id="EFC-1")],
    )
    experiments = _FakeExperimentRepository()
    dependencies = RatingCommandDependencies(
        store=EvaluationStoreDouble(repo),
        experiments=cast(RatingExperiments, experiments),
        experiment_context=ExperimentContextApplicationService(
            cast(ExperimentContextReader, experiments)
        ),
        artefacts=cast(PackArtefactsPort, NoPackArtefacts()),
    )
    with pytest.raises(EvaluationApplicationError) as info:
        await submit_h2_rating(
            dependencies=dependencies,
            evaluation_packet_id="EVP-P0-1",
            rater_id=rater.rater_id,
            submission=H2RatingSubmission(
                candidate_section_scores=(),
                section_scores=(),
                base_section_scores=(),
                notes=None,
            ),
        )
    assert info.value.status_code == 403
    assert info.value.detail == "rater_not_assigned_to_packet"


@pytest.mark.asyncio
async def test_save_audit_rating_rejects_unassigned_item() -> None:
    rater = _rater("EVR-audit")
    repo = _FakeEvaluationRepository(
        raters={rater.rater_id: rater},
        assignments=[],  # rater holds no audit assignment
        audit_items=[_audit_item(audit_item_id="SGA-1")],
    )
    with pytest.raises(EvaluationApplicationError) as info:
        await submit_audit_rating(
            EvaluationStoreDouble(repo),
            audit_item_id="SGA-1",
            rater_id=rater.rater_id,
            submission=AuditRatingSubmission(
                source_relevance=2,
                support_sufficiency=2,
                faithfulness=2,
                scope_correctness=2,
                notes=None,
            ),
        )
    assert info.value.status_code == 403
    assert info.value.detail == "rater_not_assigned_to_audit_item"
    assert repo.saved_audit_ratings == []
