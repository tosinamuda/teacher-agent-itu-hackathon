"""A condition run must record the model that actually answered it.

Harness arms switch the model per process with ``set_model_override``. Recording
the *configured* model instead would attribute one arm's packs to another's
model — a reproducibility defect in the H1 numbers, not a tidiness one.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.condition_run_artefact import (  # noqa: E501  # noqa: E501
    SqlAlchemyReviewPackArtefactWriter,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.infrastructure.models import ExperimentConditionRun
from app.domains.experiments.infrastructure.sqlalchemy_condition_runs import (
    SqlAlchemyConditionRuns,
)
from app.domains.experiments.review_pack_study.condition_runs.records import (
    ClassLevelSubject,
    CompletedConditionRun,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.infra.dspy_lm import active_model_name, build_dspy_lm, set_model_override
from app.shared.session_plan_view import SessionPlanView

_ARM_MODEL = "openrouter/some-arm/model-under-test"


@pytest.fixture
def arm_model() -> Iterator[str]:
    """Run as a harness arm would: one model pinned for this process."""
    set_model_override(_ARM_MODEL)
    yield _ARM_MODEL
    set_model_override(None)


class _StagingSession:
    """Collects what would be written, so provenance needs no database."""

    def __init__(self) -> None:
        self.added: list[object] = []

    def add(self, instance: object) -> None:
        self.added.append(instance)


def _completed_run() -> CompletedConditionRun:
    profile = profile_for(Hypothesis.H1, ConditionCode.C0)
    session_plan = SessionPlanView.model_validate({"subject": "Mathematics"})
    return CompletedConditionRun(
        execution_db_id=uuid.uuid4(),
        condition_code=ConditionCode.C0,
        subject=ClassLevelSubject(),
        result=GeneratedReviewPack(
            request=BaseReviewPackRequestBuilder().build(
                session_plan=session_plan,
                policy=profile,
                sources=LessonSources(),
            ),
            sections=[],
        ),
        plan_version_id="LPV-1",
    )


def test_the_active_model_is_the_overridden_one(arm_model: str) -> None:
    assert active_model_name() == arm_model
    assert build_dspy_lm().model == arm_model


def test_a_condition_run_records_the_model_that_answered_it(arm_model: str) -> None:
    session = _StagingSession()

    run = SqlAlchemyConditionRuns(
        cast(AsyncSession, session),
        SqlAlchemyReviewPackArtefactWriter(cast(AsyncSession, session)),
    ).add_completed(
        record=_completed_run(),
    )

    assert run.model_name == arm_model
    assert isinstance(session.added[0], ExperimentConditionRun)


def test_provenance_falls_back_to_the_configured_model() -> None:
    """With no arm pinned, the role's declared model is the one that answers.

    The assignment lives in ``llm_models.ROLES`` rather than in the environment, so a run
    records what the repository says it used — a gitignored file cannot be provenance.
    """
    from app.infra.llm_models import for_role

    assert active_model_name() == for_role("generator")
