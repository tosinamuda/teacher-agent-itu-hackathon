"""Tests for the blinded-candidate labelling (deterministic randomised order)."""

from __future__ import annotations

from app.domains.evaluation.application.candidate_blinding import (
    Candidate,
    blind_candidates,
    candidate_label,
    deanonymise,
)


def _h2() -> list[Candidate]:
    return [Candidate("run-p0", "P0"), Candidate("run-p1", "P1")]


def _h1() -> list[Candidate]:
    return [
        Candidate("EPK-c0", "C0"),
        Candidate("EPK-c1", "C1"),
        Candidate("EPK-c2", "C2"),
        Candidate("EPK-c3", "C3"),
    ]


def test_candidate_label_sequence() -> None:
    assert [candidate_label(i) for i in range(4)] == [
        "Candidate A",
        "Candidate B",
        "Candidate C",
        "Candidate D",
    ]


def test_blinding_is_deterministic_for_same_rater_and_group() -> None:
    first = blind_candidates(rater_id="r1", group_id="g1", candidates=_h1())
    second = blind_candidates(rater_id="r1", group_id="g1", candidates=_h1())
    assert [(b.candidate_id, b.label) for b in first] == [(b.candidate_id, b.label) for b in second]


def test_blinding_covers_all_candidates_with_sequential_labels() -> None:
    blinded = blind_candidates(rater_id="r1", group_id="g1", candidates=_h1())
    assert {b.candidate_id for b in blinded} == {c.candidate_id for c in _h1()}
    assert [b.label for b in blinded] == [
        "Candidate A",
        "Candidate B",
        "Candidate C",
        "Candidate D",
    ]
    assert [b.display_order for b in blinded] == [0, 1, 2, 3]


def test_blinding_never_leaks_condition() -> None:
    blinded = blind_candidates(rater_id="r1", group_id="g1", candidates=_h2())
    # BlindedCandidate has no condition attribute at all.
    assert all(not hasattr(b, "condition_code") for b in blinded)


def test_order_varies_across_raters() -> None:
    # Over many raters, the P0/P1 pair should not always land in the same order —
    # otherwise the blinding would carry a fixed position bias.
    p0_first = 0
    for index in range(40):
        blinded = blind_candidates(rater_id=f"rater-{index}", group_id="focal-1", candidates=_h2())
        if blinded[0].candidate_id == "run-p0":
            p0_first += 1
    assert 0 < p0_first < 40  # both orders occur


def test_deanonymise_recovers_condition_by_candidate_id() -> None:
    mapping = deanonymise(_h2())
    assert mapping == {"run-p0": "P0", "run-p1": "P1"}
    # Whatever order the rater saw, scores keyed by candidate_id resolve correctly.
    blinded = blind_candidates(rater_id="rX", group_id="focal-1", candidates=_h2())
    for candidate in blinded:
        assert mapping[candidate.candidate_id] in {"P0", "P1"}
