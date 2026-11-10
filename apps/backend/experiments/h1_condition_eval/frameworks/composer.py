"""The half of a framework arm that must not vary.

`compose-v2` is four things: a contract, the inputs that fill it, tools that write a draft,
and one assembly path that turns the draft into a stored section. A framework arm replaces
the fifth — the loop that calls the tools — and inherits the rest from here, so a
difference between arms is a difference between loops.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableConfig

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    normalise_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (  # noqa: E501
    COMPOSITION_MAX_ITERATIONS,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.section_draft import (  # noqa: E501
    SectionDraft,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tracing import record
from experiments.h1_condition_eval.frameworks.brief import composed_brief

SUBMITTED = "submit"
"""The model stopped calling tools, which is a native loop declaring itself finished.
dspy's word for the same event, so a trace reads the same whichever arm wrote it."""

ITERATION_LIMIT = "iteration_limit"
"""The loop was cut off mid-composition. The draft is whatever had been written."""


def superstep_budget(max_iterations: int) -> RunnableConfig:
    """What a langgraph-backed arm may spend.

    langgraph bounds a run by supersteps rather than by turns: a plain model/tools cycle
    spends two per turn, and a graph with middleware around the model spends more. So this
    is the same cap in the same unit for both langgraph arms, and NOT the same number of
    model turns — which is why a cut-off composition is recorded as `iteration_limit`
    rather than left to be inferred from a short section.
    """
    return RunnableConfig(recursion_limit=2 * max_iterations + 1)


class FrameworkComposer(ABC):
    """One section, composed by an agent framework other than dspy.

    Everything but :meth:`compose` is held against `compose-v2`: the contract and its
    inputs are asked from it, the tools write into the same draft, and the section returns
    through ``normalise_section`` so identity, provenance, figures and the reader-ready
    pass are applied identically. A subclass supplies a loop and nothing else.
    """

    framework: str

    def __init__(
        self,
        *,
        contract_mode: ContractMode = "leveled",
        max_iterations: int = COMPOSITION_MAX_ITERATIONS,
    ) -> None:
        self.contract_mode = contract_mode
        self.max_iterations = max_iterations

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        """Compose one section and assemble it the one way every arm assembles it."""
        draft = SectionDraft(unit)
        instructions, inputs = composed_brief(
            request=request, unit=unit, signatures=self.contract_mode
        )
        termination = await self.compose(draft=draft, instructions=instructions, inputs=inputs)
        record(
            {
                "kind": "compose",
                "framework": self.framework,
                "unit_id": unit.unit_id,
                "blocks_written": len(draft.blocks),
                "termination": termination,
            }
        )
        return normalise_section(draft.to_section(), unit)

    @abstractmethod
    async def compose(self, *, draft: SectionDraft, instructions: str, inputs: str) -> str:
        """Drive this framework's loop over the draft's tools, and say why it stopped."""
