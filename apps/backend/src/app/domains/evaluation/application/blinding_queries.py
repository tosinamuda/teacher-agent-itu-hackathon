"""Researcher-only blinding key: candidate label -> condition, per rater.

The rater-facing surfaces (web + printed worksheets) deliberately show only
anonymous candidate labels. This module recomputes the deterministic
candidate -> condition mapping (see ``candidate_blinding``) so the RESEARCHER can
de-anonymise printed offline worksheets when transcribing ratings — e.g. "on Dr.
Verify's printout of packet EPK-…, Candidate A is P1".

The key is derived, never stored: the same ``sha256(rater | group | candidate)``
permutation that ordered the rater's view reproduces it exactly. One row per
(rater, packet, candidate). H1 candidates are the lesson's condition packets
(C0–C3); H2 candidates are the paired packet's P0/P1 packs.

This output UNBLINDS the study by construction — it must only ever be served to
researchers/admins, never to raters.
"""

from __future__ import annotations

import uuid
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from app.domains.evaluation.application.candidate_blinding import (
    Candidate,
    blind_candidates,
)
from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.shared.experiment_enums import Hypothesis

if TYPE_CHECKING:
    from app.domains.evaluation.infrastructure.models import (
        EvaluationPacket,
        EvaluationRater,
        RaterAssignment,
    )


class BlindingKeyData(Protocol):
    async def list_assignments_for_experiment(
        self, *, experiment_db_id: uuid.UUID
    ) -> list[RaterAssignment]: ...

    async def list_raters(self) -> list[EvaluationRater]: ...


class BlindingKeyExperiments(Protocol):
    async def get_experiment(self, experiment_id: str) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_packets_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[EvaluationPacket]: ...

    async def list_condition_runs_for_executions(
        self, execution_db_ids: Sequence[uuid.UUID]
    ) -> list[ExperimentConditionRun]: ...


async def experiment_blinding_key(
    reader: BlindingKeyProjector, *, experiment_id: str
) -> list[BlindingKeyRow]:
    """Return the researcher-only condition key for one experiment."""
    return await reader.experiment_blinding_key(experiment_id=experiment_id)


@dataclass(frozen=True)
class BlindingKeyRow:
    """One de-anonymisation fact: for this rater's view, label X is condition Y."""

    rater_id: str
    rater_name: str
    hypothesis: str
    # The blinding group: the lesson execution (H1) or the focal case (H2).
    group: str
    packet_code: str
    evaluation_packet_id: str
    candidate_label: str
    condition_code: str


def build_blinding_key_rows(
    *,
    packets: list[EvaluationPacket],
    run_code: dict[str, str],
    execution_public_ids: dict[uuid.UUID, str],
    assignments: list[RaterAssignment],
    raters_by_db_id: dict[uuid.UUID, EvaluationRater],
) -> list[BlindingKeyRow]:
    """Recompute every assigned rater's candidate -> condition mapping (pure).

    Mirrors the rater-facing blinding exactly: H1 groups a lesson's packets by
    execution (candidate id = packet public id); H2 blinds within each paired
    packet (candidate id = condition-run id). Only raters actually assigned to
    the scope appear — they are the only ones whose printouts exist.
    """
    raters_by_key = {str(rater_db_id): rater for rater_db_id, rater in raters_by_db_id.items()}
    return [
        *_h1_key_rows(
            packets=packets,
            run_code=run_code,
            execution_public_ids=execution_public_ids,
            assignments=assignments,
            raters_by_key=raters_by_key,
        ),
        *_h2_key_rows(
            packets=packets,
            run_code=run_code,
            assignments=assignments,
            raters_by_key=raters_by_key,
        ),
    ]


