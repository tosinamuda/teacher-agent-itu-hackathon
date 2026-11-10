"""Cross-run contamination between condition runs of one execution.

The sibling suite ``test_condition_leakage_downstream`` asks whether a single
condition's pack can contain material that condition forbids. This one asks the
other half: can one condition run reach into another's record?

Three places share mutable state by design:

* the H2 experiment reads ONE ``ApprovedBasePack.sections`` list for every H2
  condition AND every focal learner, and persists only after all of them have
  been produced.
* the H1 condition-family executor hands C4 the very same
  ``GeneratedReviewPack`` object as C3
  (the fork is deliberate — the teacher gate must be applied to C3's actual pack),
  so two condition writes project one object.
* failed-condition regeneration deletes and re-persists a condition plus everything
  that forks it.

Each test drives the real experiment workflow (persistence faked, no DB) and asserts that
nothing one run does is observable in another's persisted projection.
"""

from __future__ import annotations

import random
import uuid
from collections.abc import Sequence
from datetime import datetime, timezone
from types import SimpleNamespace, TracebackType
from typing import Any, cast

import pytest

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    ReviewPackRequest,
    SectionGenerationUnit,
    SourceFigure,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    normalise_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.condition_run_artefact import (  # noqa: E501  # noqa: E501
    review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
)
from app.domains.experiments.application.condition_retry import regenerate_failed_condition
from app.domains.experiments.application.store import ExperimentStore
from app.domains.experiments.domain.types import ConditionCode, ConditionRunStatus, Hypothesis
from app.domains.experiments.infrastructure.generated_review_pack_record import (
    generated_pack_record,
)
from app.domains.experiments.infrastructure.models import ExperimentConditionRun
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
from app.domains.experiments.review_pack_study.h2.execution import (
    ApprovedBasePack,
    FocalLearner,
    H2ExperimentInput,
)
from app.domains.experiments.review_pack_study.h2.experiment import H2Experiment
from app.domains.experiments.review_pack_study.h2.outcomes import SomeLearnersFailed
from app.domains.experiments.review_pack_study.run import ExperimentRun, LessonUnderStudy
from tests.condition_leakage_support import (
    CanaryPlan,
    EchoModel,
    build_canary_plan,
    fuzz_seeds,
    stand_in_collaborators,
)
from tests.log_tags import active_log_tags

_CREATED_AT = datetime(2026, 8, 10, tzinfo=timezone.utc)
_MUTATION_MARK = "SCRIBBLED-BY-P1"


class _FakeStore:
    """Unit-of-work stand-in used when persistence is replaced by a recording store."""

    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1


def _condition_packs(model: EchoModel) -> GenerateBaseReviewPack:
    return build_base_review_pack_generator(stand_in_collaborators(model))


class _RecordingStore:
    def __init__(self, target: ExperimentConditionRun | None = None) -> None:
        self.target = target
        self.captured: list[tuple[ConditionCode, Any]] = []
        self.writes: list[CompletedConditionRun] = []
        self.failed_writes: list[FailedConditionRun] = []
        self.batch_sizes: list[int] = []
        self.replaced_codes: list[ConditionCode] = []

    async def save_completed(
        self,
        *,
        records: Sequence[CompletedConditionRun],
        **_kwargs: object,
    ) -> list[SimpleNamespace]:
        self.batch_sizes.append(len(records))
        self._capture(records)
        return [SimpleNamespace(condition_code=record.condition_code.value) for record in records]

    async def record(
        self,
        *,
        completed: Sequence[CompletedConditionRun],
        failed: Sequence[FailedConditionRun],
    ) -> None:
        self.failed_writes.extend(failed)
        await self.save_completed(records=completed)

    async def find(
        self,
        *,
        execution_db_id: uuid.UUID,
        condition_code: ConditionCode,
    ) -> ExperimentConditionRun | None:
        return self.target

    async def has_failures(
        self,
        *,
        execution_db_id: uuid.UUID,
    ) -> bool:
        return False

    async def replace_family(
        self,
        *,
        execution_db_id: uuid.UUID,
        condition_codes: Sequence[ConditionCode],
        records: Sequence[CompletedConditionRun],
    ) -> None:
        self.replaced_codes = condition_codes
        self._capture(records)

    def _capture(self, writes: Sequence[CompletedConditionRun]) -> None:
        self.writes.extend(writes)
        self.captured.extend((write.condition_code, write.result) for write in writes)


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
        return None


