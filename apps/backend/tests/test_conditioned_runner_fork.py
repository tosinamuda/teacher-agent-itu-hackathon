"""Runner-level test: C4 forks C3's pack instead of regenerating.

Proves the H1 generation pass calls the generator once per owning condition (C0-C3)
and that the teacher-validation condition (C4) reuses C3's *exact* generation result —
so the C3->C4 contrast isolates the teacher gate, with no wasted 5th generation.
The artefact-materialisation internals are faked (this is about the fork wiring).
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from types import TracebackType

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.condition_runs.records import (
    CompletedConditionRun,
    FailedConditionRun,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.experiments.review_pack_study.conditions.study_design import (
    PILOT_ONE_LESSON_CONFIG,
)
from app.domains.experiments.review_pack_study.h1.execution import H1ExperimentInput
from app.domains.experiments.review_pack_study.h1.experiment import H1Experiment
from app.domains.experiments.review_pack_study.h1.outcomes import (
    AllConditionsGenerated,
    SomeConditionsFailed,
)
from app.domains.experiments.review_pack_study.run import ExperimentRun, LessonUnderStudy
from app.shared.session_plan_view import SessionPlanView


class _FakeService:
    """Records which conditions actually generate and returns a unique result each time."""

    def __init__(self) -> None:
        self.generated: list[ConditionCode] = []

    async def generate(
        self,
        *,
        session_plan: SessionPlanView,
        policy: ReviewPackGenerationPolicy,
        sources: LessonSources,
    ) -> GeneratedReviewPack:
        code = _code_for(policy)
        self.generated.append(code)
        return GeneratedReviewPack(
            request=BaseReviewPackRequestBuilder().build(
                session_plan=session_plan,
                policy=policy,
                sources=sources,
            ),
            sections=[],
        )


class _RecordingStore:
    def __init__(self) -> None:
        self.successes: list[CompletedConditionRun] = []
        self.failures: list[tuple[ConditionCode, str]] = []

    async def record(
        self,
        *,
        completed: Sequence[CompletedConditionRun],
        failed: Sequence[FailedConditionRun],
    ) -> None:
        self.successes.extend(completed)
        self.failures.extend((run.condition_code, run.error) for run in failed)


class _RecordingStoreFactory:
    """Stands in for ``open_experiment_store``, counting units of work and commits."""

    def __init__(self, records: _RecordingStore) -> None:
        self.condition_runs = records
        self.opened = 0
        self.commits = 0

    def __call__(self) -> _RecordingStoreFactory:
        return self

    async def __aenter__(self) -> _RecordingStoreFactory:
        self.opened += 1
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return None

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        raise AssertionError("these tests expect the batch to commit")


def _h1_input() -> H1ExperimentInput:
    return H1ExperimentInput(
        run=ExperimentRun(
            execution_db_id=uuid.uuid4(),
            execution_id="EXE-1",
            experiment_id="EXP-1",
            plan_version_id="LPV-1",
        ),
        lesson=LessonUnderStudy(
            session_plan=SessionPlanView.model_validate({"subject": "Mathematics"}),
            sources=LessonSources(),
        ),
        design=PILOT_ONE_LESSON_CONFIG,
    )


@pytest.mark.asyncio
async def test_run_h1_generates_c0_c3_once_and_forks_c4_from_c3() -> None:
    service = _FakeService()
    store = _RecordingStore()
    open_store = _RecordingStoreFactory(store)
    experiment = H1Experiment(
        generator=service,
        open_store=open_store,
    )

    outcome = await experiment.run(experiment=_h1_input())

    # Only C0-C3 generate (4 calls, not 5); C4 owns no generation.
    assert service.generated == [
        ConditionCode.C0,
        ConditionCode.C1,
        ConditionCode.C2,
        ConditionCode.C3,
    ]
    # All five conditions still persist a run, in registry order.
    assert [write.condition_code for write in store.successes] == [
        ConditionCode.C0,
        ConditionCode.C1,
        ConditionCode.C2,
        ConditionCode.C3,
        ConditionCode.C4,
    ]
    # The fork: C4's pack IS C3's exact generation result (same object), not a new draw.
    by_code = {write.condition_code: write.result for write in store.successes}
    assert by_code[ConditionCode.C4] is by_code[ConditionCode.C3]
    assert len(store.successes) == 5
    assert isinstance(outcome, AllConditionsGenerated)
    assert open_store.opened == 1
    assert open_store.commits == 1


@pytest.mark.asyncio
async def test_run_h1_persists_and_returns_partial_when_one_condition_fails() -> None:
    """One condition failing must NOT abort the batch: the others persist + a
    FAILED run is recorded and returned as an expected application outcome."""

    class _FailC2Service:
        def __init__(self) -> None:
            self.generated: list[ConditionCode] = []

        async def generate(
            self,
            *,
            session_plan: SessionPlanView,
            policy: ReviewPackGenerationPolicy,
            sources: LessonSources,
        ) -> GeneratedReviewPack:
            code = _code_for(policy)
            self.generated.append(code)
            if code == ConditionCode.C2:
                raise RuntimeError("LLM timeout")
            return GeneratedReviewPack(
                request=BaseReviewPackRequestBuilder().build(
                    session_plan=session_plan,
                    policy=policy,
                    sources=sources,
                ),
                sections=[],
            )

    service = _FailC2Service()
    store = _RecordingStore()
    open_store = _RecordingStoreFactory(store)
    experiment = H1Experiment(
        generator=service,
        open_store=open_store,
    )

    outcome = await experiment.run(experiment=_h1_input())

    # Only C2 failed; the others persist as success (incl. C4, which forks C3).
    assert isinstance(outcome, SomeConditionsFailed)
    assert [failure.condition_code for failure in outcome.failed_conditions] == [ConditionCode.C2]
    persisted_ok = [write.condition_code for write in store.successes]
    assert ConditionCode.C2 not in persisted_ok
    assert set(persisted_ok) == {
        ConditionCode.C0,
        ConditionCode.C1,
        ConditionCode.C3,
        ConditionCode.C4,
    }
    assert [code for code, _ in store.failures] == [ConditionCode.C2]
    assert open_store.opened == 1
    assert open_store.commits == 1


def _code_for(policy: ReviewPackGenerationPolicy) -> ConditionCode:
    return next(
        code
        for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3)
        if profile_for(Hypothesis.H1, code).generation_policy() == policy
    )
