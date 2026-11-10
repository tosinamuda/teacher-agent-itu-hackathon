"""The C4 pack: C3's pack put through the teacher's review gate.

In the teacher's flow, C4's pack is the lesson's class pack: the teacher reviews, revises and
approves it, and learners' personalised packs are made from it once approved. In the condition
study the approval is programmatic instead: the first draw's C3 pack, approved once its
validation has run, takes C4's place as H2's base (``h2_base_pack``).

There is no separate decision-recording surface. The teacher approves the C4 condition-run
artefact itself, so ``current_c4_artefact`` is the single source of truth for the pack the
teacher validates, and ``c4_pack_approved`` reads its review status.
"""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.experiments.domain import ConditionCode, Hypothesis
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)


class C4ArtefactReader(Protocol):
    """Read the teacher-governed C4 pack attached to an experiment."""

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> list[ExperimentConditionRun]: ...

    async def current_artefact_for_condition_run(self, run_id: str) -> Artefact | None: ...


async def current_c4_artefact(
    *,
    experiments: C4ArtefactReader,
    experiment: Experiment,
) -> Artefact | None:
    """The experiment's C4 base-pack artefact (any review status), or None.

    This is the pack the teacher reviews and approves: the H1 pipeline forks it
    from C3 as PENDING, and the teacher's approval flips it to APPROVED. Returns
    None before H1 has run. The resolver prefers the approved version when
    several artefacts exist for the run.
    """
    for execution in await experiments.list_executions_for_experiment(experiment.id):
        if execution.hypothesis != Hypothesis.H1.value:
            continue
        for run in await experiments.list_condition_runs(execution.id):
            if run.condition_code != ConditionCode.C4.value:
                continue
            artefact = await experiments.current_artefact_for_condition_run(
                run.experiment_condition_run_id
            )
            if artefact is not None:
                return artefact
    return None


async def c4_pack_approved(
    *,
    experiments: C4ArtefactReader,
    experiment: Experiment,
) -> bool:
    """Whether the teacher has approved C4, the lesson's class pack."""
    artefact = await current_c4_artefact(experiments=experiments, experiment=experiment)
    return artefact is not None and artefact.review_status == ArtefactReviewStatus.APPROVED
