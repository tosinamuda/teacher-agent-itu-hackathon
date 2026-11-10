"""A learner's revision note written by the content engine, and stored as the pipeline's is.

The engine adapts the lesson's approved class note to one learner's marked work. It writes a part
for each objective the learner has enough evidence to adapt; every other section stays as the
class note has it. The note is checked as a learner's note is, stored pending the teacher's review,
and records the class note version it was made from.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.made_from import MADE_FROM, made_from
from app.domains.artefacts.core.domain.specification import specification_ref
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import get_plan_row
from app.domains.artefacts.types.post_class_review_pack.application.adaptation_parameters import (
    AdaptationParameters,
    resolve_parameters,
)
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    StudentPackGenerationError,
)
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    written_grounding,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_inputs import (
    LearnerInputs,
    learner_inputs,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_part_pins import (
    pinned,
)
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.application.pack_inputs import (
    PackInputs,
    base_pack_id,
    materialise_pack,
)
from app.domains.artefacts.types.post_class_review_pack.application.personalise import (
    build_personalised_review_pack_request,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.review_record import (
    review_record,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    PERSONALISED_REVIEW_PACK_POLICY,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    assemble_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.engine_draft import (
    learner_blocks_from_part,
    learner_practice_from_part,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.evidence import (
    scope_unit_evidence,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.personalisation import (
    PersonalisationOutcome,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.unit_index import (
    SectionUnitIndex,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_approved_class_pack,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.learner_state.application.service import LearnerStateService
from app.shared.json_types import JsonObject, JsonValue

#: What a draft written for a learner passed before it was saved: the destination refuses it
#: otherwise, so a stored note has passed each.
_HELD_TO = ("explanation_present", "adaptation_limits", "misconception_repair")


class EngineLearnerPackError(Exception):
    """The learner's note cannot be written or stored yet, and why."""


@dataclass(frozen=True)
class LearnerWork:
    """What a learner's note is made from: the approved class note and the learner's own work."""

    class_pack: Artefact
    base_sections: list[ReviewPackSection]
    learner: LearnerInputs

    def adapts(self, objective_id: str) -> bool:
        """Whether the learner has state for the objective and enough marked questions to adapt."""
        least = PERSONALISED_REVIEW_PACK_POLICY.personalisation.min_marked_questions
        return (
            objective_id in self.learner.states
            and self.learner.marked_questions.get(objective_id, 0) >= least
        )

    def adapted_objectives(self) -> list[str]:
        """The objectives to write a part for, in the class note's order."""
        return [
            s.lesson_objective_id for s in self.base_sections if self.adapts(s.lesson_objective_id)
        ]


def _unit_of(section: ReviewPackSection) -> SectionGenerationUnit:
    return SectionGenerationUnit(
        unit_id=section.section_id,
        lesson_objective_id=section.lesson_objective_id,
        objective_text=section.title,
    )


