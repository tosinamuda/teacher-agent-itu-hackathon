"""The product-owned request for persisting a generated review pack."""

from dataclasses import dataclass, field
from typing import Protocol

from app.domains.artefacts.core.domain.types import ArtefactScope
from app.shared.json_types import JsonObject

from ..domain.generated_review_pack import GeneratedReviewPack


@dataclass(frozen=True)
class ReviewPackMaterialisation:
    """Everything the artefact writer needs, without an experiment record."""

    condition_run_id: str
    plan_version_id: str
    scope: ArtefactScope
    learner_id: str | None
    result: GeneratedReviewPack
    requires_teacher_review: bool
    #: What the pack records of its grounding: the lesson note it read, where it read one.
    artefact_refs: JsonObject = field(default_factory=dict)


class ReviewPackArtefactWriter(Protocol):
    """Stage one generated review pack in its owning database transaction."""

    def stage(self, materialisation: ReviewPackMaterialisation) -> None: ...
