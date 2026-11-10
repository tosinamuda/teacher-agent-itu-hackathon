"""Keep skills as data, revision by revision, and let a spec pin the skills it is written with.

Revision ID: 0028_content_skills
Revises: 0027_content_drafts
Create Date: 2026-09-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0028_content_skills"
down_revision = "0027_content_drafts"
branch_labels = None
depends_on = None

_TABLE = "content_skills"
_SPECIFICATIONS = "content_specifications"


def upgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_column, has_table

    # Idempotent: 0001's create_all already builds these on a fresh DB (see migration_utils).
    if not has_table(_TABLE):
        op.create_table(
            _TABLE,
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("slug", sa.String(64), nullable=False),
            sa.Column("revision", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(120), nullable=False),
            sa.Column("description", sa.Text(), nullable=False),
            sa.Column("instructions", sa.Text(), nullable=False),
            sa.Column("created_by", sa.String(128), nullable=True),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
            sa.UniqueConstraint("slug", "revision", name="uq_content_skills_revision"),
        )
        op.create_index("ix_content_skills_slug", _TABLE, ["slug"])
    if not has_column(_SPECIFICATIONS, "skills"):
        op.add_column(_SPECIFICATIONS, sa.Column("skills", JSON(), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_table

    if has_column(_SPECIFICATIONS, "skills"):
        op.drop_column(_SPECIFICATIONS, "skills")
    if has_table(_TABLE):
        op.drop_table(_TABLE)
