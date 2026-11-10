"""A condition-run record cannot describe a run that could not have happened.

Backlog §3.2. The record used to carry ``hypothesis``, ``scope``, ``student_id``
and ``focal_case_db_id`` as four independent fields, so nothing stopped a
class-level H1 run naming a learner, or a P1 pack being recorded against the
class. Who the pack was for is one value now, and the condition code is checked
against the hypothesis that value implies.
"""

from __future__ import annotations

import uuid

import pytest

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.condition_runs.records import (
    ClassLevelSubject,
    CompletedConditionRun,
    FailedConditionRun,
    FocalLearnerSubject,
)


def _completed(code: ConditionCode, subject: object) -> CompletedConditionRun:
    return CompletedConditionRun(
        execution_db_id=uuid.uuid4(),
        condition_code=code,
        subject=subject,  # type: ignore[arg-type]
        result=None,  # type: ignore[arg-type]
        plan_version_id="LPV-1",
    )


def test_a_class_level_run_carries_no_learner() -> None:
    run = _completed(ConditionCode.C0, ClassLevelSubject())

    assert run.hypothesis is Hypothesis.H1
    assert run.scope is ArtefactScope.CLASS_LEVEL
    assert run.student_id is None
    assert run.focal_case_db_id is None


def test_a_class_level_subject_cannot_be_given_a_learner() -> None:
    with pytest.raises(TypeError):
        ClassLevelSubject(student_id="STU-1")  # type: ignore[call-arg]


def test_a_focal_learner_run_always_names_one() -> None:
    focal_case = uuid.uuid4()
    run = _completed(
        ConditionCode.P1,
        FocalLearnerSubject(student_id="STU-1", focal_case_db_id=focal_case),
    )

    assert run.hypothesis is Hypothesis.H2
    assert run.scope is ArtefactScope.LEARNER_LEVEL
    assert run.student_id == "STU-1"
    assert run.focal_case_db_id == focal_case


def test_a_focal_learner_subject_cannot_omit_the_learner() -> None:
    with pytest.raises(TypeError):
        FocalLearnerSubject()  # type: ignore[call-arg]


@pytest.mark.parametrize("code", [ConditionCode.P0, ConditionCode.P1])
def test_an_h2_condition_is_refused_against_the_class(code: ConditionCode) -> None:
    with pytest.raises(KeyError):
        _completed(code, ClassLevelSubject())


@pytest.mark.parametrize(
    "code", [ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3]
)
def test_an_h1_condition_is_refused_against_a_learner(code: ConditionCode) -> None:
    with pytest.raises(KeyError):
        _completed(code, FocalLearnerSubject(student_id="STU-1", focal_case_db_id=uuid.uuid4()))


def test_the_profile_is_derived_from_the_run_not_supplied_by_the_caller() -> None:
    run = _completed(ConditionCode.C3, ClassLevelSubject())

    assert run.profile.condition_code is ConditionCode.C3


def test_a_failed_run_is_constrained_the_same_way() -> None:
    with pytest.raises(KeyError):
        FailedConditionRun(
            execution_db_id=uuid.uuid4(),
            condition_code=ConditionCode.P1,
            subject=ClassLevelSubject(),
            error="boom",
        )
