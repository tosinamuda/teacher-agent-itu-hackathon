"""Translate a condition policy into model-facing generation policy."""

from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ReviewPackGenerationPolicy,
)

from .schemas import GenerationPolicyContext


def build_generation_policy(policy: ReviewPackGenerationPolicy) -> GenerationPolicyContext:
    """Build the actionable policy serialized into generation prompts."""
    return GenerationPolicyContext(
        require_source_refs=policy.retrieval.require_source_refs,
        use_only_provided_sources=policy.retrieval.use_only_provided_sources,
        preserve_lesson_objective=policy.personalisation.preserve_base_objectives,
        instruction_summary=instruction_summary(policy),
    )


def instruction_summary(policy: ReviewPackGenerationPolicy) -> str:
    """Describe only behavior the model can act on for this condition."""
    parts: list[str] = ["Generate the section from the context supplied for this unit."]
    if policy.retrieval.enabled:
        parts.append(
            "Ground every claim in the provided source evidence — the teacher's own "
            "lesson note for this step, exactly as she wrote it. Where the note "
            "draws a figure as LaTeX/TikZ code, that code IS the drawing. The "
            "note's figures are attached to your section automatically: refer to "
            "them by their fig-NN labels when they help, never paste drawing code "
            "into learner text, and never mention any picture that has no label."
        )
        if policy.retrieval.require_source_refs:
            parts.append(
                "Never write a source marker, reference number or citation in the "
                "block text itself — the text must read as prose to a student."
            )
        if policy.retrieval.use_only_provided_sources:
            parts.append("Use only the provided evidence; do not invent sources.")
    if policy.personalisation.adapts_to_learner_state:
        parts.append("Adapt the base section to the learner state while preserving the objective.")
    return " ".join(parts)
