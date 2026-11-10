r"""The model's markup, repaired into markup a reader can be shown.

Every case here is a shape taken from the 72 packs of ``c0c3-worksheet``: the
undelimited command that hits only the two arms the registered endpoint compares,
the field that ran past its closing quote, and the dropped delimiter that turned the
rest of a block inside out.
"""

from __future__ import annotations

import pytest

from app.shared.llm_markup import (
    close_unclosed_math,
    count_bare_math,
    delimit_bare_math,
    reader_ready,
)
from app.shared.llm_text import decode_llm_json_escapes, strip_json_residue


class TestBareCommandsInProse:
    def test_a_command_standing_in_prose_is_delimited(self) -> None:
        # C0/C1 wrote this 68 times; C2/C3, copying her note, wrote it none.
        assert delimit_bare_math(r"Perimeter = 4 \times side.") == (
            r"Perimeter = 4 \(\times\) side."
        )

    def test_only_the_command_is_wrapped_never_the_words_beside_it(self) -> None:
        r"""The extent matters: ``\(Perimeter = 4 \times side\)`` typesets nine italic
        letters where the reader wants a word."""
        out = delimit_bare_math(r"Perimeter = 2 \times (base + side).")
        assert out.startswith("Perimeter = 2 ")
        assert out.endswith("(base + side).")

    def test_a_command_keeps_its_braced_arguments(self) -> None:
        assert delimit_bare_math(r"Using \frac{22}{7} for pi.") == (
            r"Using \(\frac{22}{7}\) for pi."
        )

    def test_every_command_in_a_run_is_delimited(self) -> None:
        assert delimit_bare_math(r"Circumference = 2 \times \pi \times radius") == (
            r"Circumference = 2 \(\times\) \(\pi\) \(\times\) radius"
        )

    def test_math_that_is_already_delimited_is_untouched(self) -> None:
        for text in (
            r"Using \(\pi = \frac{22}{7}\), the circle closes.",
            r"\[P = 6 \times 5\text{cm} = 30\text{cm}.\]",
            r"The angle $60^{\circ}$ is fixed.",
        ):
            assert delimit_bare_math(text) == text

    def test_a_command_inside_an_undelimited_expression_is_left_alone(self) -> None:
        r"""``60^{\(\circ\)}`` would be worse than ``60^{\circ}``: repairing from
        inside a larger expression breaks it rather than typesetting it."""
        assert delimit_bare_math(r"an angle of 60^{\circ} at B") == r"an angle of 60^{\circ} at B"

    def test_markdown_escapes_and_line_breaks_are_not_commands(self) -> None:
        assert delimit_bare_math(r"a \_literal\_ underscore") == r"a \_literal\_ underscore"
        assert delimit_bare_math(r"end of line \\ next") == r"end of line \\ next"

    def test_it_is_idempotent(self) -> None:
        once = delimit_bare_math(r"Perimeter = 4 \times side.")
        assert delimit_bare_math(once) == once

    def test_the_count_is_what_the_repair_would_change(self) -> None:
        text = r"4 \times side, and \(\pi\) is delimited, and \frac{1}{2} is not."
        assert count_bare_math(text) == 2
        assert count_bare_math(delimit_bare_math(text)) == 0


