"""End-to-end synthetic evaluation loop — the post-generation tail in one pass.

Once the conditioned study packs have been generated (H1: C0-C4, H2: P0/P1), this
chains the three synthetic stand-ins that would otherwise be human steps:

  1. **Teacher review** — an LLM teacher approves each *pending* pack, or requests a
     concrete change and re-reviews (bounded). This clears the C4 teacher-validation
     gate (and any per-student approval gate).
  2. **Export packets** — every execution's packets are (re)exported. The gate means
     C0-C3 ship immediately and C4 ships now that step 1 approved it.
  3. **Synthetic rating** — expert-teacher-persona judges score every exported packet.

All three publish to the same per-experiment progress channel (the WS multiplexes by
``flow``), so the browser sees one continuous loop. Clearly synthetic; not a substitute
for the expert-teacher evaluation in the thesis design.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Sequence
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.evaluation.application.identity_ports import RaterRegistrationStore
from app.domains.evaluation.application.synthetic_rater import rate_experiment
from app.domains.evaluation.application.synthetic_teacher import review_experiment
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.packet_export_service import (
    PacketExportApplicationService,
)
from app.domains.experiments.application.packet_export_store import PacketExportStore
from app.domains.experiments.application.service import ExperimentApplicationService
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.shared.json_types import JsonObject

ProgressFn = Callable[[JsonObject], None]


class SyntheticExecution(Protocol):
    execution_id: str


class SyntheticExecutionReader(Protocol):
    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> Sequence[SyntheticExecution]: ...


def _emit(on_progress: ProgressFn | None, event: JsonObject) -> None:
    if on_progress is not None:
        on_progress(event)


async def _export_all_executions(
    service: ExperimentApplicationService,
    *,
    experiments: SyntheticExecutionReader,
    packet_export_store: PacketExportStore,
    experiment_id: str,
    on_progress: ProgressFn | None,
) -> tuple[int, int]:
    """Export packets for every execution; skip (don't fail) ones that aren't ready."""
    experiment = await service.get_experiment(experiment_id=experiment_id)
    executions = await experiments.list_executions_for_experiment(experiment.id)
    execution_ids = tuple(execution.execution_id for execution in executions)
    await packet_export_store.rollback()
    exported = 0
    skipped = 0
    for execution_id in execution_ids:
        try:
            packets = await PacketExportApplicationService(packet_export_store).export_packets(
                execution_id=execution_id
            )
            exported += len(packets)
        except ExperimentApplicationError as error:
            skipped += 1
            _emit(
                on_progress,
                {
                    "type": "progress",
                    "phase": "loop",
                    "message": f"Export skipped for {execution_id}: {error.detail}",
                },
            )
    _emit(
        on_progress,
        {
            "type": "progress",
            "phase": "loop",
            "message": f"{exported} packet(s) exported across {len(execution_ids)} execution(s)",
        },
    )
    return exported, skipped


async def run_synthetic_loop(
    db: AsyncSession,
    *,
    identity_store: RaterRegistrationStore,
    packet_export_store: PacketExportStore,
    experiment_id: str,
    max_rounds: int = 2,
    personas: list[str] | None = None,
    on_progress: ProgressFn | None = None,
) -> JsonObject:
    """Run teacher-review -> export -> rate for one experiment, in order."""
    experiments = ExperimentRepository(db)
    service = ExperimentApplicationService(experiments)
    _emit(
        on_progress,
        {"type": "start", "phase": "loop", "message": "Synthetic evaluation loop starting…"},
    )

    review = await review_experiment(
        db, experiment_id=experiment_id, max_rounds=max_rounds, on_progress=on_progress
    )
    exported, skipped = await _export_all_executions(
        service,
        experiments=experiments,
        packet_export_store=packet_export_store,
        experiment_id=experiment_id,
        on_progress=on_progress,
    )
    rating = await rate_experiment(
        db,
        identity_store=identity_store,
        experiment_id=experiment_id,
        personas=personas,
        on_progress=on_progress,
    )

    _emit(
        on_progress,
        {
            "type": "done",
            "phase": "loop",
            "message": (
                f"Loop complete · {review['approved']} pack(s) approved, "
                f"{exported} packet(s) exported, {rating.get('created', 0)} rating(s)"
            ),
        },
    )
    return {
        "review": review,
        "exported_packets": exported,
        "skipped_exports": skipped,
        "rating": rating,
    }
