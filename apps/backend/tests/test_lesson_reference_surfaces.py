"""Three rating surfaces, one lesson.

The LLM judge reads a markdown packet; offline raters read a worksheet PDF; the
platform's raters read the packet drawer. Each once described a different lesson:
the markdown carried the previous-knowledge line, every activity, the work set and
her evaluation questions; the PDF carried the activities; the drawer carried step
titles. These hold every surface to every item of the one reference, for every
lesson in the frozen cohort, so a pack's alignment score cannot depend on which
surface rated it.
"""

from __future__ import annotations

import json
import re
from html import unescape

import pytest

from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.evaluation.api.schemas import EvaluationReferenceSheetResponse
from app.domains.evaluation.application.lesson_reference import lesson_reference, reference_sheet
from app.domains.evaluation.application.packet_payloads import PacketDetailPayloads
from app.domains.evaluation.application.worksheet_html.renderer import render_h1_worksheet_html
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.rater_packets import packet

CASES = {c["lesson"]: c for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
LESSONS = sorted(CASES)


def _flat(text: str) -> str:
    """Text as a reader would compare it: tags gone, entities decoded, one case, one space.

    Case is layout — the markdown opens a sentence with "The teacher", the sheet
    carries "the teacher" mid-line — and a surface test is about content.
    """
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", unescape(text)).strip().lower()


def _prose(item: str) -> list[str]:
    """The parts of an item outside its maths, each long enough to be a real check.

    The worksheet typesets `$...$` the way it typesets the pack, so the source is
    not in its text; the words around it are, and those are what a surface can
    drop. The maths rendering itself is the renderer's own tests' concern.
    """
    fragments = [_flat(part) for part in re.split(r"\$[^$]*\$", item)]
    return [f for f in fragments if len(f) >= 8]


def _plan(lesson: str) -> SessionPlanView:
    return SessionPlanView.model_validate(CASES[lesson]["plan"])


def _sections(lesson: str) -> list[dict]:
    # Any pack will do for a reference test; the surface under test is the lesson half.
    return [
        {
            "title": "x",
            "lesson_objective_id": o.lesson_objective_id,
            "blocks": [{"block_type": "explanation", "text": "y"}],
            "practice": [],
        }
        for o in _plan(lesson).lesson_plan_objectives
    ]


@pytest.mark.parametrize("lesson", LESSONS)
def test_the_markdown_packet_carries_every_item(lesson: str) -> None:
    reference = lesson_reference(_plan(lesson))
    body = _flat(packet("cand-test", CASES[lesson]["plan"], _sections(lesson))["body"])
    missing = [item for item in reference.items() if _flat(item) not in body]
    assert not missing, missing


@pytest.mark.parametrize("lesson", LESSONS)
def test_the_worksheet_html_carries_every_item(lesson: str) -> None:
    reference = lesson_reference(_plan(lesson))
    detail = packet("cand-test", CASES[lesson]["plan"], _sections(lesson))["detail"]
    html = _flat(render_h1_worksheet_html(detail))
    missing = [
        item for item in reference.items() if any(fragment not in html for fragment in _prose(item))
    ]
    assert not missing, missing


@pytest.mark.parametrize("lesson", LESSONS)
def test_the_platform_drawer_carries_every_item(lesson: str) -> None:
    reference = lesson_reference(_plan(lesson))
    payload = PacketDetailPayloads().reference_sheet_payload(_plan(lesson), pack_manifest=None)
    # Through the API schema, so a field the schema drops is a field the drawer loses.
    shown = EvaluationReferenceSheetResponse.model_validate(payload).model_dump()
    text = _flat(json.dumps(shown, ensure_ascii=False))
    missing = [
        item
        for item in reference.items()
        if _flat(json.dumps(item, ensure_ascii=False)[1:-1]) not in text
    ]
    assert not missing, missing


@pytest.mark.parametrize("lesson", LESSONS)
def test_the_three_surfaces_read_the_same_sheet(lesson: str) -> None:
    plan = _plan(lesson)
    from_domain = reference_sheet(lesson_reference(plan))
    from_platform = PacketDetailPayloads().reference_sheet_payload(plan, pack_manifest=None)
    from_packet = packet("cand-test", CASES[lesson]["plan"], _sections(lesson))["detail"][
        "reference_sheet"
    ]
    assert from_platform == from_domain
    assert from_packet == from_domain


def test_her_evaluation_questions_are_on_every_surface_by_decision() -> None:
    reference = lesson_reference(_plan("t3-w02"))
    assert len(reference.evaluation) == 9
    sheet = reference_sheet(reference)
    assert sheet["evaluation"] == list(reference.evaluation)
    assert EvaluationReferenceSheetResponse.model_validate(sheet).evaluation == list(
        reference.evaluation
    )


def test_the_sequence_is_her_words_never_the_study_coding() -> None:
    for lesson in LESSONS:
        for line in reference_sheet(lesson_reference(_plan(lesson)))["lesson_sequence"]:
            for code in ("present_content", "elicit_performance", "stimulate_recall", "sets_work"):
                assert code not in line, (lesson, line)


def test_the_manifest_fills_only_what_the_plan_left_empty() -> None:
    plan = _plan("t3-w02").model_copy(update={"instructional_materials": []})
    manifest = PostClassReviewPack.model_construct(
        instructional_materials=["a manifest material"],
        curriculum_objectives=[],
        **dict.fromkeys(("subject", "grade", "term", "week", "topic", "subtopic", "theme")),
    )
    sheet = PacketDetailPayloads().reference_sheet_payload(plan, pack_manifest=manifest)
    assert sheet["instructional_materials"] == ["a manifest material"]
    assert sheet["evaluation"] == list(lesson_reference(plan).evaluation)
