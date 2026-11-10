"""Add the attachments table + on-behalf provenance columns (FD-04).

Provenance images (a photo of the original lesson plan or a student's marked
answer sheet) get an ``attachments`` row (the opaque handle; bytes live on disk).
``exit_ticket_submissions`` gains ``entered_by`` (who transcribed an on-behalf
submission; NULL = the student submitted it themselves) and
``provenance_attachment_id`` (the student's marked-sheet image).

Idempotent: 0001's create_all already builds the table + columns on a fresh DB
(the ORM metadata now defines them), so each step is guarded by an existence
check; this migration only fills the gap on existing DBs.

Revision ID: 0009_attachments_and_onbehalf
Revises: 0008_drop_subtopic_mastery_states
Create Date: 2026-06-30
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0009_attachments_and_onbehalf"
down_revision = "0008_drop_subtopic_mastery_states"
branch_labels = None
depends_on = None

_SUBMISSIONS = "exit_ticket_submissions"
_NEW_COLUMNS = ("entered_by", "provenance_attachment_id")


def upgrade() -> None:
    from app.db.metadata import target_metadata
    from app.db.migration_utils import has_column, has_table

    if not has_table("attachments"):
        target_metadata.tables["attachments"].create(bind=op.get_bind(), checkfirst=True)

    if not has_column(_SUBMISSIONS, "entered_by"):
        op.add_column(_SUBMISSIONS, sa.Column("entered_by", sa.String(128), nullable=True))
    if not has_column(_SUBMISSIONS, "provenance_attachment_id"):
        op.add_column(
            _SUBMISSIONS, sa.Column("provenance_attachment_id", sa.String(64), nullable=True)
        )


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_table

    for column in _NEW_COLUMNS:
        if has_column(_SUBMISSIONS, column):
            op.drop_column(_SUBMISSIONS, column)
    if has_table("attachments"):
        op.drop_table("attachments")
