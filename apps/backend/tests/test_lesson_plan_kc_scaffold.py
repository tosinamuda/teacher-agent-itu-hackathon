import json
from datetime import datetime, timezone
from types import SimpleNamespace

import dspy
import pytest
from pydantic import ValidationError

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute import (
    InfrastructureArtifactCache,
    KCPlanningResult,
    ObjectiveContextBuilder,
    PlanningQualityRow,
    Violation,
    render_infrastructure_quality_report,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.types import (
    CacheMetadata,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    prepare_generation_inputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.evidence_plan import (
    build_supported_evidence_plan,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    LessonStructure,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.generator import (
    CachedLessonDraftingModule,
    InfrastructurePlanningModule,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.textbook_support import (
    normalize_candidate_kcs_for_support,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    AtomicObjective,
    CandidateKC,
    CandidateKCPlan,
    CoreStepBlueprint,
    LessonPlanObjective,
    PlannerPlanStep,
    StepEvidencePlan,
)


def _curriculum_objectives() -> list[dict[str, object]]:
    return [
        {
            "curriculum_objective_id": "cur_obj01",
            "objective_text": "Convert fractions to decimals and percentages",
            "objective_order": 1,
        }
    ]


def _textbook_records() -> list[dict[str, object]]:
    return [
        {
            "type": "textbook_record",
            "record_id": "tb-def-01",
            "title": "Meaning of percentage",
            "record_type": "definition",
            "section_ref": "tb-def-01",
            "retrieval_text": "A percentage means per hundred.",
            "content": "Percentage means parts out of one hundred.",
            "asset_refs": [],
        },
        {
            "type": "textbook_record",
            "record_id": "tb-ex-01",
            "title": "Convert 1/2 to 50%",
            "record_type": "worked_example",
            "section_ref": "tb-ex-01",
            "retrieval_text": "Convert one-half to fifty percent.",
            "content": "Multiply by 100 to express the fraction as a percentage.",
            "asset_refs": [{"asset_type": "image", "src": "https://example.com/image.png"}],
        },
    ]


def _drafting_lesson_structure():
    lesson_objective = LessonPlanObjective.model_validate(
        {
            "lesson_objective_id": "lop01",
            "objective_text": "Explain what percentage means",
            "objective_order": 1,
            "curriculum_objective_id": "cur_obj01",
            "curriculum_objective_text": "Convert fractions to decimals and percentages",
            "kc_type": "concept",
            "kc_focus": "meaning of percentage",
            "source_form": None,
            "target_form": None,
        }
    )
    blueprint = CoreStepBlueprint.model_validate(
        {
            "step_id": "step01",
            "lesson_objective_id": "lop01",
            "kc_type": "concept",
            "required_block_types": ["explanation"],
        }
    )
    resolved_kc = CandidateKC.model_validate(
        {
            "kc_id": "kc01",
            "kc_type": "concept",
            "objective_text": "Explain what percentage means",
            "curriculum_objective_id": "cur_obj01",
            "kc_focus": "meaning of percentage",
            "supporting_record_ids": ["tb-def-01"],
        }
    )
    return LessonStructure(
        objectives=[lesson_objective],
        blueprints=[blueprint],
        objectives_by_id={"lop01": lesson_objective},
        kcs_by_objective_id={"lop01": resolved_kc},
    )


def _configure_kc_planning_pipeline(
    module: InfrastructurePlanningModule,
    *,
    candidate_kcs: list[dict[str, object]],
) -> None:
    class _NoopCache(InfrastructureArtifactCache):
        def get(
            self,
            *,
            subtopic_id: str,
            topic_key: str,
            textbook_hash: str,
            curriculum_hash: str,
        ) -> KCPlanningResult | None:
            return None

        def put(
            self,
            *,
            subtopic_id: str,
            textbook_hash: str,
            curriculum_hash: str,
            planning_result: KCPlanningResult,
        ) -> CacheMetadata:
            return CacheMetadata(
                infrastructure_version="test",
                textbook_hash=textbook_hash,
                curriculum_hash=curriculum_hash,
                model_name="test-model",
                computed_at=datetime.now(timezone.utc).isoformat(),
            )

    module.infrastructure_builder._cache = _NoopCache()
    module.infrastructure_builder._atomizer = lambda **_: [
        AtomicObjective.model_validate(
            {
                "atomic_objective_id": "cur_obj01-ao01",
                "curriculum_objective_id": "cur_obj01",
                "objective_text": "Convert fractions to decimals and percentages",
                "bloom_verb": "convert",
                "bloom_level": "apply",
                "objective_order": 1,
            }
        )
    ]
    module.infrastructure_builder._kc_extractor = lambda **_: CandidateKCPlan.model_validate(
        {"candidate_kcs": candidate_kcs}
    )
    module.infrastructure_builder._assessment_designer = (
        lambda *, kc, source_records, exercise_records, lesson_objective_id=None: (
            AssessmentItem.model_validate(
                {
                    "kc_id": kc.kc_id,
                    "lesson_objective_id": lesson_objective_id,
                    "question": f"How do you show {kc.kc_focus}?",
                    "expected_answer": kc.objective_text,
                    "bloom_justification": f"Targets {kc.bloom_level}.",
                }
            )
        )
    )


def _prepared_inputs():
    return prepare_generation_inputs(
        session_context={
            "session_id": "S1",
            "subject": "Mathematics",
            "track": "General",
            "grade": "JSS1",
            "term": "First Term",
            "week": 1,
            "topic": "Fractions",
            "subtopic": "Fractions and percentages",
            "duration_minutes": 40,
            "session_objectives": ["Convert fractions to decimals and percentages"],
            "theme": "Number",
        },
        curriculum_context={
            "curriculum_objectives": _curriculum_objectives(),
            "teacher_activities": [],
            "student_activities": [],
            "instructional_materials": [],
        },
        reference_context=_textbook_records(),
        requested_strategy="cached",
        default_strategy="cached",
    )


def test_kc_planning_module_accepts_multiple_kcs_for_one_curriculum_objective():
    module = InfrastructurePlanningModule()
    _configure_kc_planning_pipeline(
        module,
        candidate_kcs=[
            {
                "kc_id": "kc01",
                "kc_type": "concept",
                "objective_text": "Explain what percentage means",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "meaning of percentage",
                "supporting_record_ids": ["tb-def-01"],
            },
            {
                "kc_id": "kc02",
                "kc_type": "procedure",
                "objective_text": "Convert simple fractions to percentages",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "convert simple fractions to percentages",
                "source_form": "fraction",
                "target_form": "percentage",
                "supporting_record_ids": ["tb-ex-01"],
            },
        ],
    )

    result = module.forward(request=_prepared_inputs())

    assert len(result.combined_kc_plan.candidate_kcs) == 2
    assert len(result.lesson_structure.objectives) == 2
    assert [item.curriculum_objective_id for item in result.lesson_structure.objectives] == [
        "cur_obj01",
        "cur_obj01",
    ]


def test_normalize_candidate_kcs_downgrades_unsupported_procedure_to_concept():
    candidate_kcs = [
        CandidateKC.model_validate(
            {
                "kc_id": "kc01",
                "kc_type": "procedure",
                "objective_text": "Convert simple fractions to percentages",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "convert simple fractions to percentages",
                "source_form": "fraction",
                "target_form": "percentage",
                "supporting_record_ids": ["tb-def-01"],
            }
        )
    ]

    normalized = normalize_candidate_kcs_for_support(
        candidate_kcs,
        textbook_records=_textbook_records(),
    )

    assert normalized[0].kc_type == "concept"


def test_normalize_candidate_kcs_supplements_missing_concept_support():
    candidate_kcs = [
        CandidateKC.model_validate(
            {
                "kc_id": "kc01",
                "kc_type": "procedure",
                "objective_text": "Convert simple fractions to percentages",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "convert simple fractions to percentages",
                "source_form": "fraction",
                "target_form": "percentage",
                "supporting_record_ids": ["tb-block-01"],
            }
        )
    ]
    textbook_records = [
        *_textbook_records(),
        {
            "type": "textbook_record",
            "record_id": "tb-block-01",
            "title": "Percentage practice",
            "record_type": "exercise_block",
            "section_ref": "tb-block-01",
            "retrieval_text": "Convert simple fractions to percentages.",
            "content": "Practice converting fractions to percentages.",
            "asset_refs": [],
        },
    ]
    lesson_objective = LessonPlanObjective.model_validate(
        {
            "lesson_objective_id": "lop01",
            "objective_text": "Convert simple fractions to percentages",
            "objective_order": 1,
            "curriculum_objective_id": "cur_obj01",
            "curriculum_objective_text": "Convert fractions to decimals and percentages",
            "kc_type": "procedure",
            "kc_focus": "convert simple fractions to percentages",
            "source_form": "fraction",
            "target_form": "percentage",
        }
    )

    normalized = normalize_candidate_kcs_for_support(
        candidate_kcs,
        textbook_records=textbook_records,
    )

    assert "tb-def-01" in normalized[0].supporting_record_ids
    assert "tb-ex-01" in normalized[0].supporting_record_ids

    evidence_plan = build_supported_evidence_plan(
        lesson_objective=lesson_objective,
        candidate_kc=normalized[0],
        textbook_records=textbook_records,
    )

    assert evidence_plan is not None
    assert evidence_plan.concept_record_ids == ["tb-def-01"]
    assert evidence_plan.modeling_record_ids == ["tb-ex-01"]
    assert evidence_plan.practice_record_ids == ["tb-block-01"]


def test_build_supported_evidence_plan_uses_support_set_only():
    lesson_objective = LessonPlanObjective.model_validate(
        {
            "lesson_objective_id": "lop01",
            "objective_text": "Convert simple fractions to percentages",
            "objective_order": 1,
            "curriculum_objective_id": "cur_obj01",
            "curriculum_objective_text": "Convert fractions to decimals and percentages",
            "kc_type": "procedure",
            "kc_focus": "convert simple fractions to percentages",
            "source_form": "fraction",
            "target_form": "percentage",
        }
    )
    candidate_kc = CandidateKC.model_validate(
        {
            "kc_id": "kc01",
            "kc_type": "procedure",
            "objective_text": "Convert simple fractions to percentages",
            "curriculum_objective_id": "cur_obj01",
            "kc_focus": "convert simple fractions to percentages",
            "source_form": "fraction",
            "target_form": "percentage",
            "supporting_record_ids": ["tb-def-01", "tb-ex-01", "tb-item-01"],
        }
    )
    textbook_records = [
        *_textbook_records(),
        {
            "type": "textbook_record",
            "record_id": "tb-item-01",
            "title": "Convert 3/4 to 75%",
            "record_type": "exercise_item",
            "section_ref": "tb-item-01",
            "retrieval_text": "Convert three-quarters to seventy-five percent.",
            "content": "Multiply by 100 to write the fraction as a percentage.",
            "asset_refs": [],
        },
    ]

    evidence_plan = build_supported_evidence_plan(
        lesson_objective=lesson_objective,
        candidate_kc=candidate_kc,
        textbook_records=textbook_records,
    )

    assert evidence_plan is not None
    assert set(evidence_plan.selected_record_ids) <= set(candidate_kc.supporting_record_ids)
    assert evidence_plan.concept_record_ids == ["tb-def-01"]
    assert evidence_plan.modeling_record_ids == ["tb-ex-01"]
    assert evidence_plan.practice_record_ids == ["tb-item-01"]


def test_kc_planning_module_rejects_unknown_supporting_record_ids():
    module = InfrastructurePlanningModule()
    _configure_kc_planning_pipeline(
        module,
        candidate_kcs=[
            {
                "kc_id": "kc01",
                "kc_type": "concept",
                "objective_text": "Explain what percentage means",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "meaning of percentage",
                "supporting_record_ids": ["tb-def-01"],
            },
            {
                "kc_id": "kc02",
                "kc_type": "procedure",
                "objective_text": "Convert simple fractions to percentages",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "convert simple fractions to percentages",
                "source_form": "fraction",
                "target_form": "percentage",
                "supporting_record_ids": ["missing-record"],
            },
        ],
    )

    result = module.forward(request=_prepared_inputs())

    assert any(
        isinstance(violation, Violation) and violation.code == "source_id_not_found"
        for violation in result.violations
    )


def test_global_drafting_module_validates_core_step_output():
    module = CachedLessonDraftingModule(final_writer_mode="chain_of_thought")
    module.core_step_writer = lambda **_: SimpleNamespace(
        core_step={
            "step_id": "step01",
            "step_kind": "core",
            "kc_type": "concept",
            "lesson_objective_id": "lop01",
            "title": "Teach percentage meaning",
            "content": "Students attempt a quick task.",
            "blocks": [
                {
                    "id": "block01",
                    "type": "practice",
                    "question": "What does 50% mean?",
                    "answer": "Fifty out of one hundred.",
                }
            ],
            "estimated_minutes": 10,
            "activities": [
                {"who": "teacher", "what": "Ask a question."},
                {"who": "student", "what": "Answer the question."},
            ],
        }
    )
    lesson_structure = _drafting_lesson_structure()
    evidence_plan = StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": "lop01",
            "selected_record_ids": ["tb-def-01"],
            "concept_record_ids": ["tb-def-01"],
        }
    )

    with pytest.raises(ValueError, match="core steps require at least one explanation block"):
        module._draft_core_steps(
            lesson_structure=lesson_structure,
            evidence_by_objective={"lop01": evidence_plan},
            assessment_by_objective={},
            request=_prepared_inputs(),
        )


def test_a_retried_core_step_is_told_what_the_previous_attempt_got_wrong():
    module = CachedLessonDraftingModule(final_writer_mode="chain_of_thought")
    seen: list[list[str]] = []

    def core_step_writer(**inputs):
        seen.append(inputs["prior_violations"])
        return SimpleNamespace(
            core_step={
                "step_id": "step01",
                "step_kind": "core",
                "kc_type": "concept",
                "lesson_objective_id": "lop01",
                "title": "Teach percentage meaning",
                "content": "Explain what a percentage is.",
                "blocks": [{"id": "b1", "type": "explanation", "content": "Per hundred."}],
                "estimated_minutes": 10,
                "activities": [
                    {"who": "teacher", "what": "Explain."},
                    {"who": "student", "what": "Listen."},
                ],
            }
        )

    module.core_step_writer = core_step_writer
    evidence_plan = StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": "lop01",
            "selected_record_ids": ["tb-def-01"],
            "concept_record_ids": ["tb-def-01"],
        }
    )

    module._draft_core_steps(
        lesson_structure=_drafting_lesson_structure(),
        evidence_by_objective={"lop01": evidence_plan},
        assessment_by_objective={},
        request=_prepared_inputs(),
        prior_violations=["structural_violation: blocks.1.worked_example.source_refs"],
    )

    assert seen == [["structural_violation: blocks.1.worked_example.source_refs"]]


