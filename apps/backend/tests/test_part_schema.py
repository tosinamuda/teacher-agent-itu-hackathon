"""A spec's part schema: what a writer is shown is exactly what the app accepts."""

from __future__ import annotations

import re

import pytest

from app.domains.artefacts.core.domain.part_fields import PartInvalidError, PartSchemaError
from app.domains.artefacts.core.domain.parts import PartSchema, Unit
from app.domains.artefacts.core.domain.specification import ContentSpecification

WORKED_EXAMPLES = [
    {"name": "title", "description": "A heading for the learner", "type": "text"},
    {
        "name": "examples",
        "description": "Worked examples, each solved step by step",
        "type": "items",
        "fields": [
            {"name": "problem", "description": "The problem", "type": "markdown"},
            {"name": "solution", "description": "The working and answer", "type": "markdown"},
        ],
    },
    {"name": "tips", "description": "Short reminders", "type": "list", "required": False},
]


def test_a_part_is_stored_stripped_and_without_unset_optional_fields() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)

    stored = schema.validate(
        {"title": "  Adding fractions ", "examples": [{"problem": "1/4 + 2/4", "solution": "3/4"}]}
    )

    assert stored == {
        "title": "Adding fractions",
        "examples": [{"problem": "1/4 + 2/4", "solution": "3/4"}],
    }


def test_an_optional_field_given_empty_is_not_given() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)

    stored = schema.validate(
        {"title": "Fractions", "examples": [{"problem": "p", "solution": "s"}], "tips": []}
    )

    assert "tips" not in stored


def test_text_given_for_a_list_is_told_to_be_a_list() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)

    with pytest.raises(PartInvalidError) as refused:
        schema.validate(
            {"title": "T", "examples": [{"problem": "p", "solution": "s"}], "tips": "Check it"}
        )

    assert refused.value.problems == [
        'tips: must be a list, not text: write each item in square brackets, ["a", "b"]'
    ]


def test_a_required_field_given_empty_is_still_refused() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)

    with pytest.raises(PartInvalidError) as refused:
        schema.validate({"title": "Fractions", "examples": []})

    assert refused.value.problems == ["examples: must be a list with at least one item"]


def test_a_part_that_misses_the_schema_says_every_place_it_misses() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)

    with pytest.raises(PartInvalidError) as invalid:
        schema.validate({"title": "", "examples": [{"problem": "x"}], "extra": 1})

    assert invalid.value.problems == [
        "title: must be text that is not empty",
        "examples.0.solution: is required",
        "extra: is not a field of this part",
    ]


def test_an_unknown_field_is_dropped_when_empty_and_refused_when_not() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)
    part = {"title": "Fractions", "examples": [{"problem": "x", "solution": "y", "note": ""}]}

    assert schema.validate({**part, "extra": "", "more": [], "none": None}) == {
        "title": "Fractions",
        "examples": [{"problem": "x", "solution": "y"}],
    }
    with pytest.raises(PartInvalidError) as refused:
        schema.validate({**part, "extra": "something to say"})
    assert refused.value.problems == ["extra: is not a field of this part"]


def test_the_json_schema_a_writer_reads_is_the_one_that_checks() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES).json_schema()

    assert schema["required"] == ["title", "examples"]
    assert schema["additionalProperties"] is False
    example = schema["properties"]["examples"]["items"]
    assert example["required"] == ["problem", "solution"]
    assert example["additionalProperties"] is False
    assert schema["properties"]["tips"] == {
        "description": "Short reminders",
        "type": "array",
        "minItems": 1,
        "items": {"type": "string", "minLength": 1},
    }


def test_a_part_that_is_not_an_object_or_has_an_empty_list_is_refused() -> None:
    schema = PartSchema.from_record(WORKED_EXAMPLES)

    with pytest.raises(PartInvalidError) as not_an_object:
        schema.validate(["title"])
    with pytest.raises(PartInvalidError) as empty:
        schema.validate({"title": "T", "examples": []})

    assert not_an_object.value.problems == ["the part: must be an object"]
    assert empty.value.problems == ["examples: must be a list with at least one item"]


