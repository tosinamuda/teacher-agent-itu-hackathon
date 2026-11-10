"""The canonical lesson document: lossless, selectable, and refusing what it cannot mean.

Three claims, one test each way round.

*Lossless* — the projection of ``lessons/t3-w05.xml`` plus the note files equals the
frozen plan in ``eval_set.json`` exactly. If that holds, the JSON copy is redundant.

*Selectable* — every selection returns what today's parsing path returns. The schema is
only worth having if it changes how an answer is reached, not which answer.

*Refusing* — the defects of the last fortnight, each attempted against the format. A
drifted note, an unclaimed region, a heading that addresses nothing, a dangling
objective, an undeclared figure: all are errors here rather than silence downstream.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from lxml import etree

from app.domains.artefacts.types.lesson_plan.domain.lesson_document import GRAMMAR_PATH
from app.domains.artefacts.types.lesson_plan.drafting.domain.note_figures import figures_in_text
from app.domains.artefacts.types.post_class_review_pack.application.request.units import (
    SectionGenerationUnitProjector,
)
from app.shared.session_plan_view import SessionPlanStepView, SessionPlanView
from experiments.h1_condition_eval import lesson_selections as select
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.lesson_delivery import conditions_reaching, measure
from experiments.h1_condition_eval.lesson_document import LessonError, load
from experiments.h1_condition_eval.lesson_plan_projection import plan

PILOT = Path(__file__).parent.parent / "experiments/h1_condition_eval/lessons/t3-w05.xml"


@pytest.fixture(scope="module")
def lesson():
    return load(PILOT)


@pytest.fixture(scope="module")
def frozen() -> dict:
    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    return next(case["plan"] for case in cases if case["lesson"] == "t3-w05")


def _copy(tmp_path: Path, edit) -> Path:
    """The pilot with one thing changed, notes still pointed at the real files."""
    tree = etree.parse(str(PILOT))
    for note in tree.getroot().iter("note"):
        note.set("src", str((PILOT.parent / str(note.get("src"))).resolve()))
    edit(tree.getroot())
    path = tmp_path / "lesson.xml"
    tree.write(str(path), encoding="utf-8", xml_declaration=True)
    return path


def test_the_document_matches_its_grammar():
    grammar = etree.RelaxNG(etree.parse(str(GRAMMAR_PATH)))
    assert grammar.validate(etree.parse(str(PILOT))), list(grammar.error_log)


def test_no_prose_of_hers_is_copied_into_the_document(lesson):
    """The note is referenced. Nothing under <note> carries text."""
    root = etree.parse(str(PILOT)).getroot()
    for note in root.iter("note"):
        assert not "".join(note.itertext()).strip()
    assert sum(len(step.note_text) for step in lesson.steps) == 3241


def test_projection_equals_the_frozen_plan(lesson, frozen):
    """Field for field, but for the note's declared parts, which the frozen plan predates.

    ``regions`` is the one thing the projection adds rather than reproduces. It carries
    no text the note does not already carry — it names where that text begins and ends —
    so it is asserted separately and everything else still has to match exactly.
    """
    projected = plan(lesson)
    regions = [step.pop("regions", None) for step in projected["steps"]]
    assert projected == frozen
    assert [len(part or []) for part in regions] == [1, 3, 3, 0]


def test_student_tasks_selection_equals_the_parsing_path(lesson, frozen):
    """On core steps, which is the only place the projector asks for them.

    An evaluation step's questions are stored as practice blocks too, so the parsing
    path would answer for one if asked — it is never asked. The document keeps them
    apart by element: ``<question>`` is checked, ``<set-work>`` is set.
    """
    core = [step for step in lesson.steps if step.kind == "core"]
    frozen_core = [step for step in frozen["steps"] if step["step_kind"] == "core"]
    assert len(core) == 2
    for step, projected in zip(core, frozen_core, strict=True):
        view = SessionPlanStepView.model_validate(projected)
        parsed = SectionGenerationUnitProjector._student_tasks(view)
        assert select.student_tasks(step) == parsed, step.id


def test_assessment_points_selection_equals_the_parsing_path(lesson, frozen):
    parsed = SectionGenerationUnitProjector._assessment_points(
        SessionPlanView.model_validate(frozen)
    )
    assert select.assessment_points(lesson) == parsed


def test_figure_selection_equals_the_tikz_regex(lesson, frozen):
    parsed = [
        (step["step_id"], figure["figure_ref"], figure["caption"])
        for step in frozen["steps"]
        for figure in figures_in_text(step.get("note") or "", step["step_id"])
    ]
    assert select.figures(lesson) == parsed


def test_every_region_is_addressable_by_an_id_that_does_not_move(lesson):
    """What ``read_document`` addresses by line number, addressed by name."""
    ids = [section_id for section_id, _, _ in select.documents(lesson)]
    assert len(ids) == len(set(ids))
    assert select.region(lesson, "step-t3w05-02:b3").startswith("1. How many circular faces")


def test_a_note_edited_since_the_structure_was_declared_is_refused(tmp_path):
    path = _copy(tmp_path, lambda root: next(root.iter("note")).set("sha256", "0" * 64))
    with pytest.raises(LessonError, match="has changed since its structure was declared"):
        load(path)


def test_text_no_section_claims_is_refused(tmp_path):
    """The failure that a copied block cannot have: prose in her file that reaches nothing."""

    def drop_a_section(root):
        note = root.findall("step")[1].find("note")
        note.remove(note.findall("section")[1])

    path = _copy(tmp_path, drop_a_section)
    with pytest.raises(LessonError, match="swallows the heading 'Properties of sphere'"):
        load(path)


def test_a_note_that_grew_a_tail_no_section_claims_is_refused(tmp_path, monkeypatch):
    """Covering every character is checked separately from covering it in the right place."""

    def drop_the_last_section(root):
        note = root.findall("step")[1].find("note")
        note.remove(note.findall("section")[-1])

    path = _copy(tmp_path, drop_the_last_section)
    with pytest.raises(LessonError, match="swallows the heading 'Student activity'"):
        load(path)


def test_a_heading_that_addresses_nothing_is_refused(tmp_path):
    path = _copy(
        tmp_path,
        lambda root: root.findall("step")[1].find("note")[0].set("heading", "Properties of a cone"),
    )
    with pytest.raises(LessonError, match="no heading 'Properties of a cone'"):
        load(path)


def test_an_objective_the_lesson_does_not_declare_is_refused(tmp_path):
    path = _copy(tmp_path, lambda root: root.findall("step")[1].set("objective", "lo-t3w05-09"))
    with pytest.raises(LessonError, match="objective 'lo-t3w05-09' is not declared"):
        load(path)


def test_a_core_step_that_teaches_nothing_nameable_is_refused(tmp_path):
    path = _copy(tmp_path, lambda root: root.findall("step")[1].attrib.pop("objective"))
    with pytest.raises(LessonError, match="must name the objective it teaches"):
        load(path)


def test_a_figure_the_region_does_not_label_is_refused(tmp_path):
    path = _copy(
        tmp_path,
        lambda root: root.findall("step")[1].find("note")[0].find("figure").set("ref", "fig-09"),
    )
    with pytest.raises(
        LessonError, match="fig-09 is declared but no line above its drawing labels it"
    ):
        load(path)


def test_the_sealed_digests_are_the_ones_on_disk():
    """The drift that is live in eval_set.json today, made impossible here."""
    root = etree.parse(str(PILOT)).getroot()
    for note in root.iter("note"):
        source = (PILOT.parent / str(note.get("src"))).resolve()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == note.get("sha256"), source.name


def test_a_preamble_no_section_claims_is_refused():
    """The other way to lose text: prose above the first declared heading.

    No sibling heading is absorbed here, so the covers-every-character check is the
    only thing standing between her opening paragraph and nothing reading it.
    """
    from experiments.h1_condition_eval.lesson_document import _regions

    note = "Statistics is the study of data.\n\n#### Meaning of Data\n\nData are facts.\n"
    assert _regions(note, [None, "Meaning of Data"], "probe") == [
        "Statistics is the study of data.",
        "Data are facts.",
    ]
    with pytest.raises(LessonError, match="34 characters of the note are in no declared section"):
        _regions(note, ["Meaning of Data"], "probe")


def test_each_region_reaches_only_the_conditions_its_role_allows(lesson):
    """The builder honouring the policy, checked against her actual sentences.

    Note what this does and does not establish. ``allowed`` comes from the role's
    channel and ``profiles.py``; ``reached`` is what the builder emitted. A disagreement
    means the builder ignored a flag. It cannot catch a MIS-ROLED region, because the
    role drives the projection and the measurement moves with the mistake — that is what
    the heading cross-check below is for.
    """
    rows = measure(lesson)
    assert len(rows) == 7
    for section, kind, allowed, reached in rows:
        assert allowed == reached, f"{section.id} ({section.role}) on a {kind} step"
    reached_c1 = {section.role for section, _, _, seen in rows if "C1" in seen}
    assert reached_c1 == {"set-work"}


def test_the_conditions_a_role_reaches_are_derived_from_the_profile_registry(lesson):
    """Not a second opinion about what a condition means — the registry's own answer.

    Computed here from the flag each channel reads, so if this and ``lesson_delivery``
    ever disagree it is because one of them started holding its own copy.
    """
    from app.domains.experiments.domain.types import Hypothesis
    from app.domains.experiments.review_pack_study.conditions.profiles import (
        h1_main_condition_codes,
        profile_for,
    )

    def codes_where(flag):
        return {
            code.value
            for code in h1_main_condition_codes()
            if flag(profile_for(Hypothesis.H1, code))
        }

    section = next(s for step in lesson.steps for s in step.sections if s.role == "set-work")
    assert conditions_reaching(section, "core") == codes_where(
        lambda profile: profile.context.include_student_tasks
    )
    prose = next(s for step in lesson.steps for s in step.sections if s.role == "explanation")
    assert conditions_reaching(prose, "core") == codes_where(
        lambda profile: profile.retrieval.provides_evidence
    )
    # Step kind comes first: only core steps become generation units.
    assert conditions_reaching(section, "evaluation") == set()


def _reroled(tmp_path: Path, section_id: str, **attrs) -> Path:
    def edit(root):
        for step in root.findall("step"):
            note = step.find("note")
            for element in [] if note is None else note.findall("section"):
                if element.get("id") == section_id and step.get("id", "").endswith("05-02"):
                    for key, value in attrs.items():
                        element.set(key, value)

    return _copy(tmp_path, edit)


def test_her_heading_refuses_work_declared_as_prose(tmp_path):
    """The check the role cannot make for itself, using evidence she wrote."""
    with pytest.raises(LessonError, match="'Student activity' says it sets work"):
        load(_reroled(tmp_path, "b3", role="explanation"))


def test_her_heading_refuses_prose_declared_as_work(tmp_path):
    with pytest.raises(LessonError, match="'Properties of a cylinder' does not say it sets work"):
        load(_reroled(tmp_path, "b1", role="set-work"))


def test_a_reader_may_overrule_her_heading_but_not_silently(tmp_path):
    path = _reroled(
        tmp_path, "b3", role="explanation", **{"role-note": "checked against the source page"}
    )
    section = next(s for step in load(path).steps for s in step.sections if s.id.endswith(":b3"))
    assert section.role == "explanation"


def test_a_region_her_document_has_and_nothing_reads_is_declared_as_such(lesson):
    """The intro note reaches no condition. That is recorded, not left to be rediscovered."""
    recall = [s for step in lesson.steps for s in step.sections if s.role == "recall"]
    assert [s.delivered for s in recall] == [False]


# --- the whole corpus ----------------------------------------------------------------

LESSONS = ("t2-w09", "t3-w02", "t3-w04", "t3-w05", "t3-w06", "t3-w09")

#: What migrating each lesson changed, pinned so none of it can grow quietly, as
#: (format changes, corrections, disagreements). A *format* change is one the migration
#: makes on purpose and states as a rule. A *correction* is a frozen value a reader
#: established was wrong. A *disagreement* is neither, and every one of these was read.
#: All three are listed in LESSON-SCHEMA.md with what each turned out to be.
MIGRATION = {
    "t2-w09": (9, 3, 3),
    "t3-w02": (30, 1, 2),
    "t3-w04": (11, 0, 0),
    "t3-w05": (3, 0, 0),
    "t3-w06": (13, 0, 5),
    "t3-w09": (3, 0, 1),
}


def _path(lesson: str) -> Path:
    return PILOT.parent / f"{lesson}.xml"


@pytest.fixture(scope="module")
def corpus() -> dict:
    return {lesson: load(_path(lesson)) for lesson in LESSONS}


@pytest.fixture(scope="module")
def frozen_plans() -> dict:
    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    return {case["lesson"]: case["plan"] for case in cases}


@pytest.mark.parametrize("lesson", LESSONS)
def test_every_lesson_is_a_valid_document(corpus, lesson):
    document = corpus[lesson]
    assert document.steps and document.objectives


@pytest.mark.parametrize("lesson", LESSONS)
def test_no_lesson_copies_her_prose_into_the_document(lesson):
    """Six documents, and between them not one sentence of the thirty-nine thousand."""
    root = etree.parse(str(_path(lesson))).getroot()
    for note in root.iter("note"):
        assert not "".join(note.itertext()).strip()


@pytest.mark.parametrize("lesson", LESSONS)
def test_what_migrating_this_lesson_changed(corpus, frozen_plans, lesson):
    from experiments.h1_condition_eval.lesson_plan_projection import (
        _differences,
        _labels_by_step,
        _step_index,
        classify,
        correction,
    )

    document = corpus[lesson]
    labels = _labels_by_step(document)
    ids = [step.id for step in document.steps]

    def why(difference):
        index = _step_index(difference.path)
        return classify(difference, labels.get(ids[index], ()) if index >= 0 else ())

    found = _differences(plan(document), frozen_plans[lesson])
    formats = [d for d in found if why(d)]

    def fixed(difference):
        index = _step_index(difference.path)
        return correction(difference, labels.get(ids[index], ()) if index >= 0 else ())

    corrections = [d for d in found if not why(d) and fixed(d)]
    disagreements = [d for d in found if not why(d) and not fixed(d)]
    assert (len(formats), len(corrections), len(disagreements)) == MIGRATION[lesson], [
        d.path for d in disagreements
    ]


@pytest.mark.parametrize("lesson", LESSONS)
def test_every_region_of_every_lesson_reaches_what_its_role_allows(corpus, lesson):
    for section, kind, allowed, reached in measure(corpus[lesson]):
        assert allowed == reached, f"{section.id} ({section.role}) on a {kind} step"


@pytest.mark.parametrize("lesson", LESSONS)
def test_student_tasks_selection_matches_the_parsing_path_corpus_wide(corpus, frozen_plans, lesson):
    """Against the FROZEN blocks, not the projection — no disagreement touches practice."""
    core = [step for step in corpus[lesson].steps if step.kind == "core"]
    frozen_core = [s for s in frozen_plans[lesson]["steps"] if s["step_kind"] == "core"]
    for step, projected in zip(core, frozen_core, strict=True):
        parsed = SectionGenerationUnitProjector._student_tasks(
            SessionPlanStepView.model_validate(projected)
        )
        assert select.student_tasks(step) == parsed, step.id


@pytest.mark.parametrize("lesson", LESSONS)
def test_assessment_points_selection_matches_the_parsing_path_corpus_wide(
    corpus, frozen_plans, lesson
):
    parsed = SectionGenerationUnitProjector._assessment_points(
        SessionPlanView.model_validate(frozen_plans[lesson])
    )
    assert select.assessment_points(corpus[lesson]) == parsed


@pytest.mark.parametrize("lesson", LESSONS)
def test_figure_selection_matches_the_regex_corpus_wide(corpus, lesson):
    """Same note, two extraction methods — the document's note, which is the edited one."""
    document = corpus[lesson]
    parsed = [
        (step.id, figure["figure_ref"], figure["caption"])
        for step in document.steps
        for figure in figures_in_text(step.note_text, step.id)
    ]
    assert select.figures(document) == parsed


