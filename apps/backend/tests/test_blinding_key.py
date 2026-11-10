"""Tests for the researcher-only blinding key (candidate label -> condition)."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any

from app.domains.evaluation.application.blinding_queries import (
    build_blinding_key_rows,
)
from app.domains.evaluation.application.candidate_blinding import (
    Candidate,
    blind_candidates,
)


def _packet(packet_id: str, hypothesis: str, execution_db_id: uuid.UUID, **extra: Any) -> Any:
    return SimpleNamespace(
        evaluation_packet_id=packet_id,
        packet_code=f"CODE-{packet_id}",
        hypothesis=hypothesis,
        execution_db_id=execution_db_id,
        primary_condition_run_id=extra.get("primary_run", f"run-{packet_id}"),
        experiment_focal_case_id=extra.get("focal_case"),
        condition_run_ids=extra.get("condition_run_ids", [f"run-{packet_id}"]),
    )


def _assignment(rater_db_id: uuid.UUID, hypothesis: str, scope_id: str) -> Any:
    return SimpleNamespace(rater_db_id=rater_db_id, hypothesis=hypothesis, scope_id=scope_id)


def _rater(rater_db_id: uuid.UUID, rater_id: str, name: str) -> Any:
    return SimpleNamespace(id=rater_db_id, rater_id=rater_id, display_name=name)


def test_blinding_key_matches_the_rater_facing_h1_order() -> None:
    execution = uuid.uuid4()
    rater_db = uuid.uuid4()
    packets = [
        _packet(f"EPK-{code}", "H1", execution, primary_run=f"run-{code}")
        for code in ("c0", "c1", "c2", "c3")
    ]
    run_code = {f"run-c{i}": f"C{i}" for i in range(4)}
    rows = build_blinding_key_rows(
        packets=packets,
        run_code=run_code,
        execution_public_ids={execution: "EXE-1"},
        assignments=[_assignment(rater_db, "H1", "lesson-1")],
        raters_by_db_id={rater_db: _rater(rater_db, "EVR-1", "Dr. Key")},
    )
    assert len(rows) == 4
    # The key must reproduce EXACTLY the labels the rater-facing queue computes.
    expected = blind_candidates(
        rater_id="EVR-1",
        group_id=str(execution),
        candidates=[
            Candidate(p.evaluation_packet_id, run_code[p.primary_condition_run_id]) for p in packets
        ],
    )
    expected_label_by_packet = {entry.candidate_id: entry.label for entry in expected}
    for row in rows:
        assert row.candidate_label == expected_label_by_packet[row.evaluation_packet_id]
        assert row.condition_code in {"C0", "C1", "C2", "C3"}
    # Every label A-D appears exactly once and the mapping is invertible.
    assert {row.candidate_label for row in rows} == {
        "Candidate A",
        "Candidate B",
        "Candidate C",
        "Candidate D",
    }


def test_blinding_key_matches_the_rater_facing_h2_order() -> None:
    execution = uuid.uuid4()
    rater_db = uuid.uuid4()
    packet = _packet(
        "EPK-pair",
        "H2",
        execution,
        primary_run="run-p1",
        focal_case="EFC-1",
        condition_run_ids=["run-p0", "run-p1"],
    )
    run_code = {"run-p0": "P0", "run-p1": "P1"}
    rows = build_blinding_key_rows(
        packets=[packet],
        run_code=run_code,
        execution_public_ids={execution: "EXE-1"},
        assignments=[_assignment(rater_db, "H2", "EFC-1")],
        raters_by_db_id={rater_db: _rater(rater_db, "EVR-1", "Dr. Key")},
    )
    assert len(rows) == 2
    expected = blind_candidates(
        rater_id="EVR-1",
        group_id="EPK-pair",
        candidates=[Candidate("run-p0", "P0"), Candidate("run-p1", "P1")],
    )
    expected_condition_by_label = {entry.label: run_code[entry.candidate_id] for entry in expected}
    assert {row.candidate_label: row.condition_code for row in rows} == (
        expected_condition_by_label
    )


def test_blinding_key_covers_only_assigned_raters() -> None:
    execution = uuid.uuid4()
    assigned = uuid.uuid4()
    unassigned = uuid.uuid4()
    packet = _packet(
        "EPK-pair",
        "H2",
        execution,
        focal_case="EFC-1",
        condition_run_ids=["run-p0", "run-p1"],
    )
    rows = build_blinding_key_rows(
        packets=[packet],
        run_code={"run-p0": "P0", "run-p1": "P1"},
        execution_public_ids={},
        assignments=[_assignment(assigned, "H2", "EFC-1")],
        raters_by_db_id={
            assigned: _rater(assigned, "EVR-A", "Assigned"),
            unassigned: _rater(unassigned, "EVR-B", "Unassigned"),
        },
    )
    assert {row.rater_id for row in rows} == {"EVR-A"}
