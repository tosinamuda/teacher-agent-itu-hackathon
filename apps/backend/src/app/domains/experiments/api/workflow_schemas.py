"""Pydantic schemas for the experiment workflow read-model.

Mirrors `apps/frontend/src/features/experiments/services/workflow.ts`. The
field names are deliberately kept aligned so the frontend can stop
re-deriving the workflow client-side once it switches to this endpoint.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.shared.schema_base import UtcDatetime

WorkflowStatusKind = Literal[
    "done",
    "in_progress",
    "ready",
    "pending",
    "failed",
    "not_applicable",
]


class WorkflowItemResponse(BaseModel):
    """One row inside a phase — typically a single step in the protocol.

    Example: ``"Lesson plan approved / frozen"`` or ``"C3 generated"``. Wire
    serialisation uses snake_case to stay consistent with the rest of the
    experiments API surface; the typescript shape in
    ``apps/frontend/.../lib/workflow.ts`` mirrors these names exactly.
    """

    id: str
    label: str
    status: WorkflowStatusKind
    count: str | None = None
    timestamp: UtcDatetime | None = None
    href: str | None = None
    action_label: str | None = None
    reason: str | None = None


class WorkflowPhaseResponse(BaseModel):
    """A group of workflow items the protocol treats as one phase.

    Example: ``"Generation — H1 (C0–C3)"`` covers the four condition runs
    plus the C3 validation row.
    """

    id: str
    title: str
    description: str | None = None
    items: list[WorkflowItemResponse] = Field(default_factory=list)


class WorkflowNextActionResponse(BaseModel):
    """The single next action the researcher should take.

    Computed by walking the phases in declared order and returning the first
    ``pending`` / ``ready`` item that has an ``href``.
    """

    label: str
    href: str | None = None


class WorkflowSummaryResponse(BaseModel):
    """Top-level rollup of done / total / percent for the progress bar."""

    done: int
    total: int
    pct: int


class WorkflowSnapshotResponse(BaseModel):
    """The complete workflow view for one experiment, as one round-trip."""

    experiment_id: str
    phases: list[WorkflowPhaseResponse]
    summary: WorkflowSummaryResponse
    next_action: WorkflowNextActionResponse | None = None
    attention: list[WorkflowItemResponse] = Field(default_factory=list)
