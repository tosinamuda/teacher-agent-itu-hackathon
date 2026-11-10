"""A revision note is shown as a reader reads it, and stored as it was generated."""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.domain.reading import for_reading

GENERATED = {
    "artefact_id": "AT-1",
    "steps": [
        {
            "step_id": "s1",
            "blocks": [
                {"type": "explanation", "content": "<b>Statistics</b> is the branch"},
                {"type": "practice", "question": "Is 4 \\times 5 = 20?", "answer": "Yes<br>it is"},
                {"type": "visual", "source_tikz": "\\draw (0,0) -- (1,1);"},
            ],
        }
    ],
}


def test_a_notes_html_and_bare_maths_reach_the_reader_as_formatting() -> None:
    blocks = for_reading(GENERATED)["steps"][0]["blocks"]  # type: ignore[index,call-overload]

    assert blocks[0]["content"] == "**Statistics** is the branch"
    assert blocks[1]["question"] == "Is 4 \\(\\times\\) 5 = 20?"
    assert blocks[1]["answer"] == "Yes\nit is"
    assert blocks[2]["source_tikz"] == "\\draw (0,0) -- (1,1);"


def test_reading_changes_nothing_stored_and_nothing_already_readable() -> None:
    read = for_reading(GENERATED)

    assert GENERATED["steps"][0]["blocks"][0]["content"] == "<b>Statistics</b> is the branch"  # type: ignore[index]
    assert for_reading(read) == read
