"""Existence checks so incremental migrations are idempotent on a fresh DB.

``0001_baseline`` builds the schema with ``create_all`` from the LIVE ORM models —
which already include every constraint/column/table that later migrations (0002+)
add. So on a brand-new database 0001 creates everything and 0002+ would then try to
re-create objects that already exist (duplicate-key/column errors). Guarding each
later op with these checks makes ``alembic upgrade head`` work on BOTH a fresh DB
(objects exist after 0001 → skip) and an older DB stamped before those revisions
(objects absent → create). Reflection-based, so it tracks whatever 0001 produced.
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import inspect
from sqlalchemy.engine import Inspector


def _inspector() -> Inspector:
    return inspect(op.get_bind())


def has_table(table: str) -> bool:
    return _inspector().has_table(table)


def has_column(table: str, column: str) -> bool:
    insp = _inspector()
    return insp.has_table(table) and any(c["name"] == column for c in insp.get_columns(table))


def has_index(table: str, name: str) -> bool:
    insp = _inspector()
    return insp.has_table(table) and any(ix["name"] == name for ix in insp.get_indexes(table))


def has_unique_constraint(table: str, name: str) -> bool:
    """True if a unique constraint OR unique index named ``name`` exists on ``table``.

    MySQL implements a unique constraint as a unique index, and reflection may surface
    it under either bucket, so check both.
    """
    insp = _inspector()
    if not insp.has_table(table):
        return False
    names = {uc["name"] for uc in insp.get_unique_constraints(table)}
    names |= {ix["name"] for ix in insp.get_indexes(table) if ix.get("unique")}
    return name in names
