"""The human rating study's evaluation sets: the instrument, the allocation, the blind.

Three things a set must be. Faithful to the protocol — three criteria per part, five
descriptors each. Allocated as the workbooks say — every rater's counts equal the
workbook's own Checks sheet, in its delivery order. And blind — nothing a rater reads
names a condition, a draw, a learner, a lesson code or a run.
"""

from __future__ import annotations

import re
import shutil
import zipfile
from collections import Counter
from pathlib import Path

import pytest

from app.config import CONFIG
from app.domains.evaluation.domain.study_instrument import COMPARISON, H1_CRITERIA, H2_CRITERIA
from experiments.human_rating import (
    export,
    forms,
    h1_document,
    inspect,
    layout,
    mapping,
    material,
    mixed_model,
    panels,
    provenance,
    render,
    results,
    sources,
)
from experiments.human_rating.instructions import general_instructions_markdown

#: The personalisation runs are in the repository; the learner evidence they are read
#: against is not, so anything that needs a whole set still skips off this machine.
H2_RUNS = sources.H2_RUNS
H2_RUN = "h2-deepseek-clean"


def test_part_2_speaks_of_the_student_while_the_constructs_keep_their_names():
    """The pages call it the student's class work, so the criteria a rater reads do too."""
    rater_facing = " ".join(
        " ".join([c.name, c.question, *c.descriptors, *c.notes]) for c in H2_CRITERIA
    )
    assert "learner" not in rater_facing.lower()
    # Nothing we write into a Part 2 page says it either, including the anonymiser.
    assert "learner" not in sources._for_rater("as on `student-01`, and student-04").lower()
    assert "student" in rater_facing.lower()
    # The research-facing names stay the protocol's, so no analysis key moves.
    assert [c.id for c in H2_CRITERIA] == [
        "learner_evidence_alignment",
        "adaptive_calibration",
        "instructional_integrity",
    ]
    assert H2_CRITERIA[0].construct == "Learner-evidence alignment"


def test_the_instrument_is_three_by_five_and_says_nothing_it_must_not():
    for criteria in (H1_CRITERIA, H2_CRITERIA):
        assert len(criteria) == 3
        assert len({c.id for c in criteria}) == 3
        for criterion in criteria:
            assert len(criterion.descriptors) == 5
            assert not any("|" in d for d in criterion.descriptors), "a bar splits a matrix cell"
            render.leak_scan(
                "\n".join(
                    [criterion.name, criterion.question, *criterion.descriptors, *criterion.notes]
                )
            )
    for number in (1, 2, 3):
        render.leak_scan(general_instructions_markdown(number))


def test_h1_allocation_matches_the_workbooks_own_checks():
    rows = mapping.load_h1()
    checks = mapping.expected_checks(mapping.H1_WORKBOOK)
    assert len(rows) == 144 and len(mapping.RATERS) == 4
    for rater in mapping.RATERS:
        mine = [r for r in rows if r.rater == rater]
        assert len(mine) == int(checks["printed rows"][rater]) == 36
        assert Counter(r.condition for r in mine) == {"C0": 9, "C1": 9, "C2": 9, "C3": 9}
        assert Counter(r.version for r in mine) == {1: 12, 2: 12, 3: 12}
        assert [r.order for r in mine] == list(range(1, 37)), "the sheet order is delivery order"
    base = Counter(re.sub(r"-c\d$", "", r.internal_id) for r in rows)
    assert len(base) == 72 and set(base.values()) == {2}
    for internal in base:
        assert len({r.rater for r in rows if r.internal_id.startswith(internal)}) == 2


def test_h2_allocation_is_paired_counterbalanced_and_complete():
    rows = mapping.load_h2()
    checks = mapping.expected_checks(mapping.H2_WORKBOOK)
    assert len(rows) == 52
    for rater in mapping.RATERS:
        mine = [r for r in rows if r.rater == rater]
        assert len(mine) == int(checks["printed rows"][rater]) == 13
        assert all({r.a, r.b} == {"P0", "P1"} for r in mine)
        assert all(x.a != y.a for x, y in zip(mine, mine[1:], strict=False)), "A/B must alternate"
        assert all(x.lesson != y.lesson for x, y in zip(mine, mine[1:], strict=False))
        assert all(x.student != y.student for x, y in zip(mine, mine[1:], strict=False))
    cases = Counter(re.sub(r"-c\d$", "", r.internal_id) for r in rows)
    assert len(cases) == 26 and set(cases.values()) == {2}
    assert sum(1 for r in rows if r.a == "P0") == 26, "P0 leads in half the pairs"
    for r in rows:
        assert r.learner_card_id == f"{r.external_id}-lm"
        assert {r.a_id, r.b_id} == {f"{r.external_id}-a", f"{r.external_id}-b"}


