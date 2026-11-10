"""``focal_case_type_for_state`` labels a focal case from the learner's actual
diagnostic bands (their weakest band = greatest need), not their selection order.

Regression guard for the bug where the label was assigned by selection rank
(``FOCAL_CASE_SEQUENCE[rank % 4]``): two learners with identical diagnostics came out
with different types, and a learner with no remediate-level objective was tagged
"remediate" purely for being selected first.
"""

import pytest

from app.domains.experiments.application.focal_case_type import focal_case_type_for_state
from app.domains.experiments.domain import FocalCaseType
from app.domains.learner_state.domain.models import (
    LearnerState,
    ObjectiveLearnerState,
    misconception_codes_for_snapshot,
)


def _state(*bands: str) -> LearnerState:
    return LearnerState(
        student_id="ST-test",
        objective_states=[
            ObjectiveLearnerState(lesson_objective_id=f"lop{i:02d}", band=band)
            for i, band in enumerate(bands, start=1)
        ],
    )


@pytest.mark.parametrize(
    ("bands", "expected"),
    [
        (("extend", "extend", "extend", "extend"), FocalCaseType.EXTEND),
        (("reinforce", "extend", "extend", "extend"), FocalCaseType.REINFORCE),
        (("reinforce", "reinforce", "extend", "extend"), FocalCaseType.REINFORCE),
        (("remediate", "reinforce", "extend", "extend"), FocalCaseType.REMEDIATE),
        (("remediate",), FocalCaseType.REMEDIATE),
    ],
)
def test_focal_case_type_is_the_weakest_band(
    bands: tuple[str, ...], expected: FocalCaseType
) -> None:
    assert focal_case_type_for_state(_state(*bands)) == expected


def test_identical_diagnostics_get_the_same_type() -> None:
    bands = ("reinforce", "extend", "extend", "extend")
    assert focal_case_type_for_state(_state(*bands)) == focal_case_type_for_state(_state(*bands))


def test_no_diagnostic_evidence_is_unknown() -> None:
    assert focal_case_type_for_state(_state()) == FocalCaseType.MIXED_OR_MISCONCEPTION


# ``misconception_codes`` is a SEPARATE tag from the band: a learner can sit in the
# ``extend`` band yet still carry a misconception, so the two are reported orthogonally.


def _snapshot(*objectives: dict) -> dict:
    return {"objective_states": list(objectives)}


def test_misconception_codes_are_distinct_and_order_preserved() -> None:
    snap = _snapshot(
        {"band": "remediate", "misconception_code": "scale_confusion"},
        {"band": "reinforce", "misconception_code": "scale_confusion"},  # duplicate
        {"band": "extend", "misconception_code": "off_by_one"},
        {"band": "extend", "misconception_code": None},
    )
    assert misconception_codes_for_snapshot(snap) == ["scale_confusion", "off_by_one"]


def test_misconception_codes_empty_when_absent() -> None:
    assert misconception_codes_for_snapshot(_snapshot({"band": "extend"})) == []
    assert misconception_codes_for_snapshot(None) == []
    assert misconception_codes_for_snapshot({}) == []


def test_band_and_misconception_are_independent_tags() -> None:
    # Every objective is extend-band, but one carries a misconception: band stays
    # EXTEND while the misconception is still surfaced — the two tags don't conflate.
    state = LearnerState(
        student_id="ST-x",
        objective_states=[
            ObjectiveLearnerState(
                lesson_objective_id="lop01", band="extend", misconception_code="lingering_slip"
            ),
            ObjectiveLearnerState(lesson_objective_id="lop02", band="extend"),
        ],
    )
    assert focal_case_type_for_state(state) == FocalCaseType.EXTEND
    assert misconception_codes_for_snapshot(state.model_dump(mode="json")) == ["lingering_slip"]
