"""Keep every TikZ drawing stored content carries, drawn once as SVG.

Revision ID: 0020_figures
Revises: 0019_study_imports
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

revision = "0020_figures"
down_revision = "0019_study_imports"
branch_labels = None
depends_on = None

_LONG_TEXT = sa.Text().with_variant(mysql.MEDIUMTEXT(), "mysql")


def upgrade() -> None:
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if not has_table("figures"):
        op.create_table(
            "figures",
            sa.Column("figure_id", sa.String(64), primary_key=True),
            sa.Column("source", _LONG_TEXT, nullable=False),
            sa.Column("svg", _LONG_TEXT, nullable=True),
            sa.Column("state", sa.String(16), nullable=False, server_default="pending"),
            sa.Column("drawn_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        )


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table("figures"):
        op.drop_table("figures")
