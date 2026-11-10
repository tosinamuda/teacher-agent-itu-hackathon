"""Blinded-candidate assembly for the H2 packet detail (rater-facing anonymisation).

The internal H2 structures are labelled base (P0) / candidate (P1). Raters must not
see those roles: they get two anonymous candidates ("Candidate A" / "Candidate B")
in a per-rater randomised order (see ``candidate_blinding``). This module transforms
the internal shapes into that blinded view:

* ``h2_blinded_candidates`` — the ordered candidate descriptors, each carrying its
  stable id (the pack's condition-run id) and sanitised pack content (manifest only,
  no ``scope`` — "class_level" vs "learner_level" would unblind instantly).
* ``h2_blinded_sections`` — per-section steps re-keyed by candidate id instead of
  ``base_step``/``candidate_step``.
* ``h2_blind_rating_payload`` — an existing rating's nested ``candidate``/``base``
  section scores re-keyed by candidate id so the form can prefill without learning
  which candidate is which.

The candidate -> condition (P0/P1) mapping never leaves the backend; the save path
resolves submitted candidate ids back to conditions (see ``service.save_h2_rating``).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import cast

from app.domains.evaluation.application.candidate_blinding import (
    Candidate,
    blind_candidates,
)
from app.shared.json_types import JsonObject


def h2_blinded_candidates(
    *,
    rater_id: str,
    packet_public_id: str,
    p0_run_id: str,
    p1_run_id: str,
    pack_manifest_by_run: Mapping[str, JsonObject],
) -> list[JsonObject]:
    """Ordered anonymous candidate descriptors for one rater's view of an H2 packet.

    Collapses to a single candidate when the packet's base run IS its primary run
    (degenerate fallback), so callers never render the same pack twice.
    """
    condition_by_run = {p0_run_id: "P0", p1_run_id: "P1"}
    pool = [
        Candidate(candidate_id=run_id, condition_code=code)
        for run_id, code in condition_by_run.items()
    ]
    blinded = blind_candidates(rater_id=rater_id, group_id=packet_public_id, candidates=pool)
    return [
        {
            "candidate_id": candidate.candidate_id,
            "label": candidate.label,
            "display_order": candidate.display_order,
            "pack": {"manifest": pack_manifest_by_run[candidate.candidate_id]},
        }
        for candidate in blinded
    ]


def h2_blinded_sections(
    sections: Sequence[JsonObject],
    *,
    p0_run_id: str,
    p1_run_id: str,
) -> list[JsonObject]:
    """Re-key each section's steps by candidate id (no base/candidate roles).

    A candidate with no step for a section maps to ``None`` — the rater sees "this
    candidate has no section here" without learning which condition dropped it.
    """
    blinded: list[JsonObject] = []
    for section in sections:
        steps: JsonObject = {p0_run_id: section.get("base_step")}
        if p1_run_id != p0_run_id:
            steps[p1_run_id] = (
                None if section.get("candidate_missing") else section.get("candidate_step")
            )
        blinded.append(
            {
                "section_id": section.get("section_id"),
                "step_id": section.get("step_id"),
                "title": section.get("title"),
                "step_kind": section.get("step_kind"),
                "instructional_type": section.get("instructional_type"),
                "lesson_objective_id": section.get("lesson_objective_id"),
                "objective_text": section.get("objective_text"),
                "candidate_steps": steps,
            }
        )
    return blinded


def h2_blind_rating_payload(
    rating_payload: dict[str, object] | None,
    *,
    p0_run_id: str,
    p1_run_id: str,
) -> dict[str, object] | None:
    """Re-key a stored rating's per-section scores by candidate id (in place).

    Persisted shape is ``{section_id: {"candidate": {...}, "base": {...} | None}}``
    (legacy rows are flat candidate-only). The rater-facing payload becomes
    ``{section_id: {candidate_id: {...}}}`` so prefill carries no role labels.
    """
    if rating_payload is None:
        return None
    raw_sections = rating_payload.get("section_scores")
    if not isinstance(raw_sections, Mapping):
        return rating_payload
    blinded: dict[str, JsonObject] = {}
    for section_id, value in cast("Mapping[str, object]", raw_sections).items():
        per_candidate: dict[str, object] = {}
        if isinstance(value, Mapping):
            entry = cast("Mapping[str, object]", value)
            nested_candidate = entry.get("candidate")
            if isinstance(nested_candidate, Mapping):
                per_candidate[p1_run_id] = dict(nested_candidate)
                nested_base = entry.get("base")
                if isinstance(nested_base, Mapping):
                    per_candidate[p0_run_id] = dict(nested_base)
            else:  # legacy flat row: the entry itself is the candidate's scores
                per_candidate[p1_run_id] = dict(entry)
        blinded[section_id] = cast(JsonObject, per_candidate)
    rating_payload["section_scores"] = cast(JsonObject, blinded)
    return rating_payload
