"""Decide which learners an experiment may study."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from app.domains.assessments.models import ExitTicketSubmission
from app.domains.experiments.domain.types import ConditionedInputsMissingError
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.learners.models import LearnerProfile
from app.domains.teaching.models import TeacherWorkspace


class FocalLearnerReader(Protocol):
    """Class membership and diagnostic evidence used to validate a focal selection."""

    async def get_workspace(self, workspace_id: UUID) -> TeacherWorkspace | None: ...

    async def list_all_learners_for_class(self, *, class_id: UUID) -> list[LearnerProfile]: ...

    async def latest_diagnostic_for_learner(
        self, *, student_id: str, plan_version_id: str
    ) -> ExitTicketSubmission | None: ...


async def select_focal_learners(
    *,
    experiments: FocalLearnerReader,
    experiment: Experiment,
) -> tuple[LearnerProfile, ...]:
    """Resolve the experiment's selected focal-learner IDs to LearnerProfile rows.

    Every selected learner must be in the workspace's class AND hold a diagnostic
    submission for the plan version; each way of failing names itself.
    """
    if experiment.plan_version_id is None:
        raise ConditionedInputsMissingError("experiment_plan_not_authored")
    selected_ids = list(experiment.focal_learner_ids or [])
    if not selected_ids:
        raise ConditionedInputsMissingError("focal_learners_not_selected")

    class_id = await _workspace_class_id(experiments=experiments, experiment=experiment)
    in_class = {
        learner.student_id: learner
        for learner in await experiments.list_all_learners_for_class(class_id=class_id)
    }
    learners: list[LearnerProfile] = []
    for learner_id in selected_ids:
        learner = in_class.get(learner_id)
        if learner is None:
            raise ConditionedInputsMissingError("focal_learner_not_in_workspace_class")
        diagnostic = await experiments.latest_diagnostic_for_learner(
            student_id=learner.student_id,
            plan_version_id=experiment.plan_version_id,
        )
        if diagnostic is None:
            raise ConditionedInputsMissingError("focal_learner_evidence_missing")
        learners.append(learner)
    return tuple(learners)


async def _workspace_class_id(
    *,
    experiments: FocalLearnerReader,
    experiment: Experiment,
) -> UUID:
    """The class taught in this experiment's workspace — the only one it may select from."""
    workspace = await experiments.get_workspace(experiment.teacher_workspace_id)
    if workspace is None or workspace.term_class_subject is None:
        raise ConditionedInputsMissingError("workspace_class_not_found")
    return workspace.term_class_subject.class_id
