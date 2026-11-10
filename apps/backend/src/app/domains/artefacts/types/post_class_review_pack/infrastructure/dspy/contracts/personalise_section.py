"""Model contract for personalising one approved section."""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    GenerationPolicyContext,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import RevisedSection


class SectionPersonalisation(dspy.Signature):
    """Personalise an approved base review-pack section for one focal learner.

    The lesson objective MUST be preserved — adapt HOW it is taught, never what
    is taught. Read the learner_state as follows:

    - mastery_band prescribes the depth of adaptation. "remediate": re-teach
      with full step-by-step explanations, a required worked example, easier
      practice, generous hints, full feedback. "reinforce": consolidate with
      moderate explanation, practice at the lesson's target difficulty,
      optional hints, standard feedback. "extend": minimal re-explanation,
      stretch practice above target difficulty, concise feedback.
    - mastery states how the learner actually performed on this objective's
      diagnostic questions. The totals are often small, so treat it as coarse
      evidence, not a precise measurement.
    - confidence and perceived_difficulty are the learner's own survey
      answers. Low confidence or high perceived difficulty -> more worked
      support and hints; high confidence with strong mastery -> less
      redundancy, more challenge.
    - evidence_items are the questions the learner missed, with the option
      they chose. Use them to target the SPECIFIC misconception shown: address
      why the chosen option is tempting but wrong, phrased gently and
      impersonally — say "a common slip here is ...", NEVER "you chose ..." or
      any reference to the learner's own test answers.
    - session_signals are the learner's survey answers about the whole lesson.
      Low interest -> shorter, more direct sections; a confused or low
      end-of-lesson feeling -> reduce cognitive load and reassure.

    Keep grounding in the provided evidence. Never claim that a problem you
    generated (or its solution) exists in the textbook or source, and never
    present problems you wrote as coming from the textbook — introduce new
    items plainly (e.g. "Extra practice").

    Return every block of the base section, in the same order, adapted to the
    learner; never return an empty list of blocks.

    Return the practice too, and adapt it to the mastery_band the same way:
    "remediate" gets easier questions than the base, "reinforce" keeps them at
    the lesson's target difficulty, "extend" raises them above it. Keep roughly
    as many items as the base has. Handing the base's questions back word for
    word is not personalisation — half of what the band prescribes is the
    practice.

    Work in this order. FIRST: from learner_state.evidence_items, note the
    EXACT option the learner chose on each missed question and plan how the
    section will defuse those specific choices — never substitute an invented
    example for the learner's actual mistake, and re-check every piece of
    arithmetic you write before including it. SECOND: re-read source_evidence
    and confirm it actually supports what you attribute to it; never attribute
    content, problems or solutions to the textbook unless the excerpt you read
    contains them. THEN write the personalised section following every rule
    above.
    """

    personalisation_policy: GenerationPolicyContext = dspy.InputField(
        desc="What kind of adaptation is allowed; preservation rules."
    )
    lesson_context: dict = dspy.InputField()
    base_section: dict = dspy.InputField(
        desc=(
            "Approved base section. Its figures are attached separately and are "
            "not shown or returned here."
        )
    )
    learner_state: dict = dspy.InputField(
        desc="Objective-indexed learner state with per-question answer evidence."
    )
    session_signals: dict = dspy.InputField(
        desc="Session-level interest + end-of-lesson feeling (tone/depth modifiers)."
    )
    source_evidence: list[dict] = dspy.InputField(
        desc="The textbook excerpts the base section cites — the only citable sources."
    )
    personalised_section: RevisedSection = dspy.OutputField(
        desc=(
            "Personalised section preserving the same lesson objective. Return ALL "
            "content blocks (adapt each block's text to the learner; never return an "
            "empty blocks list)."
        )
    )