@pytest.mark.parametrize(
    ("fields", "problem"),
    [
        ([], "a part has at least one field"),
        ([{"name": "Title", "description": "d", "type": "text"}], "snake_case"),
        ([{"name": "t", "description": " ", "type": "text"}], "needs a description"),
        ([{"name": "t", "description": "d", "type": "items"}], "needs fields of its own"),
        ([{"name": "t", "description": "d", "type": "table"}], "table"),
        (
            [
                {"name": "t", "description": "d", "type": "text"},
                {"name": "t", "description": "d", "type": "text"},
            ],
            "repeats names: t",
        ),
        ([{"name": "t", "description": "d", "type": "text", "required": False}], "required"),
    ],
)
def test_a_schema_a_writer_could_not_follow_is_refused(fields: list, problem: str) -> None:
    with pytest.raises(PartSchemaError, match=problem):
        PartSchema.from_record(fields)


STEP = [
    {"name": "title", "description": "The step's title", "type": "text"},
    {"name": "minutes", "description": "How long it takes", "type": "whole_number"},
    {
        "name": "who",
        "description": "Who leads it",
        "type": "text",
        "options": ["teacher", "student"],
    },
    {"name": "graded", "description": "Whether it is marked", "type": "yes_no", "required": False},
    {
        "name": "blocks",
        "description": "What it teaches",
        "type": "items",
        "min_items": 0,
        "kinds": [
            {
                "name": "explanation",
                "description": "Something explained",
                "fields": [{"name": "content", "description": "The words", "type": "markdown"}],
            },
            {
                "name": "worked_example",
                "description": "A problem solved",
                "fields": [
                    {"name": "problem", "description": "The problem", "type": "markdown"},
                    {
                        "name": "steps",
                        "description": "The working",
                        "type": "items",
                        "fields": [{"name": "content", "description": "One step", "type": "text"}],
                    },
                ],
            },
        ],
    },
]
PLAN = [
    {
        "name": "core_step",
        "description": "The step that teaches it",
        "type": "group",
        "fields": STEP,
    }
]


def test_a_part_holds_numbers_choices_groups_and_mixed_lists() -> None:
    schema = PartSchema.from_record(PLAN)
    part = {
        "core_step": {
            "title": " Same bottoms ",
            "minutes": 20,
            "who": "teacher",
            "graded": False,
            "blocks": [
                {"kind": "explanation", "content": "Add the tops."},
                {"kind": "worked_example", "problem": "1/4 + 2/4", "steps": [{"content": "3/4"}]},
            ],
        }
    }

    stored = schema.validate(part)

    assert stored["core_step"] == {**part["core_step"], "title": "Same bottoms"}
    assert schema.validate({"core_step": {**part["core_step"], "blocks": []}})


def test_a_part_that_misses_the_new_types_says_where() -> None:
    schema = PartSchema.from_record(PLAN)

    with pytest.raises(PartInvalidError) as invalid:
        schema.validate(
            {
                "core_step": {
                    "title": "T",
                    "minutes": -1,
                    "who": "pupil",
                    "graded": "no",
                    "blocks": [{"kind": "table"}, {"kind": "explanation"}],
                }
            }
        )

    assert invalid.value.problems == [
        "core_step.minutes: must be a whole number",
        "core_step.who: must be one of: teacher, student",
        "core_step.graded: must be true or false",
        "core_step.blocks.0.kind: must be one of: explanation, worked_example",
        "core_step.blocks.1.content: is required",
    ]


def test_a_mixed_list_is_shown_as_one_of_its_kinds() -> None:
    step = PartSchema.from_record(PLAN).json_schema()["properties"]["core_step"]

    assert step["properties"]["who"]["enum"] == ["teacher", "student"]
    assert step["properties"]["minutes"]["type"] == "integer"
    blocks = step["properties"]["blocks"]
    assert blocks["minItems"] == 0
    first, second = blocks["items"]["oneOf"]
    assert first["properties"]["kind"] == {"const": "explanation"}
    assert first["required"] == ["kind", "content"]
    assert second["properties"]["steps"]["items"]["required"] == ["content"]


