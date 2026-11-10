"""Compose one section through draft-editing tools, block by block."""

from __future__ import annotations

from collections.abc import Callable

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
    normalise_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.infra.dspy_agent_loop import run_agent_loop, termination_of, trajectory_of

from .contracts.write_section import (
    ContractMode,
    WriteGroundedSectionFromSources,
    WriteSection,
    signature_for,
)
from .prompt_fingerprint import record_prompt
from .prompt_projection import (
    grounded_lesson_content,
    prompt_evidence,
    prompt_lesson,
    prompt_unit,
)
from .tools.section_draft import SectionDraft, composition_tools
from .tools.source_reading import Toolset
from .tracing import record

COMPOSITION_INSTRUCTIONS = """

Write the section by calling the tools, not by describing it. Set the title, write
the instructional support, then the worked examples, then the practice. Re-read your
draft before you finish and revise anything that falls short: teach every part of
what you were given, and never stop early because the draft already looks long enough.

Each practice question is added with the answer it is checked against. You do not
place the answers — they are collected after the activities for you.
"""
COMPOSITION_MAX_ITERATIONS = 16


def composition_contract(base: type[dspy.Signature]) -> type[dspy.Signature]:
    """Replace a returned section with completion after tool-based composition.

    Named after the contract it wraps: ``with_instructions`` rebuilds the class
    through ``Signature(fields, instructions)``, which takes dspy's default
    ``StringSignature``, and the provenance component is that name — so every
    composed arm would record the same key whatever level it wrapped.
    """
    contract = base.delete("section").append(
        "done",
        dspy.OutputField(desc="True once the whole section is written into the draft."),
        type_=bool,
    )
    composed = dspy.make_signature(
        contract.fields,
        base.instructions + COMPOSITION_INSTRUCTIONS,
        signature_name=f"Compose{base.__name__}",
    )
    if not (isinstance(composed, type) and issubclass(composed, dspy.Signature)):
        raise TypeError(f"dspy.make_signature returned {composed!r}, not a Signature class")
    return composed


class ComposeSection(dspy.Module):
    """Build one section through explicit title, block, and practice tools."""

    def __init__(
        self,
        *,
        lm: dspy.BaseLM,
        contract_mode: ContractMode = "leveled",
        source_tools: Toolset | None = None,
        max_iterations: int = COMPOSITION_MAX_ITERATIONS,
        loop: Callable[..., dspy.Module] = dspy.ReAct,
        pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
    ) -> None:
        super().__init__()
        self.lm = lm
        self.contract_mode = contract_mode
        self.source_tools = source_tools
        self.max_iterations = max_iterations
        self.loop = loop
        self.pipeline = pipeline

    def contract(self, request: ReviewPackRequest) -> type[dspy.Signature]:
        if self.source_tools and request.generation_policy.retrieval.enabled:
            return composition_contract(WriteGroundedSectionFromSources)
        base = (
            signature_for(request.generation_policy)
            if self.contract_mode == "leveled"
            else WriteSection
        )
        return composition_contract(base)

    def inputs(
        self,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        contract: type[dspy.Signature],
    ) -> dict:
        evidence = prompt_evidence(unit.source_evidence)
        available: dict[str, object] = {
            "artefact_spec": request.artefact_spec,
            "policy": request.policy,
            "lesson_context": prompt_lesson(request.lesson_context),
            "unit_context": prompt_unit(unit),
            "source_evidence": evidence,
        }
        if "lesson_content" in contract.input_fields:
            available["lesson_content"] = grounded_lesson_content(unit=unit, signature=contract)
        return {name: available[name] for name in contract.input_fields if name in available}

    async def aforward(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        draft = SectionDraft(unit)
        contract = self.contract(request)
        tools = composition_tools(draft, self.pipeline)
        if self.source_tools:
            tools += self.source_tools(request, unit)
        agent = self.loop(contract, tools=tools, max_iters=self.max_iterations)
        record_prompt(f"composition.{contract.__name__}", contract)
        result = await run_agent_loop(agent, self.lm, self.inputs(request, unit, contract))
        record(
            {
                "kind": "compose",
                "unit_id": unit.unit_id,
                "blocks_written": len(draft.blocks),
                "termination": termination_of(result),
                "trajectory": trajectory_of(result),
            }
        )
        return normalise_section(draft.to_section(), unit)

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        with dspy.settings.context(lm=self.lm):
            section: ReviewPackSection = await self.acall(request=request, unit=unit)
        return section
