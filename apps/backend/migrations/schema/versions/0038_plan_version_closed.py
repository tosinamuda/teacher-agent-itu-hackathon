"""A plan version a teacher discards or takes back keeps why, who and when.

Revision ID: 0038_plan_version_closed
Revises: 0037_draft_student
Create Date: 2026-11-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0038_plan_version_closed"
down_revision = "0037_draft_student"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds these columns on a fresh DB.
    if not has_column("plan_versions", "closed_at"):
        op.add_column("plan_versions", sa.Column("closed_at", sa.DateTime(), nullable=True))
        op.add_column("plan_versions", sa.Column("closed_by", sa.String(128), nullable=True))
        op.add_column("plan_versions", sa.Column("closed_reason", sa.String(512), nullable=True))
    op.alter_column(
        "plan_versions",
        "status",
        existing_type=sa.Enum("draft", "approved", name="plan_version_status"),
        type_=sa.Enum("draft", "approved", "rejected", "withdrawn", name="plan_version_status"),
        existing_nullable=False,
        existing_server_default=sa.text("'draft'"),
    )


def downgrade() -> None:
    from app.db.migration_utils import has_column

    op.execute(
        "UPDATE plan_versions SET status = 'draft' WHERE status IN ('rejected', 'withdrawn')"
    )
    op.alter_column(
        "plan_versions",
        "status",
        existing_type=sa.Enum(
            "draft", "approved", "rejected", "withdrawn", name="plan_version_status"
        ),
        type_=sa.Enum("draft", "approved", name="plan_version_status"),
        existing_nullable=False,
        existing_server_default=sa.text("'draft'"),
    )
    if has_column("plan_versions", "closed_at"):
        op.drop_column("plan_versions", "closed_reason")
        op.drop_column("plan_versions", "closed_by")
        op.drop_column("plan_versions", "closed_at")
