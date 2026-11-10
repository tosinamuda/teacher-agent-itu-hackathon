"""P5.7 finish — backfill the 4 curriculum-identity reference catalogs.

Resolves the remaining half of audit §2.3 ("subject/grade/term double-modelling")
by promoting the denormalised string columns on `curriculum_topics` /
`class_sessions` / `reference_materials` to reference catalogs that the
curriculum domain owns.

Source of truth for the distinct values: ``curriculum_topics``. The catalogs
hold what the NERDC-published curriculum actually carries — they're curriculum
identity (not joined to the school-side `subjects`/`grade_levels`/`terms`
tables, which encode a school's *offering* and may legitimately be a different
set). This decision is documented in `docs/domain-architecture-baseline.md`
"Canonical Lesson Chain".

The data-repair step also fixes the lone curriculum_topics row whose `term`
was the empty string — `jss1-math-subtraction-of-numbers-in-base-2-numerals`
is clearly Second Term week 4 (every sibling base-2 topic is there). After
the repair, every row has a non-empty term and the new
``curriculum_terms`` constraint can be added safely.

Idempotent: each catalog row is a get-or-create on the unique ``name``
(select-then-insert), so re-running against a populated catalog is a no-op. The
data-repair UPDATE is gated on the exact original sentinel (`term = ''`).

Invocation: see ``scripts/seed_curriculum_subject_grade_term_catalogs.py``.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass

import sqlalchemy as sa


@dataclass(frozen=True)
class _BackfillReport:
    dirty_term_rows_repaired: int
    subjects_inserted: int
    tracks_inserted: int
    grades_inserted: int
    terms_inserted: int
    orphans_against_catalogs: int


# Hard-coded repair for the lone dirty row (see module docstring for rationale).
_DIRTY_BASE2_TOPIC_KEY = "jss1-math-subtraction-of-numbers-in-base-2-numerals"


def backfill_curriculum_string_catalogs(conn: sa.Connection) -> _BackfillReport:
    """Repair the dirty term row + populate the 4 curriculum reference catalogs."""
    repair_result = conn.execute(
        sa.text(
            """
            UPDATE curriculum_topics
               SET term = 'Second Term', week = 4
             WHERE topic_key = :tk
               AND (term IS NULL OR term = '')
            """
        ),
        {"tk": _DIRTY_BASE2_TOPIC_KEY},
    )
    dirty_term_rows_repaired = repair_result.rowcount or 0

    subjects_inserted = _seed(conn, "curriculum_subjects", _distinct_values(conn, "subject"))
    tracks_inserted = _seed(conn, "curriculum_tracks", _distinct_values(conn, "track"))
    grades_inserted = _seed(conn, "curriculum_grades", _distinct_values(conn, "grade"))
    terms_inserted = _seed(conn, "curriculum_terms", _distinct_values(conn, "term"))

    orphans_row = conn.execute(
        sa.text(
            """
            SELECT count(*) FROM (
                SELECT subject AS v FROM curriculum_topics
                WHERE subject NOT IN (SELECT name FROM curriculum_subjects)
                UNION ALL
                SELECT track FROM curriculum_topics
                WHERE track NOT IN (SELECT name FROM curriculum_tracks)
                UNION ALL
                SELECT grade FROM curriculum_topics
                WHERE grade NOT IN (SELECT name FROM curriculum_grades)
                UNION ALL
                SELECT term FROM curriculum_topics
                WHERE term NOT IN (SELECT name FROM curriculum_terms)
                UNION ALL
                SELECT subject FROM class_sessions
                WHERE subject NOT IN (SELECT name FROM curriculum_subjects)
                UNION ALL
                SELECT track FROM class_sessions
                WHERE track NOT IN (SELECT name FROM curriculum_tracks)
                UNION ALL
                SELECT grade FROM class_sessions
                WHERE grade NOT IN (SELECT name FROM curriculum_grades)
                UNION ALL
                SELECT term FROM class_sessions
                WHERE term NOT IN (SELECT name FROM curriculum_terms)
                UNION ALL
                SELECT subject FROM reference_materials
                WHERE subject NOT IN (SELECT name FROM curriculum_subjects)
                UNION ALL
                SELECT track FROM reference_materials
                WHERE track NOT IN (SELECT name FROM curriculum_tracks)
                UNION ALL
                SELECT grade FROM reference_materials
                WHERE grade NOT IN (SELECT name FROM curriculum_grades)
            ) x
            """
        )
    ).first()
    orphans_against_catalogs = 0 if orphans_row is None else int(orphans_row[0])

    return _BackfillReport(
        dirty_term_rows_repaired=dirty_term_rows_repaired,
        subjects_inserted=subjects_inserted,
        tracks_inserted=tracks_inserted,
        grades_inserted=grades_inserted,
        terms_inserted=terms_inserted,
        orphans_against_catalogs=orphans_against_catalogs,
    )


def _distinct_values(conn: sa.Connection, column: str) -> list[str]:
    rows = conn.execute(
        sa.text(
            f"""
            SELECT DISTINCT {column} AS v FROM curriculum_topics
            WHERE {column} IS NOT NULL AND {column} <> ''
            ORDER BY v
            """
        )
    ).all()
    return [str(row[0]) for row in rows]


def _seed(conn: sa.Connection, table: str, names: Iterable[str]) -> int:
    inserted = 0
    for name in names:
        # Get-or-create on the unique ``name`` (select-then-insert); the id is
        # bound as ``uuid4().hex`` so it fits the ``CHAR(32)`` column. ``table``
        # is an internal constant.
        already = conn.execute(
            sa.text(f"SELECT 1 FROM {table} WHERE name = :name"),  # noqa: S608
            {"name": name},
        ).first()
        if already is None:
            conn.execute(
                sa.text(f"INSERT INTO {table} (id, name) VALUES (:id, :name)"),  # noqa: S608
                {"id": uuid.uuid4().hex, "name": name},
            )
            inserted += 1
    return inserted
