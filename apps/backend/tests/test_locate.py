"""Finding where selected text sits in a draft's parts, for any type of content."""

from __future__ import annotations

from app.domains.content_engine.domain.locate import MOST_PLACES, locate
from app.shared.json_types import JsonObject

PARTS: dict[str, JsonObject] = {
    "lesson": {"theme": "Number and Numeration", "materials": ["Number charts", "Flash cards"]},
    "po01": {
        "lesson_objectives": [
            {
                "objective": "Find the **lowest common multiple** of two numbers",
                "core_step": {
                    "blocks": [
                        {"type": "explanation", "content": "A multiple of $6$ is $12$."},
                        {"type": "practice", "question": "Find the LCM of 12 and 15."},
                    ]
                },
            }
        ]
    },
    "po02": {"lesson_objectives": [{"objective": "Find the LCM of 8 and 12"}]},
}


def test_text_inside_a_field_finds_its_unit_and_path() -> None:
    found = locate(PARTS, "Find the LCM of 12 and 15.")

    assert [(p.unit_id, p.path) for p in found] == [
        ("po01", "lesson_objectives.0.core_step.blocks.1.question")
    ]


def test_a_list_item_is_found_by_its_index() -> None:
    assert [(p.unit_id, p.path) for p in locate(PARTS, "Flash cards")] == [
        ("lesson", "materials.1")
    ]


def test_markdown_and_maths_marks_do_not_stop_a_match() -> None:
    assert [p.path for p in locate(PARTS, "lowest common multiple of two")] == [
        "lesson_objectives.0.objective"
    ]
    assert [p.path for p in locate(PARTS, "A multiple of 6 is 12.")] == [
        "lesson_objectives.0.core_step.blocks.0.content"
    ]


def test_case_and_spacing_do_not_stop_a_match() -> None:
    assert len(locate(PARTS, "  number   CHARTS ")) == 1


def test_text_in_several_fields_finds_every_one() -> None:
    found = locate(PARTS, "Find the LCM of")

    assert {(p.unit_id, p.path) for p in found} == {
        ("po01", "lesson_objectives.0.core_step.blocks.1.question"),
        ("po02", "lesson_objectives.0.objective"),
    }


def test_a_selection_across_fields_finds_the_fields_it_covers() -> None:
    found = locate(PARTS, "Number and Numeration Number charts")

    assert {(p.unit_id, p.path) for p in found} == {("lesson", "theme"), ("lesson", "materials.0")}


def test_a_field_too_short_to_tell_apart_is_not_found_by_a_selection_that_covers_it() -> None:
    assert locate(PARTS, "Number charts Flash cards extra words") == [
        locate(PARTS, "Number charts")[0]
    ]


def test_text_that_is_not_in_the_draft_finds_nothing() -> None:
    assert locate(PARTS, "LCM / HCF — LCM of whole numbers") == []
    assert locate(PARTS, "   ") == []


def test_a_match_in_a_long_field_shows_the_text_around_it_and_the_line() -> None:
    body = (
        "First line of the step.\nSecond line, with the **lowest common multiple** defined.\nThird."
    )
    parts: dict[str, JsonObject] = {"u": {"content": body + " " + "x" * 300}}

    (place,) = locate(parts, "lowest common multiple")

    assert (place.unit_id, place.path, place.line) == ("u", "content", 2)
    assert "lowest common multiple" in place.context
    assert place.context.endswith("\u2026")
    assert not place.context.startswith("\u2026")


def test_a_field_of_one_line_has_no_line() -> None:
    (place,) = locate(PARTS, "Flash cards")

    assert place.line is None
    assert place.context == "Flash cards"


def test_a_match_far_into_a_field_is_shown_with_its_own_surroundings() -> None:
    parts: dict[str, JsonObject] = {"u": {"content": "x" * 400 + " the needle phrase " + "y" * 400}}

    (place,) = locate(parts, "needle phrase")

    assert "needle phrase" in place.context
    assert place.context.startswith("\u2026") and place.context.endswith("\u2026")
    assert len(place.context) < 200


def test_the_places_are_capped() -> None:
    many: dict[str, JsonObject] = {"u": {"items": ["same words " + "x" * 300] * (MOST_PLACES + 5)}}

    assert len(locate(many, "same words")) == MOST_PLACES
