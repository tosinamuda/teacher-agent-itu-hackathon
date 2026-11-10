"""Register content types as rows, and give a spec the unit and part schemas it is drafted by.

Revision ID: 0026_content_types
Revises: 0025_job_results
Create Date: 2026-09-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0026_content_types"
down_revision = "0025_job_results"
branch_labels = None
depends_on = None

_TYPES = "content_types"
_SPECIFICATIONS = "content_specifications"


def upgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_column, has_table

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_table(_TYPES):
        op.create_table(
            _TYPES,
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("slug", sa.String(64), nullable=False),
            sa.Column("kind", sa.String(64), nullable=False),
            sa.Column("label", sa.String(120), nullable=False),
            sa.Column("audience", sa.String(16), nullable=False),
            sa.Column("engine", sa.String(16), nullable=False),
            sa.Column("made_from_a_plan_version", sa.Boolean(), nullable=False),
            sa.Column("position", sa.Integer(), nullable=False),
            sa.Column("created_by", sa.String(128), nullable=True),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
            sa.UniqueConstraint("slug", name="uq_content_types_slug"),
            sa.UniqueConstraint("kind", name="uq_content_types_kind"),
        )
    if not has_column(_SPECIFICATIONS, "unit"):
        op.add_column(_SPECIFICATIONS, sa.Column("unit", sa.String(32), nullable=True))
    if not has_column(_SPECIFICATIONS, "parts"):
        op.add_column(_SPECIFICATIONS, sa.Column("parts", JSON(), nullable=True))
    if not has_column(_SPECIFICATIONS, "lesson_parts"):
        op.add_column(_SPECIFICATIONS, sa.Column("lesson_parts", JSON(), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_table

    for column in ("lesson_parts", "parts", "unit"):
        if has_column(_SPECIFICATIONS, column):
            op.drop_column(_SPECIFICATIONS, column)
    if has_table(_TYPES):
        op.drop_table(_TYPES)