def test_an_h1_set_reads_and_scores_each_objective_and_says_nothing_identifying():
    run = sources.H1Run("c0c3-prism-objective")
    plans = sources.plans()
    assignment = mapping.load_h1()[0]
    plan = plans[assignment.lesson]
    text = h1_document.markdown(
        assignment,
        plan,
        run.pack(assignment.lesson, assignment.condition, assignment.version),
    )
    render.leak_scan(text)
    objectives = plan["lesson_plan_objectives"]
    assert text.count("— what the teacher taught") == len(objectives)
    assert text.count("— the revision material") == len(objectives)
    assert text.count("— your scores") == len(objectives)
    assert text.count("**What you are scoring.**") == len(objectives)
    assert f"Evaluation Set {assignment.external_id}" in text
    assert assignment.internal_id not in text
    marks = [
        CONFIG.institution_name.upper(),
        "### Lesson reference",
        "### Lesson objectives",
        "## Instructions",
        "## The lesson",
        "**The lesson in order.**",
        "## Objective 1 of ",
        "**Topic.**",
        "## Closing comments",
    ]
    assert [text.index(m) for m in marks] == sorted(text.index(m) for m in marks)
    # instructions, the lesson, three pages an objective, closing comments
    breaks = 1 + 1 + 3 * len(objectives) + 1
    assert text.count(layout.PAGE_BREAK) == breaks, "a page each for taught, material, scores"
    closing = text[text.index("## Closing comments") :]
    assert f"{len(objectives) * 3} scores in all" in closing
    assert "Learning objective" not in closing, "nothing is copied to the last page"


def test_a_rendered_document_keeps_structure_breaks_pages_and_carries_its_footer(
    tmp_path: Path,
):
    path = tmp_path / "set.docx"
    markdown = "\n".join(
        [
            "**UNIVERSITY**",
            "",
            CONFIG.study_title,
            "",
            layout.RULE,
            "",
            "# Evaluation Set h1-pkt-000",
            "",
            "A line with $x^2$ and cm<sup>3</sup>.",
            "",
            "1. (a) Define statistic",
            "",
            *forms.key_value_table([("Subject", "Mathematics"), ("Curriculum target", ["a", "b"])]),
            "<table><tr><th>Shape</th><th>Sides</th></tr><tr><td>Triangle</td><td>3</td></tr>"
            "</table>",
            "",
            layout.PAGE_BREAK,
            "",
            *layout.titled_page("Closing comments"),
            "**A label the renderer must not confuse with a form.**",
            "",
            *forms.scoring_body(
                H1_CRITERIA,
                ("Your",),
                tag="1",
                objective="an objective",
                subject="The revision material's section for this objective.",
                instruction="Score this objective only.",
            ),
            *forms.comments_box(),
        ]
    )
    render.to_docx(markdown, path, rater_number=2, set_id="Evaluation Set h1-pkt-000")
    text = render.docx_text(path)
    assert "Rater 2 | Evaluation Set h1-pkt-000" in text and "Page" in text
    assert layout.PAGE_BREAK not in text and layout.RULE not in text
    archive = zipfile.ZipFile(path)
    xml = archive.read("word/document.xml").decode()
    assert 'w:w="11906"' in xml, "A4"
    assert layout.FONT in archive.read("word/styles.xml").decode()
    assert xml.count("<w:tbl>") == 6, "reference, the material's own, guide, grid, rubric, box"
    assert xml.count("<w:tblBorders>") == 5, "every authored table is ruled, the material's is not"
    assert xml.count(f'w:fill="{layout.FILL}"') == 2 + 1 + 3 + 4 + 1, "keys, guide, header rows"
    assert "<w:pBdr>" in xml, "the band rule"
    assert "<w:tab/>" in archive.read("word/footer1.xml").decode()
    assert xml.count("<m:oMath>") == 1
    assert 'w:val="superscript"' in xml
    assert xml.count("<w:pageBreakBefore") == 1
    assert "<w:trHeight" in xml
    assert "bookmarkStart" not in xml, "Google Docs renders every pandoc bookmark as a flag"
    assert xml.count("<w:numPr>") == 1 + 2, "one list item, plus the reference table's two"
    assert "(a) Define statistic" in text, "no nested list"
    assert "hr-" not in xml and "**" not in text, "table markers read, then removed"
    assert "<w:b/>" in xml, "emphasis inside an authored table's cells"
    assert xml.count("<w:cantSplit/>") == 4 + 2 + 2, (
        "form rows never split across pages: the grid, the box, and the key-value rows "
        "that carry a student's working"
    )


