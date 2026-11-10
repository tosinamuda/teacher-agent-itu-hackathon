from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.types import (
    NormalizedLessonDraft,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonGenerationSession,
    PreparedGenerationInputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    collect_grounded_image_assets,
    normalize_session_plan_payload,
    normalize_step_content,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import (
    derive_textbook_references,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.artifacts import (
    GenerationArtifacts,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.textbook_support import (
    select_textbook_records,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    SessionPlan,
    SessionPlanContent,
)
from app.shared.json_types import JsonObject

DRAFT_PLAN_ID = "LP-DRAFT"


class DraftStepNormalizer:
    def normalize(
        self,
        *,
        artifacts: GenerationArtifacts,
        textbook_records: list[JsonObject],
    ) -> NormalizedLessonDraft:
        normalized_core_steps: list[JsonObject] = []
        for core_step in artifacts.core_steps:
            lesson_objective_id = core_step.lesson_objective_id
            if not lesson_objective_id:
                raise ValueError("core step is missing lesson_objective_id")
            evidence_plan = artifacts.step_evidence_plans.get(lesson_objective_id)
            if evidence_plan is None:
                raise ValueError(
                    f"missing step evidence plan for lesson objective: {lesson_objective_id}"
                )
            evidence_bundle = select_textbook_records(
                evidence_plan.selected_record_ids,
                textbook_records,
            )
            normalized_core_steps.append(
                normalize_step_content(
                    core_step.model_dump(),
                    grounded_images=collect_grounded_image_assets(evidence_bundle),
                )
            )

        global_step_payload = artifacts.global_steps.model_dump()
        normalized_global_steps = {
            key: normalize_step_content(value, grounded_images=[])
            for key, value in global_step_payload.items()
            if isinstance(value, dict)
        }
        return NormalizedLessonDraft(
            core_steps=normalized_core_steps,
            global_steps=normalized_global_steps,
        )


class SessionPlanAssembler:
    def __init__(self) -> None:
        self._draft_normalizer = DraftStepNormalizer()

    def normalize_draft(
        self,
        *,
        artifacts: GenerationArtifacts,
        inputs: PreparedGenerationInputs,
    ) -> NormalizedLessonDraft:
        return self._draft_normalizer.normalize(
            artifacts=artifacts,
            textbook_records=inputs.textbook_record_payloads(),
        )

    def build_content(
        self,
        *,
        session: LessonGenerationSession,
        inputs: PreparedGenerationInputs,
        artifacts: GenerationArtifacts,
        draft: NormalizedLessonDraft,
    ) -> SessionPlanContent:
        content = {
            "curriculum_objectives": inputs.curriculum_objective_payloads(),
            "lesson_plan_objectives": artifacts.lesson_plan_objectives,
            "misconceptions": artifacts.kc_plan.misconceptions,
            "steps": [
                draft.global_steps["intro_step"],
                *draft.core_steps,
                draft.global_steps["evaluation_step"],
            ],
            "assessments": [
                {
                    "question": item.question,
                    "answer": item.expected_answer,
                    "rubric": item.bloom_justification,
                }
                for item in artifacts.assessment_items
            ],
            "theme": artifacts.kc_plan.theme or session.theme,
            "entry_behaviour": (
                artifacts.kc_plan.entry_behaviour or inputs.curriculum.entry_behaviour
            ),
            "instructional_materials": (
                artifacts.kc_plan.instructional_materials
                or inputs.curriculum.instructional_materials
            ),
            "references": derive_textbook_references(
                artifacts.evidence_summaries,
                inputs.textbook_record_payloads(),
            ),
        }
        return SessionPlanContent.model_validate(content)

    def assemble(
        self,
        *,
        session: LessonGenerationSession,
        session_plan_content: SessionPlanContent,
    ) -> JsonObject:
        normalized_content = SessionPlanContent.model_validate(
            normalize_session_plan_payload(session_plan_content.model_dump())
        )
        return SessionPlan(
            plan_id=DRAFT_PLAN_ID,
            session_id=session.session_id,
            subject=session.subject,
            track=session.track,
            grade=session.grade,
            term=session.term,
            week=session.week,
            topic=session.topic,
            subtopic=session.subtopic,
            curriculum_objectives=normalized_content.curriculum_objectives,
            lesson_plan_objectives=normalized_content.lesson_plan_objectives,
            misconceptions=normalized_content.misconceptions,
            steps=normalized_content.steps,
            assessments=normalized_content.assessments,
            theme=normalized_content.theme,
            entry_behaviour=normalized_content.entry_behaviour,
            instructional_materials=normalized_content.instructional_materials,
            references=normalized_content.references,
        ).model_dump()
