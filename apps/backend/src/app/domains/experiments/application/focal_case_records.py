"""Record the focal case one execution studies for one learner."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from app.domains.assessments.models import ExitTicketSubmission
from app.domains.experiments.application.focal_case_type import focal_case_type_for_state
from app.domains.experiments.domain.types import ConditionedInputsMissingError
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.learner_state import LearnerStateService
from app.domains.learner_state.domain.models import LearnerState
from app.domains.learners.models import LearnerProfile
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.time import utc_now


@dataclass(frozen=True)
class RecordedFocalCase:
    """One learner, the state read for them, and the focal case persisted for it."""

    learner: LearnerProfile
    state: LearnerState
    focal_case: ExperimentFocalCase


class FocalCaseEvidenceReader(Protocol):
    """Diagnostic evidence used to snapshot one selected learner's state."""

    async def latest_diagnostic_for_learner(
        self, *, student_id: str, plan_version_id: str
    ) -> ExitTicketSubmission | None: ...


class FocalCaseWriter(Protocol):
    """Stage one focal-case row inside the H2 input transaction."""

    async def save_focal_case(self, focal_case: ExperimentFocalCase) -> ExperimentFocalCase: ...


async def record_focal_cases(
    *,
    experiments: FocalCaseEvidenceReader,
    focal_cases: FocalCaseWriter,
    execution: ExperimentExecution,
    experiment: Experiment,
    learners: Sequence[LearnerProfile],
) -> tuple[RecordedFocalCase, ...]:
    """Snapshot every selected learner's state, in selection order, as a focal case."""
    learner_states = LearnerStateService()
    recorded = [
        await _record_one(
            experiments=experiments,
            focal_cases=focal_cases,
            learner_states=learner_states,
            execution=execution,
            experiment=experiment,
            learner=learner,
            rank=rank,
        )
        for rank, learner in enumerate(learners)
    ]
    return tuple(recorded)


async def _record_one(
    *,
    experiments: FocalCaseEvidenceReader,
    focal_cases: FocalCaseWriter,
    learner_states: LearnerStateService,
    execution: ExperimentExecution,
    experiment: Experiment,
    learner: LearnerProfile,
    rank: int,
) -> RecordedFocalCase:
    """Build one learner's state from their latest diagnostic and persist its focal case."""
    if experiment.plan_version_id is None:
        raise ConditionedInputsMissingError("experiment_plan_not_authored")
    diagnostic = await experiments.latest_diagnostic_for_learner(
        student_id=learner.student_id,
        plan_version_id=experiment.plan_version_id,
    )
    diagnostic_results: JsonObject | None = (
        diagnostic.results
        if diagnostic is not None and isinstance(diagnostic.results, dict)
        else None
    )
    state = learner_states.build(
        student_id=learner.student_id,
        student_profile=learner,
        diagnostic_id=diagnostic.diagnostic_id if diagnostic is not None else None,
        diagnostic_results=diagnostic_results,
    )
    focal_case = await focal_cases.save_focal_case(
        ExperimentFocalCase(
            experiment_focal_case_id=new_public_id(PublicIdPrefix.EXPERIMENT_FOCAL_CASE),
            execution_db_id=execution.id,
            student_id=learner.student_id,
            focal_case_type=focal_case_type_for_state(state).value,
            learner_state_snapshot=state.model_dump(mode="json"),
            selection_metadata={
                "selection_rank": rank + 1,
                "source": "selected_focal_learners",
            },
            created_at=utc_now(),
        ),
    )
    return RecordedFocalCase(learner=learner, state=state, focal_case=focal_case)