def test_the_leak_scan_refuses_every_class_of_identifier(tmp_path: Path):
    for bad in (
        "condition C1 here",
        "student-04 wrote",
        "lesson t3-w06",
        "h1-l02-c3-v1-c1",
        "cand-0a619616",
        "run c0c3-native",
    ):
        with pytest.raises(render.LeakError):
            render.leak_scan(bad)
    render.leak_scan("Part 1 — Class revision material · Rater 1 · Evaluation Set h1-pkt-027")


@pytest.mark.skipif(
    not inspect.SOFFICE.exists() or not shutil.which("pdftotext"),
    reason="LibreOffice and poppler are developer tools",
)
def test_a_set_reads_as_pages_a_rater_can_follow(tmp_path: Path):
    """The structure lives on the page, so it is checked on the page."""
    run = sources.H1Run("c0c3-prism-objective")
    plans = sources.plans()
    assignment = mapping.load_h1()[0]
    plan = plans[assignment.lesson]
    document = tmp_path / "Rater-1" / "Part 1" / "R1-P1-01 h1-pkt-000.docx"
    render.to_docx(
        h1_document.markdown(
            assignment, plan, run.pack(assignment.lesson, assignment.condition, assignment.version)
        ),
        document,
        rater_number=1,
        set_id="Evaluation Set h1-pkt-000",
    )
    (pdf,) = inspect.to_pdfs([document], tmp_path / "pdf")
    assert inspect.problems(pdf) == []
    sheets = inspect.pages(pdf)
    scoring = [s for s in sheets if inspect.SCORING in s]
    assert len(scoring) == len(plan["lesson_plan_objectives"])
    assert all("What each score means" in sheet for sheet in scoring)


@pytest.mark.skipif(
    not (H2_RUNS / H2_RUN / "run.json").exists(), reason="learner data is machine-local"
)
def test_an_h2_set_rates_only_objectives_with_evidence_and_hides_the_learner():
    from experiments.human_rating import h2_document

    run = sources.H2Run(H2_RUN, H2_RUNS)
    plans = sources.plans()
    rows = mapping.load_h2()
    panels: Counter[str] = Counter()
    per_case: dict[str, set[int]] = {}
    for assignment in rows:
        evidence = sources.learner_evidence(assignment.lesson, assignment.student)
        panels[assignment.rater] += len(evidence)
        case = re.sub(r"-c\d$", "", assignment.internal_id)
        per_case.setdefault(case, set()).add(len(evidence))
        if assignment.order == 1:
            text = h2_document.markdown(
                assignment,
                plans[assignment.lesson],
                run.materials(assignment.lesson, assignment.student),
                evidence,
            )
            render.leak_scan(text)
            assert text.count("— your scores") == len(evidence)
            breaks = 1 + 1 + 5 * len(evidence) + 2 + 1
            assert text.count(layout.PAGE_BREAK) == breaks
            assert "### The student's class work, objective by objective" in text
            assert "— the student's class work" in text
            # The protocol's own descriptors say "learner"; only our own labels changed.
            for retired in (
                "Learner evidence for this objective",
                "Per-objective learner evidence",
                "Classwork question",
            ):
                assert retired not in text
            assert assignment.student not in text
    assert all(len(counts) == 1 for counts in per_case.values()), "a case's two copies differ"
    assert sum(panels.values()) == 2 * sum(next(iter(c)) for c in per_case.values())


def test_a_comparison_cell_opens_bold_so_the_table_keeps_its_page():
    """A Word heading keeps itself with the block after it.

    In a cell taller than the space left on the page, that pair takes the whole table to
    the next page and leaves the page it was on empty. Measured: a heading at the top of
    the cell moved the table every time, and bold text never did.
    """
    section = {"title": "Perimeter", "blocks": [{"text": "Add the sides."}], "practice": []}
    explanation, practice, answers = material.parts(section)
    assert explanation[0] == "**Perimeter**"
    assert not explanation[0].startswith("#")
    assert practice == [] and answers == []
    assert material.prose(section, level=4)[0].startswith("#### ")


