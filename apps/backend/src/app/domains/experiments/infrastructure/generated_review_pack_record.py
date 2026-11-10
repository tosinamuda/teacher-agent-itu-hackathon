"""Serialize a generated pack as the condition run's persisted record.

The record deliberately excludes generation units because they contain the
condition-filtered prompt context. Analysis needs the generated sections,
policy, repair state, prompt provenance, and which sections a personalised pack
actually adapted—not another copy of model inputs.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.shared.json_types import JsonObject


def generated_pack_record(result: GeneratedReviewPack) -> JsonObject:
    """The condition run's research record: the sections plus how they got there.

    Only the request's *policy* is carried, never its units: the units hold the
    condition-filtered lesson-plan context, which must not reappear in a record
    that analysis reads back per condition.
    """
    return {
        "sections": [section.model_dump(mode="json") for section in result.sections],
        "repaired": result.repaired,
        "request_policy": result.request.policy.model_dump(mode="json"),
        "prompt_provenance": result.prompt_provenance.model_dump(mode="json"),
        "personalisation": [record.model_dump(mode="json") for record in result.personalisation],
    }