def test_the_planner_is_offered_no_source_refs_on_any_block():
    schema = json.dumps(PlannerPlanStep.model_json_schema())

    assert "source_refs" not in schema
    with pytest.raises(ValidationError, match="source_refs"):
        PlannerPlanStep.model_validate(
            {
                "step_id": "step01",
                "step_role": "intro",
                "title": "Warm-up",
                "content": "Recall.",
                "blocks": [
                    {"id": "b1", "type": "explanation", "content": "x", "source_refs": ["r1"]}
                ],
                "estimated_minutes": 5,
                "activities": [
                    {"who": "teacher", "what": "Ask."},
                    {"who": "student", "what": "Answer."},
                ],
            }
        )


def test_cached_evidence_drafting_module_uses_chain_of_thought_for_final_writing():
    module = CachedLessonDraftingModule(final_writer_mode="chain_of_thought")

    assert isinstance(module.core_step_writer, dspy.ChainOfThought)
    assert isinstance(module.global_step_writer, dspy.ChainOfThought)


def test_cached_evidence_drafting_module_assembles_evaluation_deterministically():
    module = CachedLessonDraftingModule(final_writer_mode="chain_of_thought")
    # The model now authors only the intro step; the evaluation step is assembled in code
    # from the curated assessment items, so a dropped/invalid block can never crash it.
    module.global_step_writer = lambda **_: SimpleNamespace(
        intro_step={
            "step_id": "intro01",
            "step_kind": "intro",
            "title": "Warm-up",
            "content": "Recall what students already know.",
            "blocks": [],
            "estimated_minutes": 5,
            "activities": [
                {"who": "teacher", "what": "Activate prior knowledge."},
                {"who": "student", "what": "Respond to the prompt."},
            ],
        }
    )

    global_steps = module._draft_global_steps(
        lesson_structure=_drafting_lesson_structure(),
        core_steps=[],
        evidence_summaries=[],
        request=_prepared_inputs(),
        assessment_by_objective={
            "lop01": AssessmentItem(
                kc_id="kc01",
                lesson_objective_id="lop01",
                question="What does 25% mean?",
                expected_answer="Twenty-five out of one hundred.",
                bloom_justification="Assesses understanding of percentages.",
            )
        },
    )

    assert global_steps.intro_step.step_kind == "intro"
    assert global_steps.evaluation_step.step_kind == "evaluation"
    assert [block.lesson_objective_id for block in global_steps.evaluation_step.blocks] == ["lop01"]
    assert global_steps.evaluation_step.blocks[0].question == "What does 25% mean?"