def test_freezing_from_the_documents_feeds_every_condition_the_same_request():
    """The switch of source, proved inert rather than argued for.

    ``eval_set.json`` is the frozen dataset the judged runs are pinned against, and the
    documents disagree with it in eleven places — every one of them a duplicate the
    format drops or a decomposition the transcription lost. None of it reaches a
    condition: what the runner feeds is the plan with ``clean_plan`` applied, and that
    request is identical either way, for six lessons across C0-C3.
    """
    from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (  # noqa: E501
        BaseReviewPackRequestBuilder,
    )
    from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
        LessonSources,
    )
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
        prompt_evidence,
    )
    from app.domains.experiments.domain.types import Hypothesis
    from app.domains.experiments.review_pack_study.conditions.profiles import (
        h1_main_condition_codes,
        profile_for,
    )
    from experiments.h1_condition_eval.dataset import from_documents
    from experiments.h1_condition_eval.note_editorial import clean_plan

    builder = BaseReviewPackRequestBuilder()

    def request(payload, code):
        view = SessionPlanView.model_validate(payload)
        return builder.build(
            session_plan=view,
            policy=profile_for(Hypothesis.H1, code).generation_policy(),
            sources=LessonSources.unresolved(view.references),
        )

    frozen = {c["lesson"]: c["plan"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
    checked = regioned = 0
    for case in from_documents()["cases"]:
        lesson = case["lesson"]
        runner, _ = clean_plan({**frozen[lesson], "lesson_key": lesson})
        for code in h1_main_condition_codes():
            mine, theirs = request(case["plan"], code), request(runner, code)
            where = f"{lesson}/{code.value}"

            # What the model reads is identical. Regions are an ADDRESS for the reading
            # tools; left in the prompt they put the note in a second time, and t3-w02's
            # C2 evidence measured 2.12x the note it came from.
            for unit, other in zip(mine.units, theirs.units, strict=True):
                assert prompt_evidence(unit.source_evidence) == prompt_evidence(
                    other.source_evidence
                ), where
                regioned += sum(len(item.regions) for item in unit.source_evidence)

            # And the request differs by exactly that one field, nothing else.
            def without_regions(built):
                dumped = built.model_dump(mode="json")
                for unit in dumped["units"]:
                    for item in unit["source_evidence"]:
                        item.pop("regions", None)
                return dumped

            assert without_regions(mine) == without_regions(theirs), where
            checked += 1
    assert checked == 24
    assert regioned > 0


def test_freezing_from_the_documents_does_not_disarm_the_additions_guard():
    """The trap this switch sets, and the thing that stops it.

    ``note_editorial`` digests every paragraph the generation copy adds to the
    transcription. It is the only thing between a hand edit and words reaching the model
    undeclared, and it caught all 21 figure captions the moment they went in. Freeze the
    eval set from the documents and ``note`` becomes the generation copy — so comparing
    against it compares a file with itself, and the guard sees nothing. The transcription
    is carried forward as ``note_frozen`` so it keeps seeing what it saw.
    """
    from experiments.h1_condition_eval.dataset import from_documents, from_transcripts
    from experiments.h1_condition_eval.note_editorial import additions, note_path

    def visible(payload) -> int:
        return sum(
            len(additions(step["note_frozen"] or step["note"], clean.read_text(encoding="utf-8")))
            for case in payload["cases"]
            for step in case["plan"]["steps"]
            if step.get("note")
            if (clean := note_path(case["lesson"], step["step_id"])).exists()
        )

    from_the_transcripts = sum(
        len(additions(step["note"], clean.read_text(encoding="utf-8")))
        for case in from_transcripts()["cases"]
        for step in case["plan"]["steps"]
        if step.get("note")
        if (clean := note_path(case["lesson"], step["step_id"])).exists()
    )
    assert from_the_transcripts > 0
    assert visible(from_documents()) == from_the_transcripts


#: Regions whose declared role and whose CONTENT read differently, with why. A role
#: names what her heading names; ``kind`` in note_headings.json names what the region
#: turned out to hold. They agree on 44 of 47 headings. These three are the corpus's
#: one real ambiguity, and both roles feed the same channel, so the difference carries
#: no condition consequence — it is pinned to stay small, not because it is wrong.
ROLE_UNLIKE_CONTENT = {
    # Formulas for cuboid and cube, then Example 1 and Example 2 worked in full.
    # Genuinely mixed: exposition first, worked examples after.
    "step-t3w05-03:b1",
    # Entirely Example 3, under a heading that names the topic instead of the example.
    "step-t3w05-03:b2",
    # A problem, a figure and a solution, under a topic heading. Same shape as b2.
    "step-t3w05-03:b3",
}


def test_every_heading_in_the_corpus_was_read_and_recorded():
    """45 headings over 47 heading lines, each with a verdict and the reason for it."""
    rows = json.loads((PILOT.parent.parent / "note_headings.json").read_text(encoding="utf-8"))[
        "headings"
    ]
    assert len(rows) == 45
    assert all(row["confirmed_in_context"] and row["why"] for row in rows)
    assert sum(row["sets_work"] for row in rows) == 3
    assert sorted(row["heading"] for row in rows if row["sets_work"]) == [
        "Activity. Simplify the following",
        "Student activity",
        "Students activity",
    ]


@pytest.mark.parametrize("lesson", LESSONS)
def test_a_declared_role_matches_what_its_region_holds(corpus, lesson):
    """The one check on a role that reading, not the format, produced.

    ``role`` follows her heading; ``kind`` follows what the region turned out to
    contain. Where they part, a reader has to have said why — otherwise a region full
    of worked examples sitting under ``role="explanation"`` looks like a mistake to
    whoever reads it next.
    """
    kinds = {
        row["heading"]: row["kind"]
        for row in json.loads(
            (PILOT.parent.parent / "note_headings.json").read_text(encoding="utf-8")
        )["headings"]
    }
    for step in corpus[lesson].steps:
        for section in step.sections:
            if not section.heading:
                continue
            kind = kinds[section.heading]
            matches = kind == section.role or (
                kind == "exposition" and section.role == "explanation"
            )
            assert matches or section.id in ROLE_UNLIKE_CONTENT, (
                f"{section.id}: role {section.role!r} but the region reads as {kind!r}"
            )


# --- the reading tool ------------------------------------------------------------------


def _unit_for(lesson_id: str, step_id: str, code, figures="source"):
    from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
        SourceEvidenceProjector,
    )
    from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
        SectionGenerationUnit,
    )
    from app.domains.experiments.domain.types import Hypothesis
    from app.domains.experiments.review_pack_study.conditions.profiles import profile_for

    view = SessionPlanView.model_validate(plan(load(_path(lesson_id))))
    step = next(s for s in view.steps if s.step_id == step_id)
    evidence = SourceEvidenceProjector(figures=figures).for_step(
        step, profile_for(Hypothesis.H1, code).generation_policy()
    )
    return SectionGenerationUnit(
        unit_id="u", lesson_objective_id="lo", objective_text="", source_evidence=evidence
    )


