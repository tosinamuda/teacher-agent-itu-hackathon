"""Real-DB atomicity tests for the conditioned-run persistence + retry paths.

Two transaction invariants that had only been happy-path-validated live (2026-06):

* ``SqlAlchemyConditionRuns.save_completed`` — the SAVEPOINT the conditioned worker
  worker relies on. A whole H1/H2 batch must land together; a failure anywhere in
  the batch must roll back every run already staged, never a partial condition grid
  (which would corrupt the results dashboard).
* ``regenerate_failed_condition`` — the ``retry_condition_run`` worker path. Retrying a
  FAILED condition deletes the stale run and inserts a fresh succeeded run + linked
  artefact in one transaction, leaving frozen (succeeded) conditions untouched.

These run against the MySQL test DB (real INSERT/DELETE/SAVEPOINT semantics) with
the LLM generator mocked, so a transaction-boundary regression fails here rather
than only in production.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError

from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    GenerationPolicyContext,
    LessonContextForGeneration,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.prompt_provenance import (
    PromptProvenance,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.condition_run_artefact import (  # noqa: E501  # noqa: E501
    SqlAlchemyReviewPackArtefactWriter,
)
from app.domains.experiments.application.condition_retry import regenerate_failed_condition
from app.domains.experiments.domain.types import (
    ConditionCode,
    ConditionRunStatus,
    Hypothesis,
)
from app.domains.experiments.infrastructure import sqlalchemy_condition_runs as runs_module
from app.domains.experiments.infrastructure.models import ExperimentConditionRun
from app.domains.experiments.infrastructure.sqlalchemy_condition_runs import (
    SqlAlchemyConditionRuns,
)
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)
from app.domains.experiments.review_pack_study.condition_runs.records import (
    ClassLevelSubject,
    CompletedConditionRun,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.experiments.review_pack_study.conditions.study_design import (
    PILOT_ONE_LESSON_CONFIG,
)
from app.domains.experiments.review_pack_study.h1.execution import H1ExperimentInput
from app.domains.experiments.review_pack_study.run import ExperimentRun, LessonUnderStudy
from app.shared.ids import PublicIdPrefix
from app.shared.session_plan_view import SessionPlanView

pytestmark = pytest.mark.asyncio

_OBJ = "obj-1"


def _result() -> GeneratedReviewPack:
    """A minimal but real conditioned-generation result the persistence path accepts."""
    return GeneratedReviewPack(
        request=BaseReviewPackRequest(
            artefact_spec=revision_pack_spec("JSS1"),
            generation_policy=profile_for(Hypothesis.H1, ConditionCode.C0).generation_policy(),
            policy=GenerationPolicyContext(
                require_source_refs=False,
                use_only_provided_sources=False,
                preserve_lesson_objective=True,
                instruction_summary="test",
            ),
            lesson_context=LessonContextForGeneration(
                subject="Mathematics",
                grade_level="7",
                topic="Fractions",
                lesson_objectives=["Add fractions"],
            ),
            units=[
                SectionGenerationUnit(
                    unit_id="u1", lesson_objective_id=_OBJ, objective_text="Add fractions"
                )
            ],
        ),
        sections=[
            ReviewPackSection(
                section_id="s1",
                title="Adding fractions",
                lesson_objective_id=_OBJ,
                blocks=[
                    ReviewPackBlock(
                        block_id="b1",
                        block_type="explanation",
                        text="1/2 + 1/2 = 1",
                        lesson_objective_id=_OBJ,
                    )
                ],
            )
        ],
        validation=None,  # None -> the run persists as SUCCEEDED
        prompt_provenance=PromptProvenance(components={"base_generation": "prompt-test-version"}),
    )


def _payload(execution_db_id: uuid.UUID, code: ConditionCode) -> CompletedConditionRun:
    return CompletedConditionRun(
        execution_db_id=execution_db_id,
        condition_code=code,
        subject=ClassLevelSubject(),
        result=_result(),
        plan_version_id="LPV-1",
    )


class _FakeService:
    """generate_base returns a fixed real result — no LLM call."""

    async def generate(self, **_kwargs: Any) -> GeneratedReviewPack:
        return _result()


async def _count_runs(db: Any, execution_db_id: uuid.UUID) -> int:
    return await db.scalar(
        select(func.count())
        .select_from(ExperimentConditionRun)
        .where(ExperimentConditionRun.execution_db_id == execution_db_id)
    )


async def _count_artefacts_for_execution(db: Any, execution_db_id: uuid.UUID) -> int:
    return await db.scalar(
        select(func.count())
        .select_from(Artefact)
        .join(
            ExperimentConditionRun,
            Artefact.experiment_condition_run_id
            == ExperimentConditionRun.experiment_condition_run_id,
        )
        .where(ExperimentConditionRun.execution_db_id == execution_db_id)
    )


# --- conditioned-execution SAVEPOINT path ---


async def test_savepoint_persists_full_batch(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    store = SqlAlchemyConditionRuns(db, SqlAlchemyReviewPackArtefactWriter(db))
    execution_db_id = uuid.uuid4()
    payloads = [
        _payload(execution_db_id, ConditionCode.C0),
        _payload(execution_db_id, ConditionCode.C1),
    ]

    runs = await store.save_completed(records=payloads)

    assert len(runs) == 2
    expected_fingerprint = _result().prompt_provenance.composite_fingerprint
    assert all(run.prompt_version == expected_fingerprint for run in runs)
    assert all(
        run.generated_pack["prompt_provenance"]
        == {  # type: ignore[index]
            "components": {"base_generation": "prompt-test-version"}
        }
        for run in runs
    )
    assert await _count_runs(db, execution_db_id) == 2
    # Each run materialised exactly one linked artefact.
    assert await _count_artefacts_for_execution(db, execution_db_id) == 2


async def test_savepoint_rolls_back_entire_batch_on_failure(db, monkeypatch) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    store = SqlAlchemyConditionRuns(db, SqlAlchemyReviewPackArtefactWriter(db))
    execution_db_id = uuid.uuid4()

    # Force both runs to claim the SAME experiment_condition_run_id so the second
    # INSERT violates the unique index when the SAVEPOINT flushes — a real DB
    # failure mid-batch. Artefact ids keep their real (unique) values.
    real_new_id = runs_module.new_public_id

    def _collide_run_ids(prefix: PublicIdPrefix) -> str:
        if prefix == PublicIdPrefix.EXPERIMENT_CONDITION_RUN:
            return "RUN-COLLIDE"
        return real_new_id(prefix)

    monkeypatch.setattr(runs_module, "new_public_id", _collide_run_ids)

    payloads = [
        _payload(execution_db_id, ConditionCode.C0),
        _payload(execution_db_id, ConditionCode.C1),
    ]

    with pytest.raises(IntegrityError):
        await store.save_completed(records=payloads)

    # The SAVEPOINT rolled the whole batch back: neither the first run nor its
    # artefact survives, even though the first INSERT had succeeded before the
    # collision.
    assert await _count_runs(db, execution_db_id) == 0
    assert await _count_artefacts_for_execution(db, execution_db_id) == 0


# --- retry_condition_run path ---


async def test_regenerate_replaces_failed_condition_and_leaves_frozen_untouched(db) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    execution_db_id = uuid.uuid4()
    # A FAILED C0 (the retry target; failed runs carry no artefact) and a frozen,
    # SUCCEEDED C1 the retry must not touch.
    failed_c0 = ExperimentConditionRun(
        experiment_condition_run_id="RUN-C0-OLD",
        execution_db_id=execution_db_id,
        hypothesis=Hypothesis.H1.value,
        condition_code=ConditionCode.C0.value,
        status=ConditionRunStatus.FAILED,
        error_message="LLM timeout",
    )
    frozen_c1 = ExperimentConditionRun(
        experiment_condition_run_id="RUN-C1-OK",
        execution_db_id=execution_db_id,
        hypothesis=Hypothesis.H1.value,
        condition_code=ConditionCode.C1.value,
        status=ConditionRunStatus.SUCCEEDED,
    )
    db.add_all([failed_c0, frozen_c1])
    await db.flush()
    frozen_c1_pk = frozen_c1.id

    all_ok = await regenerate_failed_condition(
        store=SqlAlchemyExperimentStore(db),
        condition_runs=SqlAlchemyConditionRuns(db, SqlAlchemyReviewPackArtefactWriter(db)),
        experiment=H1ExperimentInput(
            run=ExperimentRun(
                execution_db_id=execution_db_id,
                execution_id="EXE-1",
                experiment_id="EXP-1",
                plan_version_id="LPV-1",
            ),
            lesson=LessonUnderStudy(
                session_plan=SessionPlanView.model_validate({"subject": "Mathematics"}),
                sources=LessonSources(),
            ),
            design=PILOT_ONE_LESSON_CONFIG,
        ),
        condition_code=ConditionCode.C0,
        generator=_FakeService,
    )

    assert all_ok is True  # no FAILED runs remain
    # The stale FAILED C0 row is gone, replaced by exactly one fresh SUCCEEDED run.
    c0_runs = (
        (
            await db.execute(
                select(ExperimentConditionRun).where(
                    ExperimentConditionRun.execution_db_id == execution_db_id,
                    ExperimentConditionRun.condition_code == ConditionCode.C0.value,
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(c0_runs) == 1
    fresh_c0 = c0_runs[0]
    assert fresh_c0.experiment_condition_run_id != "RUN-C0-OLD"
    assert fresh_c0.status == ConditionRunStatus.SUCCEEDED
    # Exactly one artefact for the execution, linked to the fresh run — no orphan.
    assert await _count_artefacts_for_execution(db, execution_db_id) == 1
    linked = (
        await db.execute(
            select(Artefact.experiment_condition_run_id).where(
                Artefact.experiment_condition_run_id == fresh_c0.experiment_condition_run_id
            )
        )
    ).scalar_one()
    assert linked == fresh_c0.experiment_condition_run_id
    # The frozen, succeeded C1 is the same untouched row.
    c1 = (
        await db.execute(
            select(ExperimentConditionRun).where(
                ExperimentConditionRun.execution_db_id == execution_db_id,
                ExperimentConditionRun.condition_code == ConditionCode.C1.value,
            )
        )
    ).scalar_one()
    assert c1.id == frozen_c1_pk
    assert c1.status == ConditionRunStatus.SUCCEEDED
