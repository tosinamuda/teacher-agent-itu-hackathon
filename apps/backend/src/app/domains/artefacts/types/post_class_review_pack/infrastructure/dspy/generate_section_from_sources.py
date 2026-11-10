"""Generate one section after reading its permitted sources through tools."""

from __future__ import annotations

from collections.abc import Callable

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
from app.infra.dspy_agent_loop import run_agent_loop, trajectory_of

from .contracts.write_section import WriteSectionFromSources
from .prompt_fingerprint import record_prompt
from .prompt_projection import prompt_lesson, prompt_unit
from .tools.source_reading import Toolset
from .tracing import record


class GenerateSectionFromSources(dspy.Module):
    """Read permitted evidence with tools, then generate one grounded section."""

    def __init__(
        self,
        *,
        lm: dspy.BaseLM,
        tools: Toolset,
        loop: Callable[..., dspy.Module] = dspy.ReAct,
        label: str = "source-reading",
    ) -> None:
        super().__init__()
        self.lm = lm
        self.tools = tools
        self.loop = loop
        self.label = label

    async def aforward(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        agent = self.loop(
            WriteSectionFromSources,
            tools=self.tools(request, unit),
            max_iters=request.generation_policy.execution.agent_max_iterations,
        )
        record_prompt("source_reading", WriteSectionFromSources)
        result = await run_agent_loop(
            agent,
            self.lm,
            {
                "artefact_spec": request.artefact_spec,
                "policy": request.policy,
                "lesson_context": prompt_lesson(request.lesson_context),
                "unit_context": prompt_unit(unit),
            },
        )
        record(
            {
                "kind": "generate",
                "engine": self.label,
                "unit_id": unit.unit_id,
                "trajectory": trajectory_of(result),
            }
        )
        return section_from_draft(result.section, unit)

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        with dspy.settings.context(lm=self.lm):
            section: ReviewPackSection = await self.acall(request=request, unit=unit)
        return section
