"""What a learner's section may change from the class note's, and what it must keep.

The specification names what adaptation may change (``adaptable``). Everything else of the
section stays as the class note has it, which a plain comparison can check. The title and the
drawings are the class note's by construction: the app sets them, so the writer's are never held
to them. A misconception is repaired only where the learner's state names one: a missing repair
goes back to the writer, and an unwanted one is dropped by the app.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.shared.json_types import JsonObject

#: The fields of a learner's part that each dimension of adaptation covers.
_FIELDS = {
    "depth of explanation": ("explanation",),
    "worked support": ("worked_examples",),
    "hints": ("practice",),
    "feedback": ("practice",),
    "practice difficulty": ("practice",),
    "misconception repair": ("misconception_repair",),
}


def _squash(text: object) -> str:
    return " ".join(str(text or "").split())


def adaptation_faults(
    part: JsonObject,
    base: ReviewPackSection,
    state: ObjectiveLearnerState,
    adaptable: Sequence[str],
) -> list[str]:
    """What a learner's part changes that the specification does not let adaptation change."""
    adapted = {field for dimension in adaptable for field in _FIELDS.get(dimension, ())}
    faults: list[str] = []
    if "practice" not in adapted:
        written = [(_squash(i.get("question")), _squash(i.get("answer"))) for i in _items(part)]
        kept = [(_squash(i.prompt), _squash(i.answer)) for i in base.practice]
        if written != kept:
            faults.append("keep the class note's practice as it is")
    faults.extend(_misconception_faults(part, state))
    return faults


def _items(part: JsonObject) -> list[JsonObject]:
    value = part.get("practice")
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _misconception_faults(part: JsonObject, state: ObjectiveLearnerState) -> list[str]:
    repair = _squash(part.get("misconception_repair"))
    if state.misconception and not repair:
        return [
            f"the learner's state names a misconception ({state.misconception}): write "
            "misconception_repair"
        ]
    return []
