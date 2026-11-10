"""The tables the sets author: forms a rater fills in, and reference tables.

Every table here carries its kind in an HTML id. pandoc turns the id into a bookmark in
front of the table; :mod:`layout` reads the bookmark to rule and shade the table, then
removes it. A table the material carries has no such bookmark and is left as it is.
"""

from __future__ import annotations

import hashlib
from html import escape

from app.domains.evaluation.domain.study_instrument import COMPARISON, Criterion

KEY_VALUE, LEARNER, RUBRIC, GRID, BOX = "kv", "learner", "rubric", "grid", "box"
GUIDE, STEPS = "guide", "steps"
#: Both materials in one row, and the row of choices that weighs them against each other.
COMPARE, LEAN = "compare", "lean"
ID_PREFIX = "hr"


def kind_of(bookmark_name: str) -> str | None:
    """The table kind a pandoc bookmark names, or None for any other bookmark."""
    prefix, _, rest = bookmark_name.partition("-")
    return rest.split("-")[0] if prefix == ID_PREFIX and rest else None


def rating_grid(criteria: tuple[Criterion, ...], columns: tuple[str, ...], tag: str) -> list[str]:
    """An empty grid: one numbered row per criterion, one score cell per column."""
    header = ["Criterion", *[f"{column} score (1–5)" for column in columns], "Comments"]
    rows = [
        [_criterion(number, criterion), *["" for _ in columns], ""]
        for number, criterion in enumerate(criteria, start=1)
    ]
    widths = ["44%", *["12%"] * len(columns), f"{56 - 12 * len(columns)}%"]
    return _table(GRID, widths, header, rows, tag)


def side_by_side(
    rows: list[tuple[list[str], list[str]]], labels: tuple[str, str], tag: str
) -> list[str]:
    """Both materials in columns, one row for each part they have in common.

    A comparative judgement only cancels a rater's own severity if both materials are in
    front of them at once. Read one after the other, the second is weighed against a
    memory of the first, which is the standard that does not hold steady. A row per part
    keeps the two explanations, the two sets of practice and the two sets of answers
    level with each other however differently the two are written.
    """
    filled = [(left, right) for left, right in rows if left or right]
    seed = "\x1f".join([tag, *(line for row in filled for side in row for line in side)])
    digest = hashlib.sha1(seed.encode()).hexdigest()[:6]
    header = "".join(f"<th>{label}</th>" for label in labels)
    lines = [
        f'<table id="{ID_PREFIX}-{COMPARE}-{digest}">'
        '<colgroup><col style="width:50%"><col style="width:50%"></colgroup>',
        f"<thead><tr>{header}</tr></thead>",
        "<tbody>",
    ]
    for left, right in filled:
        lines += ["<tr><td>", "", *left, "", "</td><td>", "", *right, "", "</td></tr>"]
    return [*lines, "</tbody></table>", ""]


#: What a rater writes in the cell they choose. Google Docs has no control a document
#: can carry — no radio button, and a box character is only a character, which has to be
#: selected exactly before it can be replaced. An empty cell is the one thing a rater can
#: already click into and type, so the answer is a word rather than a mark.
CHOSEN = "Yes"
_COMPARISON_WIDTHS = ["30%", *["9%"] * len(COMPARISON), "25%"]


def comparison_grid(criteria: tuple[Criterion, ...], tag: str) -> list[str]:
    """One row per criterion: which way the pair leans, and why.

    The criterion cell carries what "better" means for it, so a rater choosing a
    direction does not have to reconstruct the direction from the descriptors.
    """
    header = ["Criterion", *COMPARISON, "Your comment"]
    rows = [
        [
            f"**{number}. {escape(criterion.name)}**<br/>*Better: {escape(criterion.better)}*",
            *["" for _ in COMPARISON],
            "",
        ]
        for number, criterion in enumerate(criteria, start=1)
    ]
    return _table(LEAN, _COMPARISON_WIDTHS, header, rows, tag)


