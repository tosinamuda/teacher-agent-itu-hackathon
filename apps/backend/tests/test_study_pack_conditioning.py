"""Unit tests for the conditioned study-pack spine (eval-plan §8-20).

These prove C0-C3 are *real executable differences* without touching the LLM or
DB: the request builder hands each condition a different request, and the
validator enforces the C3/P1 checks.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from typing import get_args

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    EVIDENCE_LABEL,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.policy import (
    instruction_summary,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import (
    ExpertSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    PROSE_CHECKS,
    STRUCTURAL_CHECKS,
    ValidationCheck,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    section_from_draft,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    DraftSection,
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.repair_section import (  # noqa: E501
    RepairSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteGroundedSection,
    WriteGroundedSectionFromSources,
    WriteObjectiveSection,
    WriteSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CONTENT_CHECKS,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    prompt_lesson,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import (
    H1_CONDITION_PROFILES,
    H2_CONDITION_PROFILES,
    profile_for,
)
from app.domains.experiments.review_pack_study.conditions.study_design import (
    PILOT_ONE_LESSON_CONFIG,
    PUBLICATION_CONFIG,
)
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

SESSION_PLAN_DICT = {
    "subject": "Mathematics",
    "grade": "JSS1",
    "topic": "Area of plane shapes",
    "subtopic": "Area",
    "theme": "Mensuration",
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lop01", "objective_text": "Find the area of rectangles."},
        {"lesson_objective_id": "lop02", "objective_text": "Find the area of real-life objects."},
    ],
    "references": ["Textbook p.42: area = length x width", "Textbook p.43: worked example"],
    "instructional_materials": ["ruler", "grid paper"],
    "steps": [
        {
            "step_id": "s1",
            "step_kind": "core",
            "lesson_objective_id": "lop01",
            "title": "Rectangle area",
            "content": "Area equals length times width.",
            "instructional_type": "explanation",
            "estimated_minutes": 10,
            "activities": [
                {"who": "teacher", "what": "demonstrate"},
                {"who": "student", "what": "practise"},
            ],
        },
        {
            "step_id": "s2",
            "step_kind": "core",
            "lesson_objective_id": "lop02",
            "title": "Real-life area",
            "content": "Apply the formula to gardens.",
            "instructional_type": "practice",
            "estimated_minutes": 8,
            "activities": [
                {"who": "teacher", "what": "guide"},
                {"who": "student", "what": "solve"},
            ],
        },
        {"step_id": "s3", "step_kind": "evaluation", "title": "Exit", "content": "quiz"},
    ],
}

SESSION_PLAN = SessionPlanView.model_validate(SESSION_PLAN_DICT)

BUILDER = BaseReviewPackRequestBuilder()


def _h1_request(condition: ConditionCode):
    return BUILDER.build(
        session_plan=SESSION_PLAN,
        policy=profile_for(Hypothesis.H1, condition),
        sources=LessonSources.unresolved(SESSION_PLAN.references),
    )


def test_study_design_packet_counts() -> None:
    # H1 = lessons x main C-conditions (4: C0-C3; C4 is teacher-governance evidence,
    # not a rater packet — June-5 settled design); H2 = lessons x focal learners x P.
    assert PILOT_ONE_LESSON_CONFIG.expected_h1_packets() == 4
    assert PILOT_ONE_LESSON_CONFIG.expected_h2_packets() == 8
    assert PUBLICATION_CONFIG.expected_h1_packets() == 48
    assert PUBLICATION_CONFIG.expected_h2_packets() == 96


def test_c0_is_objective_only_no_evidence() -> None:
    request = _h1_request(ConditionCode.C0)
    assert len(request.units) == 2
    assert all(unit.unit_id.startswith("objective:") for unit in request.units)
    assert all(unit.step_content is None for unit in request.units)
    assert all(unit.source_evidence == [] for unit in request.units)


def test_c1_has_step_context_but_no_evidence() -> None:
    request = _h1_request(ConditionCode.C1)
    assert len(request.units) == 2  # only core steps
    assert all(unit.unit_id.startswith("step:") for unit in request.units)
    assert [unit.current_step for unit in request.units] == [1, 2]
    assert request.units[0].instructional_events == [
        "provide_learning_guidance",
        "elicit_performance",
    ]
    assert all(unit.source_evidence == [] for unit in request.units)


def test_the_plan_conditions_know_the_lessons_order() -> None:
    """Sections are generated by independent concurrent calls.

    Without the plan's own ordering the unit teaching the second objective cannot know
    the first exists, so it re-teaches and cannot build on what precedes it. Carried by
    ``current_step`` against the ORDERED objective list: the core steps match that order
    one-for-one on all six field lessons, so a separate sequence object only restated it.
    """
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        request = _h1_request(code)
        assert [unit.current_step for unit in request.units] == [1, 2], code
        assert request.lesson_context.lesson_objectives == [
            "Find the area of rectangles.",
            "Find the area of real-life objects.",
        ], code
    assert all(unit.current_step is None for unit in _h1_request(ConditionCode.C0).units)


def test_no_condition_receives_a_synthetic_per_step_time() -> None:
    """Her plans give one Duration line and allocate nothing to individual steps.

    The 10/10/10 and 20/20 splits were the derivation's. Sending them puts a length
    instruction in the plan conditions that the baseline never sees — and the lesson
    figure is no use either, being 40 minutes on all six lessons.
    """
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        request = _h1_request(code)
        assert all(unit.estimated_minutes is None for unit in request.units), code


def test_materials_are_lesson_level_not_step_level() -> None:
    """One list for the whole lesson is what she writes; per unit it read as step-scoped,
    handing t3-w05's volume section "shapes of cylinders and spheres"."""
    request = _h1_request(ConditionCode.C1)
    assert request.lesson_context.instructional_materials == ["ruler", "grid paper"]
    assert _h1_request(ConditionCode.C0).lesson_context.instructional_materials == []


