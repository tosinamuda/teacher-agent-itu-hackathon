"""Run and record one complete H1 experiment execution."""

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from app.domains.artefacts.types.post_class_review_pack.application.generation_roles import (
    BaseReviewPackGenerator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.experiments.application.store import ExperimentStoreFactory
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.generation_log.application.recorder import log_context
from app.shared.json_types import JsonObject

from ..condition_runs.records import (
    ClassLevelSubject,
    CompletedConditionRun,
    FailedConditionRun,
    recorded_grounding,
)
from ..condition_runs.store import record_condition_runs
from ..conditions.profiles import profile_for
from ..progress import report_generated, report_generation_failed
from ..run import ExperimentRun
from .execution import H1ExperimentInput
from .outcomes import ConditionPacks, H1Verdict, verdict_for


class H1Experiment:
    """Execute the H1 condition family and record its condition grid."""

    def __init__(
        self,
        *,
        generator: BaseReviewPackGenerator,
        open_store: ExperimentStoreFactory,
    ) -> None:
        self._generator = generator
        self._open_store = open_store

    async def run(self, *, experiment: H1ExperimentInput) -> H1Verdict:
        """Generate a pack per automated condition, fork it to the gated one, save them all."""
        to_generate = experiment.design.conditions_to_generate()
        to_fork = experiment.design.conditions_to_fork()

        packs: ConditionPacks = {}
        for condition in to_generate:
            packs[condition] = await self._generate(experiment, condition)

        forked = _forked_packs(packs, to_fork)
        packs.update(forked)

        await self._save_condition_runs(experiment.run, experiment.lesson.grounding, packs)
        return verdict_for(packs)

    async def _generate(
        self,
        experiment: H1ExperimentInput,
        condition: ConditionCode,
    ) -> Result[GeneratedReviewPack, str]:
        """One condition's pack, holding any failure so its siblings still count."""
        run, lesson = experiment.run, experiment.lesson
        try:
            with log_context(
                kind="experiment_condition",
                correlation_id=run.execution_id,
                experiment_id=run.experiment_id,
                plan_version_id=run.plan_version_id,
                hypothesis=Hypothesis.H1.value,
                condition_code=condition.value,
            ):
                pack = await self._generator.generate(
                    session_plan=lesson.session_plan,
                    policy=profile_for(Hypothesis.H1, condition).generation_policy(),
                    sources=lesson.sources,
                )
        except Exception as exc:  # noqa: BLE001 - conditions fail independently
            report_generation_failed(condition)
            return Failure(str(exc) or "generation failed")
        report_generated(condition)
        return Success(pack)

    async def _save_condition_runs(
        self, run: ExperimentRun, grounding: JsonObject, packs: ConditionPacks
    ) -> None:
        """Save every generated and failed condition as one atomic observation batch."""
        completed = [
            CompletedConditionRun(
                execution_db_id=run.execution_db_id,
                condition_code=condition,
                subject=ClassLevelSubject(),
                result=pack.unwrap(),
                plan_version_id=run.plan_version_id,
                artefact_refs=recorded_grounding(Hypothesis.H1, condition, grounding),
            )
            for condition, pack in packs.items()
            if is_successful(pack)
        ]
        failed = [
            FailedConditionRun(
                execution_db_id=run.execution_db_id,
                condition_code=condition,
                subject=ClassLevelSubject(),
                error=pack.failure(),
            )
            for condition, pack in packs.items()
            if not is_successful(pack)
        ]

        await record_condition_runs(self._open_store, completed=completed, failed=failed)


def _forked_packs(
    packs: ConditionPacks,
    to_fork: tuple[tuple[ConditionCode, ConditionCode], ...],
) -> ConditionPacks:
    """Hand each gated condition the pack that the condition it forks produced."""
    forked: ConditionPacks = {}
    for condition, generated_by in to_fork:
        pack = packs.get(generated_by)
        if pack is None:
            raise ValueError(
                f"condition {condition.value} forks {generated_by.value}, which produced no pack"
            )
        forked[condition] = pack
    return forked
