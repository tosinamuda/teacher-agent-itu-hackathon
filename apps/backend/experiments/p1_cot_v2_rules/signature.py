"""Production personalise signature + the ReAct-v2 rules, adapted for no-tool use."""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.personalise_section import (  # noqa: E501
    SectionPersonalisation,
)

# Same ordering and wording as the ReAct-v2 rules; the read_source tool
# protocol becomes "re-read the excerpt in source_evidence" — the only change.
_V2_RULES_NO_TOOL = (
    "\n\nWork in this order. FIRST: from learner_state.evidence_items, note the "
    "EXACT option the learner chose on each missed question and plan how the "
    "section will defuse those specific choices — never substitute an invented "
    "example for the learner's actual mistake, and re-check every piece of "
    "arithmetic you write before including it. SECOND: before citing any "
    "source_ref, re-read that excerpt in source_evidence and confirm it "
    "actually supports the text you attach it to; never attribute content, "
    "problems or solutions to the textbook unless the excerpt you read "
    "contains them. THEN write the personalised section following every rule "
    "above."
)

PersonaliseWithV2Rules = SectionPersonalisation.with_instructions(
    str(SectionPersonalisation.instructions) + _V2_RULES_NO_TOOL
)