def test_a_region_is_addressable_by_name_not_by_line():
    """What ``read_document`` addressed as lines 12-28, addressed as what it is.

    A line number over a markdown blob moves the moment anyone edits a word above it.
    A region id does not, which is the whole reason the note has declared parts.
    """
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools import (
        source_reading,
    )
    from app.domains.experiments.domain.types import ConditionCode

    listed, read = source_reading.reading_tools(
        _unit_for("t3-w05", "step-t3w05-02", ConditionCode.C2)
    )
    offered = {row["document"]: row["title"] for row in listed()}
    assert offered["step-t3w05-02:b3"] == "Student activity"
    assert "the lesson note" in offered
    assert "How many circular faces" in read("step-t3w05-02:b3")
    assert "No document named" in read("step-t3w05-02:b9")


def test_a_plan_that_declares_no_regions_still_reads_by_line():
    """Every plan the app drafts today. The change has to be invisible to them."""
    from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
        SourceEvidenceProjector,
    )
    from app.domains.experiments.domain.types import ConditionCode, Hypothesis
    from app.domains.experiments.review_pack_study.conditions.profiles import profile_for

    step = SessionPlanStepView(
        step_id="s1", step_kind="core", note="one\n\ntwo\n\nthree", blocks=[]
    )
    evidence = SourceEvidenceProjector(figures="source").for_step(
        step, profile_for(Hypothesis.H1, ConditionCode.C2).generation_policy()
    )
    assert evidence[0].regions == []


