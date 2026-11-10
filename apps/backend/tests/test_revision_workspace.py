"""The file-editing revision workspace: round-trip, anchors, and edit safety.

The point of the design is structural: an edit applies only where its old text
occurs exactly once, prose maps back to its own block by marker, and figures
cannot be edited at all — so repair collateral outside a flagged span is not a
risk to check for but a state the workspace cannot express.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.edit_section import (
    editing_tools,
    file_to_section,
    locate,
    section_to_file,
)


def _section() -> ReviewPackSection:
    return ReviewPackSection(
        section_id="s1",
        title="Perimeter of shapes",
        lesson_objective_id="lop01",
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="The perimeter is the distance round a shape.",
                lesson_objective_id="lop01",
            ),
            ReviewPackBlock(
                block_id="fig",
                block_type="visual",
                variant="diagram_tikz",
                figure_ref="fig-03",
                caption="A square with 4 cm sides.",
                source_tikz="\\begin{tikzpicture}...",
                lesson_objective_id="lop01",
            ),
            ReviewPackBlock(
                block_id="b2",
                block_type="worked_example",
                text="Find the perimeter of a 5 cm square. Answer: 25 cm.",
                lesson_objective_id="lop01",
            ),
        ],
    )


def test_round_trip_is_lossless_without_edits() -> None:
    section = _section()
    assert file_to_section(section_to_file(section), section) == section


def test_edit_maps_back_to_its_own_block_only() -> None:
    section = _section()
    buffer = {"text": section_to_file(section)}
    _, edit = editing_tools(buffer)
    assert edit("Answer: 25 cm.", "Answer: 20 cm.") == "Edited."
    revised = file_to_section(buffer["text"], section)
    assert revised.blocks[2].text.endswith("Answer: 20 cm.")
    assert revised.blocks[0].text == section.blocks[0].text  # untouched block intact
    assert revised.blocks[1].source_tikz == section.blocks[1].source_tikz


def test_edits_require_a_unique_match_and_spare_markers_and_figures() -> None:
    section = _section()
    buffer = {"text": section_to_file(section)}
    _, edit = editing_tools(buffer)
    assert "matches" in edit("perimeter", "boundary")  # ambiguous -> refused
    assert edit("nowhere text", "x").startswith("No match")
    assert edit("<!-- block:b1 -->", "").startswith("Refused")
    assert edit("[figure fig-03: A square with 4 cm sides.]", "gone").startswith("Refused")
    assert file_to_section(buffer["text"], section) == section  # nothing changed


def test_findings_locate_to_their_line() -> None:
    text = section_to_file(_section())
    line = locate(text, "distance round a shape")
    assert line is not None
    assert text.splitlines()[line - 1].endswith("round a shape.")
