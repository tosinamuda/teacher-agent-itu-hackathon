"""Aggregate model metadata for migrations."""

# pylint: disable=duplicate-code
# Central model registry: __all__ necessarily re-lists model class names that the
# per-domain model packages also export, and it is load-bearing (it marks the
# registration imports below as re-exported so they are not flagged unused).

from app.db.base import Base
from app.domains.artefact_revision.models import RevisionThread, RevisionTurn
from app.domains.artefacts.core.infrastructure.models import Artefact as BuiltArtefact
from app.domains.artefacts.core.infrastructure.models import (
    ArtefactPlan,
    ContentApproval,
    ContentSpecificationRecord,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.assessments.models.study_classwork import (
    StudyClassworkAnswer,
    StudyClassworkQuestion,
    StudyClassworkScript,
)
from app.domains.attachments.models import Attachment
from app.domains.content.infrastructure.models import ContentSkillRecord, ContentTypeRecord
from app.domains.content_engine.infrastructure.models import ContentDraftRecord
from app.domains.curriculum.models.curriculum import (
    ClassSession,
    CurriculumSubtopic,
    CurriculumTopic,
    ReferenceMaterial,
)
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.curriculum.models.knowledge_components import KnowledgeComponent
from app.domains.curriculum.models.themes import CurriculumTheme
from app.domains.evaluation.infrastructure import (
    EvaluationAuditItem,
    EvaluationAuditRating,
    EvaluationPacket,
    EvaluationRater,
    EvaluationRating,
)
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)
from app.domains.events.models.events import Event
from app.domains.experiments.infrastructure import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.experiments.infrastructure.study_import_models import StudyImport
from app.domains.experiments.infrastructure.study_transcript_models import StudyTranscript
from app.domains.expert_content.models import (
    AoTextbookLinkage,
    AoTextbookLinkageSeedRun,
    AoTextbookObjectiveLink,
    AoTextbookRecordLink,
    TextbookPacket,
    TextbookRecord,
    TextbookRecordSubtopic,
    TextbookSeedRun,
)
from app.domains.figures.infrastructure.models import Figure
from app.domains.generation_log.models import GenerationEvent
from app.domains.learners.models import LearnerProfile
from app.domains.school.models import (
    AcademicYear,
    Class,
    Course,
    GradeLevel,
    School,
    Subject,
    Term,
    TermClassSubject,
)
from app.domains.teaching.models import (
    LessonDelivery,
    LessonPeriod,
    SchemeOfWork,
    TeacherWorkspace,
)
from app.domains.users.models import User
from app.infra.jobs.models import Job, JobRunner
from app.infra.progress import ProgressEvent

__all__ = [
    "AcademicYear",
    "ArtefactPlan",
    "ContentApproval",
    "ContentDraftRecord",
    "ContentSpecificationRecord",
    "ContentSkillRecord",
    "ContentTypeRecord",
    "Attachment",
    "Base",
    "BuiltArtefact",
    "Class",
    "ClassSession",
    "Course",
    "CurriculumSubtopic",
    "CurriculumTheme",
    "CurriculumTopic",
    "Event",
    "EvaluationPacket",
    "EvaluationAuditItem",
    "EvaluationAuditRating",
    "EvaluationRater",
    "EvaluationRating",
    "StudyComparativeJudgement",
    "StudyCriterionScore",
    "Experiment",
    "ExperimentConditionRun",
    "ExperimentExecution",
    "ExperimentFocalCase",
    "ExitTicketItem",
    "ExitTicketSubmission",
    "GenerationEvent",
    "GradeLevel",
    "Job",
    "JobRunner",
    "ProgressEvent",
    "School",
    "KnowledgeComponent",
    "LearnerProfile",
    "LessonDelivery",
    "LessonPeriod",
    "LessonPlan",
    "PlanVersion",
    "ReferenceMaterial",
    "RevisionThread",
    "RevisionTurn",
    "SchemeOfWork",
    "StudentItemResponse",
    "StudentPackGeneration",
    "StudyClassworkAnswer",
    "StudyClassworkQuestion",
    "StudyClassworkScript",
    "StudyRatingDocument",
    "StudyImport",
    "StudyTranscript",
    "Figure",
    "Subject",
    "User",
    "TeacherWorkspace",
    "Term",
    "TermClassSubject",
    "AoTextbookLinkage",
    "AoTextbookLinkageSeedRun",
    "AoTextbookObjectiveLink",
    "AoTextbookRecordLink",
    "TextbookPacket",
    "TextbookRecord",
    "TextbookRecordSubtopic",
    "TextbookSeedRun",
]

# Alembic will use this.
target_metadata = Base.metadata
