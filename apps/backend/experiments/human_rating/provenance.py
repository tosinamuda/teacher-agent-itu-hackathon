"""Where each rated objective came from, and what personalisation actually changed in it.

Two tables the ratings alone cannot answer. The first records, for all 70 rater-panels,
which objective the delivered document named — checked per copy rather than assumed to
agree — against the ordinal an earlier export read it from. The second goes objective by
objective and compares the P0 and P1 sections for *that* objective, because a whole-pack
hash differs as soon as one section does and so says nothing about the rest.

Four different questions hide behind "did it have evidence", and they are kept apart:
whether the run held learner state, whether the objective was shown to a rater, whether
the state reached the prompt, and what the generator did. Only the first two are
recoverable from the records here; the third is not written down anywhere and stays
``unknown`` rather than being inferred from the fourth.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import mapping, material, panels, sources
from .export import RUN, _case_id, _objectives
from .results import DOCUMENT


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def panel_provenance(folder: Path, plans: dict[str, Any]) -> list[dict[str, Any]]:
    """One row per rater-panel: the objective its own heading names, and the old guess."""
    key = {(a.rater, a.external_id): a for a in mapping.load_h2()}
    rows = []
    for path in sorted(folder.glob("Part 2*/Rater */*.docx")):
        match = DOCUMENT.match(path.name)
        if not match:
            continue
        job = key[(f"rater-{match['rater']}", match["external"])]
        legacy = _objectives(job.lesson, plans)
        for panel in panels.displayed(path, plans[job.lesson]):
            guess = legacy[panel.ordinal - 1] if panel.ordinal <= len(legacy) else ""
            rows.append(
                {
                    "rater_id": job.rater,
                    "external_packet_id": job.external_id,
                    "case_id": _case_id(job.lesson, job.student),
                    "lesson_id": job.lesson,
                    "learner_id": job.student,
                    "panel_ordinal": panel.ordinal,
                    "objective_id": panel.objective_id or "",
                    "objective_heading_text": panel.heading_text,
                    "resolution": "document heading" if panel.resolved else "UNRESOLVED",
                    "objective_id_legacy_positional": guess,
                    "legacy_was_wrong": str(panel.objective_id != guess).lower(),
                    "source_file": str(path.relative_to(folder)),
                }
            )
    return rows


def _copies_agree(rows: list[dict[str, Any]]) -> dict[tuple[str, str], str]:
    """Whether both raters' copies of a case-objective named that same objective.

    Keyed by ``(case_id, objective_id)`` — the tuple the caller holds. An earlier version
    built the key from the panel *ordinal* and read it back with the objective id, so all
    35 lookups missed and every panel inherited a default of ``True``: a guard that could
    only ever agree. Absent evidence now answers ``unknown``, never ``yes``.
    """
    raters: dict[tuple[str, str], set[str]] = {}
    ordinals: dict[tuple[str, str], set[int]] = {}
    for row in rows:
        if not row["objective_id"]:
            continue
        key = (row["case_id"], row["objective_id"])
        raters.setdefault(key, set()).add(row["rater_id"])
        ordinals.setdefault(key, set()).add(row["panel_ordinal"])
    return {
        key: "yes" if len(who) == 2 and len(ordinals[key]) == 1 else "no"
        for key, who in raters.items()
    }


def objective_generation_audit(
    folder: Path, plans: dict[str, Any], run: str = RUN
) -> list[dict[str, Any]]:
    """One row per generated case-objective: state, exposure, and what P1 changed in it."""
    record = json.loads((sources.H2_RUNS / run / "run.json").read_text())
    sides: dict[tuple[str, str], dict[str, Any]] = {}
    for case in record["cases"]:
        sides.setdefault((case["lesson"], case["student"]), {})[case["condition"]] = case
    shown = panel_provenance(folder, plans)
    agree = _copies_agree(shown)
    displayed = {(r["case_id"], r["objective_id"]) for r in shown if r["objective_id"]}

    rows = []
    for (lesson, student), pair in sorted(sides.items()):
        p0 = material.by_objective(pair["P0"]["sections"])
        p1 = material.by_objective(pair["P1"]["sections"])
        outcomes = {
            row["lesson_objective_id"]: row["outcome"]
            for row in (pair["P1"].get("personalisation") or [])
        }
        case = _case_id(lesson, student)
        for objective in _objectives(lesson, plans):
            before, after = p0.get(objective), p1.get(objective)
            seen = (case, objective) in displayed
            rows.append(
                {
                    "case_id": case,
                    "lesson_id": lesson,
                    "learner_id": student,
                    "objective_id": objective,
                    "model_learner_state": {
                        "personalised": "state_present",
                        "no_learner_state": "state_absent",
                    }.get(outcomes.get(objective, ""), "not_recorded"),
                    "generation_outcome": outcomes.get(objective, "not_recorded"),
                    "evidence_in_prompt": "unknown",
                    "displayed_to_rater": "yes" if seen else "no",
                    "copies_agree_on_objective": agree.get((case, objective), "unknown")
                    if seen
                    else "not_displayed",
                    "p0_section_sha256": _sha(before) if before else "",
                    "p1_section_sha256": _sha(after) if after else "",
                    "sections_in_p0": len(before or []),
                    "sections_in_p1": len(after or []),
                    "objective_section_changed": (
                        "" if not (before and after) else str(_sha(before) != _sha(after)).lower()
                    ),
                    "hash_scope": "the objective's sections only, JSON with sorted keys",
                }
            )
    return rows