def test_no_condition_receives_the_note_derived_instructional_type() -> None:
    """It is derived from ``blocks``, a parse of her NOTE on a field plan.

    Lossy as well as misplaced: it collapses the SET of block types to one of three
    words, and on `t3-w05`'s volume step the parse read four worked examples as
    explanations and produced "explain_only" beside instructional_events
    ["present_content", "provide_learning_guidance"] — contradicting itself in one
    prompt. ``instructional_events`` carries the same signal from her Presentation
    column, ordered and plan-sourced.
    """
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        request = _h1_request(code)
        assert all(unit.instructional_type is None for unit in request.units), code


def test_c1_carries_the_evaluation_question_but_never_its_answer() -> None:
    """The task is plan evidence; the mathematics that answers it is not.

    No field plan in the study has an answer key — she wrote none. Where one is present
    it was computed downstream, and rendering it put solved mathematics into the
    condition defined as the plan WITHOUT the note: `t3-w02` carried nine and the other
    four lessons none, so C1 was materially richer on one lesson for a reason unrelated
    to her planning.
    """
    plan = deepcopy(SESSION_PLAN_DICT)
    plan["steps"][-1]["blocks"] = [
        {
            "id": "s3:q1",
            "type": "practice",
            "question": "Find the area of a 6cm by 4cm rectangle.",
            "answer": "24cm^2",
            "lesson_objective_id": "lop01",
        }
    ]
    session_plan = SessionPlanView.model_validate(plan)
    request = BUILDER.build(
        session_plan=session_plan,
        policy=profile_for(Hypothesis.H1, ConditionCode.C1),
        sources=LessonSources.unresolved(session_plan.references),
    )
    points = [point for unit in request.units for point in unit.assessment_points]
    assert points == ["Find the area of a 6cm by 4cm rectangle."]


