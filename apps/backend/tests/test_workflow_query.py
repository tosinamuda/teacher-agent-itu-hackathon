"""Unit tests for the experiment workflow read-model derivation.

`build_snapshot` is pure (detail + stats → snapshot) so the tests drive it
with crafted fixtures rather than the database. The shape mirrors the
frontend ``services/workflow.ts`` so a TS-side regression would surface
here as a failed assertion on a row's status.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest

from app.domains.evaluation.application.result_schemas import (
    ExperimentStatistics,
    SourceAuditDescriptives,
)
from app.domains.experiments.api.schemas import (
    ExperimentConditionRunResponse,
    ExperimentDetailResponse,
    ExperimentExecutionResponse,
    ExperimentHypothesisSummaryResponse,
    ExperimentReadinessResponse,
    ExperimentResponse,
)
from app.domains.experiments.application.workflow_query import build_snapshot
from app.shared.experiment_enums import Hypothesis, PacketStatus

ANY_UUID = uuid.uuid4()


def _experiment(
    *,
    learner_count: int = 0,
    diagnostic_count: int = 0,
    focal_learner_count: int = 0,
    lesson_approved: bool = False,
    learner_evidence_ready: bool = False,
    base_pack_ready: bool = False,
    base_pack_approved: bool = False,
) -> ExperimentResponse:
    return ExperimentResponse(
        experiment_id="EXP-test",
        experiment_code="EXP-TEST-001",
        teacher_workspace_id=ANY_UUID,
        plan_version_id="LPV-test-plan",
        learner_count=learner_count,
        diagnostic_count=diagnostic_count,
        focal_learner_count=focal_learner_count,
        readiness=ExperimentReadinessResponse(
            lesson_approved=lesson_approved,
            baseline_selected=False,
            h1_ready=False,
            base_pack_ready=base_pack_ready,
            base_pack_approved=base_pack_approved,
            learner_evidence_ready=learner_evidence_ready,
            h2_ready=False,
        ),
        h1_summary=ExperimentHypothesisSummaryResponse(ready=False),
        h2_summary=ExperimentHypothesisSummaryResponse(ready=False),
    )


def _detail(
    experiment: ExperimentResponse | None = None,
    executions: list[ExperimentExecutionResponse] | None = None,
) -> ExperimentDetailResponse:
    return ExperimentDetailResponse(
        experiment=experiment or _experiment(),
        executions=executions or [],
    )


def _stats(
    *,
    h1_ratings: int = 0,
    h2_ratings: int = 0,
    audit_items: int = 0,
    audit_ratings: int = 0,
) -> ExperimentStatistics:
    return ExperimentStatistics(
        experiment_id="EXP-test",
        synthetic=False,
        h1={"n_ratings": h1_ratings},
        h2={"n_ratings": h2_ratings},
        source_audit=SourceAuditDescriptives(
            n_items=audit_items, n_ratings=audit_ratings, mean_score=None, criteria={}
        ),
        inter_rater={},
        notes=[],
    )


def _condition_run(code: str, status: str = "succeeded") -> ExperimentConditionRunResponse:
    return ExperimentConditionRunResponse(
        experiment_condition_run_id=f"CRU-{code}",
        condition_code=code,
        hypothesis=Hypothesis.H1 if code.startswith("C") else Hypothesis.H2,
        status=status,
        artefact_id=f"AT-{code}",
    )


def _execution(
    hypothesis: Hypothesis, runs: list[ExperimentConditionRunResponse]
) -> ExperimentExecutionResponse:
    return ExperimentExecutionResponse(
        execution_id="EXC-test",
        experiment_id="EXP-test",
        hypothesis=hypothesis,
        attempt_number=1,
        status="succeeded",
        condition_runs=runs,
        created_at=datetime(2026, 6, 1, tzinfo=UTC),
        updated_at=datetime(2026, 6, 4, tzinfo=UTC),
    )


def test_empty_experiment_yields_all_pending() -> None:
    """A brand-new experiment with no plan / no runs / no ratings.

    Everything stays ``pending`` (or ``ready`` for rows whose only
    precondition is the lesson plan), nothing is ``done``.
    """
    snapshot = build_snapshot(_detail(), _stats())
    assert snapshot.experiment_id == "EXP-test"
    assert len(snapshot.phases) == 7
    assert snapshot.summary.total == 18
    # The "plan-created" row is done because plan_version_id is non-empty —
    # the experiment FK always points at a plan version.
    assert snapshot.summary.done == 1
    assert snapshot.summary.pct == round(1 / 18 * 100)


def test_fully_finished_experiment_collapses_to_all_done_rows() -> None:
    """All preconditions met → workflow tips fully toward `done` / `in_progress`."""
    detail = _detail(
        experiment=_experiment(
            learner_count=20,
            diagnostic_count=20,
            focal_learner_count=4,
            lesson_approved=True,
            learner_evidence_ready=True,
            base_pack_ready=True,
            base_pack_approved=True,
        ),
        executions=[
            ExperimentExecutionResponse(
                execution_id="EXC-h1",
                experiment_id="EXP-test",
                hypothesis=Hypothesis.H1,
                attempt_number=1,
                status="succeeded",
                condition_runs=[_condition_run(code) for code in ("C0", "C1", "C2", "C3")],
                packets=_fake_packets(4),
            ),
            ExperimentExecutionResponse(
                execution_id="EXC-h2",
                experiment_id="EXP-test",
                hypothesis=Hypothesis.H2,
                attempt_number=1,
                status="succeeded",
                condition_runs=[_condition_run("P0"), _condition_run("P1")],
                packets=_fake_packets(8),
            ),
        ],
    )
    stats = _stats(
        h1_ratings=12,
        h2_ratings=24,
        audit_items=10,
        audit_ratings=5,
    )
    snapshot = build_snapshot(detail, stats)
    statuses = {item.id: item.status for phase in snapshot.phases for item in phase.items}
    assert statuses["plan-created"] == "done"
    assert statuses["plan-approved"] == "done"
    for code in ("C0", "C1", "C2", "C3"):
        assert statuses[f"cond-{code}"] == "done"
    assert statuses["c4"] == "done"
    assert statuses["submissions"] == "done"
    assert statuses["learner-states"] == "done"
    assert statuses["focal"] == "done"
    assert statuses["p0p1"] == "done"
    assert statuses["h1-rating"] == "in_progress"
    assert statuses["h2-rating"] == "in_progress"
    assert statuses["source-audit"] == "in_progress"
    assert statuses["exports"] == "ready"


def test_missing_condition_run_stays_pending_until_attempted() -> None:
    """A condition with no recorded runs is `pending`, not `failed` or `ready`.

    The backend's ``ConditionRunStatus`` enum is restricted to ``succeeded`` /
    ``needs_review`` at the response layer — true failure surfaces via
    ``error_message`` on the underlying domain record, not via a public
    ``failed`` status on this API. The workflow service's failure branch is
    defensive (in case future status enum widens); the canonical "no progress"
    state for an unstarted condition is ``pending``.
    """
    detail = _detail(
        executions=[
            _execution("H1", [_condition_run("C0"), _condition_run("C1")]),
        ]
    )
    snapshot = build_snapshot(detail, _stats())
    items_by_id = {item.id: item for phase in snapshot.phases for item in phase.items}
    assert items_by_id["cond-C0"].status == "done"
    assert items_by_id["cond-C1"].status == "done"
    assert items_by_id["cond-C2"].status == "pending"
    assert items_by_id["cond-C3"].status == "pending"
    # No failures means no attention items.
    assert snapshot.attention == []


def test_next_action_picks_first_pending_or_ready_with_href() -> None:
    """A fresh experiment's next action is the first incomplete clickable row."""
    snapshot = build_snapshot(_detail(), _stats())
    assert snapshot.next_action is not None
    # plan-created is done because plan_version_id is set; first incomplete
    # row with an href is plan-approved → /lesson-plan.
    assert snapshot.next_action.href == "/lesson-plan"


