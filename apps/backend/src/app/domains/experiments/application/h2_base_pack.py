"""The base pack H2 personalises from: the approved C3 pack of the experiment's first draw.

In the condition study the approval is programmatic: the first draw's C3 pack is approved once
its validation has run, and it takes C4's place as the approved base. P0 is that pack
unchanged; P1 is the same pack personalised to a learner's recorded state, so every learner's
P0 and P1 are made from one pack.

In the teacher's own flow the approval is the teacher's: C4 is C3 put through the review gate,
and learners' packs are made from it once the teacher approves it (``c4_base_pack``).
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Protocol

from pydantic import ValidationError

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.experiments.domain import ConditionCode, Hypothesis
from app.domains.experiments.domain.types import ConditionedInputsMissingError
from app.domains.experiments.review_pack_study.h2.execution import ApprovedBasePack

H2_BASE_PACK_ID_PREFIX = "c3-first-draw:"


class Draw(Protocol):
    """An execution, as far as telling which H1 draw came first."""

    @property
    def id(self) -> uuid.UUID: ...
    @property
    def hypothesis(self) -> str: ...
    @property
    def attempt_number(self) -> int: ...
    @property
    def created_at(self) -> datetime: ...


class ConditionRun(Protocol):
    """A condition run, as far as finding the pack it produced."""

    @property
    def condition_code(self) -> str: ...
    @property
    def experiment_condition_run_id(self) -> str: ...


class BasePack(Protocol):
    """A condition run's pack, as far as H2 reads it."""

    @property
    def artefact_id(self) -> str: ...
    @property
    def review_status(self) -> ArtefactReviewStatus: ...
    @property
    def manifest(self) -> dict: ...


class ExperimentRef(Protocol):
    @property
    def id(self) -> uuid.UUID: ...


class H2BaseReader(Protocol):
    """Read an experiment's H1 draws and the pack each condition run produced."""

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> Sequence[Draw]: ...

    async def list_condition_runs(self, execution_db_id: uuid.UUID) -> Sequence[ConditionRun]: ...

    async def current_artefact_for_condition_run(self, run_id: str) -> BasePack | None: ...


def first_draw_c3_run(
    executions: Sequence[Draw],
    runs_by_execution: Mapping[uuid.UUID, Sequence[ConditionRun]],
) -> ConditionRun | None:
    """The C3 run of the earliest H1 draw that has one; an attempt that ran no C3 is no draw."""
    draws = sorted(
        (e for e in executions if e.hypothesis == Hypothesis.H1.value),
        key=lambda e: (e.attempt_number, e.created_at),
    )
    for execution in draws:
        for run in runs_by_execution.get(execution.id, []):
            if run.condition_code == ConditionCode.C3.value:
                return run
    return None


async def first_draw_c3_artefact(
    *, experiments: H2BaseReader, experiment: ExperimentRef
) -> BasePack | None:
    """The first draw's C3 pack (any review status), or None before H1 has produced it."""
    executions = await experiments.list_executions_for_experiment(experiment.id)
    runs = {e.id: await experiments.list_condition_runs(e.id) for e in executions}
    run = first_draw_c3_run(executions, runs)
    if run is None:
        return None
    return await experiments.current_artefact_for_condition_run(run.experiment_condition_run_id)


async def approved_h2_base(
    *, experiments: H2BaseReader, experiment: ExperimentRef
) -> ApprovedBasePack:
    """The approved first-draw C3 pack H2 personalises from, or why it is not usable.

    Only H2's worker path calls this, so an unmet precondition is an input the run does not
    have — recorded on the execution row, never answered to an HTTP caller.
    """
    artefact = await first_draw_c3_artefact(experiments=experiments, experiment=experiment)
    if artefact is None:
        raise ConditionedInputsMissingError("h2_requires_first_draw_c3_base")
    if artefact.review_status != ArtefactReviewStatus.APPROVED:
        raise ConditionedInputsMissingError("h2_requires_approved_c3_base")
    try:
        pack = PostClassReviewPack.model_validate(artefact.manifest)
    except ValidationError as exc:
        raise ConditionedInputsMissingError("h2_base_pack_manifest_invalid") from exc
    sections = review_pack_manifest_to_sections(pack)
    if not sections:
        raise ConditionedInputsMissingError("h2_base_pack_has_no_sections")
    return ApprovedBasePack(
        pack_id=f"{H2_BASE_PACK_ID_PREFIX}{artefact.artefact_id}",
        sections=sections,
    )
