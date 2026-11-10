"""Repair one generated section under explicit validation findings."""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    section_from_revision,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
    RevisedSection,
)

from .contracts.repair_section import repair_contract
from .prompt_fingerprint import record_prompt
from .prompt_projection import repair_inputs


class RepairGeneratedSection(dspy.Module):
    """Repair one failed section while preserving its generation unit."""

    def __init__(self, *, lm: dspy.BaseLM, pipeline: ReviewPackPipeline = CURRENT_PIPELINE) -> None:
        super().__init__()
        self.lm = lm
        self.contract = repair_contract(pipeline)
        self.repair = dspy.ChainOfThought(self.contract)

    async def aforward(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        failed_section: ReviewPackSection,
        issues: list[str],
    ) -> ReviewPackSection:
        record_prompt("section_repair", self.contract)
        result = await self.repair.acall(
            **repair_inputs(
                request=request,
                unit=unit,
                failed_section=failed_section,
                issues=issues,
            )
        )
        revised = RevisedSection.model_validate(result.repaired_section.model_dump())
        return section_from_revision(revised, unit)

    async def repair_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        failed_section: ReviewPackSection,
        issues: list[str],
    ) -> ReviewPackSection:
        with dspy.settings.context(lm=self.lm):
            repaired: ReviewPackSection = await self.acall(
                request=request,
                unit=unit,
                failed_section=failed_section,
                issues=issues,
            )
        return repaired
