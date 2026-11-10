"""Retry one failed H1 condition under the execution lock."""

import logging
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Protocol

from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
)
from app.domains.experiments.application.condition_recovery import FailedConditionRunRecovery
from app.domains.experiments.application.h1_execution import load_h1_experiment
from app.domains.experiments.application.store import ExperimentStore
from app.domains.experiments.domain.types import (
    ConditionCode,
    ConditionRunStatus,
    ExecutionStatus,
    Hypothesis,
)
from app.domains.experiments.infrastructure.execution_context import (
    ConditionRetryContext,
    open_condition_retry_context,
)
from app.domains.experiments.review_pack_study.condition_runs.records import (
    ClassLevelSubject,
    CompletedConditionRun,
    recorded_grounding,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.experiments.review_pack_study.conditions.study_design import (
    PILOT_ONE_LESSON_CONFIG,
)
from app.domains.experiments.review_pack_study.h1.execution import H1ExperimentInput
from app.domains.generation_log.application.recorder import log_context

logger = logging.getLogger(__name__)


class ConditionRetryContextFactory(Protocol):
    """Open a retry's collaborators; nothing is written unless someone commits."""

    def __call__(self) -> AbstractAsyncContextManager[ConditionRetryContext]: ...


async def retry_failed_condition(
    execution_id: str,
    condition_code: str,
    contexts: ConditionRetryContextFactory = open_condition_retry_context,
) -> None:
    """Regenerate one failed condition and complete the execution when all recover."""
    async with contexts() as context:
        execution = await context.store.execution_lifecycle.get_execution_for_update(execution_id)
        if execution is None:
            logger.warning("retry: execution not found: %s", execution_id)
            return

        experiment = await load_h1_experiment(
            experiments=context.store.h1_inputs,
            excerpts=context.excerpts,
            execution=execution,
            study_config=PILOT_ONE_LESSON_CONFIG,
        )
        try:
            all_ok = await regenerate_failed_condition(
                store=context.store,
                condition_runs=context.condition_runs,
                experiment=experiment,
                condition_code=ConditionCode(condition_code),
            )
        except Exception:  # noqa: BLE001 - a re-failure must remain retryable
            await context.store.rollback()
            logger.exception("condition retry failed: %s %s", execution_id, condition_code)
            return

        if not all_ok:
            return
        refreshed = await context.store.execution_lifecycle.get_execution(execution_id)
        if refreshed is not None:
            refreshed.status = ExecutionStatus.SUCCEEDED
            refreshed.error_message = None
            refreshed.error_category = None
            await context.store.commit()


async def regenerate_failed_condition(
    *,
    store: ExperimentStore,
    condition_runs: FailedConditionRunRecovery,
    experiment: H1ExperimentInput,
    condition_code: ConditionCode,
    generator: Callable[[], GenerateBaseReviewPack] = build_base_review_pack_generator,
) -> bool:
    """Replace one failed H1 condition and every condition that forks its generation."""
    run = experiment.run
    target = await condition_runs.find(
        execution_db_id=run.execution_db_id,
        condition_code=condition_code,
    )
    if target is not None and target.status != ConditionRunStatus.FAILED:
        return not await condition_runs.has_failures(execution_db_id=run.execution_db_id)

    generated_by = profile_for(Hypothesis.H1, condition_code).generated_by
    with log_context(
        kind="experiment_condition",
        correlation_id=run.execution_id,
        experiment_id=run.experiment_id,
        plan_version_id=run.plan_version_id,
        hypothesis=Hypothesis.H1.value,
        condition_code=generated_by.value,
    ):
        # Built here, not above: constructing a generator opens a language model, and
        # the early return above is reached without ever generating.
        result = await generator().generate(
            session_plan=experiment.lesson.session_plan,
            policy=profile_for(Hypothesis.H1, generated_by).generation_policy(),
            sources=experiment.lesson.sources,
        )

    family = [
        code
        for code in experiment.design.h1_conditions
        if profile_for(Hypothesis.H1, code).generated_by == generated_by
    ]
    await condition_runs.replace_family(
        execution_db_id=run.execution_db_id,
        condition_codes=family,
        records=[
            CompletedConditionRun(
                execution_db_id=run.execution_db_id,
                condition_code=code,
                subject=ClassLevelSubject(),
                result=result,
                plan_version_id=run.plan_version_id,
                artefact_refs=recorded_grounding(Hypothesis.H1, code, experiment.lesson.grounding),
            )
            for code in family
        ],
    )
    await store.commit()
    return not await condition_runs.has_failures(execution_db_id=run.execution_db_id)
