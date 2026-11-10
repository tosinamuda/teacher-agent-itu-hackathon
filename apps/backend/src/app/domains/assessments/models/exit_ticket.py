"""Exit-ticket submission model for learner-state evidence."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, UniqueConstraint, false, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, UUID
from app.shared.time import utc_now


class ExitTicketSubmission(Base):
    """Exit ticket submission record (was diagnostic_results)."""

    __tablename__ = "exit_ticket_submissions"
    __table_args__ = (
        # Hot read path: latest_diagnostic_for_learner and the
        # latest_diagnostic_per_student batch (ORDER BY created_at DESC +
        # newest-first dedupe) in experiments/infrastructure/repository.py. See
        # migration 20260607_index_audit_round1_fk_and_composites.
        Index(
            "ix_exit_ticket_submissions_student_plan_version_created_at",
            "student_id",
            "plan_version_id",
            text("created_at DESC"),
        ),
        # One submission per (student, lesson): a re-submit (double-click or retake)
        # is rejected with a 409 rather than appending a second submission + a second
        # set of item-responses (which double-counted mastery + learner-evidence).
        UniqueConstraint(
            "student_id", "plan_version_id", name="uq_exit_ticket_submission_student_plan"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnostic_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    student_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id", name="fk_exit_ticket_submissions_student_id"),
        index=True,
    )
    plan_version_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("plan_versions.version_id"), index=True
    )
    results: Mapped[dict] = mapped_column(JSON)
    # FD-04 on-behalf entry: who transcribed it (NULL = the student submitted it
    # themselves) and an optional photo of the student's original marked answer sheet.
    entered_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    provenance_attachment_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Set when the answers arrive before the post-class survey (the two-step student flow):
    # the learner's evidence is incomplete, so no personalised pack is made until it is cleared.
    survey_pending: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
