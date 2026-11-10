"""Orchestrate one base review pack."""

import asyncio

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.application.prompt_provenance import (  # noqa: E501
    capture_prompt_provenance,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionGenerator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.shared.session_plan_view import SessionPlanView


class GenerateBaseReviewPack:
    """Build, generate, and finalise one base review pack."""

    def __init__(
        self,
        *,
        generator: SectionGenerator,
        finalise: FinaliseReviewPack,
        request_builder: BaseReviewPackRequestBuilder | None = None,
    ) -> None:
        self._generator = generator
        self._finalise = finalise
        self._request_builder = request_builder or BaseReviewPackRequestBuilder()

    async def generate(
        self,
        *,
        session_plan: SessionPlanView,
        policy: ReviewPackGenerationPolicy,
        sources: LessonSources,
        specification: ContentSpecification | None = None,
    ) -> GeneratedReviewPack:
        """Generate every section and run the condition's revision policy."""
        request: BaseReviewPackRequest = self._request_builder.build(
            session_plan=session_plan,
            policy=policy,
            sources=sources,
            specification=specification,
        )
        with capture_prompt_provenance() as prompt_trace:
            sections = list(
                await asyncio.gather(
                    *(
                        self._generator.generate_section(request=request, unit=unit)
                        for unit in request.units
                    )
                )
            )
            result = await self._finalise.finalise(
                policy=policy,
                request=request,
                sections=sections,
            )
        return result.model_copy(update={"prompt_provenance": prompt_trace.snapshot()})
