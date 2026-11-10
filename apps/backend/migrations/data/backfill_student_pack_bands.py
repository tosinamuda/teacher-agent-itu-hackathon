r"""Back-populate the personalisation band on existing student review notes.

The per-student review note (P1 pack) is pitched at the learner's band —
``remediate`` / ``reinforce`` / ``extend`` — derived from their exit-assessment
mastery. The student reader surfaces this as a "based on your assessment"
insight. Production generation now writes ``personalisation_band`` onto each
manifest step (``StudentPackGenerationService``), but notes generated before
that fix carry no band.

This module back-fills them: for each learner-level review-pack artefact, it
recomputes the band per objective from the student's latest exit-ticket
submission (the same mastery thresholds as ``learner_state``) and sets it on any
step that's missing one. Idempotent — steps that already carry a band, and notes
with no matching submission, are left untouched.

CLI: ``uv run python -m migrations.data.backfill_student_pack_bands``.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import Any, cast

import sqlalchemy as sa

from app.db.config import get_sync_database_url
from app.domains.learner_state.application.service import _band_for_mastery
from app.shared.json_types import JsonObject


def _bands_from_results(results: Any) -> dict[str, str]:
    """Per-objective band from an exit-ticket ``results`` payload (score / max)."""
    bands: dict[str, str] = {}
    if isinstance(results, str):
        results = json.loads(results)
    objectives = results.get("objectives") if isinstance(results, dict) else None
    if not isinstance(objectives, list):
        return bands
    for objective in objectives:
        if not isinstance(objective, dict):
            continue
        objective_id = objective.get("lesson_objective_id")
        max_score = objective.get("max_score") or 0
        score = objective.get("score") or 0
        if objective_id and max_score:
            bands[objective_id] = _band_for_mastery(score / max_score)
    return bands


def _apply_bands(manifest: JsonObject, bands: dict[str, str]) -> tuple[JsonObject, int]:
    """Set ``personalisation_band`` on steps missing one. Returns (manifest, n)."""
    out = deepcopy(manifest)
    steps_raw = out.get("steps")
    if not isinstance(steps_raw, list):
        return out, 0
    changed = 0
    new_steps: list[Any] = []
    for step in steps_raw:
        if not isinstance(step, dict):
            new_steps.append(step)
            continue
        step_out = deepcopy(cast(JsonObject, step))
        objective_id = step_out.get("lesson_objective_id")
        if not step_out.get("personalisation_band") and objective_id in bands:
            step_out["personalisation_band"] = bands[objective_id]
            changed += 1
        new_steps.append(step_out)
    out["steps"] = new_steps
    return out, changed


def apply_band_backfill(connection: sa.Connection) -> dict[str, int]:
    """Back-fill bands on learner-level review-pack manifests. Idempotent."""
    rows = connection.execute(
        sa.text(
            "SELECT id, student_id, plan_version_id, manifest FROM artefacts "
            "WHERE artefact_kind = 'post_class_review_pack' "
            "AND scope = 'learner_level' AND student_id IS NOT NULL "
            "AND manifest IS NOT NULL"
        )
    ).all()
    scanned = 0
    updated = 0
    steps_changed_total = 0
    for row in rows:
        scanned += 1
        manifest_raw = row.manifest
        if isinstance(manifest_raw, str):
            manifest_raw = json.loads(manifest_raw)
        if not isinstance(manifest_raw, dict):
            continue
        results_raw = connection.execute(
            sa.text(
                "SELECT results FROM exit_ticket_submissions "
                "WHERE student_id = :sid AND plan_version_id = :pv "
                "ORDER BY created_at DESC LIMIT 1"
            ),
            {"sid": row.student_id, "pv": row.plan_version_id},
        ).scalar()
        bands = _bands_from_results(results_raw)
        if not bands:
            continue
        cleaned, steps_changed = _apply_bands(cast(JsonObject, manifest_raw), bands)
        if steps_changed == 0:
            continue
        connection.execute(
            sa.text("UPDATE artefacts SET manifest = CAST(:m AS JSON) WHERE id = :id"),
            {"m": json.dumps(cleaned), "id": row.id},
        )
        updated += 1
        steps_changed_total += steps_changed
    return {"scanned": scanned, "updated": updated, "steps_changed": steps_changed_total}


def run(database_url: str | None = None) -> dict[str, int]:
    """Apply the band back-fill to a database and return summary stats."""
    url = database_url or get_sync_database_url()
    engine = sa.create_engine(url, future=True)
    with engine.begin() as conn:
        return apply_band_backfill(conn)


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", default=None, help="Database URL override.")
    args = parser.parse_args()
    print(json.dumps(run(args.database_url), indent=2))


if __name__ == "__main__":
    _main()
