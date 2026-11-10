"""What happened to each base section when a learner's pack was built.

Personalisation keeps the approved base section when the learner has no state for
its objective, when too few of their questions were marked for a band to mean anything, or
when the model answers with nothing a learner can read. Each section's
fate is recorded rather than inferred from the prose.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class PersonalisationOutcome(str, Enum):
    """Whether one section was adapted to the learner, and why it was not."""

    PERSONALISED = "personalised"
    NO_LEARNER_STATE = "no_learner_state"
    THIN_EVIDENCE = "thin_evidence"
    EMPTY_RESULT = "empty_result"


class SectionPersonalisation(BaseModel):
    """One section's fate, as analysis reads it back off the condition run."""

    model_config = ConfigDict(extra="forbid")

    section_id: str
    lesson_objective_id: str
    outcome: PersonalisationOutcome
