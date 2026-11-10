"""Generate one base review-pack section."""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    section_from_draft,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)

from .contracts.write_section import ContractMode, WriteSection, signature_for
from .prepared_call import PreparedCall
from .prompt_fingerprint import record_prompt
from .prompt_projection import leveled_inputs, shared_inputs


class GenerateSection(dspy.Module):
    """Model-backed base review-pack section generator.

    The LM is given, not acquired: which provider serves a run is a deployment
    fact, and building one here made ``acall`` — the line that decides what
    actually goes on the wire — impossible to reach without a provider.
    """

    def __init__(
        self,
        *,
        lm: dspy.BaseLM,
        contract_mode: ContractMode = "shared",
    ) -> None:
        super().__init__()
        self.lm = lm
        self.contract_mode = contract_mode
        self.generate_predictor = dspy.ChainOfThought(WriteSection)
        self._leveled: dict[type, dspy.Module] = {}

    def prepared_call(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> PreparedCall:
        """The call this generator will make for one unit, before making it.

        Rendering a prompt and sending one read this, so a snapshot cannot describe a
        call the generator would not make.
        """
        if self.contract_mode == "leveled":
            return self._leveled_call(request=request, unit=unit)
        return PreparedCall(
            WriteSection, self.generate_predictor, shared_inputs(request=request, unit=unit)
        )

    async def aforward(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        prepared = self.prepared_call(request=request, unit=unit)
        record_prompt(self._component(prepared.contract), prepared.contract)
        result = await prepared.predictor.acall(**prepared.inputs)
        return section_from_draft(result.section, unit)

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        """Run this DSPy program for one policy-filtered generation unit."""
        with dspy.settings.context(lm=self.lm):
            section: ReviewPackSection = await self.acall(request=request, unit=unit)
        return section

    def _leveled_call(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> PreparedCall:
        """Per-level signature: only the fields this level uses, its task stated once."""
        signature = signature_for(request.generation_policy)
        module = self._leveled.get(signature)
        if module is None:
            module = dspy.ChainOfThought(signature)
            self._leveled[signature] = module
        return PreparedCall(
            signature, module, leveled_inputs(request=request, unit=unit, signature=signature)
        )

    def _component(self, contract: type[dspy.Signature]) -> str:
        """The provenance name this generator records its prompt under."""
        if self.contract_mode == "leveled":
            return f"base_generation.{contract.__name__}"
        return "base_generation"
