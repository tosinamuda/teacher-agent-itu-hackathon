"""Model contract for repairing one failed review-pack section."""

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    GenerationPolicyContext,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    ReviewPackPipeline,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import RevisedSection

from . import evaluated_revision


class RepairSection(dspy.Signature):
    """Repair a review-pack section that failed deterministic validation.

    Make the SMALLEST edit that fixes exactly the issues listed in
    validation_issues: delete or rewrite only the offending text and keep every
    other sentence and block exactly as it is, in the same order. Keep the same
    lesson objective. When an issue quotes a phrase, that phrase must not appear
    in the repaired section. Never add new claims about where content came from.
    """

    policy: GenerationPolicyContext = dspy.InputField()
    lesson_context: dict = dspy.InputField()
    unit_context: dict = dspy.InputField(
        desc="The lesson objective this section teaches, and how the lesson taught it."
    )
    source_evidence: list[dict] = dspy.InputField()
    failed_section: dict = dspy.InputField(
        desc=(
            "The section to fix. Return it with the smallest possible edit. Its "
            "figures are attached separately and are not shown or returned here."
        )
    )
    validation_issues: list[str] = dspy.InputField(
        desc=(
            "The exact problems to fix; any phrase quoted here must NOT appear "
            "in the repaired section."
        )
    )
    repaired_section: RevisedSection = dspy.OutputField(
        desc="The same section with only the offending text changed."
    )


def repair_contract(pipeline: ReviewPackPipeline) -> type[dspy.Signature]:
    """The repair contract for a pipeline version: 2026-08-25 returns Part 1's output schema."""
    if pipeline is not ReviewPackPipeline.V2026_08_25:
        return RepairSection
    evaluated: type[dspy.Signature] = RepairSection.delete("repaired_section").append(
        "repaired_section",
        dspy.OutputField(desc="The same section with only the offending text changed."),
        type_=evaluated_revision.RevisedSection,
    )
    return evaluated
