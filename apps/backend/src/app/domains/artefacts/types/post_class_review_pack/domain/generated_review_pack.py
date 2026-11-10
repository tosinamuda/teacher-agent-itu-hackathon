"""Generated study pack plus its reproducibility and validation record."""

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.prompt_provenance import (
    PromptProvenance,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.personalisation import (
    SectionPersonalisation,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)


class GeneratedReviewPack(BaseModel):
    """The reproducible output produced for one experiment condition."""

    model_config = ConfigDict(extra="forbid")

    request: ReviewPackRequest
    sections: list[ReviewPackSection]
    validation: ValidationResult | None = None
    validation_before_repair: ValidationResult | None = None
    validation_rounds: list[ValidationResult] = Field(default_factory=list)
    repaired: bool = False
    #: The sections the repair rounds rewrote from scratch, by section id, so what a reviser
    #: or a teacher asked of them may not be in the result.
    regenerated: list[str] = Field(default_factory=list)
    prompt_provenance: PromptProvenance = Field(default_factory=PromptProvenance)
    personalisation: list[SectionPersonalisation] = Field(default_factory=list)