def test_c1_never_receives_classroom_choreography() -> None:
    """The pack is written to a learner revising alone; the room is not its subject.

    Activities are who-did-what — "teacher solves some questions on the board",
    "student copy worked examples into their notes". ``artefact_spec`` forbids writing
    about the lesson as an event, so sending them hands the model a block it is told to
    ignore. Their pedagogical content, explain/example/practice, is in
    ``instructional_type`` already.
    """
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        request = _h1_request(code)
        assert all(unit.activities == [] for unit in request.units), code


def test_c1_never_receives_the_step_content_paragraph() -> None:
    """C1 is plan structure WITHOUT the note, and ``content`` is not reliably structure.

    It repeats the activities as one paragraph, and on four of the frozen set's core
    steps it carries the note itself — `t3-w06`'s construction procedure, `t2-w09`'s
    bracket sign rule. Sending it handed C1 the very material that defines C2.
    """
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        request = _h1_request(code)
        assert all(unit.step_content is None for unit in request.units), code


def test_no_condition_receives_a_step_title() -> None:
    """A step title is the transcriber's, not hers.

    She writes a bare label — "STEP 1:", "Step II" — and runs the narration on the same
    line; verified against the page images for `t2-w09`, `t3-w06` and `t3-w09`. The one
    descriptor she wrote anywhere is `t3-w09`'s "Meaning of statistics". Every other
    title paraphrases the step's OBJECTIVE, which the unit already carries verbatim, so
    the field adds nothing and sources nothing.
    """
    for code in (ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        request = _h1_request(code)
        assert all(unit.step_title is None for unit in request.units), code


def test_c2_adds_scoped_source_evidence() -> None:
    request = _h1_request(ConditionCode.C2)
    assert all(len(unit.source_evidence) == 2 for unit in request.units)
    assert request.units[0].source_evidence[0].source_ref == "REF-1"
    assert request.policy.require_source_refs is True
    assert request.policy.use_only_provided_sources is True


def test_c3_differs_from_c2_only_by_validation() -> None:
    c2 = profile_for(Hypothesis.H1, ConditionCode.C2)
    c3 = profile_for(Hypothesis.H1, ConditionCode.C3)
    assert c2.validation.enabled is False
    assert c3.validation.enabled is True
    assert c3.validation.retry_on_failure is True
    assert c2.context == c3.context and c2.retrieval == c3.retrieval


def test_c4_forks_c3_rather_than_regenerating() -> None:
    # C4 is a teacher-validation gate over C3's pack, not a fresh generation: it reuses
    # C3's generation result. C0-C3 each own their generation (no reuse).
    c4 = profile_for(Hypothesis.H1, ConditionCode.C4)
    assert c4.generated_by == ConditionCode.C3
    for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        assert profile_for(Hypothesis.H1, code).generated_by == code


def test_h2_p0_reuse_p1_personalises() -> None:
    assert H2_CONDITION_PROFILES[ConditionCode.P0].personalisation.mode == "reuse_base"
    assert H2_CONDITION_PROFILES[ConditionCode.P1].personalisation.mode == "objective_indexed"
    assert H2_CONDITION_PROFILES[ConditionCode.P1].validation.enabled is True


def _good_sections() -> list[ReviewPackSection]:
    return [
        ReviewPackSection(
            section_id=f"sec-{obj}",
            title=f"Section {obj}",
            lesson_objective_id=obj,
            blocks=[
                ReviewPackBlock(
                    block_id=f"b-{obj}",
                    block_type="explanation",
                    text="...",
                    lesson_objective_id=obj,
                    source_refs=["REF-1"],
                )
            ],
            practice=[
                ReviewPackPracticeItem(item_id=f"p-{obj}", prompt="Find the area.", answer="15")
            ],
            source_refs=["REF-1"],
        )
        for obj in ("lop01", "lop02")
    ]


def test_validator_passes_on_good_c3_pack() -> None:
    request = _h1_request(ConditionCode.C3)
    result = ReviewPackStructuralValidator().validate(
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sections=_good_sections(),
        request=request,
    )
    assert result.passed is True
    assert {check.check for check in result.checks} == {
        "objective_coverage",
        "scope_compliance",
        "source_refs_present",
        "source_refs_valid",
        "practice_is_checkable",
    }


def test_validator_fails_on_missing_objective() -> None:
    request = _h1_request(ConditionCode.C3)
    sections = _good_sections()[:1]  # drop lop02
    result = ReviewPackStructuralValidator().validate(
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sections=sections,
        request=request,
    )
    assert result.passed is False
    coverage = next(c for c in result.checks if c.check == "objective_coverage")
    assert coverage.passed is False and "lop02" in coverage.details["missing"]


def test_validator_fails_on_invalid_source_ref() -> None:
    request = _h1_request(ConditionCode.C3)
    sections = _good_sections()
    sections[0].blocks[0].source_refs = ["REF-99"]
    sections[0].source_refs = ["REF-99"]
    result = ReviewPackStructuralValidator().validate(
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sections=sections,
        request=request,
    )
    refs_valid = next(c for c in result.checks if c.check == "source_refs_valid")
    assert refs_valid.passed is False and "REF-99" in refs_valid.details["invalid_refs"]


def test_validator_objective_preservation_for_p1() -> None:
    request = _h1_request(ConditionCode.C3)  # reuse units for objectives
    base = _good_sections()
    candidate = _good_sections()[:1]  # personalisation dropped lop02
    result = ReviewPackStructuralValidator().validate(
        policy=profile_for(Hypothesis.H2, ConditionCode.P1),
        sections=candidate,
        request=request,
        base_sections=base,
    )
    preservation = next(c for c in result.checks if c.check == "objective_preservation")
    assert preservation.passed is False and "lop02" in preservation.details["dropped"]


def test_h1_registry_is_consistent_and_includes_c4() -> None:
    # The registry is the single source of truth: each entry is keyed by its own
    # condition_code, so consumers can derive the set without hardcoding it. C4 adds the
    # teacher-validation gate over C3 — assert it's wired rather than pinning the full set,
    # so adding a future condition does not break this test.
    for code, profile in H1_CONDITION_PROFILES.items():
        assert profile.condition_code == code
    assert ConditionCode.C4 in H1_CONDITION_PROFILES
    assert H1_CONDITION_PROFILES[ConditionCode.C4].teacher_validation.enabled is True
    # Only C4 carries the teacher-validation gate; the runner lands C4 artefacts as
    # "pending" (teacher review queue) and C0-C3 as "approved" based on exactly this flag.
    for code in (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3):
        assert H1_CONDITION_PROFILES[code].teacher_validation.enabled is False


def test_artefact_adapter_produces_valid_review_pack_manifest() -> None:
    from datetime import datetime, timezone

    from app.domains.artefacts.core.domain.types import ArtefactScope
    from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
        sections_to_review_pack_manifest,
    )
    from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
        LessonContextForGeneration,
    )
    from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack

    manifest = sections_to_review_pack_manifest(
        sections=_good_sections(),
        artefact_id="AT-test",
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL,
        lesson_context=LessonContextForGeneration(
            subject="Mathematics",
            grade_level="JSS1",
            topic="Area",
            lesson_objectives=["lop01", "lop02"],
        ),
        created_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
        lesson_plan_objectives=[{"lesson_objective_id": "lop01", "objective_text": "..."}],
    )
    # The manifest must validate as a PostClassReviewPack so the rater UI renders it.
    pack = PostClassReviewPack.model_validate(manifest)
    assert len(pack.steps) == 2
    assert {step.lesson_objective_id for step in pack.steps} == {"lop01", "lop02"}
    # Instructional blocks map to explanation; a practice item keeps its own type so the
    # renderer can place its answer after the activities rather than under the question.
    assert [block.type for block in pack.steps[0].blocks] == ["explanation", "practice"]
    # Provenance travels beside the prose, never inside it: a rater reads the
    # content, and a citation marker there both breaks blinding and reads as
    # bibliography to a student.
    explanation = pack.steps[0].blocks[0]
    assert explanation.source_refs == ["REF-1"]
    assert "REF-1" not in explanation.content
    practice = pack.steps[0].blocks[1]
    assert practice.question == "Find the area."
    assert practice.answer == "15"