class EngineLearnerPack:
    def __init__(
        self, inputs: PackInputs, learner_state: LearnerStateService | None = None
    ) -> None:
        self._inputs = inputs
        self._learner_state = learner_state or LearnerStateService()

    async def work(self, db: AsyncSession, plan_version_id: str, student_id: str) -> LearnerWork:
        """The approved class note and the learner's state; refused when either is missing."""
        class_pack = await the_lessons_approved_class_pack(db, plan_version_id)
        if class_pack is None:
            raise EngineLearnerPackError("the lesson's class revision note is not approved yet")
        try:
            learner = await learner_inputs(
                db, self._learner_state, student_id=student_id, plan_version_id=plan_version_id
            )
        except StudentPackGenerationError as error:
            raise EngineLearnerPackError(str(error)) from error
        sections = review_pack_manifest_to_sections(
            PostClassReviewPack.model_validate(class_pack.manifest)
        )
        return LearnerWork(class_pack, sections, learner)

    async def store(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        student_id: str,
        written: Mapping[str, JsonObject],
        generator: JsonObject,
    ) -> str:
        """The id of the learner's pack, made from the sections the engine wrote for them.

        A section with no part stays as the class note has it. The sections are checked as the
        pipeline's learner notes are, and a pack that fails them is refused with the reasons.
        """
        work = await self.work(db, plan_version_id, student_id)
        row = await get_plan_row(db, plan_or_version_id=plan_version_id)
        if row is None:
            raise EngineLearnerPackError("plan_version_not_found")
        grounding = await written_grounding(
            self._inputs.lesson_notes, db, work.class_pack.artefact_refs, plan_version_id
        )
        session_plan, sources = await self._inputs.lesson_inputs(db, row[0], grounding)
        specification = await self._inputs.specification(db)
        request = build_personalised_review_pack_request(
            session_plan=session_plan,
            learner_states=work.learner.states,
            base_pack_id=base_pack_id(plan_version_id),
            focal_learner_id=student_id,
            policy=PERSONALISED_REVIEW_PACK_POLICY,
            session_signals=work.learner.signals,
            sources=sources,
            specification=specification,
        )
        sections, outcomes = self._sections(work, request, written)
        checked = ReviewPackStructuralValidator().validate(
            policy=PERSONALISED_REVIEW_PACK_POLICY,
            sections=sections,
            request=request,
            base_sections=work.base_sections,
        )
        if not checked.passed:
            raise EngineLearnerPackError(
                "; ".join(c.message or c.check for c in checked.checks if not c.passed)
            )
        artefact = materialise_pack(
            db=db,
            sections=sections,
            lesson_context=request.lesson_context,
            plan_version_id=plan_version_id,
            scope=ArtefactScope.LEARNER_LEVEL,
            student_id=student_id,
            review_status=ArtefactReviewStatus.PENDING,
            artefact_refs={
                **specification_ref(specification),
                **grounding.refs(),
                "review": review_record(checked, request, held_to=_HELD_TO if written else ()),
                MADE_FROM: made_from(work.class_pack.artefact_id, work.class_pack.version),
                "personalisation": list[JsonValue](outcomes),
                "origin": "generated",
                "generator": generator,
            },
            personalisation_bands=work.learner.bands,
        )
        await db.commit()
        return str(artefact.artefact_id)

    def _sections(
        self,
        work: LearnerWork,
        request: PersonalisedReviewPackRequest,
        written: Mapping[str, JsonObject],
    ) -> tuple[list[ReviewPackSection], list[JsonValue]]:
        units = SectionUnitIndex.of(request.units)
        sections: list[ReviewPackSection] = []
        outcomes: list[JsonValue] = []
        for base in work.base_sections:
            part = written.get(base.lesson_objective_id)
            if part is None:
                sections.append(base)
                outcomes.append(self._kept(work, base))
                continue
            unit = scope_unit_evidence(units.resolve(base) or _unit_of(base), base)
            state = work.learner.states[base.lesson_objective_id]
            sections.append(
                assemble_section(
                    title=base.title,
                    blocks=learner_blocks_from_part(pinned(part, base, state)),
                    practice=learner_practice_from_part(part),
                    unit=unit,
                )
            )
            outcomes.append(
                _outcome(
                    base,
                    PersonalisationOutcome.PERSONALISED,
                    resolve_parameters(state),
                )
            )
        return sections, outcomes

    @staticmethod
    def _kept(work: LearnerWork, base: ReviewPackSection) -> JsonObject:
        known = base.lesson_objective_id in work.learner.states
        kept = (
            PersonalisationOutcome.THIN_EVIDENCE
            if known
            else PersonalisationOutcome.NO_LEARNER_STATE
        )
        return _outcome(base, kept)


def _outcome(
    section: ReviewPackSection,
    outcome: PersonalisationOutcome,
    parameters: AdaptationParameters | None = None,
) -> JsonObject:
    """One section's fate, with the settings it was adapted to when it was adapted."""
    recorded: JsonObject = {
        "section_id": section.section_id,
        "lesson_objective_id": section.lesson_objective_id,
        "outcome": outcome.value,
    }
    if parameters is not None:
        recorded["parameters"] = parameters.model_dump(mode="json")
    return recorded
