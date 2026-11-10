"""The revision conversation: one thread per artefact, append-only turns."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now


class RevisionThread(Base):
    """A revision conversation anchored to one artefact (spans its versions)."""

    __tablename__ = "revision_threads"
    __table_args__ = (
        # One thread per artefact and slot — the get_or_create key. Slot 0 is the artefact's
        # own conversation: concurrent "open revision chat" on the same artefact must not fork
        # into two threads with turns split across them. A later slot is a chat started on purpose.
        UniqueConstraint(
            "artefact_type",
            "subject_id",
            "slot",
            name="uq_revision_thread_type_subject_slot",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revision_thread_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    # lesson_plan (now) | post_class_review_pack | diagnostic (future).
    artefact_type: Mapped[str] = mapped_column(String(64), index=True)
    # The stable artefact key the conversation revises (lesson plan: plan_id).
    subject_id: Mapped[str] = mapped_column(String(64), index=True)
    # 0 is the artefact's own conversation; each chat started after it takes the next number.
    slot: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # The key the agent's kept session is stored under; none for a conversation with no agent.
    agent_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class ChatEvent(Base):
    """One thing that happened in a chat, in order: the transcript the page replays."""

    __tablename__ = "chat_events"

    seq: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    thread_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("revision_threads.id"), index=True
    )
    # user_message | agent_text | thinking | tool | view | turn_done | turn_failed
    kind: Mapped[str] = mapped_column(String(32))
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class RevisionTurn(Base):
    """One turn: a teacher instruction (+ highlight) and the version it produced."""

    __tablename__ = "revision_turns"
    # turn_number is len(prior_turns)+1, so concurrent turns on one thread must
    # not collide on the same number.
    __table_args__ = (
        UniqueConstraint("thread_db_id", "turn_number", name="uq_revision_turn_thread_number"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revision_turn_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    thread_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("revision_threads.id"), index=True
    )
    turn_number: Mapped[int] = mapped_column(Integer)
    instruction: Mapped[str] = mapped_column(Text)
    # Anchor: {step_id?, block_id?, lesson_objective_id?, selected_text}. Null = whole-plan.
    highlight: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # The version revised (input) and the version produced (output).
    base_version_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    result_version_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # The model's one-line "what changed" + whether the result passed validation.
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    validation_passed: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
