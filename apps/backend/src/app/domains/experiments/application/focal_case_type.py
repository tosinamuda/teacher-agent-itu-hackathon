"""Label one focal case from the learner's objective bands."""

from __future__ import annotations

from app.domains.experiments.domain import FocalCaseType
from app.domains.learner_state.domain.models import LearnerState

# A focal case carries one summary label for grouping and the rater/report surfaces;
# the per-objective bands in the learner-state snapshot are what actually drive P1.
# Derive the label from the learner's weakest band — their greatest need: remediate if
# any objective is remediate, else reinforce if any is reinforce, else extend. No
# diagnostic evidence leaves the need unknown.
_FOCAL_CASE_TYPE_BY_BAND: dict[str, FocalCaseType] = {
    "remediate": FocalCaseType.REMEDIATE,
    "reinforce": FocalCaseType.REINFORCE,
    "extend": FocalCaseType.EXTEND,
}


def focal_case_type_for_state(learner_state: LearnerState) -> FocalCaseType:
    """Summarise a learner's per-objective bands into one focal-case label (weakest band)."""
    bands = {objective.band for objective in learner_state.objective_states}
    for band in ("remediate", "reinforce", "extend"):
        if band in bands:
            return _FOCAL_CASE_TYPE_BY_BAND[band]
    return FocalCaseType.MIXED_OR_MISCONCEPTION
