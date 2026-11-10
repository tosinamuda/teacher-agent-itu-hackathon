"""What one H2 experiment is handed before it starts."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    SessionSignals,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)

from ..run import ExperimentRun, LessonUnderStudy


@dataclass(frozen=True)
class ApprovedBasePack:
    """The first draw's C3 pack, approved programmatically in C4's place; P0 and P1 start here."""

    pack_id: str
    sections: list[ReviewPackSection]


@dataclass(frozen=True)
class FocalLearner:
    """One learner the experiment personalises for, and the state P1 adapts to."""

    focal_learner_id: str
    focal_case_db_id: uuid.UUID
    learner_states: dict[str, ObjectiveLearnerState]
    session_signals: SessionSignals | None = None


@dataclass(frozen=True)
class H2ExperimentInput:
    """One H2 execution: which run, which lesson, whose approved base, which learners.

    No study design: H2 is the P0/P1 contrast itself, so its condition pair is
    fixed where the packs are made rather than configured per run.
    """

    run: ExperimentRun
    lesson: LessonUnderStudy
    base_pack: ApprovedBasePack
    learners: tuple[FocalLearner, ...]
