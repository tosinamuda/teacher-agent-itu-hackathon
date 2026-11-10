"""Blinded-candidate labelling for the expert-rater evaluation (Protocol §3/§4).

Raters must NOT see the condition behind a pack — H1 conditions (C0-C3) or H2 packs
(P0 base / P1 personalised). Instead each ratable pack is presented as an anonymous
"Candidate A/B/C/D" in a randomised order, and the rater scores each candidate
without knowing which is which. The backend keeps the candidate -> condition map and
de-anonymises on save and for analysis.

Design — derived & deterministic (no persistence):

* Each candidate carries a **stable id** taken from an id that already exists and is
  stable across packet rebuilds — for H2 the pack's condition-run id, for H1 the
  packet's public id. So "each candidate has an id" without a new table.
* The display order is a **deterministic permutation** of the candidates, seeded by
  ``sha256(rater_id | group_id | candidate_id)``. Same rater + same group always
  yields the same order, so the online form and the offline PDF worksheet agree, a
  reload is stable, and analysis can recompute the mapping. Different raters get
  independently shuffled orders, which removes the position bias of a fixed order.

This module is pure (no DB, no I/O): callers pass the candidates + condition for one
*group* (an H2 packet's two packs, or an H1 lesson's four condition packets) and get
back the blinded, ordered view plus the server-only de-anonymisation map.
"""

from __future__ import annotations

import hashlib
import string
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    """One ratable pack before blinding: a stable id + its (secret) condition."""

    candidate_id: str
    condition_code: str


@dataclass(frozen=True)
class BlindedCandidate:
    """A candidate as the rater sees it: anonymous label + position, no condition."""

    candidate_id: str
    label: str
    display_order: int


def candidate_label(display_order: int) -> str:
    """Anonymous label for a 0-based position: 0 -> "Candidate A", 1 -> "B", ...

    Beyond 26 candidates (never expected here) it wraps to "Candidate AA" etc., so the
    function stays total rather than raising.
    """
    if display_order < 0:
        raise ValueError("display_order must be non-negative")
    letters = string.ascii_uppercase
    quotient, remainder = divmod(display_order, len(letters))
    suffix = letters[remainder] if quotient == 0 else letters[quotient - 1] + letters[remainder]
    return f"Candidate {suffix}"


def _order_key(rater_id: str, group_id: str, candidate_id: str) -> str:
    """Stable per-(rater, group, candidate) sort key — a hex sha256 digest.

    Hashing the candidate id (not just an index) means the permutation depends on the
    candidate set, so adding/removing a candidate doesn't predictably reshuffle the
    rest, and the order can't be guessed from the label alone.
    """
    seed = f"{rater_id}|{group_id}|{candidate_id}".encode()
    return hashlib.sha256(seed).hexdigest()


def blind_candidates(
    *, rater_id: str, group_id: str, candidates: list[Candidate]
) -> list[BlindedCandidate]:
    """Order + anonymise a group's candidates deterministically for one rater.

    Candidates are sorted by their per-rater hash key (ties broken by candidate id for
    total determinism), then labelled A, B, C, ... in that order. The returned objects
    carry NO condition — that mapping stays server-side (see :func:`deanonymise`).
    """
    ordered = sorted(
        candidates,
        key=lambda candidate: (
            _order_key(rater_id, group_id, candidate.candidate_id),
            candidate.candidate_id,
        ),
    )
    return [
        BlindedCandidate(
            candidate_id=candidate.candidate_id,
            label=candidate_label(index),
            display_order=index,
        )
        for index, candidate in enumerate(ordered)
    ]


def deanonymise(candidates: list[Candidate]) -> dict[str, str]:
    """Server-side map ``candidate_id -> condition_code`` for de-anonymising a save.

    Order-independent: the rater submits scores keyed by ``candidate_id`` (never by
    label), so the backend resolves each back to its true condition with this map.
    """
    return {candidate.candidate_id: candidate.condition_code for candidate in candidates}


def blind_candidate_groups(
    *,
    rater_id: str,
    candidates_by_group: Mapping[str, list[Candidate]],
) -> dict[str, BlindedCandidate]:
    """Blind several independent candidate groups for one rater."""
    blinded: dict[str, BlindedCandidate] = {}
    for group_id, candidates in candidates_by_group.items():
        for entry in blind_candidates(
            rater_id=rater_id,
            group_id=group_id,
            candidates=candidates,
        ):
            blinded[entry.candidate_id] = entry
    return blinded
