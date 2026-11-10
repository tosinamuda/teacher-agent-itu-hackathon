from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
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
from app.db.enums import status_enum
from app.domains.experiments.domain.types import (
    ConditionRunStatus,
    ExecutionStatus,
    ExperimentLifecycleStatus,
    InvestigationStatus,
)
from app.shared.time import utc_now


class Experiment(Base):
    __tablename__ = "experiments"
    # Multiple experiments are allowed per (workspace, lesson_period) — reruns and
    # variants of the same lesson are first-class. The experiment's parent is its
    # study (``investigation_db_id``), not the lesson.

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    experiment_code: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    # The study this experiment belongs to — its explicit parent. Every experiment
    # lives in exactly one investigation (one-offs go to the global "Unfiled" study).
    investigation_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("investigations.id"),
        index=True,
    )
    teacher_workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teacher_workspaces.id"),
        index=True,
    )
    # The lesson/topic this experiment studies — the experiment is created
    # against this FIRST; its own plan is authored + frozen afterwards. Nullable
    # only for legacy rows pending backfill (Phase 2).
    lesson_period_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lesson_periods.id"),
        index=True,
        nullable=True,
    )
    # The experiment's OWN frozen plan (a separate PlanVersion from production),
    # bound once the teacher authors it. NULL while the experiment awaits its plan.
    plan_version_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("plan_versions.version_id"),
        index=True,
        nullable=True,
    )
    focal_learner_ids: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    # Study lifecycle (distinct from per-execution status): "active" until a
    # researcher ends the study, then "ended".
    lifecycle_status: Mapped[ExperimentLifecycleStatus] = mapped_column(
        status_enum(ExperimentLifecycleStatus, name="experiment_lifecycle_status"),
        default=ExperimentLifecycleStatus.ACTIVE,
        server_default=text("'active'"),
        index=True,
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Throwaway dev/demo/test experiment: rehearsable like any other, but
    # excluded from the investigation rollup + real reporting, and badged
    # "SANDBOX" in the UI. Distinct from the per-rating ``synthetic`` flag.
    is_sandbox: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class ExperimentExecution(Base):
    __tablename__ = "experiment_executions"
    # One row per (experiment, hypothesis, attempt): attempt_number is MAX()+1, so
    # concurrent dispatch must not mint two rows at the same attempt.
    __table_args__ = (
        UniqueConstraint(
            "experiment_db_id", "hypothesis", "attempt_number", name="uq_execution_attempt"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    experiment_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiments.id"),
        index=True,
    )
    hypothesis: Mapped[str] = mapped_column(String(8), index=True)
    attempt_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[ExecutionStatus] = mapped_column(
        status_enum(ExecutionStatus, name="execution_status"),
        index=True,
    )
    # Times a job has claimed this row. A run cut short (a crash, a deploy) is run again and
    # re-claims it; bounding this stops a generation that dies every time from looping forever.
    delivery_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False
    )
    runtime_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Structured failure category set by the worker at the catch site
    # (inputs_missing / persistence / generation). Null unless status == failed.
    # The UI reads this instead of pattern-matching ``error_message``.
    error_category: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, server_default=text("now()")
    )


class ExperimentFocalCase(Base):
    __tablename__ = "experiment_focal_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_focal_case_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    execution_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiment_executions.id"),
        index=True,
    )
    student_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id", name="fk_experiment_focal_cases_student_id"),
        index=True,
    )
    focal_case_type: Mapped[str] = mapped_column(String(32), index=True)
    learner_state_snapshot: Mapped[dict] = mapped_column(JSON)
    selection_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class ExperimentConditionRun(Base):
    __tablename__ = "experiment_condition_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_condition_run_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    execution_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiment_executions.id"),
        index=True,
    )
    focal_case_db_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiment_focal_cases.id"),
        nullable=True,
    )
    hypothesis: Mapped[str] = mapped_column(String(8), index=True)
    condition_code: Mapped[str] = mapped_column(String(8), index=True)
    student_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("student_profiles.student_id", name="fk_experiment_condition_runs_student_id"),
        index=True,
        nullable=True,
    )
    artefact_plan_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey(
            "artefact_plans.artefact_plan_id",
            name="fk_experiment_condition_runs_artefact_plan_id",
        ),
        nullable=True,
    )
    artefact_build_job_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # NB: there is no forward `artefact_id` link from a run to its pack. The
    # single run↔artefact link lives on the artefact side
    # (``Artefact.experiment_condition_run_id``); resolve a run's current pack
    # via ``ArtefactRepository.current_artefact(s)_for_condition_run``.
    status: Mapped[ConditionRunStatus] = mapped_column(
        status_enum(ConditionRunStatus, name="condition_run_status"),
        index=True,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Reproducibility (eval-plan §23): the exact condition profile used, the
    # deterministic validation outcome, the generated pack, and model/prompt
    # provenance — so C0-C3 are demonstrably real executable differences.
    condition_profile: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    validation_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    generated_pack: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, server_default=text("now()")
    )


class Investigation(Base):
    """A research study — the explicit parent of its experiments.

    A study groups experiments under a shared hypothesis. It is NOT scoped to one
    workspace: its experiments may span several schools/subjects (each experiment
    carries its own workspace + lesson). Membership is the ``Experiment.
    investigation_db_id`` FK — there is no lesson pre-scoping.
    """

    __tablename__ = "investigations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    investigation_code: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[InvestigationStatus] = mapped_column(
        status_enum(InvestigationStatus, name="investigation_status"),
        default=InvestigationStatus.ACTIVE,
        server_default=text("'active'"),
        index=True,
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )


class C4GovernanceDecision(Base):
    """A teacher-governance decision over a C4 pack — descriptive evidence only.

    June-5 settled design: C4 is the teacher review gate on C3's pack; its outcome
    (accept / regenerate / reject) is governance evidence, NOT an H1 rater score.
    One row per C4 review records the decision + reason for descriptive analysis.
    """

    __tablename__ = "c4_governance_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    experiment_db_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("experiments.id"),
        index=True,
    )
    experiment_condition_run_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey(
            "experiment_condition_runs.experiment_condition_run_id",
            name="fk_c4_governance_decisions_experiment_condition_run_id",
        ),
        index=True,
        nullable=True,
    )
    lesson_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    c3_pack_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    final_pack_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # accepted | regenerate | rejected | accepted_after_regeneration
    teacher_decision: Mapped[str] = mapped_column(String(40), index=True)
    regeneration_count: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    issue_category: Mapped[str | None] = mapped_column(String(48), nullable=True)
    teacher_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    review_time_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    decided_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, server_default=text("now()")
    )
