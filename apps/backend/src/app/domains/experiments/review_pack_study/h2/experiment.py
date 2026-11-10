"""Run and record one complete H2 experiment execution."""

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from app.domains.artefacts.types.post_class_review_pack.application.generation_roles import (
    ReviewPackPersonaliser,
)
from app.domains.artefacts.types.post_class_review_pack.application.personalise import (
    build_personalised_review_pack_request,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.experiments.application.store import ExperimentStoreFactory
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.generation_log.application.recorder import log_context

from ..condition_runs.records import (
    CompletedConditionRun,
    FailedConditionRun,
    FocalLearnerSubject,
    recorded_grounding,
)
from ..condition_runs.store import record_condition_runs
from ..conditions.profiles import condition_codes, profile_for
from ..progress import report_learner_failed, report_learner_packs
from .execution import FocalLearner, H2ExperimentInput
from .outcomes import CohortPacks, H2Verdict, LearnerPacks, verdict_for


class H2Experiment:
    """Execute every focal learner, then record the complete H2 batch."""

    def __init__(
        self,
        *,
        personaliser: ReviewPackPersonaliser,
        open_store: ExperimentStoreFactory,
    ) -> None:
        self._personaliser = personaliser
        self._open_store = open_store

    async def run(self, *, experiment: H2ExperimentInput) -> H2Verdict:
        """Copy the approved base for P0, personalise it for P1, save the whole cohort."""
        cohort_packs: CohortPacks = []
        for learner in experiment.learners:
            cohort_packs.append((learner, await self._learner_packs(experiment, learner)))

        await self._save_condition_runs(experiment, cohort_packs)
        return verdict_for(cohort_packs)

    async def _learner_packs(
        self,
        experiment: H2ExperimentInput,
        learner: FocalLearner,
    ) -> Result[LearnerPacks, str]:
        """One learner's pair, holding any failure so the rest of the cohort still counts."""
        try:
            packs: LearnerPacks = {
                ConditionCode.P0: self._copy_base_pack(experiment, learner),
                ConditionCode.P1: await self._personalise_pack(experiment, learner),
            }
        except Exception as exc:  # noqa: BLE001 - learners fail independently
            report_learner_failed(learner.focal_learner_id)
            return Failure(str(exc) or "personalisation failed")
        report_learner_packs(learner.focal_learner_id)
        return Success(packs)

    def _copy_base_pack(
        self,
        experiment: H2ExperimentInput,
        learner: FocalLearner,
    ) -> GeneratedReviewPack:
        """P0: the approved base copied for this learner. No model runs.

        It still builds its own request: every pack carries one, the rater-visible
        manifest is projected from it, and building it under P0's own profile keeps
        that record describing what the reuse arm was given — P0's units carry no
        source evidence — rather than what personalised P1.
        """
        return GeneratedReviewPack(
            request=build_personalised_review_pack_request(
                session_plan=experiment.lesson.session_plan,
                base_pack_id=experiment.base_pack.pack_id,
                focal_learner_id=learner.focal_learner_id,
                learner_states=learner.learner_states,
                policy=profile_for(Hypothesis.H2, ConditionCode.P0).generation_policy(),
                session_signals=learner.session_signals,
                sources=experiment.lesson.sources,
            ),
            sections=_own_copy(experiment.base_pack.sections),
        )

    async def _personalise_pack(
        self,
        experiment: H2ExperimentInput,
        learner: FocalLearner,
    ) -> GeneratedReviewPack:
        """P1: the approved base adapted to this learner's objective states."""
        run = experiment.run
        with log_context(
            kind="experiment_condition",
            correlation_id=run.execution_id,
            experiment_id=run.experiment_id,
            plan_version_id=run.plan_version_id,
            hypothesis=Hypothesis.H2.value,
            condition_code=ConditionCode.P1.value,
            student_id=learner.focal_learner_id,
        ):
            return await self._personaliser.personalise(
                session_plan=experiment.lesson.session_plan,
                base_sections=_own_copy(experiment.base_pack.sections),
                learner_states=learner.learner_states,
                base_pack_id=experiment.base_pack.pack_id,
                focal_learner_id=learner.focal_learner_id,
                policy=profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy(),
                session_signals=learner.session_signals,
                sources=experiment.lesson.sources,
            )

    async def _save_condition_runs(
        self,
        experiment: H2ExperimentInput,
        cohort_packs: CohortPacks,
    ) -> None:
        """Save every learner's conditions as one atomic observation batch.

        A learner who failed is recorded as a failure at BOTH conditions: the
        observation H2 makes is the pair, and a base copy with no personalisation
        beside it is not one. The grid analysis reads back therefore has a row per
        (learner, condition) either way, and the execution ends FAILED.
        """
        run = experiment.run
        completed = [
            CompletedConditionRun(
                execution_db_id=run.execution_db_id,
                condition_code=condition,
                subject=_subject(learner),
                result=pack,
                plan_version_id=run.plan_version_id,
                artefact_refs=recorded_grounding(
                    Hypothesis.H2, condition, experiment.lesson.grounding
                ),
            )
            for learner, packs in cohort_packs
            if is_successful(packs)
            for condition, pack in packs.unwrap().items()
        ]
        failed = [
            FailedConditionRun(
                execution_db_id=run.execution_db_id,
                condition_code=condition,
                subject=_subject(learner),
                error=packs.failure(),
            )
            for learner, packs in cohort_packs
            if not is_successful(packs)
            for condition in condition_codes(Hypothesis.H2)
        ]

        await record_condition_runs(self._open_store, completed=completed, failed=failed)


def _subject(learner: FocalLearner) -> FocalLearnerSubject:
    """Who a pack was generated for: this learner, and the focal case recording them."""
    return FocalLearnerSubject(
        student_id=learner.focal_learner_id,
        focal_case_db_id=learner.focal_case_db_id,
    )


def _own_copy(sections: list[ReviewPackSection]) -> list[ReviewPackSection]:
    """Deep copies, so one condition run can never write into another's sections."""
    return [section.model_copy(deep=True) for section in sections]