#: One filled row per kind of answer — towards A, neither, towards B. Showing only one
#: would teach the mechanics and suggest an answer at the same time; three balance out.
_EXAMPLE_ROWS: tuple[tuple[str, int, str], ...] = (
    (
        "Example — a criterion where A was the stronger of the two",
        1,
        "B repeats what the student can already do.",
    ),
    (
        "Example — a criterion where neither was ahead",
        2,
        "Both are accurate and both stay on the objective.",
    ),
    ("Example — a criterion where B was clearly the stronger", 4, ""),
)


def comparison_example() -> list[str]:
    """A filled-in grid, so a rater sees what an answered row looks like before meeting one.

    Its first heading is not "Criterion". The grids a rater answers are found by that
    word when the marks are read back, and an example that reads as an answered row
    would be counted as three comparisons nobody made.
    """
    header = ["Example criterion", *COMPARISON, "Your comment"]
    rows = [
        [
            f"*{escape(label)}*",
            *[CHOSEN if column == chosen else "" for column in range(len(COMPARISON))],
            escape(comment),
        ]
        for label, chosen, comment in _EXAMPLE_ROWS
    ]
    return _table(LEAN, _COMPARISON_WIDTHS, header, rows, "example")


def comparison_body(
    criteria: tuple[Criterion, ...], *, tag: str, objective: str, subject: str
) -> list[str]:
    """One objective's scoring page under the comparative instrument."""
    return [
        *guide(
            f"Write {CHOSEN} in one box on each row, and nothing in the other four. Both "
            "materials can be good — “about the same” is a real answer, not a failure to decide."
        ),
        f"**What you are comparing.** {subject}",
        "",
        f"**Learning objective.** {objective}",
        "",
        *comparison_grid(criteria, tag),
        "**What each criterion asks.**",
        "",
        *(f"{_criterion(number, criterion)}  " for number, criterion in enumerate(criteria, 1)),
        "",
    ]


def criteria_reference(criteria: tuple[Criterion, ...]) -> list[str]:
    """Each criterion, what it asks, and which way is up."""
    rows = [
        [
            f"**{number}. {escape(criterion.name)}**",
            escape(criterion.question),
            escape(criterion.better),
        ]
        for number, criterion in enumerate(criteria, start=1)
    ]
    header = ["Criterion", "What it asks", "Better means"]
    return _table(RUBRIC, ["26%", "44%", "30%"], header, rows)


def scoring_body(
    criteria: tuple[Criterion, ...],
    columns: tuple[str, ...],
    *,
    tag: str,
    objective: str,
    subject: str,
    instruction: str,
) -> list[str]:
    """One objective's scoring page: what is being rated, the grid, and what each score means.

    The criteria ask about "this section", so the page says which section that is. The
    instrument is repeated here rather than referred to: a rater choosing a number should
    not have to turn back to the instructions to recall what the number means.
    """
    return [
        *guide(instruction),
        f"**What you are scoring.** {subject}",
        "",
        f"**Learning objective.** {objective}",
        "",
        *rating_grid(criteria, columns, tag),
        "**What each score means.**",
        "",
        *rubric_matrix(criteria, with_questions=False),
    ]


def rubric_matrix(criteria: tuple[Criterion, ...], *, with_questions: bool = True) -> list[str]:
    """The whole instrument on one page: a row per score, a column per criterion.

    Beside a grid that already asks each criterion's question, the columns carry the
    criterion names alone: the same question twice on one page reads as two questions.
    """
    header = [
        "Score",
        *[
            _criterion(n, c) if with_questions else f"**{n}. {escape(c.name)}**"
            for n, c in enumerate(criteria, start=1)
        ],
    ]
    rows = [
        [f"**{score}**", *[escape(c.descriptors[score - 1]) for c in criteria]]
        for score in range(1, 6)
    ]
    widths = ["9%", *[f"{91 // len(criteria)}%"] * len(criteria)]
    return _table(RUBRIC, widths, header, rows)


