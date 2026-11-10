"""P5.6 Phase 2 — backfill ``curriculum_performance_objectives`` from the AO-link rows.

The legacy ``CurriculumSubtopic.performance_objectives`` JSON stores plain
strings (the human-readable objective text) and is NOT the source of the
structured ``curriculum_objective_id`` strings. Those ids
(``jss1-math-...-po01`` style) live today in ``ao_textbook_objective_links``,
at the atomic-objective grain — each row carries
``(subtopic_id, curriculum_objective_id, curriculum_objective_text)`` plus
its atomic-objective ``ao_id``. So the canonical
``curriculum_performance_objectives`` rows are the DISTINCT
``(subtopic_id, curriculum_objective_id)`` tuples sourced from there.

This function:

1. Reads ``DISTINCT (subtopic_id, curriculum_objective_id, curriculum_objective_text)``
   from ``ao_textbook_objective_links``.
2. UPSERTs one row per pair into ``curriculum_performance_objectives``
   (idempotent via the UNIQUE constraint on ``curriculum_objective_id``).
3. Reports the number of rows written, plus a zero-orphan re-check from
   ``plan_version_objectives.curriculum_objective_id`` against the new
   table — proves the composite FK that lands next is safe.

Invocation: see ``scripts/seed_curriculum_performance_objectives.py``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa


@dataclass(frozen=True)
class _BackfillReport:
    rows_written: int
    distinct_subtopics: int
    plan_version_objectives_orphans: int


def backfill_curriculum_performance_objectives(conn: sa.Connection) -> _BackfillReport:
    """Idempotently mirror the curriculum-side po-ids into the new table."""
    rows = conn.execute(
        sa.text(
            """
            SELECT DISTINCT subtopic_id, curriculum_objective_id, curriculum_objective_text
            FROM ao_textbook_objective_links
            ORDER BY subtopic_id, curriculum_objective_id
            """
        )
    ).all()

    written = 0
    subtopic_set: set[str] = set()
    for subtopic_id, curriculum_objective_id, curriculum_objective_text in rows:
        if not subtopic_id or not curriculum_objective_id:
            continue
        subtopic_set.add(str(subtopic_id))
        params = {
            "subtopic_id": str(subtopic_id),
            "curriculum_objective_id": str(curriculum_objective_id),
            "curriculum_objective_text": str(curriculum_objective_text or ""),
        }
        # Idempotent upsert on the ``curriculum_objective_id`` natural key:
        # select-then-insert/update. The id is bound as ``uuid4().hex`` (32-char)
        # so it fits the ``CHAR(32)`` storage the ``Uuid`` type uses.
        already = conn.execute(
            sa.text(
                "SELECT 1 FROM curriculum_performance_objectives "
                "WHERE curriculum_objective_id = :curriculum_objective_id"
            ),
            {"curriculum_objective_id": params["curriculum_objective_id"]},
        ).first()
        if already is None:
            conn.execute(
                sa.text(
                    "INSERT INTO curriculum_performance_objectives "
                    "(id, subtopic_id, curriculum_objective_id, curriculum_objective_text) "
                    "VALUES (:id, :subtopic_id, :curriculum_objective_id, "
                    ":curriculum_objective_text)"
                ),
                {"id": uuid.uuid4().hex, **params},
            )
        else:
            conn.execute(
                sa.text(
                    "UPDATE curriculum_performance_objectives SET "
                    "subtopic_id = :subtopic_id, "
                    "curriculum_objective_text = :curriculum_objective_text, "
                    "updated_at = now() "
                    "WHERE curriculum_objective_id = :curriculum_objective_id"
                ),
                params,
            )
        written += 1

    orphan_row = conn.execute(
        sa.text(
            """
            SELECT count(DISTINCT pvo.curriculum_objective_id)
            FROM plan_version_objectives pvo
            WHERE pvo.curriculum_objective_id IS NOT NULL
              AND NOT EXISTS (
                SELECT 1 FROM curriculum_performance_objectives cpo
                WHERE cpo.curriculum_objective_id = pvo.curriculum_objective_id
              )
            """
        )
    ).first()
    plan_version_objectives_orphans = 0 if orphan_row is None else int(orphan_row[0])

    return _BackfillReport(
        rows_written=written,
        distinct_subtopics=len(subtopic_set),
        plan_version_objectives_orphans=plan_version_objectives_orphans,
    )
