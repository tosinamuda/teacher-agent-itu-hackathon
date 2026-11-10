"""The study's four raters, as rater profiles the app knows them by.

They rated on the study's documents, not in the app, so none can sign in or be assigned: each
is a profile of origin ``study_record``, named as the release names them.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable

from app.domains.evaluation.infrastructure.models import EvaluationRater

RATER_ID_PREFIX = "STUDY-"
Raters = dict[str, EvaluationRater]


def rater_rows(codes: Iterable[str]) -> Raters:
    """One profile per rater code the ratings use, e.g. ``rater-2`` as "Study rater 2"."""
    return {
        code: EvaluationRater(
            id=uuid.uuid4(),
            rater_id=f"{RATER_ID_PREFIX}{code}",
            display_name=f"Study rater {code.removeprefix('rater-')}",
            user_id=None,
            origin="study_record",
        )
        for code in sorted(set(codes))
    }
