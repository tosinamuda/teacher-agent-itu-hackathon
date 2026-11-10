import dspy

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import PlannerPlanStep


class GenerateGlobalStepsSignature(dspy.Signature):
    """Write the lesson-wide intro step around the drafted core steps.

    The evaluation step is assembled deterministically from the curated assessment items
    (one practice block per objective), so this signature only authors the intro.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(
        desc="The lesson-plan specification: what the plan is, who it is for, and the "
        "requirements it must meet. Follow every requirement exactly."
    )
    scope_context = dspy.InputField(
        desc=(
            "Lesson scope as a self-describing context envelope with keys "
            "_context_name, purpose, shape, field_meanings, and scope."
        )
    )
    curriculum_context = dspy.InputField(
        desc=(
            "Curriculum and scheme context as a self-describing context envelope "
            "with keys _context_name, purpose, shape, field_meanings, and curriculum."
        )
    )
    lesson_objectives = dspy.InputField(
        desc="Resolved lesson-plan objectives created from the compressed KC plan."
    )
    core_steps = dspy.InputField(desc="The generated core steps for the lesson objectives.")
    evidence_summaries = dspy.InputField(
        desc="Summaries of the evidence bundles used for the core steps."
    )
    prior_violations = dspy.InputField(
        desc="Semantic violations from the PREVIOUS attempt's intro step (empty on "
        "the first attempt). If non-empty, FIX every one — e.g. remove any mention "
        "of ungrounded materials like 'worksheet' or 'answer key'."
    )

    intro_step: PlannerPlanStep = dspy.OutputField(
        desc=(
            "Return exactly one lesson-wide intro step (step_role='intro') that activates "
            "prior knowledge and frames the lesson for the listed objectives. Do NOT set "
            "lesson_objective_id or knowledge_type (those are for core steps "
            "only). Do NOT invent or "
            "mention ungrounded materials/aids such as 'worksheet', 'answer key', 'attached', "
            "or 'response cards' unless that exact material is listed in the curriculum "
            "instructional_materials."
        )
    )
