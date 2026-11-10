"""Prepare and run one complete H2 experiment.

H2 starts from the first draw's C3 pack, approved once its validation has run, so its
precondition is that pack rather than a generation. Selecting the focal learners writes their
focal-case rows, which is why the transaction is committed before generation —
minutes of model calls must not hold it open.

Every precondition here fails as ``ConditionedInputsMissingError``: this path is
reached from the worker, so a failure is recorded on the execution row under the
INPUTS_MISSING category, not answered to an HTTP caller.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Protocol

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.learner_state_input import (
    to_session_signals,
    to_spec_objective_state,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_sources import (
    resolve_lesson_sources,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.experiments.application.conditioned_plan import (
    SessionPlanReader,
    validated_session_plan,
)
from app.domains.experiments.application.focal_case_records import (
    RecordedFocalCase,
    record_focal_cases,
)
from app.domains.experiments.application.focal_learner_selection import select_focal_learners
from app.domains.experiments.application.h2_base_pack import approved_h2_base
from app.domains.experiments.application.store import ExperimentStore
from app.domains.experiments.domain.types import ConditionedInputsMissingError
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
)
from app.domains.experiments.review_pack_study.h2.execution import (
    ApprovedBasePack,
    FocalLearner,
    H2ExperimentInput,
)
from app.domains.experiments.review_pack_study.h2.experiment import H2Experiment
from app.domains.experiments.review_pack_study.h2.outcomes import H2Verdict
from app.domains.experiments.review_pack_study.progress import ProgressSink, watch_generation
from app.domains.experiments.review_pack_study.run import ExperimentRun, LessonUnderStudy
from app.domains.expert_content.application.excerpts_port import ExcerptsPort
from app.domains.learners.models import LearnerProfile
from app.domains.teaching.models import TeacherWorkspace
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


class H2InputReader(SessionPlanReader, Protocol):
    """Base pack, learner, and diagnostic reads, beside the frozen plan, required for H2."""

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...

    async def list_executions_for_experiment(
        self, experiment_db_id: uuid.UUID
    ) -> list[ExperimentExecution]: ...

    async def list_condition_runs(
        self, execution_db_id: uuid.UUID
    ) -> list[ExperimentConditionRun]: ...

    async def current_artefact_for_condition_run(self, run_id: str) -> Artefact | None: ...

    async def get_workspace(self, workspace_id: uuid.UUID) -> TeacherWorkspace | None: ...

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[LearnerProfile]: ...

    async def latest_diagnostic_for_learner(
        self, *, student_id: str, plan_version_id: str
    ) -> ExitTicketSubmission | None: ...


@dataclass(frozen=True)
class H2Inputs:
    """The frozen records an H2 execution is entitled to run against."""

    experiment: Experiment
    plan_version_id: str
    session_plan: SessionPlanView
    grounding: JsonObject


async def run_h2_execution(
    *,
    store: ExperimentStore,
    excerpts: ExcerptsPort,
    execution: ExperimentExecution,
    runner: H2Experiment,
    on_progress: ProgressSink | None = None,
) -> H2Verdict:
    """Check the gate, record the focal cases, commit, then generate."""
    experiments = store.h2_inputs
    try:
        inputs = await validated_h2_inputs(experiments=experiments, execution=execution)
        base_pack = await approved_h2_base(
            experiments=experiments,
            experiment=inputs.experiment,
        )
        learners = await select_focal_learners(
            experiments=experiments,
            experiment=inputs.experiment,
        )
        focal_cases = await record_focal_cases(
            experiments=experiments,
            focal_cases=store.focal_cases,
            execution=execution,
            experiment=inputs.experiment,
            learners=learners,
        )
        experiment = await load_h2_experiment(
            excerpts=excerpts,
            execution=execution,
            inputs=inputs,
            base_pack=base_pack,
            focal_cases=focal_cases,
        )
        await store.commit()
    except BaseException:
        await store.rollback()
        raise

    with watch_generation(on_progress, total=len(experiment.learners)):
        return await runner.run(experiment=experiment)


async def validated_h2_inputs(
    *,
    experiments: H2InputReader,
    execution: ExperimentExecution,
) -> H2Inputs:
    """The experiment and the frozen plan it studies, or why neither is usable."""
    experiment = await experiments.get_experiment_by_db_id(execution.experiment_db_id)
    if experiment is None:
        raise ConditionedInputsMissingError("experiment_not_found")
    if experiment.plan_version_id is None:
        raise ConditionedInputsMissingError("experiment_plan_not_authored")
    plan = await validated_session_plan(experiments, experiment.plan_version_id)
    return H2Inputs(
        experiment=experiment,
        plan_version_id=experiment.plan_version_id,
        session_plan=plan.session_plan,
        grounding=plan.grounding,
    )


async def load_h2_experiment(
    *,
    excerpts: ExcerptsPort,
    execution: ExperimentExecution,
    inputs: H2Inputs,
    base_pack: ApprovedBasePack,
    focal_cases: tuple[RecordedFocalCase, ...],
) -> H2ExperimentInput:
    """Assemble what the H2 workflow runs against, resolving the lesson's sources."""
    return H2ExperimentInput(
        run=ExperimentRun(
            execution_db_id=execution.id,
            execution_id=execution.execution_id,
            experiment_id=inputs.experiment.experiment_id,
            plan_version_id=inputs.plan_version_id,
        ),
        lesson=LessonUnderStudy(
            session_plan=inputs.session_plan,
            sources=await resolve_lesson_sources(excerpts, inputs.session_plan),
            grounding=inputs.grounding,
        ),
        base_pack=base_pack,
        learners=tuple(_focal_learner(case) for case in focal_cases),
    )


def _focal_learner(case: RecordedFocalCase) -> FocalLearner:
    """Project one recorded focal case into what the H2 workflow personalises against."""
    return FocalLearner(
        focal_learner_id=case.learner.student_id,
        focal_case_db_id=case.focal_case.id,
        learner_states={
            objective.lesson_objective_id: to_spec_objective_state(objective)
            for objective in case.state.objective_states
        },
        session_signals=to_session_signals(case.state),
    )