class TestUnclosedDelimiters:
    def test_an_unclosed_inline_run_is_closed_before_the_full_stop(self) -> None:
        # t3-w06 C3 draw 3: the tail of the answer rendered as source.
        text = r"Therefore, \(EF = EM + MF = 7\text{ cm} + 7\text{ cm} = 14\text{ cm}."
        assert close_unclosed_math(text) == (
            r"Therefore, \(EF = EM + MF = 7\text{ cm} + 7\text{ cm} = 14\text{ cm}\)."
        )

    def test_an_unclosed_display_run_is_closed(self) -> None:
        assert close_unclosed_math(r"\[P = 6 \times 5") == r"\[P = 6 \times 5\]"

    def test_balanced_math_is_untouched(self) -> None:
        text = r"Since \(M\) is the midpoint, \(EM = MF = 7\) cm."
        assert close_unclosed_math(text) == text

    def test_two_missing_closers_are_left_for_a_reader_to_see(self) -> None:
        r"""One dropped delimiter has an unambiguous repair; two is a guess about
        which run each belonged to, and a wrong guess reads as the model's words."""
        text = r"\(a = 1 and \(b = 2"
        assert close_unclosed_math(text) == text

    def test_the_run_closes_at_its_paragraph_not_at_the_end_of_the_field(self) -> None:
        r"""A ``\(…\)`` spanning a blank line is split by markdown before arithmatex
        sees it, and neither half gets marked — the delimiters reach the reader."""
        text = "Therefore \\(EF = 14\\text{ cm}.\n\nThe next paragraph."
        assert close_unclosed_math(text) == (
            "Therefore \\(EF = 14\\text{ cm}\\).\n\nThe next paragraph."
        )


class TestDollarRunsCannotSwallowProse:
    r"""One dropped ``$`` in ``**Join $A$ to $B**.`` re-paired every ``$`` after it."""

    SLIP = (
        "5. **Join $A$ to $B**. The ray $BA$ forms a $60^{\\circ}$ angle at $B$."
        "\\n\\nWhy does this work?"
    )

    def test_the_paragraph_break_after_the_slip_still_decodes(self) -> None:
        # The mis-paired run had swallowed the literal \n\n and passed it through.
        assert "\n\nWhy does this work?" in decode_llm_json_escapes(self.SLIP)

    def test_the_commands_after_the_slip_stay_inside_their_math(self) -> None:
        assert count_bare_math(reader_ready(self.SLIP)) == 0

    def test_the_slip_itself_is_left_as_the_teacher_would_read_it(self) -> None:
        """Nothing invents the delimiter the model dropped; the damage is contained."""
        assert "**Join $A$ to $B**." in reader_ready(self.SLIP)

    def test_a_dollar_run_may_still_span_a_single_newline(self) -> None:
        text = "the value $a +\nb$ is used"
        assert count_bare_math(text) == 0

    def test_an_undecoded_newline_is_never_delimited_as_a_command(self) -> None:
        r"""``\(\nWhy\)`` would be a worse defect than the one being repaired, and the
        backslash alone cannot tell a paragraph break from a four-letter command —
        which is why :func:`reader_ready` decodes before it delimits."""
        assert reader_ready(r"One paragraph.\n\nThe next.") == "One paragraph.\n\nThe next."


class TestJsonResidue:
    @pytest.mark.parametrize(
        ("stored", "expected"),
        [
            ('32 + 4x",', "32 + 4x"),
            ('15x + 2x = 17x"', "15x + 2x = 17x"),
            ('4xy",\n          "worked_solution":', "4xy"),
        ],
    )
    def test_the_rest_of_the_object_is_cut_off(self, stored: str, expected: str) -> None:
        assert strip_json_residue(stored) == expected

    def test_a_word_the_model_quoted_on_purpose_survives(self) -> None:
        text = 'Give the answer with the unit "cm".'
        assert strip_json_residue(text) == text

    def test_it_is_idempotent(self) -> None:
        once = strip_json_residue('32 + 4x",')
        assert strip_json_residue(once) == once


class TestReaderReady:
    def test_the_close_runs_before_the_wrap(self) -> None:
        r"""Wrapping first would delimit ``\text{ cm}`` inside a run that the close
        then re-opens around it, nesting maths in maths."""
        out = reader_ready(r"Therefore \(EF = 7\text{ cm} + 7\text{ cm}.")
        assert out == r"Therefore \(EF = 7\text{ cm} + 7\text{ cm}\)."

    def test_a_field_carrying_both_defects_comes_back_clean(self) -> None:
        out = reader_ready('Area = 4 \\times side",')
        assert out == r"Area = 4 \(\times\) side"

    def test_it_is_idempotent(self) -> None:
        once = reader_ready(r"Perimeter = 4 \times side")
        assert reader_ready(once) == once

    def test_clean_text_passes_through_unchanged(self) -> None:
        text = "A square has four equal sides. Add them to get the perimeter."
        assert reader_ready(text) == text