# --- scoped note evidence (C2+) -------------------------------------------------------
# The plan's own step content is withheld from C1 and re-enters at C2 as cited evidence
# for the one step it belongs to. Before this, `evidence_scope` was read nowhere: every
# unit got the same list built from `plan.references`, truncated to
# `max_evidence_items_per_unit` across the WHOLE plan.

_PLAN_WITH_NOTE = SessionPlanView.model_validate(
    {
        **SESSION_PLAN_DICT,
        "steps": [
            {
                **SESSION_PLAN_DICT["steps"][0],
                "note": (
                    "A rectangle has four sides.\n\n"
                    "#### Example 1.\n\nFind the area of a 6cm by 4cm rectangle.\n\n"
                    "**Solution**\n\n6 x 4 = 24 square centimetres."
                ),
            },
            {**SESSION_PLAN_DICT["steps"][1], "note": "Gardens are rectangles too."},
            SESSION_PLAN_DICT["steps"][2],
        ],
    }
)

#: The same lesson as the app drafts it: typed blocks in each step, and no lesson note.
_PLAN_WITHOUT_NOTE = SessionPlanView.model_validate(
    {
        **SESSION_PLAN_DICT,
        "steps": [
            {
                **SESSION_PLAN_DICT["steps"][0],
                "blocks": [
                    {"id": "s1:b1", "type": "explanation", "content": "A rectangle has four sides."}
                ],
            },
            SESSION_PLAN_DICT["steps"][1],
            SESSION_PLAN_DICT["steps"][2],
        ],
    }
)


