"""ReAct personaliser variant — verify a source before citing it.

Same signature fields as production (the harness service calls it
identically); the module is ``dspy.ReAct`` with one tool. The evidence for the
current section is staged into a module-level store right before each call —
ReAct tools are plain functions, so the store is how the tool sees the
request-scoped data.
"""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.personalise_section import (  # noqa: E501
    SectionPersonalisation,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.infra.dspy_lm import build_dspy_lm

# v2 ordering (2026-06-11): v1 led with source verification and the model's
# reasoning budget followed — it generalised away from the learner's actual
# distractors and slipped on arithmetic. Targeting comes FIRST now, with
# explicit anti-substitution and arithmetic-check rules; verification second.
_REACT_RULES = (
    "\n\nWork in this order. FIRST: from learner_state.evidence_items, note the "
    "EXACT option the learner chose on each missed question and plan how the "
    "section will defuse those specific choices — never substitute an invented "
    "example for the learner's actual mistake, and re-check every piece of "
    "arithmetic you write before including it. SECOND: you have a read_source "
    "tool — before citing any source_ref, call read_source with that ref and "
    "confirm the excerpt actually supports the text you attach it to; never "
    "attribute content, problems or solutions to the textbook unless "
    "read_source returned them, and do not cite a ref read_source reports as "
    "unknown. THEN write the personalised section following every rule above."
)

# Evidence for the section currently being personalised (set per call).
_CURRENT_EVIDENCE: dict[str, str] = {}


def read_source(source_ref: str) -> str:
    """Return the full textbook excerpt for a source_ref (e.g. "REF-1")."""
    text = _CURRENT_EVIDENCE.get(source_ref.strip())
    if text:
        return text
    return f"UNKNOWN REF {source_ref!r} — this source does not exist; do not cite it."


class ReActPersonaliser(PersonaliseSection):
    """Production personaliser with the module swapped for ReAct + read_source."""

    def __init__(self, *, lm: dspy.BaseLM) -> None:
        contract = SectionPersonalisation.with_instructions(
            str(SectionPersonalisation.instructions) + _REACT_RULES
        )
        super().__init__(lm=lm, contract=contract)
        self.personalise = dspy.ReAct(
            self.contract,
            tools=[read_source],
            max_iters=5,
        )

    async def personalise_section(
        self,
        *,
        request: PersonalisedReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        _CURRENT_EVIDENCE.clear()
        _CURRENT_EVIDENCE.update({item.source_ref: item.excerpt for item in unit.source_evidence})
        return await super().personalise_section(
            request=request,
            unit=unit,
            base_section=base_section,
            learner_state=learner_state,
        )


def build_react_personaliser() -> ReActPersonaliser:
    """Factory the eval harness resolves via --variant."""
    return ReActPersonaliser(lm=build_dspy_lm())