def _manifest(result: Any, artefact_id: str, *, student_id: str | None = None) -> dict:
    return review_pack_manifest(
        result,
        artefact_id=artefact_id,
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL if student_id is None else ArtefactScope.LEARNER_LEVEL,
        student_id=student_id,
        created_at=_CREATED_AT,
    )


# ===== H2: one base pack, many condition runs and learners =====


class _ScribblingPersonaliser(EchoModel):
    """Personaliser that writes on the base section it was handed.

    Nothing in production mutates a base section today, so this stands in for any
    future in-place normalisation — and for the real hazard the learner executor
    could expose: P0's record and every later learner read the same objects.
    """

    async def personalise_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        learner_id = cast(PersonalisedReviewPackRequest, request).focal_learner_id
        base_section.title = f"{_MUTATION_MARK} {learner_id}"
        base_section.blocks.append(
            ReviewPackBlock(
                block_id=f"{_MUTATION_MARK}-{learner_id}",
                block_type="explanation",
                text=f"{_MUTATION_MARK} {learner_id}",
                lesson_objective_id=base_section.lesson_objective_id,
            )
        )
        return await super().personalise_section(
            request=request,
            unit=unit,
            base_section=base_section,
            learner_state=learner_state,
        )


async def _base_sections(plan: CanaryPlan) -> list[ReviewPackSection]:
    """An approved C4-style base pack for the H2 runs to share."""
    result = await _condition_packs(EchoModel()).generate(
        session_plan=plan.view,
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sources=plan.sources,
    )
    return result.sections


def _learner_ctx(plan_sections: list[ReviewPackSection], learner: str) -> FocalLearner:
    return FocalLearner(
        focal_learner_id=learner,
        focal_case_db_id=uuid.uuid4(),
        learner_states={
            section.lesson_objective_id: ObjectiveLearnerState(
                lesson_objective_id=section.lesson_objective_id, mastery_band="remediate"
            )
            for section in plan_sections
        },
    )


def _run() -> ExperimentRun:
    return ExperimentRun(
        execution_db_id=uuid.uuid4(),
        execution_id="EXE-1",
        experiment_id="EXP-1",
        plan_version_id="LPV-1",
    )


def _h1_input(plan: CanaryPlan) -> H1ExperimentInput:
    return H1ExperimentInput(
        run=_run(),
        lesson=LessonUnderStudy(session_plan=plan.view, sources=plan.sources),
        design=PILOT_ONE_LESSON_CONFIG,
    )


def _h2_input(
    plan: CanaryPlan,
    base_sections: list[ReviewPackSection],
    *,
    learners: tuple[FocalLearner, ...],
) -> H2ExperimentInput:
    return H2ExperimentInput(
        run=_run(),
        lesson=LessonUnderStudy(session_plan=plan.view, sources=plan.sources),
        base_pack=ApprovedBasePack(pack_id="AT-C4", sections=base_sections),
        learners=learners,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(11, 47))
async def test_h2_runs_never_share_base_section_objects(
    seed: int,
) -> None:
    plan = build_canary_plan(random.Random(seed))
    base_sections = await _base_sections(plan)
    pristine = [section.model_dump(mode="json") for section in base_sections]
    store = _RecordingStore()
    open_store = _RecordingStoreFactory(store)
    experiment = H2Experiment(
        personaliser=build_review_pack_personaliser(
            stand_in_collaborators(_ScribblingPersonaliser())
        ),
        open_store=open_store,
    )
    await experiment.run(
        experiment=_h2_input(
            plan,
            base_sections,
            learners=tuple(_learner_ctx(base_sections, learner) for learner in ("STU-A", "STU-B")),
        ),
    )
    payloads_by_learner = {
        learner: {
            write.condition_code: write.result
            for write in store.writes
            if write.student_id == learner
        }
        for learner in ("STU-A", "STU-B")
    }
    assert store.batch_sizes == [4]
    assert open_store.opened == 1
    assert open_store.commits == 1

    # The execution's approved base pack is untouched by any learner's run.
    assert [section.model_dump(mode="json") for section in base_sections] == pristine

    for learner, by_code in payloads_by_learner.items():
        assert isinstance(by_code[ConditionCode.P0].request, PersonalisedReviewPackRequest)
        p0_projection = str(
            (
                generated_pack_record(by_code[ConditionCode.P0]),
                _manifest(by_code[ConditionCode.P0], "AT-P0", student_id=learner),
            )
        )
        assert _MUTATION_MARK not in p0_projection, f"{learner}: P1 rewrote P0's record"
        # Positive control: the personaliser really did run and really did scribble.
        assert _MUTATION_MARK in str(generated_pack_record(by_code[ConditionCode.P1]))
        # No learner sees another learner's personalisation.
        other = "STU-B" if learner == "STU-A" else "STU-A"
        assert other not in p0_projection

    # P0 is the approved base verbatim: same sections, in order, with the base's
    # own titles — every learner's copy alike.
    for learner in payloads_by_learner:
        p0_manifest = _manifest(payloads_by_learner[learner][ConditionCode.P0], "AT-P0")
        assert [step["title"] for step in p0_manifest["steps"]] == [
            section["title"] for section in pristine
        ]

    # Pinned, not endorsed: P0's request is built with the focal learner's states,
    # so its manifest records a personalisation_band per step even though P0's
    # profile forbids using learner state. P1's bands are identical, so the pair
    # stays blind — but a P0 artefact does carry state P0 never consumed.
    bands_by_code = {
        code: [step.get("personalisation_band") for step in _manifest(result, "AT-x")["steps"]]
        for code, result in payloads_by_learner["STU-A"].items()
    }
    assert bands_by_code[ConditionCode.P0] == bands_by_code[ConditionCode.P1]
    assert set(bands_by_code[ConditionCode.P0]) == {"remediate"}


