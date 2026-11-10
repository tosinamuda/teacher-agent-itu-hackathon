"""DSPy contract for one teacher-directed review-pack revision."""

import dspy

from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)


class ApplyReviewPackFeedback(dspy.Signature):
    """Apply one teacher instruction to a personalised study pack, minimally.

    Apply exactly the requested change and nothing else. Preserve every other
    section, block and field verbatim, including stable identifiers. Keep full
    objective coverage: do not drop, merge, or renumber sections. If a highlighted
    part is given, scope the change to it; otherwise apply the instruction to the
    pack as a whole. Keep existing source references unless their content changes,
    never invent sources, and return the complete revised pack rather than a diff.
    """

    lesson_context: dict = dspy.InputField(
        desc="Subject, grade, topic, subtopic, and lesson objectives for the pack."
    )
    current_sections: list[ReviewPackSection] = dspy.InputField(
        desc="The full current study pack to revise."
    )
    highlighted_part = dspy.InputField(
        desc="The highlighted anchor and text, or empty for a whole-pack instruction."
    )
    revision_instruction = dspy.InputField(desc="The teacher's requested change.")
    conversation_summary = dspy.InputField(desc="Summary of earlier revision turns.")

    revised_sections: list[ReviewPackSection] = dspy.OutputField(
        desc="The complete revised pack with stable section and objective identities."
    )
    change_summary: str = dspy.OutputField(desc="One sentence describing the change.")