def guide(text: str) -> list[str]:
    """One line saying what to do on this page, where the doing happens."""
    return _table(GUIDE, ["100%"], None, [[f"**{escape(text)}**"]])


def step_table(rows: list[tuple[str, str, str]]) -> list[str]:
    """The lesson in order: each step, what it covered, and the objective it served."""
    return _table(
        STEPS,
        ["14%", "44%", "42%"],
        ["Step", "What it covered", "For"],
        [[escape(cell) for cell in row] for row in rows],
    )


def closing_comments(
    expected: str, *, given: str = "Your scores are on the scoring pages"
) -> list[str]:
    """The last page. Answers stay where they were given; nothing is copied here."""
    return [
        f"{given}, one for each objective. Nothing is copied here.",
        "",
        f"**Before you finish.** {expected}",
        "",
        "Any general comments on this set are welcome below, and are optional.",
        "",
        *comments_box(),
    ]


def comments_box() -> list[str]:
    return _table(BOX, ["100%"], ["Your comments on this set (optional)"], [["&nbsp;"]])


def key_value_table(rows: list[tuple[str, str | list[str]]]) -> list[str]:
    """A label column and a value column, no header row; the renderer shades the labels."""
    return _table(KEY_VALUE, ["24%", "76%"], None, [[escape(k), _value(v)] for k, v in rows])


def objectives_table(objectives: list[str]) -> list[str]:
    rows = [[f"Objective {i}", escape(text)] for i, text in enumerate(objectives, start=1)]
    return _table(KEY_VALUE, ["24%", "76%"], None, rows)


def class_work_table(rows: list[tuple[str, str, str]]) -> list[str]:
    header = ["Objective", "Result on the marked class work", "What the class work showed"]
    body = [[escape(cell) for cell in row] for row in rows]
    return _table(LEARNER, ["28%", "22%", "50%"], header, body)


def marked_question(
    number: int,
    *,
    question: str,
    wrote: str,
    expected: str | None,
    result: str,
    interpretation: str | None,
) -> list[str]:
    """One marked class work question: what was asked, what the student did, how it went.

    A table rather than a run of prose. The four things a rater weighs are the same four
    every time, and set against their own labels they can be found without reading.
    Values are not escaped: they are reader-ready mathematics and carry their own TeX.
    """
    rows = [
        (f"Question {number}", question),
        ("The student wrote", wrote or "*(no working captured)*"),
    ]
    if expected:
        rows.append(("Expected answer", expected))
    rows.append(("Result", f"**{result}**"))
    if interpretation:
        rows.append(("Interpretation", interpretation))
    return _table(KEY_VALUE, ["24%", "76%"], None, [[escape(label), v] for label, v in rows])


def _criterion(number: int, criterion: Criterion) -> str:
    return f"**{number}. {escape(criterion.name)}** — *{escape(criterion.question)}*"


def _value(value: str | list[str]) -> str:
    if isinstance(value, list):
        items = "".join(f"<li>{escape(item)}</li>" for item in value)
        return f"<ul>{items}</ul>" if value else "—"
    return escape(value)


def _table(
    kind: str,
    widths: list[str],
    header: list[str] | None,
    rows: list[list[str]],
    tag: str = "",
) -> list[str]:
    content = "\x1f".join([tag, *(cell for row in rows for cell in row)])
    digest = hashlib.sha1(content.encode()).hexdigest()[:6]
    columns = "".join(f'<col style="width:{width}">' for width in widths)
    lines = [f'<table id="{ID_PREFIX}-{kind}-{digest}"><colgroup>{columns}</colgroup>']
    if header:
        lines.append(
            "<thead><tr>" + "".join(f"<th>{cell}</th>" for cell in header) + "</tr></thead>"
        )
    lines.append("<tbody>")
    lines += ["<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows]
    lines += ["</tbody></table>", ""]
    return lines