def _note_units(condition: ConditionCode):
    return BUILDER.build(
        session_plan=_PLAN_WITH_NOTE,
        policy=profile_for(Hypothesis.H1, condition),
        sources=LessonSources.unresolved(_PLAN_WITH_NOTE.references),
    ).units


def _evidence_refs(expert: ExpertSources) -> list[str]:
    units = BUILDER.build(
        session_plan=_PLAN_WITH_NOTE,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=replace(LessonSources.unresolved(_PLAN_WITH_NOTE.references), expert=expert),
    ).units
    return [item.source_ref for item in units[0].source_evidence]


def test_textbook_grounds_a_step_in_the_references_though_it_has_a_note() -> None:
    assert _evidence_refs(ExpertSources.TEXTBOOK) == ["REF-1", "REF-2"]


def test_both_grounds_a_step_in_its_note_then_the_references() -> None:
    note = _evidence_refs(ExpertSources.LESSON_NOTE)
    assert note and "REF-1" not in note
    assert _evidence_refs(ExpertSources.BOTH) == [*note, "REF-1", "REF-2"]


def test_c1_never_sees_the_note_even_when_the_plan_carries_one() -> None:
    assert all(not unit.source_evidence for unit in _note_units(ConditionCode.C1))


def test_c2_evidence_is_the_step_s_own_note_and_nothing_else() -> None:
    units = _note_units(ConditionCode.C2)
    assert [len(unit.source_evidence) for unit in units] == [1, 1]
    first, second = (unit.source_evidence[0] for unit in units)
    # The model cites this, so it names the thing — never a record key, and never the
    # step's planning label (her headings are a bare "STEP 1:").
    assert (first.source_ref, second.source_ref) == (EVIDENCE_LABEL, EVIDENCE_LABEL)
    assert "s1" not in (first.source_ref, second.source_ref)
    # No cross-contamination: step 2's note must not reach step 1, nor the reverse.
    assert "Gardens" not in first.excerpt
    assert "rectangle has four sides" not in second.excerpt


def test_c2_evidence_keeps_a_worked_example_s_working() -> None:
    """The note reaches the model whole: a worked example's working as well as its problem."""
    excerpt = _note_units(ConditionCode.C2)[0].source_evidence[0].excerpt
    assert "Find the area of a 6cm by 4cm rectangle." in excerpt
    assert "6 x 4 = 24 square centimetres." in excerpt


