"""What the app sets on a learner's part, so the writer is asked only for what it alone can write.

The class note's drawings are copied back exactly, and a misconception repair is kept only where
the learner's state names a misconception. Both are known to the app, and a writer asked to
copy a drawing or to leave a field out can fail them through every retry.
"""

from __future__ import annotations

import re

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.shared.json_types import JsonObject

_DRAWING = r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}"
_DRAWN = re.compile(rf"({_DRAWING})(?:[ \t]*\n\s*\*([^*\n]+)\*)?", re.DOTALL)
_TIKZ = re.compile(_DRAWING, re.DOTALL)


def drawings_of(base: ReviewPackSection) -> list[JsonObject]:
    """The class section's drawings, each with the caption that follows it, in order."""
    prose = "\n\n".join(b.text for b in base.blocks if b.block_type == "explanation")
    return [
        {"drawing": found.group(1), "caption": (found.group(2) or "").strip()}
        for found in _DRAWN.finditer(prose)
    ]


def pinned(part: JsonObject, base: ReviewPackSection, state: ObjectiveLearnerState) -> JsonObject:
    """The part with the class note's drawings and without a repair the state does not call for."""
    explanation = _TIKZ.sub("", str(part.get("explanation") or "")).strip()
    kept = {
        key: value
        for key, value in part.items()
        if key not in {"figures", "explanation"}
        and (key != "misconception_repair" or state.misconception)
    }
    return {**kept, "explanation": explanation, "figures": list(drawings_of(base))}
