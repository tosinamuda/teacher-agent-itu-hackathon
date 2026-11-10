"""Let a plugin add a generator to a type: the spec it carries and the flag on its install.

Revision ID: 0035_plugin_generators
Revises: 0034_content_type_generators
Create Date: 2026-10-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0035_plugin_generators"
down_revision = "0034_content_type_generators"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.migration_utils import has_column

    # Idempotent: 0001's create_all already builds these columns on a fresh DB.
    if not has_column("content_specifications", "generator"):
        op.add_column(
            "content_specifications", sa.Column("generator", sa.String(128), nullable=True)
        )
    if not has_column("content_plugins", "implements"):
        op.add_column(
            "content_plugins",
            sa.Column("implements", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        )


def downgrade() -> None:
    from app.db.migration_utils import has_column

    if has_column("content_plugins", "implements"):
        op.drop_column("content_plugins", "implements")
    if has_column("content_specifications", "generator"):
        op.drop_column("content_specifications", "generator")
