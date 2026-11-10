from __future__ import annotations

CANONICAL_SCHOOL_CODE = "PTRS"
CANONICAL_GRADE_NAME = "JSS1"
CANONICAL_SUBJECT_CODE = "MATH"
CANONICAL_SUBJECT_NAME = "Mathematics"

_TERM_ORDER = {
    "First Term": 0,
    "Second Term": 1,
    "Third Term": 2,
}


def canonical_term_sort_key(term: str | None) -> tuple[int, str]:
    normalized_term = term or ""
    return (_TERM_ORDER.get(normalized_term, len(_TERM_ORDER)), normalized_term)
