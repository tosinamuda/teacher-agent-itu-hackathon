"""The generation-log table: one row per recorded LLM generation call."""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Identity, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now


class GenerationEvent(Base):
    """A single recorded LLM generation (one DSPy LM call).

    Kept as token-usage and research data. Populated
    cross-cuttingly by ``GenerationLogRecorder``; app code adds the surrounding
    context (which lesson plan / student / objective / experiment condition) via
    ``log_context(...)``.
    """

    __tablename__ = "generation_events"

    # Monotonic global ordering AND the primary key, so rows read back in
    # the order they happened. It is the PK because MySQL only AUTO_INCREMENTs a key
    # column.
    seq: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    # Stable surrogate id set by the recorder; unique, but not the PK.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True
    )
    # lesson_plan | diagnostic | personalise_section | experiment_condition | lm_call.
    kind: Mapped[str] = mapped_column(String(64), default="lm_call", index=True)
    model: Mapped[str] = mapped_column(String(200))
    # Groups the calls of one run (plan_version_id / artefact_plan_id /
    # experiment condition-run id). Null when no context was set.
    correlation_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    # Free-form tags set by the app (plan_version_id, student_id, lesson_objective_id,
    # condition_code, ...). Groups and labels the calls of a run.
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    # The LM request: {messages: [...], prompt?: str, params?: {...}} (JSON-safe).
    request: Mapped[dict] = mapped_column(JSON, default=dict)
    # The LM response: {completions: [...]} or {error: str} (JSON-safe).
    response: Mapped[dict] = mapped_column(JSON, default=dict)
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    token_usage: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
