"""Behavior contract for validating an experiment's selected focal learners."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from typing import Any, cast

import pytest

from app.domains.experiments.application.focal_learner_selection import (
    FocalLearnerReader,
    select_focal_learners,
)
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.learners.models import LearnerProfile


class _FocalLearnerReader:
    def __init__(self, learners: list[LearnerProfile]) -> None:
        self.class_id = uuid.uuid4()
        self.learners = learners
        self.diagnostic_students: list[str] = []

    async def get_workspace(self, workspace_id: uuid.UUID) -> Any:
        return SimpleNamespace(term_class_subject=SimpleNamespace(class_id=self.class_id))

    async def list_all_learners_for_class(self, *, class_id: uuid.UUID) -> list[LearnerProfile]:
        assert class_id == self.class_id
        return self.learners

    async def latest_diagnostic_for_learner(self, *, student_id: str, plan_version_id: str) -> Any:
        assert plan_version_id == "LPV-focal"
        self.diagnostic_students.append(student_id)
        return SimpleNamespace(diagnostic_id=f"D-{student_id}")


@pytest.mark.asyncio
async def test_selected_focal_learners_preserve_selection_order_and_require_evidence() -> None:
    learners = [
        LearnerProfile(
            student_id="student-a",
            full_name="Student A",
            grade="10",
            track="general",
        ),
        LearnerProfile(
            student_id="student-b",
            full_name="Student B",
            grade="10",
            track="general",
        ),
    ]
    reader = _FocalLearnerReader(learners)
    experiment = Experiment(
        experiment_id="EXP-focal",
        experiment_code="EXP-FOCAL",
        teacher_workspace_id=uuid.uuid4(),
        plan_version_id="LPV-focal",
        focal_learner_ids=["student-b", "student-a"],
    )

    selected = await select_focal_learners(
        experiments=cast(FocalLearnerReader, reader),
        experiment=experiment,
    )

    assert [learner.student_id for learner in selected] == ["student-b", "student-a"]
    assert reader.diagnostic_students == ["student-b", "student-a"]
