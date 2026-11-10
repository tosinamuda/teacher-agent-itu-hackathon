"""Bloom's-taxonomy level + verb→level map — single source of truth.

Two domains previously kept their own copies (``lesson_plan/drafting/domain/bloom``
and ``expert_content/application/linkage_models``). They diverged: the
expert_content copy added ``interpret`` under "understand" plus 11 more "apply"
verbs (compute, add, subtract, multiply, divide, round, estimate, approximate,
express, present, bisect, measure). The lesson-plan copy was missing all of those.

Unifying here uses the SUPERSET of both copies — any verb either domain knew is
now known to both, eliminating the silent divergence.

Live in ``app/shared/`` because BloomLevel is curriculum-grammar, used across
``artefacts``, ``expert_content``, and (potentially) ``evaluation``. No
domain-cross dependency: both consuming domains import down into shared, not
sideways into each other.
"""

from __future__ import annotations

from typing import Literal

BloomLevel = Literal["remember", "understand", "apply", "analyze"]

# Lower-case verb → Bloom level. The SUPERSET of the two former copies; do not
# narrow without a deliberate reason recorded here.
BLOOM_VERB_MAP: dict[str, BloomLevel] = {
    "list": "remember",
    "name": "remember",
    "state": "remember",
    "define": "remember",
    "identify": "remember",
    "recall": "remember",
    "recognise": "remember",
    "recognize": "remember",
    "count": "remember",
    "write": "remember",
    "read": "remember",
    "explain": "understand",
    "describe": "understand",
    "discuss": "understand",
    "distinguish": "understand",
    "classify": "understand",
    "compare": "understand",
    "interpret": "understand",
    "convert": "apply",
    "solve": "apply",
    "calculate": "apply",
    "apply": "apply",
    "use": "apply",
    "draw": "apply",
    "construct": "apply",
    "find": "apply",
    "determine": "apply",
    "compute": "apply",
    "add": "apply",
    "subtract": "apply",
    "multiply": "apply",
    "divide": "apply",
    "round": "apply",
    "estimate": "apply",
    "approximate": "apply",
    "express": "apply",
    "present": "apply",
    "bisect": "apply",
    "measure": "apply",
    "analyze": "analyze",
    "analyse": "analyze",
    "differentiate": "analyze",
    "examine": "analyze",
    "verify": "analyze",
}
