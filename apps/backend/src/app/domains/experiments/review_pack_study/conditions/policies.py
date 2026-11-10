"""Experiment labels combined with product-owned review-pack generation policy."""

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ContextPolicy,
    GenerationExecutionPolicy,
    PersonalisationPolicy,
    RetrievalPolicy,
    ReviewPackGenerationPolicy,
    ValidationPolicy,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis


class TeacherValidationPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    allowed_actions: tuple[str, ...] = ("approve", "reject", "request_regeneration")
    allow_manual_edits: bool = False
    require_decision_reason: bool = True


class ConditionProfile(BaseModel):
    """A study treatment plus the product policy it exercises."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    hypothesis: Hypothesis
    condition_code: ConditionCode
    description: str
    context: ContextPolicy
    retrieval: RetrievalPolicy = Field(default_factory=RetrievalPolicy)
    validation: ValidationPolicy = Field(default_factory=ValidationPolicy)
    teacher_validation: TeacherValidationPolicy = Field(default_factory=TeacherValidationPolicy)
    personalisation: PersonalisationPolicy = Field(default_factory=PersonalisationPolicy)
    execution: GenerationExecutionPolicy = Field(default_factory=GenerationExecutionPolicy)
    generated_by: ConditionCode

    def generation_policy(self) -> ReviewPackGenerationPolicy:
        return ReviewPackGenerationPolicy(
            context=self.context,
            retrieval=self.retrieval,
            validation=self.validation,
            personalisation=self.personalisation,
            execution=self.execution,
        )


__all__ = [
    "ConditionProfile",
    "ContextPolicy",
    "PersonalisationPolicy",
    "RetrievalPolicy",
    "TeacherValidationPolicy",
    "ValidationPolicy",
]