@pytest.mark.asyncio
async def test_h2_p1_model_calls_are_tagged_with_the_execution_and_learner() -> None:
    class _TagRecorder:
        def __init__(self) -> None:
            self._real = build_review_pack_personaliser(stand_in_collaborators(EchoModel()))
            self.tags: list[dict[str, Any]] = []

        def build_request(self, **kwargs: Any) -> Any:
            return self._real.build_request(**kwargs)

        async def personalise(self, **kwargs: Any) -> Any:
            self.tags.append(active_log_tags())
            return await self._real.personalise(**kwargs)

    plan = build_canary_plan(random.Random(83))
    base_sections = await _base_sections(plan)
    personaliser = _TagRecorder()
    experiment = H2Experiment(
        personaliser=personaliser,
        open_store=_RecordingStoreFactory(_RecordingStore()),
    )

    await experiment.run(
        experiment=_h2_input(plan, base_sections, learners=(_learner_ctx(base_sections, "STU-A"),)),
    )

    assert personaliser.tags == [
        {
            "kind": "experiment_condition",
            "correlation_id": "EXE-1",
            "experiment_id": "EXP-1",
            "plan_version_id": "LPV-1",
            "hypothesis": "H2",
            "condition_code": "P1",
            "student_id": "STU-A",
        }
    ]


@pytest.mark.asyncio
async def test_h2_records_the_learners_it_finished_when_one_learner_fails() -> None:
    """A learner's failure costs that learner, not the cohort.

    Every learner already produced is minutes of model calls, and nothing about a
    later learner's failure makes them unusable. The write is still one batch and
    the execution still ends FAILED (``SomeLearnersFailed``), so no partial cohort
    is ever read as complete. The failed learner is recorded as failed at BOTH
    conditions: H2's observation is the pair.
    """

    class _FailSecondLearner:
        """The real personaliser, except that one learner never finishes."""

        def __init__(self) -> None:
            self._real = build_review_pack_personaliser(stand_in_collaborators(EchoModel()))

        def build_request(self, **kwargs: Any) -> Any:
            return self._real.build_request(**kwargs)

        async def personalise(self, **kwargs: Any) -> Any:
            if kwargs["focal_learner_id"] == "STU-B":
                raise RuntimeError("personalisation failed")
            return await self._real.personalise(**kwargs)

    plan = build_canary_plan(random.Random(83))
    base_sections = await _base_sections(plan)
    store = _RecordingStore()
    open_store = _RecordingStoreFactory(store)
    experiment = H2Experiment(
        personaliser=_FailSecondLearner(),
        open_store=open_store,
    )

    verdict = await experiment.run(
        experiment=_h2_input(
            plan,
            base_sections,
            learners=tuple(_learner_ctx(base_sections, learner) for learner in ("STU-A", "STU-B")),
        ),
    )

    assert isinstance(verdict, SomeLearnersFailed)
    assert verdict.completed_learners == ("STU-A",)
    assert [failure.focal_learner_id for failure in verdict.failed_learners] == ["STU-B"]
    assert verdict.failed_learners[0].message == "personalisation failed"

    # One batch, one commit — the cohort is still written as a single observation.
    assert store.batch_sizes == [2]
    assert open_store.opened == 1
    assert open_store.commits == 1
    assert {(write.student_id, write.condition_code) for write in store.writes} == {
        ("STU-A", ConditionCode.P0),
        ("STU-A", ConditionCode.P1),
    }
    assert {(write.student_id, write.condition_code) for write in store.failed_writes} == {
        ("STU-B", ConditionCode.P0),
        ("STU-B", ConditionCode.P1),
    }


