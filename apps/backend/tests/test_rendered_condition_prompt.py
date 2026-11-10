"""What each H1 condition actually puts in front of the model, read off the prompt.

Three test files already covered this ground and all three missed C0 being handed
``"entry_behaviour": [], "instructional_materials": []``:

- ``test_study_pack_conditioning`` asserted the request OBJECT, which was correct — the
  profile had emptied both fields. The serialisation of that object was not.
- ``test_no_ids_in_prompt`` asserted the payload, but built its blob from the unit alone,
  so half of what the model reads was never in it.
- ``test_study_pack_prompt_hygiene`` rendered a real ChatAdapter prompt — from a
  hand-built lesson context and a raw unit, bypassing both serialisers. It read a prompt
  no run produces, and checked it for study labels rather than for what it carried.

So these render the prompt through ``leveled_inputs``, the same function the generator
calls, over the frozen field plans rather than a fixture.
"""

from __future__ import annotations

import json
import re

import dspy
import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    signature_for,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    leveled_inputs,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

CASES = json.loads(EVAL_SET_PATH.read_text())["cases"]
LESSONS = [case["lesson"] for case in CASES]
LADDER = [ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3]

# Every field C1 adds to C0. None may appear in a C0 prompt in any form.
PLAN_FIELDS = (
    "entry_behaviour",
    "instructional_materials",
    "current_step",
    "instructional_events",
    "student_tasks",
    "assessment_points",
)
RECORD_KEY = re.compile(r"\b(?:lo-|step-|unit:|objective:)[a-z0-9:\-]+", re.IGNORECASE)


def _serialised_inputs(lesson: str, code: ConditionCode) -> list[str]:
    """The rendered value of every input field, one string per generation call."""
    case = next(c for c in CASES if c["lesson"] == lesson)
    profile = H1_CONDITION_PROFILES[code]
    plan = SessionPlanView.model_validate(case["plan"])
    request = BaseReviewPackRequestBuilder(figures="source").build(
        session_plan=plan,
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )
    signature = signature_for(profile.generation_policy())
    rendered = []
    for unit in request.units:
        inputs = leveled_inputs(request=request, unit=unit, signature=signature)
        messages = dspy.ChatAdapter().format(signature, demos=[], inputs=inputs)
        user = [m for m in messages if m["role"] == "user"][-1]["content"]
        rendered.append(str(user))
    return rendered


@pytest.mark.parametrize("lesson", LESSONS)
@pytest.mark.parametrize("code", LADDER)
def test_a_field_with_nothing_in_it_is_absent_not_empty(lesson: str, code: ConditionCode) -> None:
    """A condition that withholds a field must not announce that it withheld it."""
    for prompt in _serialised_inputs(lesson, code):
        for empty in ('": []', '": {}', '": null', '": ""'):
            assert empty not in prompt, f"{lesson} {code.value}: {empty}"


@pytest.mark.parametrize("lesson", LESSONS)
def test_c0_names_none_of_the_plan_fields(lesson: str) -> None:
    """The control reads the curriculum specification and nothing else.

    Not "reads them as empty" — the field NAME is itself information about what a
    lesson plan holds, and C0's whole claim is that it never saw one.
    """
    for prompt in _serialised_inputs(lesson, ConditionCode.C0):
        present = [field for field in PLAN_FIELDS if field in prompt]
        assert not present, f"{lesson}: C0 was shown {present}"


@pytest.mark.parametrize("lesson", LESSONS)
def test_c1_adds_to_c0_rather_than_replacing_it(lesson: str) -> None:
    """Whatever C0 is told, C1 is told too — the arms differ by addition only."""
    for c0, c1 in zip(
        _serialised_inputs(lesson, ConditionCode.C0),
        _serialised_inputs(lesson, ConditionCode.C1),
        strict=False,
    ):
        for line in re.findall(r'"(\w+)":', c0):
            assert f'"{line}"' in c1, f"{lesson}: C1 dropped {line}, which C0 carries"


def test_the_plan_fields_do_reach_c1() -> None:
    """Otherwise the two tests above pass on a C1 that carries nothing extra."""
    seen: set[str] = set()
    for lesson in LESSONS:
        for prompt in _serialised_inputs(lesson, ConditionCode.C1):
            seen |= {field for field in PLAN_FIELDS if field in prompt}
    assert seen == set(PLAN_FIELDS), sorted(set(PLAN_FIELDS) - seen)


@pytest.mark.parametrize("lesson", LESSONS)
@pytest.mark.parametrize("code", LADDER)
def test_no_record_key_survives_into_the_rendered_prompt(lesson: str, code: ConditionCode) -> None:
    """The same claim ``test_no_ids_in_prompt`` makes, now against the whole payload."""
    for prompt in _serialised_inputs(lesson, code):
        body = prompt.split("[[ ## artefact_spec ## ]]")[-1]
        assert not RECORD_KEY.findall(body), f"{lesson} {code.value}"
