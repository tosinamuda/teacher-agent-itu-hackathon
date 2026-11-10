from __future__ import annotations

import re

# Source of truth lives in ``app.shared.bloom_taxonomy``; this domain only
# re-exports for the convenience of existing callers (``infer_bloom_level``,
# ``extract_primary_verb``) that consume the map. See the module docstring
# in ``bloom_taxonomy`` for why this was lifted out of the domain.
from app.shared.bloom_taxonomy import BLOOM_VERB_MAP, BloomLevel

_WORD_RE = re.compile(r"[A-Za-z]+")
_BLOOM_ORDER: dict[BloomLevel, int] = {
    "remember": 0,
    "understand": 1,
    "apply": 2,
    "analyze": 3,
}


def infer_bloom_level(verb: str) -> BloomLevel:
    return BLOOM_VERB_MAP.get(verb.lower().strip(), "apply")


def extract_primary_verb(objective_text: str) -> str:
    words = [str(token) for token in _WORD_RE.findall(objective_text)]
    for word in words:
        normalized = word.lower().strip()
        if normalized in BLOOM_VERB_MAP:
            return normalized
    return words[0].lower() if words else "apply"


def bloom_level_rank(level: BloomLevel) -> int:
    return _BLOOM_ORDER[level]