def test_a_comparison_sets_the_two_materials_row_for_row():
    """Each part faces its own counterpart, whatever length the other side runs to."""
    rows = [(["left one"], ["right one"]), ([], ["right only"]), (["left only"], [])]
    table = "\n".join(forms.side_by_side(rows, ("Material A", "Material B"), tag="1"))
    assert table.count("<tr><td>") == 3
    assert forms.kind_of(re.search(r'id="([^"]+)"', table).group(1)) == forms.COMPARE
    empty = "\n".join(forms.side_by_side([([], [])], ("Material A", "Material B"), tag="1"))
    assert "<tr><td>" not in empty


@pytest.mark.skipif(
    not (H2_RUNS / H2_RUN / "run.json").exists(), reason="learner data is machine-local"
)
def test_a_comparative_set_pairs_the_materials_and_turns_the_page_sideways():
    from experiments.human_rating import h2_comparative

    run = sources.H2Run(H2_RUN, H2_RUNS)
    plans = sources.plans()
    assignment = next(a for a in mapping.load_h2() if a.order == 1)
    evidence = sources.learner_evidence(assignment.lesson, assignment.student)
    text = h2_comparative.markdown(
        assignment,
        plans[assignment.lesson],
        run.materials(assignment.lesson, assignment.student),
        evidence,
    )
    render.leak_scan(text)
    assert text.count("— the two materials") == len(evidence)
    assert text.count("— your comparison") == len(evidence)
    # Every objective turns the page sideways once and turns it back once, and the last
    # one is turned back before the complete materials.
    assert text.count(layout.SHAPE[layout.LANDSCAPE]) == len(evidence)
    assert text.count(layout.SHAPE[layout.PORTRAIT]) == len(evidence)
    shapes = re.findall(r"\[\[\[(landscape|portrait)\]\]\]", text)
    assert shapes == ["landscape", "portrait"] * len(evidence)
    # Nothing asks for a score out of five any more.
    assert "score (1–5)" not in text


def test_only_the_grid_a_rater_answers_carries_both_marks_of_one():
    """Two headings tell an answer sheet from its neighbours, and it takes both.

    A page carries three tables that begin with "Criterion" and two that carry the
    comparison columns. The answer sheet is the only one with both. Each test alone has
    already let something through: keying on the first cell counted the criteria
    reference, keying on the columns counted the worked example — as three comparisons
    nobody made, on every set.
    """
    first, columns = "<th>Criterion</th>", f"<th>{COMPARISON[0]}</th>"
    answered = "\n".join(forms.comparison_grid(H2_CRITERIA, tag="1"))
    example = "\n".join(forms.comparison_example())
    catalogue = "\n".join(forms.criteria_reference(H2_CRITERIA))
    assert first in answered and columns in answered, "the answer sheet carries both"
    for other, name in ((example, "the worked example"), (catalogue, "the criteria reference")):
        assert not (first in other and columns in other), f"{name} reads as an answer sheet"
    # Each heading alone still matches one of them, which is why both are required.
    assert columns in example and first in catalogue
    assert forms.CHOSEN in example and forms.CHOSEN not in answered


def test_a_row_a_rater_added_is_not_a_missing_rating(tmp_path: Path):
    """Google Docs adds a table row when Tab is pressed in the last cell.

    One such row exists in the delivered Part 1 documents. Counted as a criterion, it
    reports a rating absent that the instrument never asked for — which is how a
    coverage total came to disagree with the design by one.
    """
    grid = forms.rating_grid(H1_CRITERIA, ("Your",), tag="1")
    filled = [line.replace("<td></td>", "<td>4</td>", 1) for line in grid]
    stray = "<tr><td></td><td></td><td></td></tr>"
    markdown = "\n".join([*filled[:-2], stray, *filled[-2:]])
    path = tmp_path / "set.docx"
    render.to_docx(markdown, path, rater_number=1, set_id="Evaluation Set h1-pkt-000")
    marks, sheets, unanswered = results.answers(path)
    assert sheets == 1
    assert len(marks) == len(H1_CRITERIA), "every criterion row is read"
    assert unanswered == 0, "the blank row a rater created is not a missing rating"


