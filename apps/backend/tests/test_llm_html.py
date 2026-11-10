r"""The HTML the model wrote, as a reader can be shown it.

Every shape here occurs in the 72 packs of ``c0c3-prism-objective``: 1,712 ``<strong>``,
844 ``<em>``, whole ``<table>``s, ``cm<sup>3</sup>``, ``<span>90°</span>``, and the
``<p>…<br>`` worked example that reached a blinded judge as literal tags.
"""

from __future__ import annotations

import pytest

from app.shared.llm_html import count_html_tags, demote_html

WORKED_EXAMPLE = (
    "<p><strong>Worked Example 1 – no brackets</strong><br> Simplify "
    "<strong>4x + 2 × 3x</strong>.</p> <p><strong>Step 1:</strong> Do the "
    "multiplication first. <strong>2 × 3x = 6x</strong>.<br> <strong>Step 2:</strong> "
    "Now add. <strong>4x + 6x = 10x</strong>.<br> <strong>Answer:</strong> 10x</p>"
)


class TestEmphasis:
    def test_bold_and_italic_become_markers(self) -> None:
        assert demote_html("<strong>Read</strong> the <em>whole</em> <b>table</b>") == (
            "**Read** the *whole* **table**"
        )

    def test_whitespace_stays_outside_the_markers(self) -> None:
        assert demote_html("say<strong> 10x </strong>now") == "say **10x** now"

    def test_nested_emphasis(self) -> None:
        assert demote_html("<strong>a <em>b</em> c</strong>") == "**a *b* c**"

    def test_an_empty_element_leaves_nothing(self) -> None:
        assert demote_html("x <b></b> y") == "x  y"


class TestBlocks:
    def test_the_worked_example_from_the_run(self) -> None:
        assert demote_html(WORKED_EXAMPLE) == (
            "**Worked Example 1 – no brackets**\n"
            "Simplify **4x + 2 × 3x**.\n\n"
            "**Step 1:** Do the multiplication first. **2 × 3x = 6x**.\n"
            "**Step 2:** Now add. **4x + 6x = 10x**.\n"
            "**Answer:** 10x"
        )

    def test_headings(self) -> None:
        assert demote_html("<h3>The cube</h3>A cube has six faces.") == (
            "### The cube\n\nA cube has six faces."
        )

    def test_an_ordered_list_with_emphasis_inside(self) -> None:
        html = (
            "<ol>\n<li><strong>Read</strong> the headings.</li>\n"
            "<li><strong>Compare</strong> the numbers.</li>\n</ol>"
        )
        assert demote_html(html) == "1. **Read** the headings.\n2. **Compare** the numbers."

    def test_a_nested_list(self) -> None:
        assert demote_html("<ul><li>a<ul><li>b</li></ul></li><li>c</li></ul>") == (
            "- a\n  - b\n- c"
        )

    def test_a_table_becomes_a_pipe_table(self) -> None:
        html = (
            "<table>\n<tr><th>Way of travelling</th><th>Number of students</th></tr>\n"
            "<tr><td>Walking</td><td>14</td></tr>\n<tr><td>Bus</td><td>6</td></tr>\n</table>"
        )
        assert demote_html(html) == (
            "| Way of travelling | Number of students |\n"
            "| --- | --- |\n"
            "| Walking | 14 |\n"
            "| Bus | 6 |"
        )


class TestScripts:
    def test_units_get_unicode_superscripts(self) -> None:
        assert demote_html("in cm<sup>3</sup> or m<sup>3</sup>") == "in cm³ or m³"

    def test_a_fraction_written_with_sup_and_sub(self) -> None:
        assert demote_html("about <sup>3</sup>/<sub>4</sub> of it") == "about ³/₄ of it"

    def test_text_with_no_glyph_falls_back_to_a_caret(self) -> None:
        assert demote_html("the 5<sup>th</sup> term") == "the 5^th term"


class TestUnwrapping:
    def test_span_center_and_underline_keep_their_text(self) -> None:
        assert demote_html("<span>90°</span> at <u>B</u>") == "90° at B"
        assert demote_html("<center>Volume = s × s × s</center>") == "Volume = s × s × s"

    def test_an_unknown_tag_keeps_its_text(self) -> None:
        assert demote_html("<font color='red'>see</font> here") == "see here"


class TestEntities:
    def test_nbsp_is_a_space(self) -> None:
        assert demote_html("4&nbsp;cm <b>x</b>") == "4 cm **x**"

    def test_an_escaped_tag_stays_escaped(self) -> None:
        assert demote_html("<b>x</b> and &lt;i&gt;") == "**x** and &lt;i&gt;"


class TestMath:
    def test_a_comparison_inside_math_is_not_a_tag(self) -> None:
        assert demote_html("$a<b$ and \\(x<y\\) and <b>ok</b>") == (
            "$a<b$ and \\(x<y\\) and **ok**"
        )

    def test_a_bare_less_than_in_prose_is_not_a_tag(self) -> None:
        assert demote_html("3 < 5 and x<5 <b>ok</b>") == "3 < 5 and x<5 **ok**"

    def test_clean_text_is_returned_as_the_same_object(self) -> None:
        text = "Perimeter = 4 × 5 cm = 20 cm, so $P < 25$."
        assert demote_html(text) is text


@pytest.mark.parametrize(
    "text",
    [
        WORKED_EXAMPLE,
        "<table><tr><th>a</th></tr><tr><td>1</td></tr></table>",
        "<ul><li>a<ul><li>b</li></ul></li></ul>",
        "cm<sup>3</sup> and <b>x</b> and &lt;i&gt; and $a<b$",
    ],
)
def test_it_is_idempotent(text: str) -> None:
    once = demote_html(text)
    assert demote_html(once) == once
    assert count_html_tags(once) == 0


def test_the_count_is_what_the_demotion_removes() -> None:
    assert count_html_tags("<p><b>x</b></p> and $a<b$ and 3 < 5") == 4


class TestMathIsNeverEntered:
    r"""The guarantee the .docx layer depends on: math runs pass through untouched.

    Practice prompts, answers and worked solutions render as OMML equations in the rater
    documents, so a conversion inside `$…$` would reach a rater as broken mathematics.
    Checked over the whole corpus in `test_no_math_run_changes_across_the_corpus`; these
    pin the shapes that would break it.
    """

    @pytest.mark.parametrize(
        "text",
        [
            r"Volume is $V = l \times b \times h$ and <b>not</b> $l + b$.",
            r"$$\frac{22}{7} \times r^2$$ then <p>a paragraph</p>",
            r"Compare $a<b$ with $b>a$ — <em>both</em> hold.",
            r"\(P = 2(l+b)\) in a <strong>rectangle</strong>",
            r"cm<sup>3</sup> beside $35\,\text{cm} \times 4\,\text{cm}^{2}$",
        ],
    )
    def test_every_math_run_survives_byte_for_byte(self, text: str) -> None:
        from app.shared.llm_text import is_math_run, split_math_runs

        math = [p for p in split_math_runs(text) if is_math_run(p)]
        assert math, "the fixture must contain math to be a test of math"
        assert [p for p in split_math_runs(demote_html(text)) if is_math_run(p)] == math

    def test_a_tag_inside_math_is_left_for_a_reader_to_see(self) -> None:
        # Not ours to repair: inside a run it is the model's mathematics, and a silent
        # rewrite there would be a worse defect than the one being fixed.
        assert demote_html(r"$a <b> c$") == r"$a <b> c$"
