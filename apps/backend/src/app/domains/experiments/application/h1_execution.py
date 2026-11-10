"""Prepare and run one complete H1 experiment.

Nothing is written while the inputs are read, but the transaction is still
committed before generation: it releases the connection rather than holding one
per run across minutes of model calls, and the runner opens its own store to
record what was produced.
"""

from __future__ import annotations

import uuid
from typing import Protocol

from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_sources import (
    resolve_lesson_sources,
)
from app.domains.experiments.application.conditioned_plan import (
    SessionPlanReader,
    validated_session_plan,
)
from app.domains.experiments.application.store import ExperimentStore
from app.domains.experiments.domain.types import ConditionedInputsMissingError
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.domains.experiments.review_pack_study.conditions.study_design import StudyDesignConfig
from app.domains.experiments.review_pack_study.h1.execution import H1ExperimentInput
from app.domains.experiments.review_pack_study.h1.experiment import H1Experiment
from app.domains.experiments.review_pack_study.h1.outcomes import H1Verdict
from app.domains.experiments.review_pack_study.progress import ProgressSink, watch_generation
from app.domains.experiments.review_pack_study.run import ExperimentRun, LessonUnderStudy
from app.domains.expert_content.application.excerpts_port import ExcerptsPort


class H1InputReader(SessionPlanReader, Protocol):
    """Experiment identity, beside the frozen plan and its note, required to prepare H1."""

    async def get_experiment_by_db_id(self, experiment_db_id: uuid.UUID) -> Experiment | None: ...


async def run_h1_execution(
    *,
    store: ExperimentStore,
    excerpts: ExcerptsPort,
    execution: ExperimentExecution,
    study_config: StudyDesignConfig,
    runner: H1Experiment,
    on_progress: ProgressSink | None = None,
) -> H1Verdict:
    """Load the frozen inputs, close the transaction, then generate."""
    experiment = await load_h1_experiment(
        experiments=store.h1_inputs,
        excerpts=excerpts,
        execution=execution,
        study_config=study_config,
    )
    await store.commit()
    with watch_generation(on_progress, total=len(experiment.design.conditions_to_generate())):
        return await runner.run(experiment=experiment)


async def load_h1_experiment(
    *,
    experiments: H1InputReader,
    excerpts: ExcerptsPort,
    execution: ExperimentExecution,
    study_config: StudyDesignConfig,
) -> H1ExperimentInput:
    """The lesson every condition generates from, or which input is missing."""
    experiment = await experiments.get_experiment_by_db_id(execution.experiment_db_id)
    if experiment is None:
        raise ConditionedInputsMissingError("experiment_not_found")
    if experiment.plan_version_id is None:
        raise ConditionedInputsMissingError("experiment_plan_not_authored")

    plan = await validated_session_plan(experiments, experiment.plan_version_id)

    return H1ExperimentInput(
        run=ExperimentRun(
            execution_db_id=execution.id,
            execution_id=execution.execution_id,
            experiment_id=experiment.experiment_id,
            plan_version_id=experiment.plan_version_id,
        ),
        lesson=LessonUnderStudy(
            session_plan=plan.session_plan,
            sources=await resolve_lesson_sources(excerpts, plan.session_plan),
            grounding=plan.grounding,
        ),
        design=study_config,
    )
