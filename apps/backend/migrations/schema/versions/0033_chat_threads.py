"""Several chats on one artefact, each with its own agent, and the events of a chat.

Revision ID: 0033_chat_threads
Revises: 0032_plugin_files
Create Date: 2026-10-01
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0033_chat_threads"
down_revision = "0032_plugin_files"
branch_labels = None
depends_on = None

_THREADS = "revision_threads"
_OLD = "uq_revision_thread_type_subject"
_NEW = "uq_revision_thread_type_subject_slot"


def upgrade() -> None:
    from app.db.coltypes import JSON, UUID
    from app.db.migration_utils import has_column, has_table, has_unique_constraint

    # Idempotent: 0001's create_all already builds the current shape on a fresh DB (see
    # migration_utils).
    if not has_column(_THREADS, "slot"):
        op.add_column(
            _THREADS, sa.Column("slot", sa.Integer(), nullable=False, server_default=sa.text("0"))
        )
    if not has_column(_THREADS, "title"):
        op.add_column(_THREADS, sa.Column("title", sa.String(200), nullable=True))
    if not has_column(_THREADS, "agent_key"):
        op.add_column(_THREADS, sa.Column("agent_key", sa.String(100), nullable=True))
    if not has_unique_constraint(_THREADS, _NEW):
        op.create_unique_constraint(_NEW, _THREADS, ["artefact_type", "subject_id", "slot"])
    if has_unique_constraint(_THREADS, _OLD):
        op.drop_constraint(_OLD, _THREADS, type_="unique")
    if not has_table("chat_events"):
        # A foreign key needs the referenced column's collation, which a released database
        # sets on the table itself, so it is read, not assumed.
        collation = (
            op.get_bind()
            .execute(
                sa.text(
                    "SELECT collation_name FROM information_schema.columns "
                    "WHERE table_schema = DATABASE() AND table_name = :table AND column_name = 'id'"
                ),
                {"table": _THREADS},
            )
            .scalar()
        )
        op.create_table(
            "chat_events",
            sa.Column("seq", sa.BigInteger(), primary_key=True, autoincrement=True),
            sa.Column(
                "thread_db_id",
                UUID(as_uuid=True),
                sa.ForeignKey("revision_threads.id"),
                nullable=False,
            ),
            sa.Column("kind", sa.String(32), nullable=False),
            sa.Column("data", JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
            mysql_charset="utf8mb4",
            mysql_collate=collation,
        )
        op.create_index("ix_chat_events_thread_db_id", "chat_events", ["thread_db_id"])


def downgrade() -> None:
    from app.db.migration_utils import has_column, has_table, has_unique_constraint

    if has_table("chat_events"):
        op.drop_table("chat_events")
    if has_unique_constraint(_THREADS, _NEW):
        op.drop_constraint(_NEW, _THREADS, type_="unique")
    if not has_unique_constraint(_THREADS, _OLD):
        op.create_unique_constraint(_OLD, _THREADS, ["artefact_type", "subject_id"])
    for column in ("agent_key", "title", "slot"):
        if has_column(_THREADS, column):
            op.drop_column(_THREADS, column)
