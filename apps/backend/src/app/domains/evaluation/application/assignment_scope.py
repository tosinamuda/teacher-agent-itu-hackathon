"""Scope a rater's evaluation work to their ``rater_assignments`` (Phase H).

The ``rater_assignments`` table binds a rater to a unit of work; this module
turns those rows into the filter the rater-facing queues + rating-write paths
use, so a rater only ever sees / scores the work assigned to them:

- **H1** — ``scope_id`` is the experiment's ``lesson_period_id`` (UUID string).
  A packet's scope is its execution's experiment's lesson period (shared by the
  four C0–C3 packets of that lesson).
- **H2** — ``scope_id`` is the packet's own ``experiment_focal_case_id``.
- **audit** — ``scope_id`` is the ``audit_item_id``.

Adjudicator rows carry the same ``scope_id`` as primaries, so an adjudicator
assigned to a scope is included by every filter here — ``is_adjudicator`` only
governs caps + analysis, never queue visibility.

Lives apart from the queue/rating services so the assignment-scoping concern has
one home, shared by packet-rating and audit-rating commands.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import Protocol

from app.domains.evaluation.application.assignment_commands import HYPOTHESIS_AUDIT
from app.domains.evaluation.infrastructure.models import EvaluationPacket, RaterAssignment
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.shared.experiment_enums import Hypothesis


class AssignmentReader(Protocol):
    """Assignment reads used by queues and rating authorization."""

    async def list_assignments_for_rater(
        self, *, rater_db_id: uuid.UUID
    ) -> Sequence[RaterAssignment]: ...


class AssignmentScopeExperiments(Protocol):
    async def get_execution_by_db_id(
        self, execution_db_id: uuid.UUID
    ) -> ExperimentExecution | None: ...

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...


class AssignmentScope:
    """Turn ``rater_assignments`` into the filter the rater-facing surfaces use."""

    def __init__(
        self,
        repository: AssignmentReader,
        *,
        experiment_repository: AssignmentScopeExperiments,
    ) -> None:
        self.repository = repository
        self.experiment_repository = experiment_repository

    async def assigned_scope_ids(self, *, rater_db_id: uuid.UUID, hypothesis: str) -> set[str]:
        """The ``scope_id``s this rater is assigned for one lane (``H1``/``H2``/``audit``)."""
        rows = await self.repository.list_assignments_for_rater(rater_db_id=rater_db_id)
        return {row.scope_id for row in rows if row.hypothesis == hypothesis}

    async def assigned_audit_item_ids(self, *, rater_db_id: uuid.UUID) -> set[str]:
        """The ``audit_item_id``s this rater is assigned (``scope_id`` == ``audit_item_id``)."""
        return await self.assigned_scope_ids(rater_db_id=rater_db_id, hypothesis=HYPOTHESIS_AUDIT)

    async def filter_assigned_packets(
        self,
        *,
        packets: list[EvaluationPacket],
        hypothesis: Hypothesis,
        rater_db_id: uuid.UUID,
    ) -> list[EvaluationPacket]:
        """Keep only the packets whose scope is assigned to this rater (empty if none)."""
        scope_ids = await self.assigned_scope_ids(
            rater_db_id=rater_db_id, hypothesis=hypothesis.value
        )
        if not scope_ids:
            return []
        cache: dict[uuid.UUID, str | None] = {}
        kept: list[EvaluationPacket] = []
        for packet in packets:
            scope_id = await self._packet_scope_id(
                packet=packet, hypothesis=hypothesis, cache=cache
            )
            if scope_id is not None and scope_id in scope_ids:
                kept.append(packet)
        return kept

    async def is_packet_assigned(
        self,
        *,
        packet: EvaluationPacket,
        hypothesis: Hypothesis,
        rater_db_id: uuid.UUID,
    ) -> bool:
        """Whether this rater holds the assignment covering this packet's scope."""
        scope_id = await self._packet_scope_id(packet=packet, hypothesis=hypothesis, cache={})
        if scope_id is None:
            return False
        scope_ids = await self.assigned_scope_ids(
            rater_db_id=rater_db_id, hypothesis=hypothesis.value
        )
        return scope_id in scope_ids

    async def _packet_scope_id(
        self,
        *,
        packet: EvaluationPacket,
        hypothesis: Hypothesis,
        cache: dict[uuid.UUID, str | None],
    ) -> str | None:
        """The assignment ``scope_id`` for one packet under one hypothesis."""
        if hypothesis == Hypothesis.H2:
            return packet.experiment_focal_case_id
        # H1 — the scope is the experiment's lesson period, shared by C0–C3.
        return await self._lesson_period_id(execution_db_id=packet.execution_db_id, cache=cache)

    async def _lesson_period_id(
        self,
        *,
        execution_db_id: uuid.UUID,
        cache: dict[uuid.UUID, str | None],
    ) -> str | None:
        """Resolve a packet's execution to its experiment's ``lesson_period_id`` (cached)."""
        if execution_db_id in cache:
            return cache[execution_db_id]
        lesson_period_id: str | None = None
        execution = await self.experiment_repository.get_execution_by_db_id(execution_db_id)
        if execution is not None:
            experiment = await self.experiment_repository.get_experiment_by_db_id(
                execution.experiment_db_id
            )
            if experiment is not None and experiment.lesson_period_id is not None:
                lesson_period_id = str(experiment.lesson_period_id)
        cache[execution_db_id] = lesson_period_id
        return lesson_period_id
