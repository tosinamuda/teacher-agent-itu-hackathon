"""Filter bag for ``list_experiments`` — one Pydantic model, five layers.

The dashboard's list-experiments read flows through route → view builder →
service → port → repository, with each layer historically taking the same
9–11 individual filter arguments. ``ExperimentListFilters`` is the single
typed shape that replaces those positional argument tapes (see audit
remediation P-?). Adding a new dashboard filter is now one field on this
model instead of touching five signatures.

Where each filter is applied
============================

- ``school_id`` — applied in ``ExperimentApplicationService.list_experiments``
  (post-filter: it loads each experiment's workspace and checks the school).
- ``query`` — applied in ``experiment_views.list_experiment_views``
  (post-filter: free-text match against the rendered DTO).
- ``teacher_id`` / ``workspace_id`` / ``plan_version_id`` /
  ``experiment_code`` / ``hypothesis`` / ``status`` / ``limit`` — pushed
  all the way into the repository SQL.

The model carries every filter even though they're applied at different
layers; the point is one canonical shape for "what the dashboard is asking
for", not one query plan.

The model is ``frozen=True`` and ``extra="forbid"``: it's a request-time
value object, never mutated, and unknown fields surface as validation
errors rather than silently doing nothing.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domains.experiments.domain.types import Hypothesis


class ExperimentListFilters(BaseModel):
    """Shape of one ``GET /experiments`` request, propagated through the read chain."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    school_id: UUID | None = None
    teacher_id: UUID | None = None
    workspace_id: UUID | None = None
    plan_version_id: str | None = None
    experiment_code: str | None = None
    hypothesis: Hypothesis | None = None
    status: str | None = None
    query: str | None = None
    limit: int = Field(default=50, ge=1, le=200)