@pytest.mark.parametrize(
    ("field", "problem"),
    [
        ({"name": "t", "description": "d", "type": "markdown", "options": ["a"]}, "options"),
        ({"name": "t", "description": "d", "type": "text", "min_items": 0}, "how many"),
        ({"name": "t", "description": "d", "type": "group"}, "needs fields"),
        (
            {
                "name": "t",
                "description": "d",
                "type": "items",
                "kinds": [
                    {
                        "name": "k",
                        "description": "d",
                        "fields": [{"name": "kind", "description": "d", "type": "text"}],
                    }
                ],
            },
            "cannot have a field named kind",
        ),
    ],
)
def test_a_field_the_new_types_cannot_hold_is_refused(field: dict, problem: str) -> None:
    with pytest.raises(PartSchemaError, match=problem):
        PartSchema.from_record([field])


def test_a_part_nested_deeper_than_a_writer_can_follow_is_refused() -> None:
    field: dict = {"name": "leaf", "description": "d", "type": "text"}
    for depth in range(5):
        field = {"name": f"g{depth}", "description": "d", "type": "group", "fields": [field]}

    with pytest.raises(PartSchemaError, match="at most 4 deep"):
        PartSchema.from_record([field])


def test_a_spec_with_a_lesson_part_takes_that_part_for_the_lesson() -> None:
    spec = ContentSpecification.from_record(
        {
            "kind": "k",
            "revision": 1,
            "material": "m",
            "audience": "a",
            "levels": ["class_level"],
            "requirements": ["r"],
            "unit": "curriculum_objective",
            "parts": WORKED_EXAMPLES,
            "lesson_parts": PLAN,
        }
    )

    assert spec.schema_for(Unit.LESSON).fields[0].name == "core_step"
    assert spec.schema_for(Unit.CURRICULUM_OBJECTIVE).fields[0].name == "title"
    assert spec.structure[0].startswith("for the lesson: core_step")
    assert ContentSpecification.from_record(spec.to_record()) == spec
    with pytest.raises(ValueError, match="no part for a plan step"):
        spec.schema_for(Unit.PLAN_STEP)


def test_an_engine_spec_states_its_structure_from_its_parts_unless_given() -> None:
    spec = ContentSpecification.from_record(
        {
            "kind": "worked_examples",
            "revision": 1,
            "material": "worked examples",
            "audience": "{reader}",
            "levels": ["class_level"],
            "requirements": ["Show every step."],
            "unit": "plan_step",
            "parts": WORKED_EXAMPLES,
        }
    )

    assert spec.structure == (
        "title: A heading for the learner",
        "examples: Worked examples, each solved step by step (each with problem, solution)",
        "tips: Short reminders (optional)",
    )
    assert ContentSpecification.from_record(spec.to_record()) == spec


def test_unit_and_parts_are_set_together() -> None:
    with pytest.raises(ValueError, match="unit and parts are set together"):
        ContentSpecification.from_record(
            {
                "kind": "worked_examples",
                "revision": 1,
                "material": "m",
                "audience": "a",
                "levels": ["class_level"],
                "structure": ["s"],
                "requirements": ["r"],
                "parts": WORKED_EXAMPLES,
            }
        )


def test_a_drawing_is_a_tikzpicture_and_is_found_wherever_it_sits() -> None:
    schema = PartSchema.from_record(
        [
            {"name": "title", "description": "A title", "type": "text"},
            {
                "name": "figures",
                "description": "Drawings",
                "type": "items",
                "fields": [{"name": "drawing", "description": "One stage", "type": "tikz"}],
            },
        ]
    )
    picture = "\\begin{tikzpicture}\\draw (0,0) -- (1,0);\\end{tikzpicture}"

    stored = schema.validate({"title": "T", "figures": [{"drawing": picture}]})

    assert schema.drawings(stored) == [("figures.0.drawing", picture)]
    with pytest.raises(PartInvalidError, match="must be a tikzpicture environment"):
        schema.validate({"title": "T", "figures": [{"drawing": "a line from A to B"}]})


