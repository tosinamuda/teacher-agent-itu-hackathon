"""Keep every teacher approval of content, with the version it approved.

Revision ID: 0013_content_approvals
Revises: 0012_content_specifications
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0013_content_approvals"
down_revision = "0012_content_specifications"
branch_labels = None
depends_on = None

_TABLE = "content_approvals"


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_table

    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if has_table(_TABLE):
        return
    op.create_table(
        _TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("approval_id", sa.String(64), nullable=False),
        sa.Column("artefact_id", sa.String(64), nullable=False),
        sa.Column("approved_version", sa.Integer(), nullable=False),
        sa.Column("approved_by", sa.String(128), nullable=True),
        sa.Column("approved_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["artefact_id"],
            ["artefacts.artefact_id"],
            name="fk_content_approvals_artefact_id",
        ),
    )
    op.create_index("ix_content_approvals_approval_id", _TABLE, ["approval_id"], unique=True)
    op.create_index("ix_content_approvals_artefact_id", _TABLE, ["artefact_id"])


def downgrade() -> None:
    from app.db.migration_utils import has_table

    if has_table(_TABLE):
        op.drop_table(_TABLE)
