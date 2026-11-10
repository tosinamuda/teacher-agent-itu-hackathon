"""The precondition a synthetic-student run has to clear before it starts.

Not a view — it reads the same experiment context the dashboard does, which is
why it sits here, but its job is to refuse a run rather than to render one.
"""

from __future__ import annotations

from app.domains.experiments.application.c4_base_pack import (
    C4ArtefactReader,
    c4_pack_approved,
)
from app.domains.experiments.application.errors import ExperimentApplicationError
from app.domains.experiments.application.experiment_context_service import (
    ExperimentContextApplicationService,
    ExperimentContextReader,
)
from app.domains.experiments.infrastructure.models import Experiment


class SyntheticStudentContextQuery:
    """Resolve the plan/class inputs required to launch synthetic students."""

    def __init__(
        self,
        contexts: ExperimentContextReader,
        c4_artefacts: C4ArtefactReader,
    ) -> None:
        self.contexts = contexts
        self.c4_artefacts = c4_artefacts

    async def resolve(self, *, experiment: Experiment) -> tuple[str, str | None]:
        return await resolve_synthetic_students_context(
            self.contexts,
            self.c4_artefacts,
            experiment=experiment,
        )


async def resolve_synthetic_students_context(
    contexts: ExperimentContextReader,
    c4_artefacts: C4ArtefactReader,
    *,
    experiment: Experiment,
) -> tuple[str, str | None]:
    """Verify the synthetic-students precondition and return ``(plan_version_id, class_id)``.

    Raises ``ExperimentApplicationError(409)`` if the class-level base pack is not
    approved yet (synthetic students must answer a teacher-approved diagnostic).
    """
    context = await ExperimentContextApplicationService(contexts).get_experiment_context(
        experiment=experiment
    )
    if experiment.plan_version_id is None:
        raise ExperimentApplicationError(409, "experiment_plan_not_authored")
    # The base pack is the teacher-validated C4 condition-run artefact — gate on
    # its approval, not the auto-approved C3 (which would let students answer an
    # unvalidated diagnostic).
    if not await c4_pack_approved(experiments=c4_artefacts, experiment=experiment):
        raise ExperimentApplicationError(
            409, "Approve the class-level base pack before running synthetic students."
        )
    tcs = context.workspace.term_class_subject
    class_id = str(tcs.class_id) if tcs is not None and tcs.class_id is not None else None
    return experiment.plan_version_id, class_id
