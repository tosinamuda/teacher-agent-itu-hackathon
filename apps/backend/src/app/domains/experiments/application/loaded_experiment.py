"""An experiment plus the things its dashboard view is rendered from.

The two view paths differ only in how they obtain these. The detail endpoint
loads one experiment's set directly (four round-trips); the list endpoint
batch-loads all N sets in a constant number of queries (see
``experiment_list_loader``). Both then render through the same
``experiment_views.experiment_view``, so this dataclass is where the
"what does a view need?" question has one answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.artefacts.core.infrastructure.models import Artefact
    from app.domains.experiments.application.experiment_context_service import (
        ExperimentContext,
        ExperimentFocalLearnerCandidate,
    )
    from app.domains.experiments.application.h2_base_pack import BasePack
    from app.domains.experiments.application.lesson_notes import LessonNoteState
    from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution


@dataclass(frozen=True)
class LoadedExperiment:
    """One experiment with its related rows resolved — no further I/O needed."""

    experiment: Experiment
    context: ExperimentContext
    executions: list[ExperimentExecution]
    focal_learners: list[ExperimentFocalLearnerCandidate]
    # The C4 pack, the lesson's class pack the teacher reviews, at whatever review status.
    base_pack: Artefact | None
    # H2's base, the first draw's C3 pack, at whatever review status.
    h2_base_pack: BasePack | None = None
    # The lesson's newest lesson note, at whatever review status.
    lesson_note: LessonNoteState | None = None
