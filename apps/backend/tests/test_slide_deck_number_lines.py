"""A number line on a slide places each mark where its value belongs."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.number_lines import (
    marks_of,
    number_line_issues,
)
from tests.slide_deck_support import deck, slide


def _line(marks: str) -> str:
    return (
        "\\begin{tikzpicture}\\draw[thick] (0,0) -- (10,0);"
        f"\\foreach \\x/\\label in {{{marks}}} {{\\draw (\\x,0.15) -- (\\x,-0.15);}}"
        "\\end{tikzpicture}"
    )


def _drawn(marks: str) -> dict[str, object]:
    return {**slide("A number line", title="Rounding"), "figure": _line(marks)}


def test_the_marks_of_a_foreach_list_are_read_as_value_to_position() -> None:
    assert marks_of(_line("0/6, 10/7")) == {6.0: 0.0, 7.0: 10.0}
    assert marks_of("\\draw (0,0) -- (1,0);") == {}


def test_marks_spaced_by_their_values_with_the_whole_numbers_around_a_decimal_pass() -> None:
    draft = deck(core=[_drawn("0/6, 9/6.9, 10/7")])

    assert number_line_issues(draft) == []


def test_a_mark_out_of_place_is_told_where_it_belongs() -> None:
    issues = number_line_issues(deck(core=[_drawn("0/6, 2/6.9, 10/7")]))

    assert issues == ["core: slide 1: the mark 6.9 is at x=2 and belongs at x=9.00"]


def test_a_decimal_without_the_whole_numbers_around_it_is_sent_back() -> None:
    issues = number_line_issues(deck(core=[_drawn("2/6.9, 7/7")]))

    assert len(issues) == 1
    assert "6.9 lies between 6 and 7: mark both" in issues[0]
    assert issues[0].endswith("{0/6, 9/6.9, 10/7}")


def test_whole_number_marks_and_slides_without_a_line_are_not_checked() -> None:
    draft = deck(core=[_drawn("0/7000, 5/7500, 10/8000"), slide("No picture")])

    assert number_line_issues(draft) == []


def test_labels_that_carry_their_unit_are_read_and_checked_too() -> None:
    marks = "6.9/6.9\\,km, 7/7\\,km"

    assert marks_of(_line(marks)) == {6.9: 6.9, 7.0: 7.0}
    assert "6.9 lies between 6 and 7" in number_line_issues(deck(core=[_drawn(marks)]))[0]


def _hand_drawn(*nodes: str) -> str:
    return "\\begin{tikzpicture}\\draw[<->] (0,0) -- (6,0);" + "".join(nodes) + "\\end{tikzpicture}"


def test_a_line_drawn_by_hand_is_checked_where_its_labels_stand() -> None:
    figure = _hand_drawn(
        "\\node at (0,-0.4) {\\Huge 6 km};",
        "\\node at (6,-0.4) {\\Huge 7 km};",
        "\\draw[blue] (3,0.2) -- (3,-0.2) node[below] {\\Huge 6.9 km};",
    )

    issues = number_line_issues(deck(core=[{**slide("A line"), "figure": figure}]))

    assert issues == ["core: slide 1: the mark 6.9 is at x=3 and belongs at x=5.40"]


def test_a_number_line_that_marks_only_the_decimal_is_sent_back() -> None:
    figure = (
        "\\begin{tikzpicture}\\draw[thick] (0,0) -- (10,0);"
        "\\node[above=4pt] at (8.75,0) {\\Huge 6.875};\\end{tikzpicture}"
    )

    issues = number_line_issues(deck(core=[{**slide("A line"), "figure": figure}]))

    assert len(issues) == 1 and "6.875 lies between 6 and 7: mark both" in issues[0]


def test_a_shape_with_decimal_side_labels_is_not_a_number_line() -> None:
    triangle = (
        "\\begin{tikzpicture}\\draw (0,0) -- (4,0) -- (0,3) -- cycle;"
        "\\node at (2,-0.3) {4.5 cm};\\end{tikzpicture}"
    )

    assert number_line_issues(deck(core=[{**slide("A shape"), "figure": triangle}])) == []


def test_marks_so_close_that_their_labels_overlap_are_told_to_stand_them_apart() -> None:
    issues = number_line_issues(deck(core=[_drawn("6/6, 6.9/6.9, 7/7")]))

    assert issues == [
        "core: slide 1: the labels of the marks run together; write the label of the number you "
        "mark above the line and the labels of the whole numbers below it. Do not lengthen the "
        "line: a longer line makes every label smaller"
    ]


def test_wide_labels_run_together_where_short_ones_do_not() -> None:
    wide = number_line_issues(deck(core=[_drawn("0/6000, 9/6900, 10/7000")]))
    short = number_line_issues(deck(core=[_drawn("0/6, 9/6.9, 10/7")]))

    assert short == []
    assert len(wide) == 1 and "run together" in wide[0]


def test_a_line_longer_than_the_slide_keeps_its_labels_large_is_sent_back() -> None:
    long = (
        "\\begin{tikzpicture}\\draw (0,0) -- (17,0);"
        "\\node[below=4pt] at (0,0) {\\Huge 6};\\node[below=4pt] at (17,0) {\\Huge 7};"
        "\\end{tikzpicture}"
    )

    issues = number_line_issues(deck(core=[{**slide("A line"), "figure": long}]))

    assert len(issues) == 1 and "the line is 17 long" in issues[0]


def _labelled(size: str) -> str:
    return (
        "\\begin{tikzpicture}\\draw (0,0) -- (10,0);"
        f"\\node[below=4pt] at (0,0) {{{size} 6}};\\node[below=4pt] at (10,0) {{{size} 7}};"
        "\\end{tikzpicture}"
    )


def test_labels_too_small_to_read_from_the_back_are_sent_back() -> None:
    small = {**slide("A line"), "figure": _labelled("\\large")}
    big = {**slide("A line"), "figure": _labelled("\\Huge")}

    issues = number_line_issues(deck(core=[small]))

    assert len(issues) == 1 and "too small to read from the back" in issues[0]
    assert number_line_issues(deck(core=[big])) == []


def test_bigger_labels_need_more_room_between_marks() -> None:
    marks = "0/6, 9/6.9, 10/7"
    huge = _line(marks).replace("\\foreach", "\\node at (0,0) {\\Huge 6};\\foreach")

    assert number_line_issues(deck(core=[_drawn(marks)])) == []
    assert "run together" in " ".join(
        number_line_issues(deck(core=[{**slide("A"), "figure": huge}]))
    )


def _placed(*labels: str) -> dict[str, object]:
    figure = "\\begin{tikzpicture}\\draw (0,0) -- (10,0);" + "".join(labels) + "\\end{tikzpicture}"
    return {**slide("A line"), "figure": figure}


def test_labels_set_by_separate_nodes_on_one_side_run_together_when_they_stand_close() -> None:
    six, seven = "\\node[below=4pt] at (0,0) {\\Huge 6};", "\\node[below=4pt] at (10,0) {\\Huge 7};"
    same_side = _placed(six, seven, "\\node[below=4pt] at (9,0) {\\Huge 6.9};")
    other_side = _placed(six, seven, "\\node[above=4pt] at (9,0) {\\Huge 6.9};")

    assert "run together" in " ".join(number_line_issues(deck(core=[same_side])))
    assert number_line_issues(deck(core=[other_side])) == []