def test_a_step_without_a_lesson_note_is_grounded_in_the_plan_s_references() -> None:
    """A plan's own blocks are the plan, not a lesson note, so they never stand in for one."""
    units = BUILDER.build(
        session_plan=_PLAN_WITHOUT_NOTE,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=LessonSources.unresolved(_PLAN_WITHOUT_NOTE.references),
    ).units

    evidence = units[0].source_evidence
    assert [item.source_ref for item in evidence] == ["REF-1", "REF-2"]
    assert all("four sides" not in item.excerpt for item in evidence)


_VERBATIM_NOTE = (
    "**Procedures:**\n\n1. Open a pair of compasses.\n\n"
    "**fig-10.** The line segment $AB$.\n\n"
    "\\begin{center}\n\\begin{tikzpicture}\n\\draw (0,0) -- (7,0);\n"
    "\\end{tikzpicture}\n\\end{center}"
)


def test_c2_evidence_is_the_note_with_drawings_as_references() -> None:
    """Her prose reaches the model verbatim; each drawing becomes a reference.

    The typed ``blocks`` are a lossy parse (never mixed in when a verbatim ``note``
    exists). The TikZ source is data the model is forbidden to reproduce and the
    figure rides with the section as an object — so in the PROMPT the code is
    replaced by a pointer to that attached figure, caption intact. The note on
    disk stays byte-for-byte verbatim.
    """
    plan = SessionPlanView.model_validate(
        {
            **SESSION_PLAN_DICT,
            "steps": [
                {
                    **SESSION_PLAN_DICT["steps"][0],
                    "note": _VERBATIM_NOTE,
                    "blocks": [{"id": "s1:b1", "type": "explanation", "content": "lossy parse"}],
                },
                SESSION_PLAN_DICT["steps"][1],
                SESSION_PLAN_DICT["steps"][2],
            ],
        }
    )
    units = BUILDER.build(
        session_plan=plan,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=LessonSources.unresolved(plan.references),
    ).units
    excerpt = units[0].source_evidence[0].excerpt
    assert "**Procedures:**" in excerpt and "**fig-10.** The line segment $AB$." in excerpt
    assert "tikzpicture" not in excerpt
    assert "[drawing attached to this section as fig-10]" in excerpt
    assert "lossy parse" not in excerpt


def test_her_drawings_ride_with_the_note_as_attached_figures() -> None:
    """A note that draws a figure yields a figure block the pack can contain.

    Without this, evidence conditions read her drawings but can attach nothing, and
    packs point at pictures they do not carry ("as shown", "look at the diagram").
    """
    plan = SessionPlanView.model_validate(
        {
            **SESSION_PLAN_DICT,
            "steps": [
                {**SESSION_PLAN_DICT["steps"][0], "note": _VERBATIM_NOTE},
                SESSION_PLAN_DICT["steps"][1],
                SESSION_PLAN_DICT["steps"][2],
            ],
        }
    )
    for code, expected in ((ConditionCode.C1, 0), (ConditionCode.C2, 1)):
        units = BUILDER.build(
            session_plan=plan,
            policy=profile_for(Hypothesis.H1, code),
            sources=LessonSources.unresolved(plan.references),
        ).units
        assert len(units[0].source_figures) == expected, code
    figure = (
        BUILDER.build(
            session_plan=plan,
            policy=profile_for(Hypothesis.H1, ConditionCode.C2),
            sources=LessonSources.unresolved(plan.references),
        )
        .units[0]
        .source_figures[0]
    )
    assert figure.variant == "diagram_tikz"
    assert figure.figure_ref == "fig-10"
    assert figure.caption == "The line segment $AB$."
    assert "tikzpicture" in figure.source_tikz


def test_source_markers_are_forbidden_in_the_prose() -> None:
    """C0/C1 carry no markers, so one leaking into C2's text identifies the condition."""
    summary = BUILDER.build(
        session_plan=_PLAN_WITH_NOTE,
        policy=profile_for(Hypothesis.H1, ConditionCode.C2),
        sources=LessonSources.unresolved(_PLAN_WITH_NOTE.references),
    ).policy.instruction_summary
    assert "Never write a source marker" in summary
    # The model is no longer asked to cite: a unit carries one note, so provenance
    # is stamped from the unit rather than claimed block by block.
    assert "source_refs" not in summary


