r"""LaTeX math survives JSON-escape decoding, regardless of delimiter family.

Regression guard for the corruption where ``decode_llm_json_escapes`` only
treated ``$…$`` as math and so mangled ``\(\frac{2}{5}\)`` into
``\(`` + form-feed + ``rac{2}{5}\)`` (``\f`` decoded as form-feed).
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    section_from_draft,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import DraftSection
from app.shared.llm_text import decode_llm_json_escapes, repair_math_control_chars


def test_decode_preserves_paren_delimited_math() -> None:
    text = r"For example \(\frac{2}{5}\) and \(5 \times \frac{1}{4}\)."
    # No corruption: backslash-f / backslash-t inside \(...\) stay intact.
    assert decode_llm_json_escapes(text) == text
    assert "\f" not in decode_llm_json_escapes(text)
    assert "\t" not in decode_llm_json_escapes(text)


def test_decode_preserves_bracket_block_math() -> None:
    text = r"\[\frac{a}{b} = \frac{c}{d}\]"
    assert decode_llm_json_escapes(text) == text


def test_decode_still_decodes_escapes_outside_math() -> None:
    # Literal backslash-n between paragraphs is a real escape and must decode,
    # while the math run is left untouched.
    text = r"First line.\n\nThen \(\frac{1}{2}\)."
    decoded = decode_llm_json_escapes(text)
    assert "\n\n" in decoded
    assert r"\frac{1}{2}" in decoded


def test_repair_reverses_corrupted_math() -> None:
    corrupted = "Add \\(\frac{2}{5}\\) here"  # noqa: W605 — \f is the corruption
    # Sanity: the corrupted form actually contains a form-feed, not "\f".
    assert "\f" in corrupted
    repaired = repair_math_control_chars(corrupted)
    assert repaired == r"Add \(\frac{2}{5}\) here"
    # Idempotent: repairing clean math is a no-op.
    assert repair_math_control_chars(repaired) == repaired


def test_repair_leaves_real_newlines_outside_math() -> None:
    text = "Para one.\n\nPara two with \\(\frac{1}{2}\\)."  # noqa: W605
    repaired = repair_math_control_chars(text)
    # The paragraph break outside math is preserved; only the math is repaired.
    assert "Para one.\n\nPara two" in repaired
    assert r"\frac{1}{2}" in repaired


def test_a_command_eaten_in_prose_is_restored() -> None:
    r"""``\times`` with one backslash is valid JSON, so the parser eats it before we look.

    The reader gets "4 imes 5", which two blinded judges marked packs down for. Twenty-two
    of these reached the 2026-08-09 runs and not one legitimate tab did.
    """
    assert repair_math_control_chars("Perimeter = 4 \times 5 cm") == (r"Perimeter = 4 \times 5 cm")
    assert repair_math_control_chars("h = 3\\,\text{m} outside math") == (
        "h = 3\\,\\text{m} outside math"
    )


def test_prose_formatting_survives_the_repair() -> None:
    """Newlines out here are paragraph breaks, and a tab before whitespace is layout."""
    assert repair_math_control_chars("One.\n\nTwo.") == "One.\n\nTwo."
    assert repair_math_control_chars("col\t | col") == "col\t | col"
    assert repair_math_control_chars("a\t9 b") == "a\t9 b"


def test_the_decode_can_itself_eat_a_command() -> None:
    r"""A ``\\times`` that survives JSON is decoded to a tab by our own escape pass.

    So the repair has to run after the decode, not instead of it.
    """
    survived = "Area = 4 \\times 5"
    assert "\t" in decode_llm_json_escapes(survived)
    assert repair_math_control_chars(decode_llm_json_escapes(survived)) == r"Area = 4 \times 5"


def test_the_generation_path_itself_restores_an_eaten_command() -> None:
    r"""``repair_math_control_chars`` had a test and no caller for months.

    Everything above proves the function works, which is not the property that failed —
    23 corrupted packs were written while every one of those assertions passed. This
    drives ``section_from_draft``, the path a real section takes, and is the only test
    here that would have gone red.
    """
    unit = SectionGenerationUnit(
        unit_id="objective:lop01",
        lesson_objective_id="lop01",
        objective_text="Find the perimeter of a rectangle",
    )
    draft = DraftSection(
        title="Perimeter",
        instructional_support="Perimeter = 4 \times 5 cm = 20 cm.",
        worked_examples=[],
        practice=[],
    )
    written = section_from_draft(draft, unit).blocks[0].text
    assert "\t" not in written
    # Restored, and then delimited: the command was standing in prose, where the
    # renderer would have shown the backslash rather than the sign.
    assert written == r"Perimeter = 4 \(\times\) 5 cm = 20 cm."


def test_a_display_block_written_over_several_lines_keeps_its_line_breaks() -> None:
    r"""The textbook writes display maths over lines; each break was once turned into ``\n``."""
    block = "$$\n\\begin{array}{r}\n8\\\\\n3\\enclose{longdiv}{26}\n\\end{array}\n$$"

    assert repair_math_control_chars(block) == block


def test_a_newline_that_ate_a_command_in_maths_is_restored() -> None:
    assert repair_math_control_chars("$x \neq y$") == r"$x \neq y$"
    assert repair_math_control_chars("$$4\newline 7$$") == r"$$4\newline 7$$"


def test_a_line_of_maths_that_begins_with_a_variable_is_left_a_line() -> None:
    assert repair_math_control_chars("$$a\nu = 5$$") == "$$a\nu = 5$$"


def test_a_python_escape_the_corpus_ate_is_restored() -> None:
    r"""``\angle`` in a Python string is a bell and ``ngle``, as the textbook records carry it."""
    assert repair_math_control_chars("$\x07ngle AGE$") == r"$\angle AGE$"


def test_the_rows_of_an_environment_standing_in_prose_are_not_decoded() -> None:
    bare = r"Divide: \begin{array}{r} 8\\ 3 \end{array} so 8."

    assert decode_llm_json_escapes(bare) == bare


def test_an_environment_escaped_twice_is_decoded_like_the_rest_of_its_prose() -> None:
    assert decode_llm_json_escapes(r"\\begin{array}{r} 8\\\\ 3 \\end{array}") == (
        r"\begin{array}{r} 8\\ 3 \end{array}"
    )
