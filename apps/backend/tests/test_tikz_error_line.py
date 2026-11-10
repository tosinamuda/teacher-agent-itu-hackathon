"""What a writer is told when its drawing does not compile."""

import pytest

from app.shared.tikz_svg import first_error, tikz_available, tikz_problem

LOG = [
    "This is pdfTeX",
    r"./drawing.tex:3: LaTeX Error: There's no line here to end.",
    "",
    "See the LaTeX manual or LaTeX Companion for explanation.",
    "Type  H <return>  for immediate help.",
    r"l.3 \draw (1,1) -- (2,2) node {A \\",
    "                                    B};",
    "! Emergency stop.",
]


def test_the_error_is_given_with_its_line_in_the_drawing_and_the_text_read() -> None:
    assert first_error(LOG) == (
        r"LaTeX Error: There's no line here to end. "
        r"(line 3 of the drawing: \draw (1,1) -- (2,2) node {A \\)"
    )


def test_an_error_in_the_wrapper_is_given_by_its_message() -> None:
    assert first_error(["! LaTeX Error: File `x.sty' not found."]) == (
        "LaTeX Error: File `x.sty' not found."
    )


def test_a_log_with_no_error_says_tex_refused_it() -> None:
    assert first_error(["fine"]) == "TeX refused it"


def test_a_drawing_with_doubled_backslashes_is_told_to_write_one() -> None:
    doubled = "\\\\begin{tikzpicture}\n\\\\draw (0,0) -- (1,0);\n\\\\end{tikzpicture}"

    assert tikz_problem(doubled) == (
        r"the drawing has two backslashes before a command: write one, as in \begin and \draw"
    )


@pytest.mark.skipif(not tikz_available(), reason="TeX is not installed")
def test_a_real_broken_drawing_is_placed_on_its_own_line() -> None:
    source = "\n".join(
        (
            r"\begin{tikzpicture}",
            r"\draw (0,0) -- (1,1);",
            r"\draw (1,1) -- (2,2) \\",
            r"\end{tikzpicture}",
        )
    )

    assert "line 3 of the drawing" in str(tikz_problem(source))


@pytest.mark.skipif(not tikz_available(), reason="TeX is not installed")
def test_a_good_drawing_has_no_problem() -> None:
    assert tikz_problem(r"\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}") is None