def test_provenance_is_stamped_not_claimed() -> None:
    unit = _note_units(ConditionCode.C2)[0]
    draft = DraftSection(
        title="Area",
        instructional_support="Area is length x breadth.",
        worked_examples=[],
        practice=[],
    )
    section = section_from_draft(draft, unit)
    assert [block.source_refs for block in section.blocks if block.text] == [
        [unit.source_evidence[0].source_ref]
    ]


def test_an_ungrounded_unit_stamps_no_provenance() -> None:
    unit = _note_units(ConditionCode.C1)[0]
    assert unit.source_evidence == []
    draft = DraftSection(
        title="Area",
        instructional_support="Area is length x breadth.",
        worked_examples=[],
        practice=[],
    )
    assert section_from_draft(draft, unit).blocks[0].source_refs == []


def test_the_instruction_summary_does_not_vary_between_c0_and_c1() -> None:
    """It branched — "from the lesson objective only" against "from the provided
    lesson-plan step context" — which is a task difference between the two arms of the
    study's primary comparison. It reached no run, because the signature C0/C1 use
    carries no ``policy`` field, but the packed generator does carry one."""
    summaries = {
        instruction_summary(profile_for(Hypothesis.H1, code))
        for code in (ConditionCode.C0, ConditionCode.C1)
    }
    assert len(summaries) == 1


def test_a_question_never_carries_drawing_source() -> None:
    """Her `t3-w02` evaluation Q8 travelled as prose PLUS 286 characters of TikZ.

    Drawing source is content the model is forbidden to reproduce, and it reached a
    condition that receives no figures: it read the coordinates as a shape, flattened
    them to a list of sides and answered 27cm for a figure of about 32cm. The
    measurements are the question and stay; the source goes.
    """
    plan = deepcopy(SESSION_PLAN_DICT)
    plan["steps"][-1]["blocks"] = [
        {
            "id": "s3:q1",
            "type": "practice",
            "answer": "",
            "lesson_objective_id": "lop01",
            "question": "Calculate the perimeter of the figure below.\n\n"
            "\\begin{center}\n\\begin{tikzpicture}[scale=0.4]\n"
            "  \\draw (0,0)--(9,0)--(9,5)--(0,5)--cycle;\n"
            "  \\node[below] at (4.5,0) {9cm};\n  \\node[right] at (9,2.5) {5cm};\n"
            "\\end{tikzpicture}\n\\end{center}",
        }
    ]
    session_plan = SessionPlanView.model_validate(plan)
    request = BUILDER.build(
        session_plan=session_plan,
        policy=profile_for(Hypothesis.H1, ConditionCode.C1),
        sources=LessonSources.unresolved(session_plan.references),
    )
    points = [p for unit in request.units for p in unit.assessment_points]
    assert points == [
        "Calculate the perimeter of the figure below. "
        "[the figure is not included here, marked 9cm, 5cm]"
    ]


