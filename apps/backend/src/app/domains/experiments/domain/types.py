from __future__ import annotations

from enum import Enum

# Hypothesis, PacketStatus and FocalCaseType are shared with the evaluation
# domain and now live in the shared kernel; re-exported here so this domain's
# existing call sites keep importing them from ``experiments.domain``.
from app.shared.experiment_enums import (
    FocalCaseType as FocalCaseType,
)
from app.shared.experiment_enums import (
    Hypothesis as Hypothesis,
)
from app.shared.experiment_enums import (
    PacketStatus as PacketStatus,
)


class ConditionCode(str, Enum):
    C0 = "C0"
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    P0 = "P0"
    P1 = "P1"


class ExecutionStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ExecutionErrorCategory(str, Enum):
    """Why an execution failed, classified by the worker at the catch site.

    Persisted on the execution row so the UI reads a structured category
    instead of pattern-matching the raw ``error_message`` string (which is
    the formatted exception text — brittle to library/locale changes). The
    raw message is still kept for the "technical details" disclosure.
    """

    #: A required input was unavailable (lesson plan / approved version).
    INPUTS_MISSING = "inputs_missing"
    #: A database error while saving results (e.g. an integrity violation).
    PERSISTENCE = "persistence"
    #: Anything during the generation pipeline (LLM call, validation, etc.).
    GENERATION = "generation"
    #: The attempt was interrupted (worker shutdown or task timeout), not failed.
    CANCELLED = "cancelled"
    #: Delivered more times than the poison bound allows; refused rather than re-run.
    POISON = "poison"


class ConditionedInputsMissingError(RuntimeError):
    """Raised when a conditioned execution can't resolve its required inputs.

    A typed exception (rather than ``RuntimeError("...")``) so the worker can
    classify it via ``isinstance`` instead of inspecting the message string.
    """


class ConditionRunStatus(str, Enum):
    """Status of one ``ExperimentConditionRun``.

    ``SUCCEEDED`` = generation completed; ``NEEDS_REVIEW`` = generated but the
    deterministic validator flagged issues (expert evaluation continues, not
    a hard failure — see ``SqlAlchemyConditionRuns.add_completed``);
    ``FAILED`` = this one condition's generation failed (the others in the batch
    that succeeded are persisted + frozen, and this one is retryable on its own).
    """

    SUCCEEDED = "succeeded"
    NEEDS_REVIEW = "needs_review"
    FAILED = "failed"


class ExperimentLifecycleStatus(str, Enum):
    """Distinct from per-execution status; whether the *study* is still running."""

    ACTIVE = "active"
    ENDED = "ended"


class InvestigationStatus(str, Enum):
    """An ``Investigation`` is the parent of one or more experiments; same lifecycle vocab."""

    ACTIVE = "active"
    ENDED = "ended"
