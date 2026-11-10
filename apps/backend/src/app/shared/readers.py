"""Who a learner-facing material is written for, named from the lesson's grade."""

_READERS = {
    "JSS1": "a junior secondary student aged about 11-13",
    "JSS2": "a junior secondary student aged about 12-14",
    "JSS3": "a junior secondary student aged about 13-15",
}


def reader_for(grade_level: str) -> str:
    """The reader a grade names, or a secondary student when the grade is not bound."""
    return _READERS.get(grade_level.strip().upper(), "a secondary student")