def test_context_assembler_uses_prior_subtopics_from_topic_catalog():
    assembler = ObjectiveContextBuilder(
        scope_context={
            "subject": "Mathematics",
            "grade": "JSS1",
            "topic_key": "jss1-math-percentages",
            "subtopic_id": "jss1-math-percentages-meaning",
            "topic": "Percentages",
            "subtopic": "Meaning of percentage",
        },
        curriculum_context={
            "entry_behaviour": ["Recall fractions."],
            "evaluation_guide": ["Ask one question."],
        },
        textbook_records=_textbook_records(),
        topics_enriched=[
            {
                "topic_key": "jss1-math-percentages",
                "subtopics": [
                    {
                        "subtopic_id": "jss1-math-percentages-intro",
                        "title": "Introduction to percentages",
                        "performance_objectives": ["Define percentage."],
                    },
                    {
                        "subtopic_id": "jss1-math-percentages-meaning",
                        "title": "Meaning of percentage",
                        "performance_objectives": ["Explain percentages."],
                    },
                ],
            }
        ],
    )

    context = assembler.assemble(
        AtomicObjective.model_validate(
            {
                "atomic_objective_id": "cur_obj01-ao01",
                "curriculum_objective_id": "cur_obj01",
                "objective_text": "Explain percentages.",
                "bloom_verb": "explain",
                "bloom_level": "understand",
                "objective_order": 1,
            }
        )
    )

    assert context.prior_subtopic_objectives == ["Define percentage."]