def test_a_teachers_mark_is_read_as_a_share_not_a_total():
    """The three papers are out of four, eight and six, so totals do not compare.

    Ranking on a sum would put whoever sat the eight-mark paper best at the top of the
    class regardless of the other two.
    """
    assert results._share("6/8") == 0.75
    assert results._share("1/4") == 0.25
    assert results._share(None) is None and results._share("") is None
    assert results._share("no mark recorded") is None


@pytest.mark.skipif(
    not (H2_RUNS / H2_RUN / "run.json").exists(), reason="learner data is machine-local"
)
def test_the_nine_are_split_into_three_ability_thirds():
    """The sample was drawn from three ability categories; the categories were not kept.

    They are recovered from the teacher's own totals so the grouping comes from the
    record. Every student sat at least two of the three papers, so no third rests on one.
    """
    rows = results.students()
    assert len(rows) == 9
    assert Counter(r["ability_stratum"] for r in rows) == {"top": 3, "middle": 3, "lower": 3}
    shares = [r["mean_share_correct"] for r in rows]
    assert shares == sorted(shares, reverse=True), "ranked best first"
    assert min(shares) < 0.5 < max(shares), "the sample spans the ability range"
    assert all(r["lessons_sat"] >= 2 for r in rows)


#: The committed snapshot as the raters returned it: the full assignment roster, with every
#: mark they made and every cell they left blank.
DELIVERED = Path(__file__).resolve().parents[1] / "experiments" / "human_rating" / "delivered"


def test_a_comparative_response_is_the_column_not_the_tick_the_rater_typed():
    """The rater writes only "Yes"; the answer is which column carries it.

    Reading the typed mark as the response loses the whole scale — every row scores
    alike, or not at all. The export did exactly that until the CSV came back with an
    empty score on every answered row.
    """
    assert export._score("B clearly better", "P0", "P1") == ("P1", 2)
    assert export._score("B clearly better", "P1", "P0") == ("P0", -2)
    assert export._score("A slightly better", "P0", "P1") == ("P0", -1)
    assert export._score("A slightly better", "P1", "P0") == ("P1", 1)
    assert export._score("About the same", "P0", "P1") == ("neither", 0)


def test_the_export_carries_every_assigned_cell_and_scores_no_silence_as_a_tie():
    """Zero is a rater calling the two equal. A cell nobody answered is not a zero."""
    rows = export.ratings_long(DELIVERED, sources.plans())
    assert len(rows) == 210, "the roster is 70 objective panels by three criteria"
    blank = [r for r in rows if r["response_status"] == "blank"]
    answered = [r for r in rows if r["response_status"] == "answered"]
    assert (len(answered), len(blank)) == (199, 11), "the cells the panel returned"
    assert all(r["score_used"] == "" and r["response_raw"] == "" for r in blank)
    assert all(r["score_used"] != "" and r["response_raw"] != "" for r in answered)


def test_both_copies_of_a_case_share_a_panel_id_though_they_swap_a_and_b():
    """The join key has to survive the blinding, or two ratings look like two targets.

    Keying on the packet id instead once made a fully doubly-rated design read as having
    no overlap at all.
    """
    rows = export.ratings_long(DELIVERED, sources.plans())
    raters, sides, packets = {}, {}, {}
    for row in rows:
        raters.setdefault(row["panel_id"], set()).add(row["rater_id"])
        sides.setdefault(row["panel_id"], set()).add((row["condition_a"], row["condition_b"]))
        packets.setdefault(row["panel_id"], set()).add(row["external_packet_id"])
    assert raters and all(len(v) == 2 for v in raters.values())
    assert all(v == {("P0", "P1"), ("P1", "P0")} for v in sides.values())
    assert all(len(v) == 2 for v in packets.values()), "the two copies stay separately blinded"


def _comparison_stream(*titles: str) -> list[tuple[str, str]]:
    """A document's styled paragraphs, carrying one comparison panel per title."""
    stream = [("Heading1", "Revision Material Evaluation Worksheet")]
    for ordinal, title in enumerate(titles, start=1):
        stream += [
            ("Heading2", f"Objective {ordinal} of {len(titles)} — your comparison"),
            ("Normal", "Write Yes in one box on each row."),
            ("Normal", f"Learning objective. {title}"),
        ]
    return stream