def test_grounded_figures_are_spliced_into_sections_as_copies() -> None:
    """A repair re-normalises the SAME unit, so two sections meet the same figure.

    Splicing the request's own block object in would put one mutable figure in two
    sections and in the request that produced them.
    """
    figure = SourceFigure(
        figure_id="fig1",
        variant="image",
        url="https://figures.example/one.png",
        caption="original caption",
        source_record_id="rec-1",
    )
    unit = SectionGenerationUnit(
        unit_id="step:s1",
        lesson_objective_id="lop01",
        objective_text="Objective",
        source_figures=[figure],
    )
    first = normalise_section(_empty_section("first"), unit)
    second = normalise_section(_empty_section("second"), unit)

    assert first.blocks[-1] is not second.blocks[-1]
    assert first.blocks[-1] is not figure
    first.blocks[-1].caption = "edited by the first section"
    assert second.blocks[-1].caption == "original caption"
    assert figure.caption == "original caption"
    assert not hasattr(figure, "lesson_objective_id")  # output identity never enters the request


def _empty_section(section_id: str) -> ReviewPackSection:
    return ReviewPackSection(
        section_id=section_id, title="t", lesson_objective_id="draft", blocks=[]
    )


# ===== H1: C4 forks C3's result object =====


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(19, 53))
async def test_c4_persist_cannot_reach_back_into_c3(
    seed: int,
) -> None:
    plan = build_canary_plan(random.Random(seed))
    store = _RecordingStore()
    experiment = H1Experiment(
        generator=_condition_packs(EchoModel()),
        open_store=_RecordingStoreFactory(store),
    )
    await experiment.run(experiment=_h1_input(plan))

    by_code = dict(store.captured)
    c3_result = by_code[ConditionCode.C3]
    assert by_code[ConditionCode.C4] is c3_result  # the fork is deliberate

    before = (generated_pack_record(c3_result), _manifest(c3_result, "AT-C3"))
    c4_manifest = _manifest(by_code[ConditionCode.C4], "AT-C4")
    after = (generated_pack_record(c3_result), _manifest(c3_result, "AT-C3"))
    assert after == before, "projecting C4 mutated the shared generation result"

    assert c4_manifest["artefact_id"] == "AT-C4"
    assert c4_manifest["steps"] == before[1]["steps"]
    # C4 lands as `pending` and can be edited under the teacher gate; that edit
    # must not travel back into C3's frozen manifest.
    c4_manifest["steps"][0]["title"] = "teacher edited this"
    c4_manifest["steps"][0]["blocks"].clear()
    assert _manifest(c3_result, "AT-C3") == before[1]


# ===== failed-condition regeneration scope =====


@pytest.mark.asyncio
async def test_regenerator_only_touches_the_forked_family() -> None:
    """Regenerating C3 re-persists C3 + its fork C4, and nothing else.

    Every affected condition must carry the SAME fresh result: a fork borrowing a
    sibling's older pack would silently break the C3->C4 contrast.
    """
    plan = build_canary_plan(random.Random(71))
    store = _RecordingStore(
        target=ExperimentConditionRun(
            experiment_condition_run_id="RUN-C3-FAILED",
            execution_db_id=uuid.uuid4(),
            hypothesis=Hypothesis.H1.value,
            condition_code="C3",
            status=ConditionRunStatus.FAILED,
        )
    )
    generator = _condition_packs(EchoModel())
    complete = await regenerate_failed_condition(
        store=cast(ExperimentStore, _FakeStore()),
        experiment=_h1_input(plan),
        condition_code=ConditionCode.C3,
        generator=lambda: generator,
        condition_runs=store,
    )

    assert complete is True
    assert [code for code, _ in store.captured] == [ConditionCode.C3, ConditionCode.C4]
    results = {id(result) for _, result in store.captured}
    assert len(results) == 1, "C4 must persist the freshly regenerated C3 result"
    assert store.replaced_codes == [ConditionCode.C3, ConditionCode.C4]
