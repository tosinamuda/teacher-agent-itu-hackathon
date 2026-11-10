"""Conduct one claimed conditioned experiment and record its terminal status."""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from app.domains.experiments.application.execution_lifecycle import (
    claim_execution,
    finalize_execution,
)
from app.domains.experiments.application.execution_outcome import (
    CompletionStatus,
    ExperimentOutcome,
    cancelled_completion,
    completion_status_for,
    failed_completion,
)
from app.domains.experiments.application.execution_progress import (
    discard_progress,
    progress_publisher,
)
from app.domains.experiments.application.h1_execution import run_h1_execution
from app.domains.experiments.application.h2_execution import run_h2_execution
from app.domains.experiments.domain.types import ExecutionStatus, Hypothesis
from app.domains.experiments.infrastructure.execution_context import (
    ExecutionContext,
    open_execution_context,
)
from app.domains.experiments.infrastructure.models import ExperimentExecution
from app.domains.experiments.review_pack_study.conditions.study_design import (
    PILOT_ONE_LESSON_CONFIG,
    StudyDesignConfig,
)
from app.domains.experiments.review_pack_study.progress import ProgressSink
from app.domains.experiments.review_pack_study.wiring import (
    build_h1_experiment,
    build_h2_experiment,
)
from app.shared.json_types import JsonObject

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HypothesisRun:
    """What an operator is told a run will do, and the use case that does it."""

    announcement: JsonObject
    conduct: Callable[[], Awaitable[ExperimentOutcome]]


async def conduct_conditioned_execution(
    execution_id: str,
    study_config: StudyDesignConfig | None = None,
    *,
    redelivered: bool = False,
) -> None:
    """Claim, conduct, classify, and finalize one conditioned experiment."""
    config = study_config or PILOT_ONE_LESSON_CONFIG
    publish: ProgressSink = discard_progress
    cancellation: asyncio.CancelledError | None = None
    async with open_execution_context() as context:
        execution = await claim_execution(context.store, execution_id, redelivered=redelivered)
        if execution is None:
            return
        publish = await progress_publisher(context.store.execution_progress, execution)

        try:
            outcome = await run_hypothesis(
                context=context,
                execution=execution,
                study_config=config,
                publish=publish,
            )
        except asyncio.CancelledError as exc:
            # Shutdown or task timeout. Recorded before unwinding, or the row is
            # stranded RUNNING and nothing retries what looks like work in progress.
            logger.warning("conditioned execution cancelled: %s", execution_id)
            cancellation = exc
            completion = cancelled_completion()
        except Exception as exc:  # noqa: BLE001 - terminal failure is persisted here
            logger.exception("conditioned execution failed: %s", execution_id)
            completion = failed_completion(exc)
        else:
            completion = completion_status_for(outcome)

    # Outside the attempt's own unit of work, and ahead of the event: the row is
    # what recovery reads, and a shielded write survives a second cancellation.
    await asyncio.shield(_finalize(execution_id, completion))
    publish(_terminal_event(completion))
    if cancellation is not None:
        raise cancellation


async def run_hypothesis(
    *,
    context: ExecutionContext,
    execution: ExperimentExecution,
    study_config: StudyDesignConfig,
    publish: ProgressSink,
) -> ExperimentOutcome:
    """Announce the work, then run the use case for this execution's hypothesis."""
    run = hypothesis_run(
        context=context,
        execution=execution,
        study_config=study_config,
        publish=publish,
    )
    publish(run.announcement)
    return await run.conduct()


def hypothesis_run(
    *,
    context: ExecutionContext,
    execution: ExperimentExecution,
    study_config: StudyDesignConfig,
    publish: ProgressSink,
) -> HypothesisRun:
    """This execution's hypothesis, wired to the attempt's collaborators.

    Only the selected hypothesis is built, and its runner only when ``conduct``
    runs: constructing one opens a language model.
    """
    hypothesis = Hypothesis(execution.hypothesis)
    match hypothesis:
        case Hypothesis.H1:
            generating = len(study_config.conditions_to_generate())
            return HypothesisRun(
                announcement=_start_event(
                    f"Generating {generating} study pack(s)…",
                    total=generating,
                ),
                conduct=lambda: run_h1_execution(
                    store=context.store,
                    excerpts=context.excerpts,
                    execution=execution,
                    study_config=study_config,
                    runner=build_h1_experiment(),
                    on_progress=publish,
                ),
            )
        case Hypothesis.H2:
            return HypothesisRun(
                announcement=_start_event("Generating personalised packs (P0/P1)…"),
                conduct=lambda: run_h2_execution(
                    store=context.store,
                    excerpts=context.excerpts,
                    execution=execution,
                    runner=build_h2_experiment(),
                    on_progress=publish,
                ),
            )
        case _:
            raise ValueError(f"unsupported experiment hypothesis: {hypothesis.value}")


async def _finalize(execution_id: str, completion: CompletionStatus) -> None:
    """Write the terminal status through a store this attempt has not used.

    The attempt's own unit of work has either been sitting idle across minutes of
    model calls or is carrying whatever just failed; the one write that must not
    be lost does not go through it.
    """
    async with open_execution_context() as context:
        await finalize_execution(
            context.store,
            execution_id,
            status=completion.status,
            error=completion.error,
            error_category=completion.error_category,
        )


def _start_event(message: str, *, total: int | None = None) -> JsonObject:
    """Announce work about to begin, with its size when that is known up front."""
    event: JsonObject = {"type": "start", "phase": "generation", "message": message}
    if total is not None:
        event |= {"done": 0, "total": total}
    return event


def _terminal_event(completion: CompletionStatus) -> JsonObject:
    """One terminal event per run: done when it succeeded, error when it did not."""
    return {
        "type": "done" if completion.status == ExecutionStatus.SUCCEEDED else "error",
        "phase": "generation",
        "message": completion.summary,
    }
