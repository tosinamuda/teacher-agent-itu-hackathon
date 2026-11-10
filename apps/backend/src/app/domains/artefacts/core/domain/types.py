from __future__ import annotations

from enum import Enum


class ArtefactType(str, Enum):
    LESSON_PLAN = "lesson_plan"
    LESSON_NOTE = "lesson_note"
    POST_CLASS_REVIEW_PACK = "post_class_review_pack"
    #: The class test. The value is the key its revision threads were stored under.
    DIAGNOSTIC = "diagnostic"


class ArtefactScope(str, Enum):
    CLASS_LEVEL = "class_level"
    LEARNER_LEVEL = "learner_level"


class ArtefactPlanStatus(str, Enum):
    """Lifecycle of a class-level/learner-level ``ArtefactPlan`` (the build request)."""

    DRAFT = "draft"
    APPROVED = "approved"


class ArtefactReviewStatus(str, Enum):
    """Teacher review gate on a generated ``Artefact`` before students see it."""

    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"


DEFAULT_ARTEFACT_TYPE: ArtefactType = ArtefactType.POST_CLASS_REVIEW_PACK
