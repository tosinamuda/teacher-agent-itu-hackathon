"""P5.6 Phase 1 — backfill ``plan_version_objectives`` from the JSON source.

The new ``plan_version_objectives`` table is a derived projection of the
``plan_versions.session_plan -> lesson_plan_objectives`` JSON array. The
JSON stays as the LLM's natural output shape (canonical at write time); the
table mirrors it so ``exit_ticket_items(plan_version_id, lesson_objective_id)``
can hold a composite foreign key into it.

This function:

1. Reads every ``plan_versions`` row whose ``session_plan`` is a dict with a
   non-empty ``lesson_plan_objectives`` array.
2. For each ``(plan_version_id, lesson_objective_id)`` pair found in the JSON,
   ``UPSERT``s a row into ``plan_version_objectives`` (idempotent via the
   ``uq_plan_version_objectives_pv_lop`` unique constraint).
3. Reports the count of rows written and re-confirms 0 orphans for the
   ``exit_ticket_items.lesson_objective_id`` references against the new table.

Invocation: see ``scripts/seed_plan_version_objectives.py``.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

import sqlalchemy as sa


@dataclass(frozen=True)
class _BackfillReport:
    plan_versions_scanned: int
    objectives_written: int
    exit_ticket_orphans: int


def backfill_plan_version_objectives(conn: sa.Connection) -> _BackfillReport:
    """Sync every plan_version's session_plan.lesson_plan_objectives to the table."""
    plan_version_rows = conn.execute(
        sa.text("SELECT version_id, session_plan FROM plan_versions")
    ).all()
    scanned = 0
    written = 0
    for version_id, session_plan in plan_version_rows:
        if isinstance(session_plan, str):
            session_plan = json.loads(session_plan)
        if not isinstance(session_plan, Mapping):
            continue
        objectives = session_plan.get("lesson_plan_objectives")
        if not isinstance(objectives, list) or not objectives:
            continue
        scanned += 1
        for ordinal, entry in enumerate(objectives, start=1):
            if not isinstance(entry, Mapping):
                continue
            lesson_objective_id = str(entry.get("lesson_objective_id") or "").strip()
            if not lesson_objective_id:
                continue
            payload = _entry_payload(entry, ordinal_default=ordinal)
            key_params = {
                "plan_version_id": version_id,
                "lesson_objective_id": lesson_objective_id,
            }
            # Idempotent upsert on the ``(plan_version_id, lesson_objective_id)``
            # natural key (select-then-insert/update). ``plan_version_id`` is a
            # string FK; only the uuid PK needs ``.hex`` for the ``CHAR(32)`` column.
            already = conn.execute(
                sa.text(
                    "SELECT 1 FROM plan_version_objectives "
                    "WHERE plan_version_id = :plan_version_id "
                    "AND lesson_objective_id = :lesson_objective_id"
                ),
                key_params,
            ).first()
            if already is None:
                conn.execute(
                    sa.text(
                        "INSERT INTO plan_version_objectives ("
                        "id, plan_version_id, lesson_objective_id, objective_text, "
                        "objective_order, kc_type, kc_focus, "
                        "curriculum_objective_id, curriculum_objective_text) "
                        "VALUES (:id, :plan_version_id, :lesson_objective_id, :objective_text, "
                        ":objective_order, :kc_type, :kc_focus, "
                        ":curriculum_objective_id, :curriculum_objective_text)"
                    ),
                    {"id": uuid.uuid4().hex, **key_params, **payload},
                )
            else:
                conn.execute(
                    sa.text(
                        "UPDATE plan_version_objectives SET "
                        "objective_text = :objective_text, "
                        "objective_order = :objective_order, "
                        "kc_type = :kc_type, kc_focus = :kc_focus, "
                        "curriculum_objective_id = :curriculum_objective_id, "
                        "curriculum_objective_text = :curriculum_objective_text, "
                        "updated_at = now() "
                        "WHERE plan_version_id = :plan_version_id "
                        "AND lesson_objective_id = :lesson_objective_id"
                    ),
                    {**key_params, **payload},
                )
            written += 1

    orphans_row = conn.execute(
        sa.text(
            """
            SELECT count(*) FROM exit_ticket_items eti
            WHERE eti.lesson_objective_id IS NOT NULL
              AND NOT EXISTS (
                SELECT 1 FROM plan_version_objectives pvo
                WHERE pvo.plan_version_id = eti.plan_version_id
                  AND pvo.lesson_objective_id = eti.lesson_objective_id
              )
            """
        )
    ).first()
    exit_ticket_orphans = 0 if orphans_row is None else int(orphans_row[0])

    return _BackfillReport(
        plan_versions_scanned=scanned,
        objectives_written=written,
        exit_ticket_orphans=exit_ticket_orphans,
    )


def _entry_payload(entry: Mapping[str, object], *, ordinal_default: int) -> dict[str, object]:
    objective_text = str(entry.get("objective_text") or "").strip()
    order_value = entry.get("objective_order")
    if isinstance(order_value, int):
        objective_order: int = order_value
    elif isinstance(order_value, str) and order_value.isdigit():
        objective_order = int(order_value)
    else:
        objective_order = ordinal_default
    kc_type = _opt_str(entry.get("kc_type"))
    kc_focus = _opt_str(entry.get("kc_focus"))
    curriculum_objective_id = _opt_str(entry.get("curriculum_objective_id"))
    curriculum_objective_text = _opt_str(entry.get("curriculum_objective_text"))
    return cast(
        "dict[str, object]",
        {
            "objective_text": objective_text,
            "objective_order": objective_order,
            "kc_type": kc_type,
            "kc_focus": kc_focus,
            "curriculum_objective_id": curriculum_objective_id,
            "curriculum_objective_text": curriculum_objective_text,
        },
    )


def _opt_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
