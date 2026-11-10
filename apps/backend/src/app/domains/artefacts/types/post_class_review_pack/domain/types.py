"""Domain types for the post-class review pack.

``StudentPackGenerationStatus`` is the lifecycle of one *generation attempt* for a
learner's pack — distinct from ``ArtefactReviewStatus`` (the teacher approval gate on
the produced pack). Generation is a background job that may be queued, running,
or have failed before any pack exists; the review gate only applies once a pack is
produced. Mirrors ``ExecutionStatus`` for experiment executions.
"""

from __future__ import annotations

from enum import Enum


class StudentPackGenerationStatus(str, Enum):
    """Lifecycle of one async student-pack generation attempt."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


# A generation that has not reached a terminal state still owns the (student, lesson)
# slot — a second dispatch while one of these is in flight is a duplicate.
IN_FLIGHT_GENERATION_STATUSES: tuple[StudentPackGenerationStatus, ...] = (
    StudentPackGenerationStatus.QUEUED,
    StudentPackGenerationStatus.RUNNING,
)

TERMINAL_GENERATION_STATUSES: tuple[StudentPackGenerationStatus, ...] = (
    StudentPackGenerationStatus.SUCCEEDED,
    StudentPackGenerationStatus.FAILED,
)
