"""Evaluation domain vocabulary: rating rubrics + source-audit criteria.

Shared by the rating, packet-detail, statistics and source-audit concerns, so it
lives here rather than in any one service module.
"""

from __future__ import annotations

from collections.abc import Mapping

from app.config import CONFIG
from app.shared.experiment_enums import Hypothesis
from app.shared.json_types import JsonObject

# Shown beside the rubric on every rating surface — the LLM packet, the worksheet,
# the platform drawer — and recorded in each judge pass's header. The reference
# sheet carries the teacher's evaluation questions so that assessment congruence
# can be rated at all; this is what keeps a pack that merely copies them from
# scoring as aligned for it. The rubric itself is frozen and unchanged.
H1_ALIGNMENT_GUIDANCE: tuple[str, ...] = (
    "The reference sheet includes the teacher's evaluation questions. A pack that "
    "reuses them, reworded or verbatim, may be credited for matching how the lesson "
    "was assessed — but reuse on its own does not establish taught-lesson alignment. "
    "Rate alignment on the whole of it: the objectives covered, the order taught, "
    "what the activities had the students do, the method, and the expected depth.",
)

H1_RUBRIC = (
    {
        "criterion_id": "objective_curriculum_alignment",
        "label": "Objective and curriculum alignment",
        "description": (
            "Does the revision note cover the intended lesson objectives and curriculum target?"
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "taught_lesson_alignment",
        "label": "Taught-lesson alignment",
        "description": (
            "Does it reflect the taught lesson — its sequence, emphasis, activities, "
            "and expected depth?"
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "scope_conceptual_correctness",
        "label": "Scope and conceptual correctness",
        "description": (
            "Does it stay within the expected lesson boundary and avoid "
            "conceptual/mathematical errors?"
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "clarity_usefulness",
        "label": "Student-facing clarity and usefulness",
        "description": (
            "Can JSS1 learners understand and use it meaningfully as take-home review material?"
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
)

H2_RUBRIC = (
    {
        "criterion_id": "learner_state_suitability",
        "label": "Learner-state suitability",
        "description": "Does this section match the learner's objective-level need?",
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "scaffolding_appropriateness",
        "label": "Scaffolding appropriateness",
        "description": (
            "Is the amount of help, explanation, worked example, hint, or feedback suitable?"
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "challenge_calibration",
        "label": "Challenge calibration",
        "description": "Is the difficulty too easy, too hard, or appropriate for the learner?",
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "misconception_support",
        "label": "Misconception support",
        "description": (
            "If a misconception is recorded, does the section address it? Mark N/A if none."
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
    {
        "criterion_id": "objective_preservation",
        "label": "Objective preservation",
        "description": (
            "Does the candidate preserve the original lesson objective and instructional scope?"
        ),
        "scale_min": 1,
        "scale_max": 5,
    },
)


SOURCE_AUDIT_CRITERIA: tuple[JsonObject, ...] = (
    {
        "criterion_id": "source_relevance",
        "label": "Source relevance",
        "description": "Is the cited source about the same concept/objective as the excerpt?",
        "scale_min": 0,
        "scale_max": 2,
    },
    {
        "criterion_id": "support_sufficiency",
        "label": "Support sufficiency",
        "description": "Does the source actually support the generated claim/example/item?",
        "scale_min": 0,
        "scale_max": 2,
    },
    {
        "criterion_id": "faithfulness",
        "label": "Faithfulness",
        "description": (
            "Does the generated text avoid distorting the source or adding unsupported claims?"
        ),
        "scale_min": 0,
        "scale_max": 2,
    },
    {
        "criterion_id": "scope_correctness",
        "label": "Scope correctness",
        "description": "Is the source within the approved lesson/topic/scope boundary?",
        "scale_min": 0,
        "scale_max": 2,
    },
)
_SOURCE_AUDIT_CRITERION_IDS: tuple[str, ...] = (
    "source_relevance",
    "support_sufficiency",
    "faithfulness",
    "scope_correctness",
)


# ===== Per-hypothesis registry (OCP) =====
#
# Replaces ``rubric = H1_RUBRIC if hyp == Hypothesis.H1 else H2_RUBRIC``-style
# switches scattered through the codebase. Adding a new hypothesis means adding
# one entry here, not editing every call site.

RUBRIC_BY_HYPOTHESIS: Mapping[Hypothesis, tuple[Mapping[str, object], ...]] = {
    Hypothesis.H1: H1_RUBRIC,
    Hypothesis.H2: H2_RUBRIC,
}


def rubric_for(hypothesis: Hypothesis | str) -> tuple[Mapping[str, object], ...]:
    """Return the per-hypothesis rubric (accepts enum or string value)."""
    key = hypothesis if isinstance(hypothesis, Hypothesis) else Hypothesis(hypothesis)
    return RUBRIC_BY_HYPOTHESIS[key]


def rubric_for_display(rubric: tuple[Mapping[str, object], ...]) -> list[dict[str, object]]:
    """Attach configured teacher-facing labels to rubric criteria."""
    aliases = CONFIG.rater_term_aliases
    return [
        {
            **criterion,
            "display_label": aliases.get(str(criterion["criterion_id"]), str(criterion["label"])),
        }
        for criterion in rubric
    ]
