"""Keep why the teacher rejected a pending version or withdrew an approved one.

Revision ID: 0036_artefact_review_reason
Revises: 0035_plugin_generators
Create Date: 2026-10-19
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0036_artefact_review_reason"
down_revision = "0035_plugin_generators"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds this column on a fresh DB.
    if not has_column("artefacts", "review_reason"):
        op.add_column("artefacts", sa.Column("review_reason", sa.String(512), nullable=True))


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column("artefacts", "review_reason"):
        op.drop_column("artefacts", "review_reason")