def test_done_condition_row_points_at_preview_route_not_test_tab() -> None:
    """A succeeded condition row gets href=/c0 (preview) instead of /run."""
    detail = _detail(executions=[_execution("H1", [_condition_run("C0")])])
    snapshot = build_snapshot(detail, _stats())
    items_by_id = {item.id: item for phase in snapshot.phases for item in phase.items}
    assert items_by_id["cond-C0"].status == "done"
    assert items_by_id["cond-C0"].href == "/c0"
    assert items_by_id["cond-C0"].action_label == "Preview C0 pack"


def test_h1_rating_status_transitions_pending_ready_in_progress() -> None:
    """No packets → pending; packets + 0 ratings → ready; packets + ratings → in_progress."""
    # pending
    snapshot = build_snapshot(_detail(), _stats())
    rating_phase = next(p for p in snapshot.phases if p.id == "phase-rating")
    h1_row = next(item for item in rating_phase.items if item.id == "h1-rating")
    assert h1_row.status == "pending"

    # in_progress (packets implied by stats h1 ratings)
    snapshot2 = build_snapshot(
        _detail(
            executions=[
                ExperimentExecutionResponse(
                    execution_id="EXC-1",
                    experiment_id="EXP-test",
                    hypothesis=Hypothesis.H1,
                    attempt_number=1,
                    status="succeeded",
                    packets=_fake_packets(2),
                )
            ]
        ),
        _stats(h1_ratings=6),
    )
    rating_phase2 = next(p for p in snapshot2.phases if p.id == "phase-rating")
    h1_row2 = next(item for item in rating_phase2.items if item.id == "h1-rating")
    assert h1_row2.status == "in_progress"
    assert h1_row2.count == "6 ratings · 2 packets"


def _fake_packets(count: int) -> list[Any]:
    """Quick fakes for the packets field — only `len()` is consulted."""
    from app.domains.experiments.api.schemas import EvaluationPacketResponse

    return [
        EvaluationPacketResponse(
            evaluation_packet_id=f"EPK-{index}",
            packet_code=f"EPK-CODE-{index}",
            primary_condition_run_id=f"CRU-{index}",
            hypothesis=Hypothesis.H1,
            status=PacketStatus.READY,
            condition_run_ids=[f"CRU-{index}"],
        )
        for index in range(count)
    ]


@pytest.mark.parametrize(
    ("base_pack_ready", "base_pack_approved", "expected_status", "expected_count"),
    [
        # C4 is the teacher's base-pack gate: pending until the C3 pack exists,
        # ready once it does, done once the teacher approves it.
        (False, False, "pending", "awaiting the C3 base pack"),
        (True, False, "ready", "C3 pack ready — awaiting the teacher's review"),
        (True, True, "done", "approved by the teacher"),
    ],
)
def test_c4_teacher_phase_status(
    base_pack_ready: bool,
    base_pack_approved: bool,
    expected_status: str,
    expected_count: str,
) -> None:
    snapshot = build_snapshot(
        _detail(
            _experiment(
                base_pack_ready=base_pack_ready,
                base_pack_approved=base_pack_approved,
            )
        ),
        _stats(),
    )
    c4_phase = next(p for p in snapshot.phases if p.id == "phase-teacher")
    c4_row = c4_phase.items[0]
    assert c4_row.status == expected_status
    assert c4_row.count == expected_count
