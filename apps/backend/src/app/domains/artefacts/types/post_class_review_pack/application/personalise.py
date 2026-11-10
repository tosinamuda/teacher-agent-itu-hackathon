"""Personalise one approved study pack for a focal learner."""

import logging
from collections.abc import Mapping
from dataclasses import dataclass

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.application.prompt_provenance import (  # noqa: E501
    capture_prompt_provenance,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
    SessionSignals,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.section_generation import (
    SectionPersonaliser,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    scope_unit_evidence,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.personalisation import (
    PersonalisationOutcome,
    SectionPersonalisation,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.unit_index import (
    SectionUnitIndex,
)
from app.shared.session_plan_view import SessionPlanView

logger = logging.getLogger(__name__)

SectionOutcome = tuple[ReviewPackSection, PersonalisationOutcome]


@dataclass(frozen=True)
class PersonalisedSections:
    """The sections a learner's pack is assembled from, and how each one got there."""

    sections: list[ReviewPackSection]
    outcomes: list[SectionPersonalisation]

    @classmethod
    def of(cls, resolved: list[SectionOutcome]) -> "PersonalisedSections":
        """Split each section from the record of how personalisation left it."""
        return cls(
            sections=[section for section, _ in resolved],
            outcomes=[
                SectionPersonalisation(
                    section_id=section.section_id,
                    lesson_objective_id=section.lesson_objective_id,
                    outcome=outcome,
                )
                for section, outcome in resolved
            ],
        )


def _unit_for_section(section: ReviewPackSection) -> SectionGenerationUnit:
    return SectionGenerationUnit(
        unit_id=section.section_id,
        lesson_objective_id=section.lesson_objective_id,
        objective_text=section.title,
    )


def _too_thin(
    policy: ReviewPackGenerationPolicy, marked_questions: Mapping[str, int] | None
) -> frozenset[str]:
    """The objectives with fewer marked questions than the policy needs to adapt a section."""
    least = policy.personalisation.min_marked_questions
    if marked_questions is None or least == 0:
        return frozenset()
    return frozenset(objective for objective, marked in marked_questions.items() if marked < least)


def _wrote_something(section: ReviewPackSection) -> bool:
    return any(block.block_type != "visual" for block in section.blocks)


def _resolve_section(
    base_section: ReviewPackSection,
    personalised: ReviewPackSection,
    focal_learner_id: str,
) -> SectionOutcome:
    """Take the personalised section, or the base one it failed to improve on."""
    if _wrote_something(personalised):
        return personalised, PersonalisationOutcome.PERSONALISED
    logger.warning(
        "Personalisation kept the base section: no learner-facing block was written "
        "(learner=%s section=%s)",
        focal_learner_id,
        base_section.section_id,
    )
    return base_section, PersonalisationOutcome.EMPTY_RESULT


def build_personalised_review_pack_request(
    *,
    session_plan: SessionPlanView,
    learner_states: dict[str, ObjectiveLearnerState],
    base_pack_id: str,
    focal_learner_id: str,
    policy: ReviewPackGenerationPolicy,
    session_signals: SessionSignals | None,
    sources: LessonSources,
    specification: ContentSpecification | None = None,
) -> PersonalisedReviewPackRequest:
    """Build the immutable request recorded for a reused base pack."""
    return PersonalisedReviewPackRequestBuilder().build(
        session_plan=session_plan,
        base_pack_id=base_pack_id,
        focal_learner_id=focal_learner_id,
        learner_states=learner_states,
        policy=policy,
        session_signals=session_signals,
        sources=sources,
        specification=specification,
    )


class PersonaliseReviewPack:
    """Adapt approved base sections to one learner without changing objectives."""

    def __init__(
        self,
        *,
        personaliser: SectionPersonaliser,
        finalise: FinaliseReviewPack,
        request_builder: PersonalisedReviewPackRequestBuilder | None = None,
    ) -> None:
        self._personaliser = personaliser
        self._finalise = finalise
        self._request_builder = request_builder or PersonalisedReviewPackRequestBuilder()

    def build_request(
        self,
        *,
        session_plan: SessionPlanView,
        learner_states: dict[str, ObjectiveLearnerState],
        base_pack_id: str,
        focal_learner_id: str,
        policy: ReviewPackGenerationPolicy,
        session_signals: SessionSignals | None = None,
        sources: LessonSources,
        specification: ContentSpecification | None = None,
    ) -> PersonalisedReviewPackRequest:
        """Build the reproducible request recorded for personalisation."""
        return self._request_builder.build(
            session_plan=session_plan,
            base_pack_id=base_pack_id,
            focal_learner_id=focal_learner_id,
            learner_states=learner_states,
            policy=policy,
            session_signals=session_signals,
            sources=sources,
            specification=specification,
        )

    async def personalise(
        self,
        *,
        session_plan: SessionPlanView,
        base_sections: list[ReviewPackSection],
        learner_states: dict[str, ObjectiveLearnerState],
        base_pack_id: str,
        focal_learner_id: str,
        policy: ReviewPackGenerationPolicy,
        session_signals: SessionSignals | None = None,
        sources: LessonSources,
        specification: ContentSpecification | None = None,
        marked_questions: Mapping[str, int] | None = None,
    ) -> GeneratedReviewPack:
        """Personalise applicable sections and run the condition's revision policy.

        ``marked_questions`` counts each objective's marked questions. Where the policy asks for
        a minimum and an objective has fewer, its base section stays.
        """
        request = self.build_request(
            session_plan=session_plan,
            base_pack_id=base_pack_id,
            focal_learner_id=focal_learner_id,
            learner_states=learner_states,
            policy=policy,
            session_signals=session_signals,
            sources=sources,
            specification=specification,
        )
        with capture_prompt_provenance() as prompt_trace:
            assembled = await self._personalised_sections(
                request=request,
                base_sections=base_sections,
                learner_states=learner_states,
                focal_learner_id=focal_learner_id,
                too_thin=_too_thin(policy, marked_questions),
            )
            result = await self._finalise.finalise(
                policy=policy,
                request=request,
                sections=assembled.sections,
                base_sections=base_sections,
            )
        return result.model_copy(
            update={
                "prompt_provenance": prompt_trace.snapshot(),
                "personalisation": assembled.outcomes,
            }
        )

    async def _personalised_sections(
        self,
        *,
        request: PersonalisedReviewPackRequest,
        base_sections: list[ReviewPackSection],
        learner_states: dict[str, ObjectiveLearnerState],
        focal_learner_id: str,
        too_thin: frozenset[str],
    ) -> PersonalisedSections:
        """Adapt every section the learner has enough state for, recording what became of each."""
        units = SectionUnitIndex.of(request.units)
        resolved: list[SectionOutcome] = []
        for base_section in base_sections:
            state = learner_states.get(base_section.lesson_objective_id)
            if state is None:
                resolved.append((base_section, PersonalisationOutcome.NO_LEARNER_STATE))
                continue
            if base_section.lesson_objective_id in too_thin:
                resolved.append((base_section, PersonalisationOutcome.THIN_EVIDENCE))
                continue
            unit = scope_unit_evidence(
                units.resolve(base_section) or _unit_for_section(base_section),
                base_section,
            )
            personalised = await self._personaliser.personalise_section(
                request=request,
                unit=unit,
                base_section=base_section,
                learner_state=state,
            )
            resolved.append(_resolve_section(base_section, personalised, focal_learner_id))
        return PersonalisedSections.of(resolved)
