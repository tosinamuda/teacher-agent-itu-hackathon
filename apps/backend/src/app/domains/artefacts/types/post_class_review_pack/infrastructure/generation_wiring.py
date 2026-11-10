"""Compose review-pack generation from model-backed collaborators.

This is the only product module naming both live DSPy modules and the application
operations that use them. Tests may pass stand-ins through ``collaborators``.
"""

from dataclasses import dataclass

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.personalise import (
    PersonaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionCritic,
    SectionGenerator,
    SectionPersonaliser,
    SectionRepairer,
    SectionReviser,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (  # noqa: E501
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CritiqueSections,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.repair_section import (
    RepairGeneratedSection,
)
from app.infra.dspy_lm import build_dspy_lm


@dataclass(frozen=True)
class SectionCollaborators:
    """Every model-backed seam a review pack is written through."""

    generator: SectionGenerator
    repairer: SectionRepairer
    personaliser: SectionPersonaliser
    critic: SectionCritic
    reviser: SectionReviser | None = None


def live_section_collaborators(
    pipeline: ReviewPackPipeline = CURRENT_PIPELINE,
) -> SectionCollaborators:
    """The live DSPy modules of one pipeline version, over the configured language model."""
    return section_collaborators(build_dspy_lm(), pipeline)


def section_collaborators(
    lm: dspy.BaseLM, pipeline: ReviewPackPipeline = CURRENT_PIPELINE
) -> SectionCollaborators:
    """The DSPy modules production runs, over one given language model.

    The served-prompt snapshots build through here with a recording model, so they
    capture the call production would make rather than a reconstruction of it.
    """
    return SectionCollaborators(
        # ComposeSection over ReActV2, matching the harness the H1 evaluation judged:
        # 72 packs, 144 judgments and all four rendering fixes were verified on it, and
        # nothing in the bake-off separates it from GenerateSection on quality. Deploying
        # the other one would leave the whole evidence base describing a system that does
        # not ship. See experiments/h1_condition_eval/HARNESS-DECISION.md.
        generator=ComposeSection(
            lm=lm, contract_mode="leveled", loop=dspy.ReActV2, pipeline=pipeline
        ),
        repairer=RepairGeneratedSection(lm=lm, pipeline=pipeline),
        personaliser=PersonaliseSection(lm=lm),
        critic=CritiqueSections(lm=lm, pipeline=pipeline),
    )


def build_base_review_pack_generator(
    collaborators: SectionCollaborators | None = None,
    *,
    validator: ReviewPackStructuralValidator | None = None,
) -> GenerateBaseReviewPack:
    """Build the live base review-pack generator."""
    collaborators = collaborators or live_section_collaborators()
    return GenerateBaseReviewPack(
        request_builder=class_note_requests(),
        generator=collaborators.generator,
        finalise=_finalise(collaborators, validator),
    )


def class_note_requests() -> BaseReviewPackRequestBuilder:
    """How a class revision note's request is built when the pipeline writes or checks it."""
    # The teacher's drawings travel as their source, as they did for the rated notes.
    return BaseReviewPackRequestBuilder(figures="source")


def live_finalise(pipeline: ReviewPackPipeline) -> FinaliseReviewPack:
    """The checks and bounded repair of one pipeline version, over the configured model."""
    return _finalise(live_section_collaborators(pipeline), None)


def build_review_pack_personaliser(
    collaborators: SectionCollaborators | None = None,
    *,
    validator: ReviewPackStructuralValidator | None = None,
) -> PersonaliseReviewPack:
    """Build the live review-pack personaliser."""
    collaborators = collaborators or live_section_collaborators()
    return PersonaliseReviewPack(
        personaliser=collaborators.personaliser,
        finalise=_finalise(collaborators, validator),
    )


def _finalise(
    collaborators: SectionCollaborators,
    validator: ReviewPackStructuralValidator | None,
) -> FinaliseReviewPack:
    """Build validation and revision shared by base and personalised packs."""
    return FinaliseReviewPack(
        generator=collaborators.generator,
        repairer=collaborators.repairer,
        critic=collaborators.critic,
        validator=validator,
        reviser=collaborators.reviser,
    )
