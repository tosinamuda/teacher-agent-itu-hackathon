"""Baseline schema.

Squashes the prior migration chain (32 revisions) into a single baseline that
builds the schema from the live ORM metadata via ``create_all``.

Why ``create_all`` instead of explicit ``op.create_table`` calls: the current
59-table model graph is the authoritative end-state; the renames and drops
scattered through the old history (``teachers`` → ``users``,
``investigation_lessons`` dropped, …) are irrelevant to a fresh deploy. The test
suite already provisions its DB via ``create_all`` and passes, so this is the
proven schema.

``casbin_rule`` is created explicitly: it is the policy-storage table owned by
``casbin-async-sqlalchemy-adapter``, not an ORM model in ``target_metadata``, so
``create_all`` does not emit it.

Revision ID: 0001_baseline
Revises:
Create Date: squash (2026-06-15)
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def _create_casbin_rule() -> None:
    """The Casbin adapter's policy table (not an ORM model, hence explicit).

    Mirrors the DDL the adapter expects: an autoincrement PK plus ``ptype`` and
    ``v0``–``v5`` rule columns, with a covering index on ``ptype`` (the hot path
    is "load all rules at boot" + "find rules for a ptype").
    """
    op.create_table(
        "casbin_rule",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("ptype", sa.String(length=255), nullable=True),
        sa.Column("v0", sa.String(length=255), nullable=True),
        sa.Column("v1", sa.String(length=255), nullable=True),
        sa.Column("v2", sa.String(length=255), nullable=True),
        sa.Column("v3", sa.String(length=255), nullable=True),
        sa.Column("v4", sa.String(length=255), nullable=True),
        sa.Column("v5", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_casbin_rule_ptype", "casbin_rule", ["ptype"])


def upgrade() -> None:
    # Imported lazily so the module imports cleanly even when the app package
    # isn't on the path (e.g. alembic offline tooling that only reads metadata).
    from app.db.metadata import target_metadata

    target_metadata.create_all(bind=op.get_bind())
    _create_casbin_rule()


def downgrade() -> None:
    from app.db.metadata import target_metadata

    op.drop_index("ix_casbin_rule_ptype", table_name="casbin_rule")
    op.drop_table("casbin_rule")
    target_metadata.drop_all(bind=op.get_bind())
