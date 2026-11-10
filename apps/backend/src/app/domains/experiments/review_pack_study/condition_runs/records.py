"""Records produced when H1 or H2 attempts an experimental condition.

Who a pack was generated for decides three things at once — the hypothesis, the
artefact scope, and whether a learner is named — so they are one value here
rather than four fields a caller could disagree with itself about. H1 produces
one pack for the class; H2 produces one per focal learner.
"""

import uuid
from dataclasses import dataclass, field
from typing import ClassVar

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    reads_lesson_note,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.shared.json_types import JsonObject

from ..conditions.policies import ConditionProfile
from ..conditions.profiles import profile_for


@dataclass(frozen=True)
class ClassLevelSubject:
    """H1: the pack belongs to the class, so there is no learner to name.

    No fields — ``student_id`` and ``focal_case_db_id`` are constants a caller
    cannot set, which is what stops a class-level run carrying a learner.
    """

    hypothesis = Hypothesis.H1
    scope = ArtefactScope.CLASS_LEVEL
    student_id: ClassVar[None] = None
    focal_case_db_id: ClassVar[None] = None


@dataclass(frozen=True)
class FocalLearnerSubject:
    """H2: the pack belongs to one focal learner, who is always named."""

    student_id: str
    focal_case_db_id: uuid.UUID

    hypothesis = Hypothesis.H2
    scope = ArtefactScope.LEARNER_LEVEL


ConditionRunSubject = ClassLevelSubject | FocalLearnerSubject


@dataclass(frozen=True)
class _ConditionRun:
    """What every condition-run observation carries, whoever it was generated for."""

    execution_db_id: uuid.UUID
    condition_code: ConditionCode
    subject: ConditionRunSubject

    def __post_init__(self) -> None:
        # Raises when the code does not belong to the subject's hypothesis — a C0
        # recorded against a learner, or a P1 against the class.
        profile_for(self.subject.hypothesis, self.condition_code)

    @property
    def hypothesis(self) -> Hypothesis:
        return self.subject.hypothesis

    @property
    def scope(self) -> ArtefactScope:
        return self.subject.scope

    @property
    def student_id(self) -> str | None:
        return self.subject.student_id

    @property
    def focal_case_db_id(self) -> uuid.UUID | None:
        return self.subject.focal_case_db_id

    @property
    def profile(self) -> ConditionProfile:
        """The executable spec this condition ran under — never a caller's copy."""
        return profile_for(self.subject.hypothesis, self.condition_code)


@dataclass(frozen=True)
class CompletedConditionRun(_ConditionRun):
    """One completed condition and the generated pack to persist for it."""

    result: GeneratedReviewPack
    plan_version_id: str
    #: The lesson note the pack read, where its condition reads one.
    artefact_refs: JsonObject = field(default_factory=dict)


def recorded_grounding(
    hypothesis: Hypothesis, condition: ConditionCode, lesson_grounding: JsonObject
) -> JsonObject:
    """What a condition's pack records of the lesson's grounding: only a note it read."""
    policy = profile_for(hypothesis, condition).generation_policy()
    return dict(lesson_grounding) if reads_lesson_note(policy) else {}


@dataclass(frozen=True)
class FailedConditionRun(_ConditionRun):
    """One failed condition and the error to persist for it."""

    error: str
