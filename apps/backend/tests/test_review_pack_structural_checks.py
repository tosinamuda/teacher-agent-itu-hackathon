"""The structural checks the class note and a personalised note must pass."""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    BASE_REVIEW_PACK_POLICY,
    MIN_EXPLANATION_CHARS,
    PERSONALISED_REVIEW_PACK_POLICY,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from tests.test_study_pack_conditioning import BUILDER, SESSION_PLAN, LessonSources

REQUEST = BUILDER.build(
    session_plan=SESSION_PLAN,
    policy=BASE_REVIEW_PACK_POLICY,
    sources=LessonSources.unresolved(SESSION_PLAN.references),
)
PROSE = "x" * MIN_EXPLANATION_CHARS


def _section(objective: str, explanation: str = PROSE) -> ReviewPackSection:
    return ReviewPackSection(
        section_id=f"sec-{objective}",
        title=f"Section {objective}",
        lesson_objective_id=objective,
        blocks=[
            ReviewPackBlock(
                block_id=f"b-{objective}",
                block_type="explanation",
                text=explanation,
                lesson_objective_id=objective,
                source_refs=["REF-1"],
            )
        ],
        practice=[ReviewPackPracticeItem(item_id=f"p-{objective}", prompt="Find.", answer="15")],
        source_refs=["REF-1"],
    )


def _result(policy, sections, base=None):
    return ReviewPackStructuralValidator().validate(
        policy=policy, sections=sections, request=REQUEST, base_sections=base
    )


def _check(result, name):
    return next(check for check in result.checks if check.check == name)


def test_the_class_note_policy_requires_an_explanation_of_the_least_length() -> None:
    sections = [_section("lop01"), _section("lop02", "One line.")]

    check = _check(_result(BASE_REVIEW_PACK_POLICY, sections), "explanation_present")

    assert check.passed is False
    assert check.details == {
        "explanation_characters": {"sec-lop02": len("One line.")},
        "minimum": MIN_EXPLANATION_CHARS,
    }


def test_a_section_with_no_explanation_block_fails_the_check() -> None:
    bare = _section("lop01")
    bare.blocks[0].block_type = "worked_example"

    check = _check(
        _result(BASE_REVIEW_PACK_POLICY, [bare, _section("lop02")]), "explanation_present"
    )

    assert check.passed is False
    assert check.details["explanation_characters"] == {"sec-lop01": 0}


def test_explanation_split_across_blocks_counts_together() -> None:
    section = _section("lop01", "x" * (MIN_EXPLANATION_CHARS // 2))
    section.blocks.append(section.blocks[0].model_copy(update={"block_id": "b2"}))

    check = _check(
        _result(BASE_REVIEW_PACK_POLICY, [section, _section("lop02")]), "explanation_present"
    )

    assert check.passed is True


def test_a_personalised_section_for_an_objective_the_base_pack_lacks_fails() -> None:
    base = [_section("lop01")]
    personalised = [_section("lop01"), _section("lop02")]

    result = _result(PERSONALISED_REVIEW_PACK_POLICY, personalised, base)

    added = _check(result, "no_added_objectives")
    assert (added.passed, added.details) == (False, {"added": ["lop02"]})
    assert _check(result, "objective_preservation").passed is True


def test_a_personalised_pack_that_keeps_the_base_objectives_passes_the_added_check() -> None:
    base = [_section("lop01"), _section("lop02")]

    result = _result(PERSONALISED_REVIEW_PACK_POLICY, [_section("lop01"), _section("lop02")], base)

    assert _check(result, "no_added_objectives").passed is True
