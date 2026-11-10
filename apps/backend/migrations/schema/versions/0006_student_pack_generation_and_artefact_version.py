"""Student-pack generation job table + Artefact optimistic-version column.

Two additions, both additive (no data rewrite of existing rows):

* ``student_pack_generations`` — the async-generation lifecycle for a learner's
  post-class pack (queued/running/succeeded/failed + attempt + error), so a failed
  generation is visible and concurrent dispatches can't both generate. Created from
  the ORM model so the DDL can't drift from ``StudentPackGeneration``.

* ``artefacts.version`` — an optimistic-concurrency token for the teacher review
  gate (approve carries the version it reviewed; a mismatch is a 409). Backfilled
  to 1 for existing rows via the server default.

Revision ID: 0006_student_pack_gen_artefact_version
Revises: 0005_exit_submission_unique
Create Date: 2026-06-17
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0006_student_pack_gen_artefact_version"
down_revision = "0005_exit_submission_unique"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Build the new table from the ORM model so columns/constraints/indexes match
    # create_all exactly (same approach as the baseline). Imported lazily so the
    # module still imports under offline alembic tooling.
    from app.db.migration_utils import has_column, has_table
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
        StudentPackGeneration,
    )

    # Idempotent: 0001's create_all already builds both on a fresh DB (see migration_utils).
    if not has_table("student_pack_generations"):
        StudentPackGeneration.__table__.create(bind=op.get_bind())

    if not has_column("artefacts", "version"):
        op.add_column(
            "artefacts",
            sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        )


def downgrade() -> None:
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
        StudentPackGeneration,
    )

    op.drop_column("artefacts", "version")
    StudentPackGeneration.__table__.drop(bind=op.get_bind())
