from __future__ import annotations

import uuid
from enum import Enum


class PublicIdPrefix(str, Enum):
    LESSON_PLAN = "LP"
    LESSON_PLAN_VERSION = "LPV"
    LESSON_NOTE = "LN"
    ARTEFACT_PLAN = "ATP"
    ARTEFACT = "AT"
    CONTENT_APPROVAL = "CAP"
    ARTEFACT_BUILD_JOB = "ABJ"
    ARTEFACT_BATCH = "ATB"
    STUDENT_PACK_GENERATION = "SPG"
    EXPERIMENT = "EXP"
    EXPERIMENT_EXECUTION = "EXE"
    JOB = "JOB"
    EXPERIMENT_CONDITION_RUN = "ECR"
    EXPERIMENT_FOCAL_CASE = "EFC"
    EVALUATION_PACKET = "EPK"
    EVALUATION_RATER = "EVR"
    EVALUATION_RATING = "EVS"
    EVALUATION_AUDIT_ITEM = "SGA"
    EVALUATION_AUDIT_RATING = "SGR"
    RATER_ASSIGNMENT = "RAS"
    LEARNER = "ST"
    DIAGNOSTIC = "DG"
    EVENT = "EVT"
    REVISION_THREAD = "RVT"
    REVISION_TURN = "RVN"
    INVESTIGATION = "INV"
    C4_GOVERNANCE_DECISION = "C4G"
    CONTENT_DRAFT = "CDR"


def new_public_id(prefix: PublicIdPrefix | str) -> str:
    normalized_prefix = prefix.value if isinstance(prefix, PublicIdPrefix) else prefix
    return f"{normalized_prefix}-{uuid.uuid4().hex}"