def test_a_withheld_field_is_absent_from_the_prompt_not_present_and_empty() -> None:
    """C0 was shown `"entry_behaviour": [], "instructional_materials": []`.

    The profile decides the CONTENT of those fields, but the whole model was serialised
    into the prompt, so the key survived with an empty value — telling the control arm
    that prior knowledge and materials exist for this lesson and were withheld from it.
    A control that is told what it is missing is not a control. ``prompt_unit`` had
    dropped empties from the unit since it was written; the lesson did not.

    Read off the frozen field plans rather than the fixture above: the fixture states
    neither field, so it cannot tell a withheld field from an absent one.
    """
    for case in json.loads(EVAL_SET_PATH.read_text())["cases"]:
        plan = SessionPlanView.model_validate(case["plan"])
        seen = {}
        for code in (ConditionCode.C0, ConditionCode.C1):
            request = BUILDER.build(
                session_plan=plan,
                policy=profile_for(Hypothesis.H1, code),
                sources=LessonSources.unresolved(plan.references),
            )
            seen[code] = prompt_lesson(request.lesson_context)
        where = case["lesson"]
        assert "entry_behaviour" not in seen[ConditionCode.C0], where
        assert "instructional_materials" not in seen[ConditionCode.C0], where
        assert not any(v in ([], {}, "", None) for v in seen[ConditionCode.C1].values()), where
        # C1 differs by carrying more, never by carrying the same keys emptied out.
        assert set(seen[ConditionCode.C0]) <= set(seen[ConditionCode.C1]), where
    # And the difference is not vacuous: her plans do state both.
    assert "entry_behaviour" in seen[ConditionCode.C1]
    assert "instructional_materials" in seen[ConditionCode.C1]


def test_every_generation_signature_takes_the_pruned_lesson() -> None:
    """A typed lesson_context field re-serialises the whole model and reinstates the leak.

    The pruning happens at the call site, so a signature still declaring
    ``LessonContextForGeneration`` would take the object and format it in full — which is
    how the empty fields reached C0 while ``prompt_lesson``'s counterpart for the unit
    had been in place for months.
    """
    signatures = [
        WriteSection,
        RepairSection,
        WriteObjectiveSection,
        WriteGroundedSection,
        WriteGroundedSectionFromSources,
    ]
    for signature in signatures:
        field = signature.input_fields["lesson_context"]
        assert field.annotation is dict, signature.__name__


def test_every_declared_check_has_an_owner() -> None:
    """A profile lists structural and prose checks in one tuple; both must be answerable.

    ``validate`` dropped anything outside its own dispatch with a bare ``if check in
    dispatch``, which is how it passes over the three the LM critic answers — and also how
    a name implemented NOWHERE would be dropped in silence and reported as a pass. The
    split is now named, so this can tell the two apart.
    """
    assert set(STRUCTURAL_CHECKS) | set(PROSE_CHECKS) == set(get_args(ValidationCheck))
    assert not set(STRUCTURAL_CHECKS) & set(PROSE_CHECKS)
    assert set(CONTENT_CHECKS.values()) == set(PROSE_CHECKS), (
        "a prose check no critic defect maps to"
    )
    validator = ReviewPackStructuralValidator()
    for registry in (H1_CONDITION_PROFILES, H2_CONDITION_PROFILES):
        for profile in registry.values():
            if profile.validation.enabled:
                validator.validate(
                    policy=profile, sections=[], request=_h1_request(ConditionCode.C0)
                )


def test_a_check_no_one_implements_fails_loudly() -> None:
    profile = H1_CONDITION_PROFILES[ConditionCode.C3].model_copy(
        update={
            "validation": H1_CONDITION_PROFILES[ConditionCode.C3].validation.model_copy(
                update={"checks": ("objective_coverage", "no_such_check")}
            )
        }
    )
    with pytest.raises(NotImplementedError, match="no_such_check"):
        ReviewPackStructuralValidator().validate(
            policy=profile, sections=[], request=_h1_request(ConditionCode.C0)
        )


def test_practice_without_an_answer_fails_validation() -> None:
    """The brief has always required it; nothing could check it until now.

    While the question and its answer were one paragraph of prose, "answers at the end"
    was a sentence the model could ignore, and it did — in 9 of 12 lesson/condition
    cells (issue #163). The answer is a field now, so this is a shape, not a hope.
    """
    sections = _good_sections()
    sections[0].practice[0].answer = "   "
    sections[1].practice = []
    result = ReviewPackStructuralValidator().validate(
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sections=sections,
        request=_h1_request(ConditionCode.C3),
    )
    assert result.passed is False
    failed = next(c for c in result.checks if c.check == "practice_is_checkable")
    assert failed.details == {
        "unanswered": ["p-lop01"],
        "sections_without_practice": ["sec-lop02"],
    }