def _h1_key_rows(
    *,
    packets: list[EvaluationPacket],
    run_code: dict[str, str],
    execution_public_ids: dict[uuid.UUID, str],
    assignments: list[RaterAssignment],
    raters_by_key: dict[str, EvaluationRater],
) -> list[BlindingKeyRow]:
    """H1: each lesson execution's packets blind into Candidate A–D per rater."""
    rows: list[BlindingKeyRow] = []
    h1_rater_keys = sorted(
        {str(a.rater_db_id) for a in assignments if a.hypothesis == Hypothesis.H1.value}
    )
    h1_groups: dict[uuid.UUID, list[EvaluationPacket]] = defaultdict(list)
    for packet in packets:
        if packet.hypothesis == Hypothesis.H1.value:
            h1_groups[packet.execution_db_id].append(packet)
    for execution_db_id, group_packets in h1_groups.items():
        pool = [
            Candidate(
                candidate_id=packet.evaluation_packet_id,
                condition_code=run_code.get(packet.primary_condition_run_id) or "",
            )
            for packet in group_packets
        ]
        packet_by_id = {packet.evaluation_packet_id: packet for packet in group_packets}
        condition_by_id = {candidate.candidate_id: candidate.condition_code for candidate in pool}
        for rater_key in h1_rater_keys:
            rater = raters_by_key.get(rater_key)
            if rater is None:
                continue
            for entry in blind_candidates(
                rater_id=rater.rater_id, group_id=str(execution_db_id), candidates=pool
            ):
                packet = packet_by_id[entry.candidate_id]
                rows.append(
                    BlindingKeyRow(
                        rater_id=rater.rater_id,
                        rater_name=rater.display_name,
                        hypothesis=Hypothesis.H1.value,
                        group=execution_public_ids.get(execution_db_id, str(execution_db_id)),
                        packet_code=packet.packet_code,
                        evaluation_packet_id=packet.evaluation_packet_id,
                        candidate_label=entry.label,
                        condition_code=condition_by_id[entry.candidate_id],
                    )
                )
    return rows


def _h2_key_rows(
    *,
    packets: list[EvaluationPacket],
    run_code: dict[str, str],
    assignments: list[RaterAssignment],
    raters_by_key: dict[str, EvaluationRater],
) -> list[BlindingKeyRow]:
    """H2: each paired packet's P0/P1 packs blind into Candidate A/B per rater."""
    rows: list[BlindingKeyRow] = []
    raters_by_focal_case: dict[str, set[str]] = defaultdict(set)
    for assignment in assignments:
        if assignment.hypothesis == Hypothesis.H2.value:
            raters_by_focal_case[assignment.scope_id].add(str(assignment.rater_db_id))
    for packet in packets:
        if packet.hypothesis != Hypothesis.H2.value or not packet.experiment_focal_case_id:
            continue
        pool = [
            Candidate(candidate_id=run_id, condition_code=run_code.get(run_id) or "")
            for run_id in dict.fromkeys(packet.condition_run_ids or [])
        ]
        condition_by_id = {candidate.candidate_id: candidate.condition_code for candidate in pool}
        for rater_key in sorted(raters_by_focal_case.get(packet.experiment_focal_case_id, set())):
            rater = raters_by_key.get(rater_key)
            if rater is None:
                continue
            for entry in blind_candidates(
                rater_id=rater.rater_id,
                group_id=packet.evaluation_packet_id,
                candidates=pool,
            ):
                rows.append(
                    BlindingKeyRow(
                        rater_id=rater.rater_id,
                        rater_name=rater.display_name,
                        hypothesis=Hypothesis.H2.value,
                        group=packet.experiment_focal_case_id,
                        packet_code=packet.packet_code,
                        evaluation_packet_id=packet.evaluation_packet_id,
                        candidate_label=entry.label,
                        condition_code=condition_by_id[entry.candidate_id],
                    )
                )
    return rows


class BlindingKeyProjector:
    """Load an experiment's packets + assignments and emit the de-anonymisation key."""

    def __init__(
        self,
        repository: BlindingKeyData,
        *,
        experiment_repository: BlindingKeyExperiments,
    ) -> None:
        self.repository = repository
        self.experiment_repository = experiment_repository

    async def experiment_blinding_key(self, *, experiment_id: str) -> list[BlindingKeyRow]:
        experiment = await self.experiment_repository.get_experiment(experiment_id)
        if experiment is None:
            raise EvaluationApplicationError(404, "experiment_not_found")
        executions = await self.experiment_repository.list_executions_for_experiment(experiment.id)
        execution_ids = [execution.id for execution in executions]
        packets = await self.experiment_repository.list_packets_for_executions(
            execution_db_ids=execution_ids
        )
        condition_runs = await self.experiment_repository.list_condition_runs_for_executions(
            execution_db_ids=execution_ids
        )
        run_code = {run.experiment_condition_run_id: run.condition_code for run in condition_runs}
        assignments = await self.repository.list_assignments_for_experiment(
            experiment_db_id=experiment.id
        )
        raters_by_db_id = {rater.id: rater for rater in await self.repository.list_raters()}
        return build_blinding_key_rows(
            packets=packets,
            run_code=run_code,
            execution_public_ids={execution.id: execution.execution_id for execution in executions},
            assignments=assignments,
            raters_by_db_id=raters_by_db_id,
        )
