"""Record which release and importer wrote an imported study, and whose raters are the app's.

Revision ID: 0019_study_imports
Revises: 0018_study_rating_documents
Create Date: 2026-09-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0019_study_imports"
down_revision = "0018_study_rating_documents"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.coltypes import UUID
    from app.db.migration_utils import has_column, has_table

    if not has_column("evaluation_raters", "origin"):
        op.add_column(
            "evaluation_raters",
            sa.Column("origin", sa.String(16), nullable=False, server_default="app"),
        )
    # Idempotent: 0001's create_all already builds this on a fresh DB (see migration_utils).
    if not has_table("study_imports"):
        op.create_table(
            "study_imports",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("investigation_id", sa.String(64), nullable=False, unique=True),
            sa.Column("release", sa.JSON(), nullable=False),
            sa.Column("importer", sa.String(64), nullable=False),
            sa.Column("imported_at", sa.DateTime(), nullable=False),
        )


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_table

    if has_table("study_imports"):
        op.drop_table("study_imports")
    if has_column("evaluation_raters", "origin"):
        op.drop_column("evaluation_raters", "origin")
