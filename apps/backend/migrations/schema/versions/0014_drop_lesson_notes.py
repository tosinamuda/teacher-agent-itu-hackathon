"""Drop lesson_notes: no code ever wrote it; a lesson note is content like any other.

Revision ID: 0014_drop_lesson_notes
Revises: 0013_content_approvals
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0014_drop_lesson_notes"
down_revision = "0013_content_approvals"
branch_labels = None
depends_on = None

_TABLE = "lesson_notes"


def upgrade() -> None:
    from app.db.migration_utils import has_table

    if not has_table(_TABLE):
        return
    rows = op.get_bind().execute(sa.text(f"SELECT COUNT(*) FROM {_TABLE}")).scalar_one()
    if rows:
        raise RuntimeError(f"{_TABLE} holds {rows} rows; move them to lesson notes before dropping")
    op.drop_table(_TABLE)


def downgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "subtopic_id",
            sa.String(200),
            sa.ForeignKey("curriculum_subtopics.subtopic_id"),
            nullable=False,
        ),
        sa.Column(
            "plan_version_id",
            sa.String(64),
            sa.ForeignKey("plan_versions.version_id"),
            nullable=True,
        ),
        sa.Column("content_markdown", sa.Text(), nullable=False),
        sa.Column("provenance", JSON, nullable=True),
        sa.Column("teacher_additions", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
