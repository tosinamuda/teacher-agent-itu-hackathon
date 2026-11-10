"""Nothing the model reads may be a record key.

Packs have printed "*Source:* step-t3w09-03" into learner text and narrated
"lo-t3w06-02" back at us. The ids buy nothing: ``normalise_section`` stamps the
unit's own ids onto the result, so whatever the model echoes is discarded.
"""

from __future__ import annotations

import json
import re

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    EVIDENCE_LABEL,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    normalise_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    RECORD_KEYS,
    prompt_lesson,
    prompt_unit,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.dump_inputs import _dump_lesson_json

CASES = json.loads(EVAL_SET_PATH.read_text())["cases"]
RECORD_KEY = re.compile(r"\b(?:lo-|step-|unit:|objective:)[a-z0-9:\-]+", re.IGNORECASE)


def _prompt_blob(lesson: str, plan: dict, code: ConditionCode) -> str:
    session_plan = SessionPlanView.model_validate(plan)
    request = BaseReviewPackRequestBuilder().build(
        session_plan=session_plan,
        policy=H1_CONDITION_PROFILES[code],
        sources=LessonSources.unresolved(session_plan.references),
    )
    parts = []
    for unit in request.units:
        parts.append(json.dumps(prompt_unit(unit), ensure_ascii=False))
        parts += [item.model_dump_json() for item in unit.source_evidence]
    return "\n".join(parts)


@pytest.mark.parametrize("case", CASES, ids=[c["lesson"] for c in CASES])
@pytest.mark.parametrize("code", [ConditionCode.C1, ConditionCode.C2, ConditionCode.C3])
def test_no_record_keys_reach_the_model(case: dict, code: ConditionCode) -> None:
    assert not RECORD_KEY.findall(_prompt_blob(case["lesson"], case["plan"], code))


@pytest.mark.parametrize("case", CASES, ids=[c["lesson"] for c in CASES])
def test_the_citable_label_is_the_lessons_own_words(case: dict) -> None:
    session_plan = SessionPlanView.model_validate(case["plan"])
    request = BaseReviewPackRequestBuilder().build(
        session_plan=session_plan,
        policy=H1_CONDITION_PROFILES[ConditionCode.C2],
        sources=LessonSources.unresolved(session_plan.references),
    )
    for unit in request.units:
        for item in unit.source_evidence:
            assert not RECORD_KEY.match(item.source_ref)
            assert item.source_ref == EVIDENCE_LABEL


def test_identity_is_restored_after_generation() -> None:
    """The ids are withheld from the prompt precisely because we stamp them."""
    session_plan = SessionPlanView.model_validate(CASES[0]["plan"])
    request = BaseReviewPackRequestBuilder().build(
        session_plan=session_plan,
        policy=H1_CONDITION_PROFILES[ConditionCode.C2],
        sources=LessonSources.unresolved(session_plan.references),
    )
    unit = request.units[0]
    stray = ReviewPackSection(
        section_id="whatever-the-model-said",
        title="t",
        lesson_objective_id="also-wrong",
        blocks=[
            ReviewPackBlock(block_id="", block_type="explanation", text="x", lesson_objective_id="")
        ],
    )
    fixed = normalise_section(stray, unit)
    assert fixed.section_id == unit.unit_id
    assert fixed.lesson_objective_id == unit.lesson_objective_id
    assert fixed.blocks[0].lesson_objective_id == unit.lesson_objective_id


def test_record_keys_are_named_where_they_are_dropped() -> None:
    """One list, covering every spelling an id takes on its way to a prompt.

    Written out rather than derived, so dropping a key from the strip has to be
    an edit here too — a set built from the models would move with them.
    """
    assert set(RECORD_KEYS) == {
        "unit_id",
        "source_step_id",
        "section_id",
        "block_id",
        "item_id",
        "lesson_objective_id",
        "curriculum_objective_id",
        "source_refs",
    }


def test_the_evidence_label_is_never_a_planning_label() -> None:
    """Her step headings are bare — "STEP 1:" — so titling the source with one named
    nothing and put a planning label in front of the model, which the spec forbids.
    Each unit carries exactly one evidence item, so it only has to name the thing."""
    assert EVIDENCE_LABEL == "the lesson note"


@pytest.mark.parametrize("case", CASES, ids=[c["lesson"] for c in CASES])
@pytest.mark.parametrize("code", [ConditionCode.C0, ConditionCode.C1, ConditionCode.C2])
def test_the_input_dump_prints_the_payload_itself(case: dict, code: ConditionCode) -> None:
    """`C0-C1-INPUTS.md` is the artefact reviewers read to see what a condition sends.

    It used to serialise the models a second way of its own, which is how it showed a
    tidier payload than the one the generator built — the file said `curriculum_scope`
    was absent while the prompt carried it as null. It renders through the generator's
    own two functions now, and this fails if it stops.
    """
    session_plan = SessionPlanView.model_validate(case["plan"])
    request = BaseReviewPackRequestBuilder().build(
        session_plan=session_plan,
        policy=H1_CONDITION_PROFILES[code],
        sources=LessonSources.unresolved(session_plan.references),
    )
    dumped = json.loads(_dump_lesson_json(request))
    assert dumped == prompt_lesson(request.lesson_context)
