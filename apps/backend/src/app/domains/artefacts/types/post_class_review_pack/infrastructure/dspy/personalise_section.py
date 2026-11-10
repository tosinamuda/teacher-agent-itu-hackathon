"""Personalise one approved section for a focal learner."""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    section_from_revision,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)

from .contracts.personalise_section import SectionPersonalisation
from .prepared_call import PreparedCall
from .prompt_fingerprint import record_prompt
from .prompt_projection import personalise_inputs


class PersonaliseSection(dspy.Module):
    """Adapt one approved section to one learner's objective state."""

    def __init__(
        self,
        *,
        lm: dspy.BaseLM,
        contract: type[dspy.Signature] | None = None,
    ) -> None:
        super().__init__()
        self.lm = lm
        self.contract = contract or SectionPersonalisation
        self.personalise = dspy.ChainOfThought(self.contract)

    def prepared_call(
        self,
        *,
        request: PersonalisedReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> PreparedCall:
        """The call this personaliser will make for one section, before making it."""
        return PreparedCall(
            self.contract,
            self.personalise,
            personalise_inputs(
                request=request,
                unit=unit,
                base_section=base_section,
                learner_state=learner_state,
            ),
        )

    async def aforward(
        self,
        *,
        request: PersonalisedReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        prepared = self.prepared_call(
            request=request,
            unit=unit,
            base_section=base_section,
            learner_state=learner_state,
        )
        record_prompt(f"personalisation.{self.contract.__name__}", self.contract)
        result = await self.personalise.acall(**prepared.inputs)
        return section_from_revision(result.personalised_section, unit)

    async def personalise_section(
        self,
        *,
        request: PersonalisedReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection:
        with dspy.settings.context(lm=self.lm):
            personalised: ReviewPackSection = await self.acall(
                request=request,
                unit=unit,
                base_section=base_section,
                learner_state=learner_state,
            )
        return personalised