def _two_objective_plan() -> dict:
    """A plan whose objectives are deliberately not what a positional read would pick."""
    return {
        "lesson_plan_objectives": [
            {"lesson_objective_id": "lo-01", "objective_text": "first objective"},
            {"lesson_objective_id": "lo-02", "objective_text": "second objective"},
            {"lesson_objective_id": "lo-03", "objective_text": "third objective"},
        ]
    }


def test_a_panel_resolves_to_the_objective_it_names_not_the_one_at_its_position():
    """Only objectives the student has class work for are shown, so panel 1 is not lo-01.

    Reading the ordinal instead misidentified 36 of the 70 delivered panels, and that
    error alone produced a reported finding that half the rated objectives had no learner
    evidence behind them.
    """
    plan = _two_objective_plan()
    only_second = panels.resolve(_comparison_stream("second objective"), plan)
    assert [p.objective_id for p in only_second] == ["lo-02"]
    assert only_second[0].ordinal == 1


def test_a_gap_in_the_shown_objectives_does_not_shift_the_ones_after_it():
    plan = _two_objective_plan()
    shown = panels.resolve(_comparison_stream("first objective", "third objective"), plan)
    assert [p.objective_id for p in shown] == ["lo-01", "lo-03"]


def test_a_heading_that_matches_no_objective_resolves_to_nothing_rather_than_guessing():
    """A wrong id that looks plausible is worse than a gap that announces itself."""
    shown = panels.resolve(
        _comparison_stream("an objective this lesson never had"), _two_objective_plan()
    )
    assert shown and shown[0].objective_id is None
    assert not shown[0].resolved


def _panel_row(case: str, objective: str, rater: str, ordinal: int = 1) -> dict:
    return {
        "case_id": case,
        "objective_id": objective,
        "rater_id": rater,
        "panel_ordinal": ordinal,
    }


def test_the_copy_guard_answers_no_when_the_two_copies_name_different_objectives():
    """The guard has to be able to fail, or it is not a guard.

    Its first version keyed on the panel ordinal and read back with the objective id, so
    all 35 lookups missed and every panel inherited a default of True — a check that
    could only ever agree.
    """
    agreed = provenance._copies_agree(
        [
            _panel_row("les/stu", "lo-01", "rater-1"),
            _panel_row("les/stu", "lo-01", "rater-2"),
        ]
    )
    assert agreed == {("les/stu", "lo-01"): "yes"}

    disagreed = provenance._copies_agree(
        [
            _panel_row("les/stu", "lo-01", "rater-1"),
            _panel_row("les/stu", "lo-02", "rater-2"),
        ]
    )
    assert disagreed == {("les/stu", "lo-01"): "no", ("les/stu", "lo-02"): "no"}


def test_the_copy_guard_will_not_pass_one_rater_or_the_same_objective_at_two_positions():
    one_rater = provenance._copies_agree([_panel_row("les/stu", "lo-01", "rater-1")])
    assert one_rater == {("les/stu", "lo-01"): "no"}

    shifted = provenance._copies_agree(
        [
            _panel_row("les/stu", "lo-01", "rater-1", ordinal=1),
            _panel_row("les/stu", "lo-01", "rater-2", ordinal=2),
        ]
    )
    assert shifted == {("les/stu", "lo-01"): "no"}


def _h1_workbook(rows: list[tuple], path: Path) -> Path:
    """A one-sheet workbook shaped like the H1 scores the analysis reads."""
    import openpyxl

    book = openpyxl.Workbook()
    sheet = book.active
    sheet.title = "H1 scores"
    sheet.append(
        [
            "rater",
            "internal_packet_id",
            "lesson",
            "condition",
            "draw",
            "lesson_objective_id",
            "criterion",
            "score",
        ]
    )
    for row in rows:
        sheet.append(list(row))
    book.save(path)
    return path


def test_the_pack_effect_groups_both_raters_copies_of_one_pack(tmp_path: Path):
    """The -cN suffix names a rater's copy, not a pack. Grouping on it halves every pack."""
    path = _h1_workbook(
        [
            ("rater-1", "h1-l06-c0-v3-c1", "t3-w09", "C0", 3, "lo-t3w09-01", 2, 4),
            ("rater-2", "h1-l06-c0-v3-c2", "t3-w09", "C0", 3, "lo-t3w09-01", 2, 5),
        ],
        tmp_path / "two-copies.xlsx",
    )

    frame = mixed_model.scores(path)

    assert frame["internal_packet_id"].nunique() == 2
    assert frame["packet"].nunique() == 1
    assert set(frame["packet"]) == {"h1-l06-c0-v3"}