class TestHtmlInsideReaderReady:
    def test_html_is_demoted(self) -> None:
        assert reader_ready("<p><strong>Answer:</strong> 10x</p>") == "**Answer:** 10x"

    def test_the_close_sees_the_paragraph_the_html_made(self) -> None:
        # The run is open across what the model wrote as two paragraphs. Demoted
        # first, the break is there for the close to stop at; demoted after, the
        # close would have run on to the end of the field.
        stored = r"<p>Volume is \(V = lbh.</p><p>Try one.</p>"
        assert reader_ready(stored) == "Volume is \\(V = lbh\\).\n\nTry one."

    def test_it_is_idempotent(self) -> None:
        once = reader_ready("<p>Use <b>4 \\times 5</b>.</p>")
        assert reader_ready(once) == once


def test_a_command_keeps_its_optional_argument_when_it_is_wrapped() -> None:
    r"""`\sqrt[3]{512}` is a cube root, and wrapping only the command destroys it.

    The pattern consumed `{...}` arguments and not `[...]`, so a cube root became
    `\(\sqrt\)[3]{512}` — an unparseable fragment followed by literal junk. It was the
    one expression the typesetter still refused across the judged run, and it was read
    as malformed input rather than as this bug until the sites were read one by one.
    """
    from app.domains.evaluation.application.worksheet_html.math_svg import render_latex_svg

    assert reader_ready(r"a = \sqrt[3]{512} = 8 cm") == r"a = \(\sqrt[3]{512}\) = 8 cm"
    assert "<svg " in render_latex_svg(r"\sqrt[3]{512}", display=False)

    # The ordinary forms are untouched by the widening.
    assert reader_ready(r"use \frac{22}{7}") == r"use \(\frac{22}{7}\)"
    assert reader_ready(r"Perimeter = 4 \times side") == r"Perimeter = 4 \(\times\) side"


class TestBareEnvironments:
    r"""An environment standing in prose is one piece of display maths, not a run of commands.

    Wrapped command by command it came out ``\(\begin{array}{r}\) 8\ 3 \(\end{array}\)``:
    no array, and its row break decoded to a lone backslash.
    """

    BARE = r"Divide: \begin{array}{r} 8\\ 3\enclose{longdiv}{26} \end{array} so 8."

    def test_it_is_displayed_whole(self) -> None:
        assert reader_ready(self.BARE) == (
            r"Divide: \[\begin{array}{r} 8\\ 3\enclose{longdiv}{26} \end{array}\] so 8."
        )

    def test_it_counts_as_one_piece_of_bare_maths(self) -> None:
        assert count_bare_math(self.BARE) == 1

    def test_it_is_idempotent(self) -> None:
        assert reader_ready(reader_ready(self.BARE)) == reader_ready(self.BARE)

    def test_an_environment_inside_display_maths_is_left_there(self) -> None:
        displayed = "$$\n\\require{enclose}\n\\begin{array}{r}\n8\\newline\n\\end{array}\n$$"

        assert reader_ready(displayed) == displayed


def test_a_spaced_line_break_is_not_an_unclosed_display_run() -> None:
    assert close_unclosed_math(r"\(a \\[4pt] b\)") == r"\(a \\[4pt] b\)"


def test_a_drawing_is_left_as_written_and_only_the_text_around_it_is_cleaned() -> None:
    drawing = (
        "\\begin{center}\n\\begin{tikzpicture}\n  \\draw (0,0) -- (2,0);\n"
        "  \\node at (1,0.3) {$A$};\n\\end{tikzpicture}\n\\end{center}"
    )
    text = f"The angle is \\frac{{1}}{{2}} of a turn.\n\n{drawing}\n\nSo \\angle ABC = 90^\\circ."

    ready = reader_ready(text)

    assert drawing in ready
    assert ready.count("\\(") == 0 or "\\(\\begin" not in ready
    assert reader_ready(ready) == ready