def test_a_region_cannot_leak_a_drawing_the_whole_note_withheld():
    """The figure policy applies part by part, not only to the blob.

    Under ``figures="reference"`` a drawing reaches the model as a label, never as
    TikZ. A region that skipped that treatment would be a way round it.
    """
    from app.domains.experiments.domain.types import ConditionCode

    unit = _unit_for("t3-w05", "step-t3w05-02", ConditionCode.C2, figures="reference")
    item = unit.source_evidence[0]
    assert "tikzpicture" not in item.excerpt
    assert item.regions
    for region in item.regions:
        assert "tikzpicture" not in region.excerpt


def test_no_region_reaches_a_condition_that_gets_no_evidence():
    """Regions travel on the evidence item, so they inherit its gate. Asserted, not assumed."""
    from app.domains.experiments.domain.types import ConditionCode

    for code in (ConditionCode.C0, ConditionCode.C1):
        assert _unit_for("t3-w05", "step-t3w05-02", code).source_evidence == []
    for code in (ConditionCode.C2, ConditionCode.C3):
        unit = _unit_for("t3-w05", "step-t3w05-02", code)
        assert [r.region_id for r in unit.source_evidence[0].regions] == [
            "step-t3w05-02:b1",
            "step-t3w05-02:b2",
            "step-t3w05-02:b3",
        ]
