"""Clear everything made for one lesson, so it can be started again from its empty state.

The lesson itself, its place in the scheme of work and the class's learners stay. What goes is what
was made for it: its plans and their objectives, every material and draft made from them, the
learners' results and notes, and any evaluation marks copied onto it. The rows are found through
the lesson's plan versions and then through every foreign key that points at them, so a table
added later is cleared with the rest.

A lesson the study ran on is refused. The logged model calls of its drafts go with it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import sqlalchemy as sa
from sqlalchemy.engine import Connection

_PLANS = "plan_id IN (SELECT plan_id FROM lesson_plans WHERE lesson_period_id = :lesson)"
_VERSIONS = f"plan_version_id IN (SELECT version_id FROM plan_versions WHERE {_PLANS})"
#: Tables that mean the lesson belongs to the study, which this never clears.
_STUDY_TABLES = ("experiments", "study_transcripts")
#: Rows that name a draft by id with no foreign key, so they go before the drafts they name.
_NAMES_A_DRAFT = ("generation_events",)


@dataclass(frozen=True)
class ResetPlan:
    """What would be cleared, and why it may not be."""

    counts: dict[str, int]
    blocked: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


def _quoted(name: str) -> str:
    return f"`{name}`"


def _conditions(conn: Connection) -> dict[str, str]:
    """For each table, the WHERE clause that selects the lesson's rows in it."""
    inspector = sa.inspect(conn)
    tables = set(inspector.get_table_names())
    found: dict[str, str] = {"lesson_plans": "lesson_period_id = :lesson", "plan_versions": _PLANS}
    for table in tables:
        if any(column["name"] == "plan_version_id" for column in inspector.get_columns(table)):
            found[table] = _VERSIONS
    if "generation_events" in tables and "content_drafts" in found:
        found["generation_events"] = (
            f"correlation_id IN (SELECT * FROM (SELECT draft_id FROM content_drafts WHERE "
            f"{found['content_drafts']}) AS drafts)"
        )
    changed = True
    while changed:
        changed = False
        for child in tables:
            for key in inspector.get_foreign_keys(child):
                parent = key["referred_table"]
                if parent not in found or parent == child or len(key["constrained_columns"]) != 1:
                    continue
                column, referred = key["constrained_columns"][0], key["referred_columns"][0]
                clause = (
                    f"{_quoted(column)} IN (SELECT * FROM (SELECT {_quoted(referred)} FROM "
                    f"{_quoted(parent)} WHERE {found[parent]}) AS parents)"
                )
                if clause not in found.get(child, ""):
                    found[child] = f"({found[child]}) OR {clause}" if child in found else clause
                    changed = True
    return found


def _count(conn: Connection, table: str, where: str, lesson: str) -> int:
    sql = f"SELECT COUNT(*) FROM {_quoted(table)} WHERE {where}"
    return int(conn.execute(sa.text(sql), {"lesson": lesson}).scalar_one())


def plan_reset(conn: Connection, lesson_period_id: str) -> ResetPlan:
    """What clearing the lesson would remove; the lesson id is given as the database spells it."""
    where = _conditions(conn)
    counts = {t: n for t, c in where.items() if (n := _count(conn, t, c, lesson_period_id))}
    blocked = [
        f"the study ran on this lesson ({table})" for table in _STUDY_TABLES if counts.get(table)
    ]
    return ResetPlan(counts, blocked)


def _children_first(conn: Connection, tables: list[str]) -> list[str]:
    """The tables ordered so that one holding a foreign key into another goes before it."""
    inspector = sa.inspect(conn)
    pending = set(tables)
    pointing: dict[str, set[str]] = {
        table: {
            key["referred_table"]
            for key in inspector.get_foreign_keys(table)
            if key["referred_table"] in pending and key["referred_table"] != table
        }
        for table in tables
    }
    ordered: list[str] = []
    while pending:
        free = [
            t for t in pending if not any(t in pointing[other] for other in pending if other != t)
        ]
        batch = sorted(free) or sorted(pending)
        ordered.extend(batch)
        pending -= set(batch)
    return ordered


def reset_lesson(conn: Connection, lesson_period_id: str) -> dict[str, int]:
    """Clear the lesson's made data and return how many rows went from each table."""
    plan = plan_reset(conn, lesson_period_id)
    if plan.blocked:
        raise ValueError("; ".join(plan.blocked))
    where = _conditions(conn)
    removed: dict[str, int] = {}
    conn.execute(sa.text("SET FOREIGN_KEY_CHECKS=0"))
    try:
        tables = _children_first(conn, [t for t in plan.counts if t in where])
        tables.sort(key=lambda table: table not in _NAMES_A_DRAFT)
        for table in tables:
            sql = f"DELETE FROM {_quoted(table)} WHERE {where[table]}"
            removed[table] = conn.execute(sa.text(sql), {"lesson": lesson_period_id}).rowcount
    finally:
        conn.execute(sa.text("SET FOREIGN_KEY_CHECKS=1"))
    return removed