def test_the_minimum_detectable_effect_is_the_number_the_dissertation_prints():
    """SE 0.1679 on the primary endpoint, at the level and power the study reports."""
    assert round(mixed_model.minimum_detectable_effect(0.1679), 2) == 0.47
    assert round(mixed_model.minimum_detectable_effect(0.1679, one_sided=True), 2) == 0.42
    assert round(mixed_model.minimum_detectable_effect(0.1679, power=0.90), 2) == 0.54


def test_a_fit_reports_which_optimiser_reached_it_and_how_well():
    """A near-singular fit is optimiser-dependent, so it has to carry its own provenance."""
    import random

    import pandas as pd

    generator = random.Random(20260913)
    rows = [
        {
            "score": generator.choice([3, 4, 5]),
            "condition": f"C{condition}",
            "rater": f"rater-{rater}",
            "lesson": f"lesson-{lesson}",
            "objective": f"lesson-{lesson}/objective-{objective}",
            "packet": f"pack-{lesson}-{condition}",
            "rater_condition": f"rater-{rater}:C{condition}",
            "one": 1,
        }
        for lesson in range(6)
        for condition in range(4)
        for rater in range(4)
        for objective in range(2)
    ]
    frame = pd.DataFrame(rows)

    fit = mixed_model.fit_crossed(frame, "score ~ C(condition)", "synthetic")

    assert fit.optimiser in mixed_model.OPTIMISERS
    assert fit.observations == 192
    assert {item.name for item in fit.contrasts} == {"C1", "C2", "C3"}
    assert round(sum(fit.shares.values()), 6) == 1.0


def test_the_workbook_ratings_join_each_pack_length_and_drop_what_was_not_answered():
    rating = {
        "rater_id": "rater-1",
        "internal_packet_id": "h1-l06-c3-v2-c1",
        "lesson_id": "t3-w09",
        "condition": "C3",
        "draw": 2,
        "objective_id": "lo-t3w09-01",
        "criterion_index": 2,
        "score": 4,
        "response_status": "answered",
    }
    skipped = {**rating, "rater_id": "rater-2", "score": None, "response_status": "missing"}
    generation = [
        {"lesson": "t3-w09", "condition": "C3", "repeat": 2, "chars": 6250},
        {"lesson": "t3-w09", "condition": "C3", "repeat": 1, "chars": 9000},
    ]

    frame = mixed_model.workbook_scores([rating, skipped], generation)

    assert len(frame) == 1
    assert frame.iloc[0][mixed_model.LENGTH_TERM] == 6.25
    assert frame.iloc[0]["packet"] == "h1-l06-c3-v2"
    assert frame.iloc[0]["objective"] == "t3-w09/lo-t3w09-01"


def test_a_specification_fits_its_own_components_and_reports_its_covariates():
    import random

    import pandas as pd

    generator = random.Random(20260923)
    rater_effect = {rater: generator.gauss(0, 0.6) for rater in range(4)}
    lesson_effect = {lesson: generator.gauss(0, 0.4) for lesson in range(6)}
    frame = pd.DataFrame(
        [
            {
                "score": 3.5
                + 0.2 * condition
                + rater_effect[rater]
                + lesson_effect[lesson]
                + generator.gauss(0, 0.7),
                "condition": f"C{condition}",
                "criterion": mixed_model.LESSON_CONTEXT_CRITERION,
                "rater": f"rater-{rater}",
                "lesson": f"lesson-{lesson}",
                "objective": f"lesson-{lesson}/objective-1",
                "packet": f"pack-{lesson}-{condition}",
                "rater_condition": f"rater-{rater}:C{condition}",
                mixed_model.LENGTH_TERM: generator.uniform(5, 10),
                "one": 1,
            }
            for lesson in range(6)
            for condition in range(4)
            for rater in range(4)
            for _ in range(3)
        ]
    )

    fit = mixed_model.fit(mixed_model.PRIMARY_LENGTH, frame)

    assert [term.name for term in fit.covariates] == [mixed_model.LENGTH_TERM]
    assert {term.name for term in fit.contrasts} == {"C1", "C2", "C3"}
    assert fit.optimiser in fit.converged
    refit = mixed_model.fit(mixed_model.SECONDARY_REFITS[2], frame.assign(criterion=1))
    assert set(refit.shares) == {"rater", "lesson", "packet", "residual"}