def test_kc_decomposition_cache_writes_per_atomic_objective_artifacts(tmp_path):
    atomic_objective = AtomicObjective.model_validate(
        {
            "atomic_objective_id": "cur_obj01-ao01",
            "curriculum_objective_id": "cur_obj01",
            "objective_text": "Explain percentages.",
            "bloom_verb": "explain",
            "bloom_level": "understand",
            "objective_order": 1,
        }
    )
    candidate_kc = CandidateKC.model_validate(
        {
            "kc_id": "cur_obj01-ao01-kc01",
            "kc_type": "concept",
            "objective_text": "Explain what percentage means",
            "curriculum_objective_id": "cur_obj01",
            "kc_focus": "meaning of percentage",
            "supporting_record_ids": ["tb-def-01"],
        }
    )
    assessment_item = AssessmentItem.model_validate(
        {
            "kc_id": candidate_kc.kc_id,
            "question": "What does 25% mean?",
            "expected_answer": "Twenty-five out of one hundred.",
            "bloom_justification": "Checks conceptual understanding.",
        }
    )
    lesson_assessment = assessment_item.model_copy(update={"lesson_objective_id": "lop01"})
    cache = InfrastructureArtifactCache(tmp_path)
    planning_result = KCPlanningResult(
        subtopic_id="jss1-math-percentages-meaning",
        topic_key="jss1-math-percentages",
        atomic_objectives=[atomic_objective],
        kc_plans={
            atomic_objective.atomic_objective_id: CandidateKCPlan.model_validate(
                {"candidate_kcs": [candidate_kc.model_dump()]}
            )
        },
        step_evidence_plans={
            "lop01": StepEvidencePlan.model_validate(
                {
                    "lesson_objective_id": "lop01",
                    "selected_record_ids": ["tb-def-01"],
                    "concept_record_ids": ["tb-def-01"],
                }
            )
        },
        assessment_items_by_atomic_objective={
            atomic_objective.atomic_objective_id: [assessment_item]
        },
        assessment_items={"lop01": lesson_assessment},
        lesson_structure=_drafting_lesson_structure(),
        combined_kc_plan=CandidateKCPlan.model_validate(
            {"candidate_kcs": [candidate_kc.model_dump()]}
        ),
        resolved_kcs=[candidate_kc],
        violations_by_atomic_objective={
            atomic_objective.atomic_objective_id: [
                Violation(code="type_inconsistency", message="Needs review.")
            ]
        },
        violations=[Violation(code="type_inconsistency", message="Needs review.")],
    )

    cache.put(
        subtopic_id=planning_result.subtopic_id,
        textbook_hash="textbook-hash",
        curriculum_hash="curriculum-hash",
        planning_result=planning_result,
    )
    loaded = cache.get(
        subtopic_id=planning_result.subtopic_id,
        topic_key=planning_result.topic_key,
        textbook_hash="textbook-hash",
        curriculum_hash="curriculum-hash",
    )

    subtopic_dir = next(tmp_path.iterdir())
    assert (subtopic_dir / "ao-01" / "assessment_items.json").exists()
    assert (subtopic_dir / "ao-01" / "verification.json").exists()
    assert loaded is not None
    assert (
        loaded.assessment_items_by_atomic_objective["cur_obj01-ao01"][0].kc_id == candidate_kc.kc_id
    )


def test_render_infrastructure_quality_report_includes_failure_reason():
    report = render_infrastructure_quality_report(
        [
            PlanningQualityRow(
                subtopic_id="jss1-math-percentages-meaning",
                violations=[
                    Violation(
                        code="zero_linked_textbook_records",
                        message="zero linked textbook records (cannot generate KCs)",
                    )
                ],
            )
        ]
    )

    assert "jss1-math-percentages-meaning" in report
    assert "Reason: zero linked textbook records (cannot generate KCs)" in report