@pytest.mark.parametrize(
    ("line", "problem"),
    [
        ("$\\frac{80^\\circ}{2} = 40^\\circ$", None),
        ("$x = 5$ cm", None),
        ("$\\text{Place the set square on } AB$", "a sentence in \\text{}"),
        ("Half of 80 is 40", "between $ signs"),
    ],
)
def test_a_line_of_working_is_mathematics(line: str, problem: str | None) -> None:
    schema = PartSchema.from_record(
        [{"name": "working", "description": "One line of working", "type": "maths"}]
    )

    if problem is None:
        assert schema.validate({"working": line}) == {"working": line}
    else:
        with pytest.raises(PartInvalidError, match=re.escape(problem)):
            schema.validate({"working": line})


@pytest.mark.parametrize(
    "line",
    ["Chimaka → proper noun", "The market is full of buyers.", "$\\text{Ibadan}$ is a proper noun"],
)
def test_a_lesson_whose_working_is_not_a_calculation_writes_its_lines_as_plain_text(
    line: str,
) -> None:
    schema = PartSchema.from_record(
        [{"name": "working", "description": "One line of working", "type": "maths"}]
    )

    assert schema.validate({"working": line}, formulas=False) == {"working": line}
    with pytest.raises(PartInvalidError):
        schema.validate({"working": "Chimaka → proper noun"})


@pytest.mark.parametrize(
    ("text", "problem"),
    [
        ("Add the numerators: $\\frac{1}{4} + \\frac{2}{4}$.\nThen simplify.", None),
        ("It costs \\$5 and $x^2 = \\nu$.", None),
        ("The factors are 1, 3\\;\\nThe common factors are 1", "\\n outside a formula"),
        ("Spaced\\;out", "\\; outside a formula"),
        ("Find $x = 4 here", "never closed"),
    ],
)
def test_markdown_that_would_show_as_code_is_refused(text: str, problem: str | None) -> None:
    schema = PartSchema.from_record(
        [{"name": "body", "description": "Some text", "type": "markdown"}]
    )

    if problem is None:
        assert schema.validate({"body": text}) == {"body": text}
    else:
        with pytest.raises(PartInvalidError, match=re.escape(problem)):
            schema.validate({"body": text})


def test_a_number_given_for_a_text_field_is_told_to_be_written_as_text() -> None:
    schema = PartSchema.from_record([{"name": "marks", "description": "The marks", "type": "text"}])

    with pytest.raises(PartInvalidError, match=re.escape('write it between quotes, such as "2"')):
        schema.validate({"marks": 2})


_OPTIONS = [
    {
        "name": "options",
        "description": "The four options",
        "type": "group",
        "fields": [
            {"name": letter, "description": f"Option {letter.upper()}", "type": "markdown"}
            for letter in "abcd"
        ],
    },
]


def test_a_field_keyed_in_capitals_is_the_field_of_that_name() -> None:
    schema = PartSchema.from_record(_OPTIONS)

    stored = schema.validate({"options": {"A": "3/4", "B": "3/8", "C": "1/4", "D": "2/4"}})

    assert stored == {"options": {"a": "3/4", "b": "3/8", "c": "1/4", "d": "2/4"}}


def test_a_capital_key_does_not_override_the_lowercase_one_the_part_also_gives() -> None:
    schema = PartSchema.from_record(_OPTIONS)

    with pytest.raises(PartInvalidError) as refused:
        schema.validate({"options": {"a": "x", "A": "y", "b": "1", "c": "2", "d": "3"}})

    assert "options.A: is not a field of this part" in str(refused.value)


def test_a_key_that_names_no_field_in_any_case_is_still_refused() -> None:
    schema = PartSchema.from_record(_OPTIONS)

    with pytest.raises(PartInvalidError) as refused:
        schema.validate({"options": {"a": "1", "b": "2", "c": "3", "d": "4", "E": "5"}})

    assert "options.E: is not a field of this part" in str(refused.value)
