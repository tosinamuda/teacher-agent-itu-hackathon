import dspy

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import PlannerPlanStep


class GenerateCoreStepSignature(dspy.Signature):
    """Write one teacher-facing core step from already-selected textbook evidence.

    Figures: the source's image figures are attached automatically after your text, each with
    its own caption. Do NOT reproduce or invent what a figure shows (e.g. do not state the
    numbers or steps in a chart you cannot see) — refer to it generally ("the chart below")
    and let its caption carry the specifics. Reproduce source *tables* as LaTeX as usual.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(
        desc="The lesson-plan specification: what the plan is, who it is for, and the "
        "requirements it must meet. Follow every requirement exactly."
    )
    scope_context = dspy.InputField(
        desc="Lesson scope object with subject, grade, term, week, topic, subtopic, and duration."
    )
    curriculum_context = dspy.InputField(
        desc=(
            "Curriculum and scheme context object with curriculum objectives, "
            "activities, materials, and prior knowledge."
        )
    )
    lesson_objective = dspy.InputField(
        desc="One lesson-plan objective linked to one curriculum objective and KC type."
    )
    knowledge_component = dspy.InputField(
        desc=(
            "The resolved knowledge item for this step, including knowledge_focus, optional "
            "source_form/target_form, and supporting_record_ids."
        )
    )
    step_blueprint = dspy.InputField(
        desc="One core-step blueprint linked to the lesson-plan objective and required block types."
    )
    step_evidence_plan = dspy.InputField(
        desc="The selected supporting record ids and grouped evidence roles for this step."
    )
    evidence_bundle = dspy.InputField(
        desc=(
            "The selected textbook records for this step, under key `evidence`, "
            "as the only allowed grounding source."
        )
    )
    target_assessment = dspy.InputField(
        desc="The pre-designed assessment item this step must prepare students for."
    )
    prior_violations = dspy.InputField(
        desc="Violations found in the PREVIOUS attempt at this lesson (empty on the first "
        "attempt). If non-empty, FIX every one that concerns this step."
    )

    core_step: PlannerPlanStep = dspy.OutputField(
        desc=(
            "Return one fully specified core step with step_role='core' and "
            "aligned grounded blocks for this lesson objective."
        )
    )
