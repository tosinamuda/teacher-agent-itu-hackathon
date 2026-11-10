import asyncio
import logging
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute import KCPlanningResult
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    DspyStatusLogger,
    LessonGenerationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    service as generation_service_module,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    clean_latex as _clean_latex,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    normalize_session_plan_payload,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    build_lesson_structure_from_kcs,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.generator import (
    LessonGenerationArtifacts,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    CandidateKC,
    CandidateKCPlan,
    ExplanationBlock,
    GlobalStepSet,
    PlannerPlanStep,
    PracticeBlock,
    SessionPlan,
    StepEvidencePlan,
    VisualBlock,
    WorkedExampleBlock,
)
from app.shared.json_types import JsonObject


def _json_object(value: object) -> JsonObject:
    assert isinstance(value, dict)
    return cast(JsonObject, value)


def _json_object_list(value: object) -> list[JsonObject]:
    assert isinstance(value, list)
    return [_json_object(item) for item in value if isinstance(item, dict)]


def test_clean_latex_repairs_array_rows_before_hline():
    broken = (
        "\\begin{array}{|c|c|} \\hline \\text{t} & \\text{u} \\ \\hline "
        "1 & 0 \\ \\hline \\end{array}"
    )

    assert _clean_latex(broken) == (
        "\n$$\n\\begin{array}{|c|c|} \\hline \\text{t} & \\text{u} \\\\ \\hline "
        "1 & 0 \\\\ \\hline \\end{array}\n$$\n"
    )


def test_clean_latex_decodes_escaped_newlines_and_delimiters():
    raw = r"Digits: \(1,000,000,000,000\)\nWords: one trillion"

    assert _clean_latex(raw) == "Digits: $1,000,000,000,000$\nWords: one trillion"


def test_clean_latex_keeps_commands_that_begin_like_an_escaped_newline():
    r"""``\newline`` came out as a line break and ``ewline``, and ``\neq`` as ``eq``."""
    raw = "$$\n\\begin{array}{r}\n4\\newline\n7\n\\end{array}\n$$ and $x \\neq y$"

    assert _clean_latex(raw) == raw


def test_clean_latex_does_not_display_an_environment_that_is_displayed_already():
    """An environment after ``\\require`` inside ``$$`` was wrapped in a second ``$$`` pair."""
    raw = (
        "$$\n\\require{enclose}\n\\begin{array}{r}\n4\\\\\n"
        "7 \\enclose{longdiv}{30}\n\\end{array}\n$$"
    )

    assert _clean_latex(raw) == raw


def test_normalize_session_plan_payload_normalizes_saved_steps():
    session_plan = cast(
        JsonObject,
        {
            "steps": [
                {
                    "step_id": "step-core-01",
                    "step_kind": "core",
                    "instructional_type": "explain_practice",
                    "kc_type": "representation",
                    "lesson_objective_id": "obj01",
                    "title": "Practice",
                    "content": r"Write \(1,000,000,000,000\)\nIn words.",
                    "estimated_minutes": 10,
                    "activities": [],
                    "blocks": [
                        {
                            "id": "block-exp-01",
                            "type": "explanation",
                            "content": r"A trillion is \(1,000,000,000,000\).",
                        },
                        {
                            "id": "block-pr-01",
                            "type": "practice",
                            "question": r"Write \(1,000,000,000,000\) in words.",
                            "answer": r"Digits: \(1,000,000,000,000\)\nWords: one trillion",
                            "hints": [r"Start with \(1,000,000,000,000\)."],
                        },
                    ],
                }
            ]
        },
    )

    normalized = normalize_session_plan_payload(session_plan)
    normalized_step = _json_object_list(normalized["steps"])[0]
    block = _json_object_list(normalized_step["blocks"])[1]

    assert normalized_step["content"] == "Write $1,000,000,000,000$\nIn words."
    assert block["question"] == "Write $1,000,000,000,000$ in words."
    assert block["answer"] == "Digits: $1,000,000,000,000$\nWords: one trillion"
    assert block["hints"] == ["Start with $1,000,000,000,000$."]


def test_planner_step_accepts_visual_without_grounding_metadata():
    step = PlannerPlanStep.model_validate(
        {
            "step_id": "step-core-01",
            "step_kind": "core",
            "instructional_type": "explain_example_practice",
            "kc_type": "procedure",
            "lesson_objective_id": "obj01",
            "title": "Counting chart",
            "content": "Use the chart.",
            "estimated_minutes": 10,
            "activities": [],
            "blocks": [
                {
                    "id": "block-exp-01",
                    "type": "explanation",
                    "content": "Use the chart to model counting.",
                },
                {
                    "id": "block-we-01",
                    "type": "worked_example",
                    "problem": "Read the number shown on the chart.",
                    "steps": [{"label": "Step 1", "content": "Identify the digits."}],
                    "final_answer": "One million.",
                },
                {
                    "id": "block-pr-01",
                    "type": "practice",
                    "question": "Write the number shown on the chart.",
                    "answer": "One million.",
                    "hints": ["Read the place values from left to right."],
                },
                {
                    "id": "block-vis-01",
                    "type": "visual",
                    "variant": "image",
                    "url": "https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-004.png",
                    "caption": "Counting chart to one million and hundred-thousands.",
                },
            ],
        }
    )

    assert step.blocks[3].type == "visual"


def test_planner_step_derives_instructional_type_from_blocks():
    step = PlannerPlanStep.model_validate(
        {
            "step_id": "step-core-02",
            "step_kind": "core",
            "instructional_type": "practice",
            "kc_type": "concept",
            "lesson_objective_id": "obj02",
            "title": "Explain percentage",
            "content": "Explain what percentage means.",
            "estimated_minutes": 8,
            "activities": [],
            "blocks": [
                {
                    "id": "block-exp-02",
                    "type": "explanation",
                    "content": "A percentage means parts out of one hundred.",
                }
            ],
        }
    )

    assert step.instructional_type == "explain_only"


def test_lesson_generation_service_does_not_configure_dspy(monkeypatch):
    configure_calls: list[dict[str, object]] = []
    settings = SimpleNamespace(lm=object(), callbacks=[])
    created_modules: list[dict[str, object]] = []

    monkeypatch.setattr(generation_service_module.dspy, "settings", settings)
    monkeypatch.setattr(
        generation_service_module.dspy,
        "configure",
        lambda **kwargs: configure_calls.append(kwargs),
    )
    monkeypatch.setattr(
        generation_service_module,
        "LessonGenerationModule",
        lambda **kwargs: created_modules.append(kwargs) or {"module_kwargs": kwargs},
    )

    first = LessonGenerationService()
    second = LessonGenerationService(final_writer_mode="predict")

    assert not configure_calls
    assert first.lm is settings.lm
    assert second.lm is settings.lm
    assert created_modules[0]["final_writer_mode"] == "chain_of_thought"
    assert created_modules[1]["final_writer_mode"] == "predict"


def test_status_callback_logs_handled_chatadapter_parse_fallback_as_info(caplog):
    logger = logging.getLogger("tests.lesson_plan_drafting.status")
    callback = DspyStatusLogger(logger=logger)
    adapter = type("ChatAdapter", (), {"use_json_adapter_fallback": True})()

    caplog.set_level(logging.INFO, logger=logger.name)

    callback.on_adapter_parse_start(
        call_id="call-1",
        instance=adapter,
        inputs={"completion": "raw response"},
    )
    callback.on_adapter_parse_end(
        call_id="call-1",
        outputs=None,
        exception=ValueError("missing field header"),
    )

    assert "DSPy status: adapter parse fallback adapter=ChatAdapter" in caplog.text
    assert "fallback=JSONAdapter" in caplog.text
    assert not any(record.levelno >= logging.WARNING for record in caplog.records)


def test_status_callback_keeps_non_fallback_adapter_parse_failures_as_warnings(caplog):
    logger = logging.getLogger("tests.lesson_plan_drafting.status.no_fallback")
    callback = DspyStatusLogger(logger=logger)
    adapter = type("ChatAdapter", (), {"use_json_adapter_fallback": False})()

    caplog.set_level(logging.INFO, logger=logger.name)

    callback.on_adapter_parse_start(
        call_id="call-2",
        instance=adapter,
        inputs={"completion": "raw response"},
    )
    callback.on_adapter_parse_end(
        call_id="call-2",
        outputs=None,
        exception=ValueError("missing field header"),
    )

    assert "DSPy status: adapter parse failed adapter=ChatAdapter" in caplog.text
    assert any(record.levelno == logging.WARNING for record in caplog.records)


class _AsyncResponder:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)
        return self.payload

    async def acall(self, **kwargs):
        self.calls.append(kwargs)
        return self.payload

    async def aforward(self, **kwargs):
        self.calls.append(kwargs)
        return self.payload


def _planning_fixture(
    *,
    candidate_kcs: list[CandidateKC],
    curriculum_objectives: list[dict[str, object]],
    step_evidence_plans: dict[str, StepEvidencePlan],
    assessment_items: dict[str, AssessmentItem] | None = None,
    entry_behaviour: list[str] | None = None,
    instructional_materials: list[str] | None = None,
    from_cache: bool = True,
) -> tuple[KCPlanningResult, CandidateKCPlan]:
    combined_kc_plan = CandidateKCPlan.model_validate(
        {
            "candidate_kcs": [candidate_kc.model_dump() for candidate_kc in candidate_kcs],
            "entry_behaviour": entry_behaviour or [],
            "instructional_materials": instructional_materials or [],
        }
    )
    lesson_structure = build_lesson_structure_from_kcs(
        candidate_kcs,
        curriculum_objectives=curriculum_objectives,
    )
    planning_result = KCPlanningResult(
        subtopic_id="test-subtopic",
        topic_key="test-topic",
        atomic_objectives=[],
        kc_plans={},
        step_evidence_plans=step_evidence_plans,
        assessment_items_by_atomic_objective={},
        assessment_items=assessment_items or {},
        lesson_structure=lesson_structure,
        combined_kc_plan=combined_kc_plan,
        resolved_kcs=candidate_kcs,
        violations_by_atomic_objective={},
        violations=[],
        from_cache=from_cache,
    )
    return planning_result, combined_kc_plan


def test_lesson_plan_generator_runs_staged_flow(monkeypatch, tmp_path):
    monkeypatch.setattr(generation_service_module.dspy, "LM", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        generation_service_module.dspy.settings,
        "context",
        lambda **kwargs: nullcontext(),
    )
    monkeypatch.setattr(
        generation_service_module.DiagnosticLogWriter,
        "output_dir",
        lambda self: tmp_path,
    )

    kc_plan = {
        "candidate_kcs": [
            {
                "kc_id": "kc01",
                "kc_type": "procedure",
                "objective_text": "Convert simple fractions to decimals",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "convert simple fractions to decimals",
                "source_form": "fraction",
                "target_form": "decimal",
                "supporting_record_ids": [
                    "tb-decimals-concept",
                    "tb-decimals-model",
                    "tb-decimals-practice",
                ],
                "ordering_notes": "Teach after recalling fraction notation.",
            }
        ],
        "misconceptions": ["Confusing numerator and denominator roles."],
        "theme": "Number and Numeration",
        "entry_behaviour": ["Recall equivalent fractions."],
        "instructional_materials": ["Board", "Textbook"],
    }
    step_evidence_plan = {
        "lesson_objective_id": "lop01",
        "selected_record_ids": [
            "tb-decimals-concept",
            "tb-decimals-model",
            "tb-decimals-practice",
        ],
        "concept_record_ids": ["tb-decimals-concept"],
        "modeling_record_ids": ["tb-decimals-model"],
        "practice_record_ids": ["tb-decimals-practice"],
        "visual_record_ids": ["tb-decimals-model"],
    }
    core_step = {
        "step_id": "step01",
        "step_kind": "core",
        "instructional_type": "explain_example_practice",
        "kc_type": "procedure",
        "lesson_objective_id": "lop01",
        "title": "Fractions to decimals",
        "content": (
            "Guide learners through converting common fractions to decimals such as "
            "\\(\\frac{1}{2}\\)."
        ),
        "estimated_minutes": 20,
        "activities": [
            {"who": "teacher", "what": "Model the conversion."},
            {"who": "student", "what": "Follow the worked example."},
        ],
        "blocks": [
            {
                "id": "block-exp-01",
                "type": "explanation",
                "content": (
                    "A fraction like \\(\\frac{1}{2}\\) can be written as a decimal.\n\n"
                    "\\begin{array}{|c|c|}\\hline \\text{t} & \\text{u} \\\\ \\hline "
                    "1 & 0 \\\\ \\hline \\end{array}"
                ),
            },
            {
                "id": "block-we-01",
                "type": "worked_example",
                "problem": "Convert \\(\\frac{1}{2}\\) to a decimal.",
                "steps": [
                    {"label": "Step 1", "content": "Think of \\(\\frac{1}{2}\\) as division."},
                    {"label": "Step 2", "content": "Compute \\(1 \\div 2 = 0.5\\)."},
                ],
                "final_answer": "\\(0.5\\)",
            },
            {
                "id": "block-pr-01",
                "type": "practice",
                "question": "Convert \\(\\frac{3}{4}\\) to a decimal.",
                "answer": "\\(0.75\\)",
                "hints": ["Think of the fraction as division."],
            },
            {
                "id": "block-vis-01",
                "type": "visual",
                "variant": "image",
                "url": "https://invalid.example/invented.png",
                "caption": "A grounded textbook visual for \\(\\frac{1}{2}\\).",
            },
        ],
    }
    global_steps = {
        "intro_step": {
            "step_id": "step-intro",
            "step_kind": "intro",
            "instructional_type": None,
            "kc_type": None,
            "lesson_objective_id": None,
            "title": "Introduction",
            "content": "Activate prior knowledge about fractions.",
            "estimated_minutes": 5,
            "activities": [
                {"who": "teacher", "what": "Ask recall questions."},
                {"who": "student", "what": "Respond orally."},
            ],
            "blocks": [],
        },
        "evaluation_step": {
            "step_id": "step-evaluation",
            "step_kind": "evaluation",
            "instructional_type": "check",
            "kc_type": None,
            "lesson_objective_id": None,
            "title": "Evaluation",
            "content": "Check conversions across the lesson objective.",
            "estimated_minutes": 10,
            "activities": [
                {"who": "teacher", "what": "Ask exit questions."},
                {"who": "student", "what": "Solve quick checks."},
            ],
            "blocks": [
                {
                    "id": "block-eval-01",
                    "type": "practice",
                    "question": "Convert \\(\\frac{1}{4}\\) to a decimal.",
                    "answer": "\\(0.25\\)",
                    "hints": ["Divide numerator by denominator."],
                    "lesson_objective_id": "lop01",
                }
            ],
        },
    }

    candidate_kc = CandidateKC.model_validate(kc_plan["candidate_kcs"][0])
    step_evidence_plans = {"lop01": StepEvidencePlan.model_validate(step_evidence_plan)}
    planning_result, combined_kc_plan = _planning_fixture(
        candidate_kcs=[candidate_kc],
        curriculum_objectives=[
            {
                "curriculum_objective_id": "cur_obj01",
                "objective_text": "Convert fractions to decimals",
                "objective_order": 1,
            }
        ],
        step_evidence_plans=step_evidence_plans,
        entry_behaviour=["Recall equivalent fractions"],
        instructional_materials=["Board"],
    )
    fake_lesson_plan_module = _AsyncResponder(
        LessonGenerationArtifacts(
            planning_result=planning_result,
            kc_plan=combined_kc_plan,
            resolved_kcs=[candidate_kc],
            lesson_plan_objectives=planning_result.lesson_structure.objectives,
            core_step_blueprints=planning_result.lesson_structure.blueprints,
            assessment_items=[],
            step_evidence_plans=step_evidence_plans,
            core_steps=[PlannerPlanStep.model_validate(core_step)],
            global_steps=GlobalStepSet.model_validate(global_steps),
            evidence_summaries=[
                {
                    "lesson_objective_id": "lop01",
                    "records": [
                        {
                            "title": "Fractions to decimals",
                            "section_ref": "tb-decimals-model",
                            "record_type": "worked_example",
                            "asset_refs": [
                                {
                                    "asset_type": "image",
                                    "src": "https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-fractions-01.png",
                                }
                            ],
                        }
                    ],
                }
            ],
            planning_duration_ms=0,
            drafting_duration_ms=0,
            drafting_llm_call_estimate=0,
        )
    )

    generator = LessonGenerationService()
    generator.generation_program = fake_lesson_plan_module

    result = asyncio.run(
        generator.generate(
            session_context={
                "session_id": "S1",
                "subject": "Mathematics",
                "track": "General",
                "grade": "JSS1",
                "term": "First Term",
                "week": 1,
                "topic": "Fractions",
                "subtopic": "Fractions to decimals",
                "duration_minutes": 40,
                "session_objectives": ["Convert fractions to decimals"],
                "theme": "Number and Numeration",
                "performance_objectives": ["Convert fractions to decimals"],
                "entry_behaviour": ["Recall equivalent fractions"],
                "instructional_materials": ["Board"],
            },
            curriculum_context={
                "performance_objectives": ["Convert fractions to decimals"],
                "teacher_activities": ["Model the conversion"],
                "student_activities": ["Try the examples"],
                "instructional_materials": ["Board"],
                "evaluation_guide": ["Quick oral quiz"],
                "entry_behaviour": ["Recall equivalent fractions"],
            },
            reference_context=[
                {
                    "type": "textbook_record",
                    "title": "Fractions as decimals",
                    "section_ref": "tb-decimals-concept",
                    "record_id": "tb-decimals-concept",
                    "retrieval_text": (
                        "A fraction can be written as a decimal by dividing "
                        "the numerator by the denominator."
                    ),
                    "content": (
                        "A fraction can be written as a decimal by dividing "
                        "the numerator by the denominator."
                    ),
                    "record_type": "exposition",
                },
                {
                    "type": "textbook_record",
                    "title": "Fractions to decimals",
                    "section_ref": "tb-decimals-model",
                    "record_id": "tb-decimals-model",
                    "retrieval_text": "Convert fractions to decimals using worked examples.",
                    "content": "Convert fractions to decimals using worked examples.",
                    "record_type": "worked_example",
                    "asset_refs": [
                        {
                            "asset_type": "image",
                            "src": "https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-fractions-01.png",
                        }
                    ],
                    "source_html_path": "chapter-04.html",
                    "source_anchor_id": "ch04-b001",
                },
                {
                    "type": "textbook_record",
                    "title": "Practice converting fractions to decimals",
                    "section_ref": "tb-decimals-practice",
                    "record_id": "tb-decimals-practice",
                    "retrieval_text": (
                        "Practice converting fractions such as three-quarters to decimals."
                    ),
                    "content": "Practice converting fractions such as three-quarters to decimals.",
                    "record_type": "exercise_item",
                },
                {
                    "type": "textbook_record",
                    "title": "Highest common factor",
                    "section_ref": "tb-hcf",
                    "retrieval_text": "Find the highest common factor of whole numbers.",
                    "content": "Find the highest common factor of whole numbers.",
                    "record_type": "worked_example",
                },
            ],
            evidence_selection_strategy="per_kc_rlm",
        )
    )

    session_plan = SessionPlan.model_validate(result.session_plan)
    first_objective = session_plan.lesson_plan_objectives[0]
    assert first_objective.lesson_objective_id == "lop01"
    assert first_objective.kc_type == "procedure"
    assert first_objective.kc_focus == ("convert simple fractions to decimals")
    assert [step.step_kind for step in session_plan.steps] == [
        "intro",
        "core",
        "evaluation",
    ]
    assert session_plan.references == ["Fractions to decimals (tb-decimals-model)"]
    core_blocks = session_plan.steps[1].blocks
    explanation_block = cast(ExplanationBlock, core_blocks[0])
    worked_example_block = cast(WorkedExampleBlock, core_blocks[1])
    practice_block = cast(PracticeBlock, core_blocks[2])
    visual_block = cast(VisualBlock, core_blocks[3])
    assert explanation_block.content == (
        "A fraction like $\\frac{1}{2}$ can be written as a decimal.\n\n$$\n"
        "\\begin{array}{|c|c|}\\hline \\text{t} & \\text{u} \\\\ \\hline 1 & 0 "
        "\\\\ \\hline \\end{array}\n$$\n"
    )
    assert worked_example_block.problem == "Convert $\\frac{1}{2}$ to a decimal."
    assert worked_example_block.final_answer == "$0.5$"
    assert practice_block.question == "Convert $\\frac{3}{4}$ to a decimal."
    assert practice_block.answer == "$0.75$"
    assert visual_block.url == (
        "https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-fractions-01.png"
    )
    assert visual_block.source_record_id == "tb-decimals-model"
    assert visual_block.caption == "A grounded textbook visual for $\\frac{1}{2}$."
    assert visual_block.type == "visual"
    assert sorted(fake_lesson_plan_module.calls[0]) == ["prior_violations", "request"]
    # First refine attempt feeds no prior violations back to the program.
    assert fake_lesson_plan_module.calls[0]["prior_violations"] is None
    prompt_inputs = _json_object(result.run_metadata.get("prompt_inputs") or {})
    assert prompt_inputs["final_writer_mode"] == "chain_of_thought"
    assert prompt_inputs["evidence_selection_strategy"] == "cached"
    diagnostic_log_path = result.run_metadata.get("diagnostic_log_path")
    assert isinstance(diagnostic_log_path, str)
    diagnostic_log = Path(diagnostic_log_path).read_text(encoding="utf-8")
    assert "## Original Input" in diagnostic_log
    assert "**Subject**" in diagnostic_log
    assert "Mathematics" in diagnostic_log
    assert "## Original Curriculum Context" in diagnostic_log
    assert "Model the conversion" in diagnostic_log
    assert "Try the examples" in diagnostic_log
    assert "## Original Curriculum Objectives" in diagnostic_log
    assert "Convert fractions to decimals" in diagnostic_log
    assert "## Original Subtopic Textbook Content" in diagnostic_log
    assert (
        "A fraction can be written as a decimal by dividing the numerator by the denominator."
    ) in diagnostic_log
    assert "## Intermediate Data" in diagnostic_log
    assert "### Candidate KC Plan JSON" in diagnostic_log
    assert "## New Lesson Objectives" in diagnostic_log
    assert "lop01" in diagnostic_log
    assert "## New Knowledge Components" in diagnostic_log
    assert "kc01" in diagnostic_log
    assert "## Step Evidence Plans" in diagnostic_log
    assert "Selected Record IDs" in diagnostic_log
    assert "Modeling Record IDs" in diagnostic_log
    assert "tb-decimals-model" in diagnostic_log
    assert "### Evidence Summaries" in diagnostic_log
    assert "### Draft Core Steps" in diagnostic_log
    assert "## Consistency Checks" in diagnostic_log
    assert "## Final Output" in diagnostic_log
    assert "### Final Session Plan JSON" in diagnostic_log
    assert "## Final Session Plan Steps" in diagnostic_log
    assert "step01" in diagnostic_log


def test_lesson_plan_generator_uses_typed_planning_result(monkeypatch, tmp_path):
    monkeypatch.setattr(generation_service_module.dspy, "LM", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        generation_service_module.dspy.settings,
        "context",
        lambda **kwargs: nullcontext(),
    )
    monkeypatch.setattr(
        generation_service_module.DiagnosticLogWriter,
        "output_dir",
        lambda self: tmp_path,
    )

    candidate_kc = CandidateKC.model_validate(
        {
            "kc_id": "kc01",
            "kc_type": "concept",
            "objective_text": "Explain what percentage means",
            "curriculum_objective_id": "cur_obj01",
            "kc_focus": "meaning of percentage",
            "supporting_record_ids": ["tb-def-01"],
            "bloom_level": "understand",
        }
    )
    combined_kc_plan = CandidateKCPlan.model_validate(
        {
            "candidate_kcs": [candidate_kc.model_dump()],
            "entry_behaviour": ["Recall fractions as parts of a whole."],
            "instructional_materials": ["Board"],
        }
    )
    lesson_structure = build_lesson_structure_from_kcs(
        [candidate_kc],
        curriculum_objectives=[
            {
                "curriculum_objective_id": "cur_obj01",
                "objective_text": "Explain percentages",
                "objective_order": 1,
            }
        ],
    )
    assessment_item = AssessmentItem.model_validate(
        {
            "kc_id": "kc01",
            "lesson_objective_id": "lop01",
            "question": "What does 25% mean?",
            "expected_answer": "Twenty-five out of one hundred.",
            "bloom_justification": "Checks conceptual understanding of percentage.",
        }
    )
    planning_result = KCPlanningResult(
        subtopic_id="jss1-math-percentages-meaning",
        topic_key="jss1-math-percentages",
        atomic_objectives=[],
        kc_plans={},
        step_evidence_plans={
            "lop01": StepEvidencePlan.model_validate(
                {
                    "lesson_objective_id": "lop01",
                    "selected_record_ids": ["tb-def-01"],
                    "concept_record_ids": ["tb-def-01"],
                }
            )
        },
        assessment_items_by_atomic_objective={},
        assessment_items={"lop01": assessment_item},
        lesson_structure=lesson_structure,
        combined_kc_plan=combined_kc_plan,
        resolved_kcs=[candidate_kc],
        violations_by_atomic_objective={},
        violations=[],
        from_cache=True,
    )
    fake_lesson_plan_module = _AsyncResponder(
        LessonGenerationArtifacts(
            planning_result=planning_result,
            kc_plan=combined_kc_plan,
            resolved_kcs=[candidate_kc],
            lesson_plan_objectives=lesson_structure.objectives,
            core_step_blueprints=lesson_structure.blueprints,
            assessment_items=[assessment_item],
            step_evidence_plans=dict(planning_result.step_evidence_plans),
            core_steps=[
                PlannerPlanStep.model_validate(
                    {
                        "step_id": "step01",
                        "step_kind": "core",
                        "instructional_type": "explain_only",
                        "kc_type": "concept",
                        "lesson_objective_id": "lop01",
                        "title": "Meaning of percentage",
                        "content": "Explain percentage as parts out of one hundred.",
                        "estimated_minutes": 15,
                        "activities": [
                            {"who": "teacher", "what": "Explain percentage meaning."},
                            {"who": "student", "what": "Listen and answer examples."},
                        ],
                        "blocks": [
                            {
                                "id": "block-exp-01",
                                "type": "explanation",
                                "content": "A percentage means parts out of one hundred.",
                            }
                        ],
                    }
                )
            ],
            global_steps=GlobalStepSet.model_validate(
                {
                    "intro_step": {
                        "step_id": "intro01",
                        "step_kind": "intro",
                        "instructional_type": None,
                        "kc_type": None,
                        "lesson_objective_id": None,
                        "title": "Warm-up",
                        "content": "Recall fractions from previous lessons.",
                        "estimated_minutes": 5,
                        "activities": [
                            {"who": "teacher", "what": "Ask recall questions."},
                            {"who": "student", "what": "Respond orally."},
                        ],
                        "blocks": [],
                    },
                    "evaluation_step": {
                        "step_id": "eval01",
                        "step_kind": "evaluation",
                        "instructional_type": "check",
                        "kc_type": None,
                        "lesson_objective_id": None,
                        "title": "Exit ticket",
                        "content": "Check understanding of percentage.",
                        "estimated_minutes": 5,
                        "activities": [
                            {"who": "teacher", "what": "Ask the exit-ticket question."},
                            {"who": "student", "what": "Answer the exit-ticket question."},
                        ],
                        "blocks": [
                            {
                                "id": "block-eval-01",
                                "type": "practice",
                                "question": "What does 25% mean?",
                                "answer": "Twenty-five out of one hundred.",
                                "lesson_objective_id": "lop01",
                            }
                        ],
                    },
                }
            ),
            evidence_summaries=[
                {
                    "lesson_objective_id": "lop01",
                    "records": [
                        {
                            "title": "Meaning of percentage",
                            "section_ref": "tb-def-01",
                            "record_type": "definition",
                            "asset_refs": [],
                        }
                    ],
                }
            ],
            planning_duration_ms=0,
            drafting_duration_ms=0,
            drafting_llm_call_estimate=0,
        )
    )

    generator = LessonGenerationService()
    generator.generation_program = fake_lesson_plan_module

    result = asyncio.run(
        generator.generate(
            session_context={
                "session_id": "S2",
                "subject": "Mathematics",
                "track": "General",
                "grade": "JSS1",
                "term": "First Term",
                "week": 1,
                "topic": "Percentages",
                "subtopic": "Meaning of percentage",
                "duration_minutes": 25,
                "session_objectives": ["Explain percentages"],
                "theme": "Number",
            },
            curriculum_context={
                "performance_objectives": ["Explain percentages"],
                "teacher_activities": ["Explain percentages."],
                "student_activities": ["Answer examples."],
                "instructional_materials": ["Board"],
                "evaluation_guide": ["Ask one exit-ticket question."],
            },
            reference_context=[
                {
                    "type": "textbook_record",
                    "record_id": "tb-def-01",
                    "title": "Meaning of percentage",
                    "section_ref": "tb-def-01",
                    "retrieval_text": "A percentage means parts out of one hundred.",
                    "content": "A percentage means parts out of one hundred.",
                    "record_type": "definition",
                    "asset_refs": [],
                }
            ],
            evidence_selection_strategy="per_kc_rlm",
        )
    )

    session_plan = cast(dict[str, object], result.session_plan)
    assert session_plan["assessments"] == [
        {
            "question": "What does 25% mean?",
            "answer": "Twenty-five out of one hundred.",
            "rubric": "Checks conceptual understanding of percentage.",
        }
    ]
    generation_metrics = cast(
        dict[str, object],
        result.run_metadata.get("generation_metrics") or {},
    )
    assert generation_metrics.get("cached_planning") is True
    assert generation_metrics.get("assessment_item_count") == 1
    assert generation_metrics.get("llm_calls_planning") == 0
    assert generation_metrics.get("planning_duration_ms") == 0


def test_lesson_plan_generator_rejects_model_authored_references(monkeypatch):
    monkeypatch.setattr(generation_service_module.dspy, "LM", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        generation_service_module.dspy.settings,
        "context",
        lambda **kwargs: nullcontext(),
    )

    kc_plan = {
        "candidate_kcs": [
            {
                "kc_id": "kc01",
                "kc_type": "procedure",
                "objective_text": "Convert simple fractions to decimals",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "convert simple fractions to decimals",
                "supporting_record_ids": ["tb-decimals"],
            }
        ],
        "references": ["Invented reference"],
    }

    fake_lesson_plan_module = _AsyncResponder(SimpleNamespace(kc_plan=kc_plan))

    generator = LessonGenerationService()
    generator.generation_program = fake_lesson_plan_module

    with pytest.raises(ValueError, match="lesson_generation_program returned unsupported payload"):
        asyncio.run(
            generator.generate(
                session_context={
                    "session_id": "S1",
                    "subject": "Mathematics",
                    "track": "General",
                    "grade": "JSS1",
                    "term": "First Term",
                    "week": 1,
                    "topic": "Fractions",
                    "subtopic": "Fractions to decimals",
                    "duration_minutes": 40,
                    "session_objectives": ["Convert fractions to decimals"],
                },
                curriculum_context={
                    "performance_objectives": ["Convert fractions to decimals"],
                },
                reference_context=[
                    {
                        "type": "textbook_record",
                        "title": "Fractions to decimals",
                        "section_ref": "tb-decimals",
                        "retrieval_text": (
                            "Convert fractions to decimals and decimals to fractions."
                        ),
                    }
                ],
            )
        )


def test_lesson_plan_generator_supports_global_evidence_strategy(monkeypatch):
    monkeypatch.setattr(generation_service_module.dspy, "LM", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        generation_service_module.dspy.settings,
        "context",
        lambda **kwargs: nullcontext(),
    )

    kc_plan = {
        "candidate_kcs": [
            {
                "kc_id": "kc01",
                "kc_type": "concept",
                "objective_text": "Explain the meaning of a fraction",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "meaning of a fraction",
                "supporting_record_ids": ["tb-fractions-01"],
            },
            {
                "kc_id": "kc02",
                "kc_type": "representation",
                "objective_text": "Write simple fractions in words and symbols",
                "curriculum_objective_id": "cur_obj01",
                "kc_focus": "write simple fractions in words and symbols",
                "source_form": "words",
                "target_form": "symbols",
                "supporting_record_ids": ["tb-fractions-02-note", "tb-fractions-02-item"],
            },
        ],
    }
    all_step_evidence_plans = {
        "lop01": StepEvidencePlan.model_validate(
            {
                "lesson_objective_id": "lop01",
                "selected_record_ids": ["tb-fractions-01"],
                "concept_record_ids": ["tb-fractions-01"],
                "modeling_record_ids": [],
                "practice_record_ids": [],
                "visual_record_ids": [],
            }
        ),
        "lop02": StepEvidencePlan.model_validate(
            {
                "lesson_objective_id": "lop02",
                "selected_record_ids": ["tb-fractions-02-note", "tb-fractions-02-item"],
                "concept_record_ids": ["tb-fractions-02-note"],
                "modeling_record_ids": ["tb-fractions-02-item"],
                "practice_record_ids": ["tb-fractions-02-item"],
                "visual_record_ids": [],
            }
        ),
    }
    core_steps = [
        {
            "step_id": "step01",
            "step_kind": "core",
            "instructional_type": "explain_only",
            "kc_type": "concept",
            "lesson_objective_id": "lop01",
            "title": "Meaning of fraction",
            "content": "Explain the meaning of a fraction.",
            "estimated_minutes": 15,
            "activities": [
                {"who": "teacher", "what": "Define fraction."},
                {"who": "student", "what": "Listen and respond."},
            ],
            "blocks": [
                {
                    "id": "block-exp-01",
                    "type": "explanation",
                    "content": "A fraction is part of a whole.",
                }
            ],
        },
        {
            "step_id": "step02",
            "step_kind": "core",
            "instructional_type": "explain_example_practice",
            "kc_type": "representation",
            "lesson_objective_id": "lop02",
            "title": "Write fractions",
            "content": "Write fractions in words and symbols.",
            "estimated_minutes": 15,
            "activities": [
                {"who": "teacher", "what": "Model examples."},
                {"who": "student", "what": "Write examples."},
            ],
            "blocks": [
                {
                    "id": "block-exp-02",
                    "type": "explanation",
                    "content": "A fraction can be written with numerator and denominator.",
                },
                {
                    "id": "block-we-02",
                    "type": "worked_example",
                    "problem": "Write one-half as a symbol.",
                    "steps": [
                        {
                            "label": "Step 1",
                            "content": "Use 1 as the numerator and 2 as the denominator.",
                        }
                    ],
                    "final_answer": "$\\frac{1}{2}$",
                },
                {
                    "id": "block-pr-02",
                    "type": "practice",
                    "question": "Write one-half as a symbol.",
                    "answer": "$\\frac{1}{2}$",
                    "hints": ["Use numerator over denominator."],
                },
            ],
        },
    ]
    global_steps = {
        "intro_step": {
            "step_id": "step-intro",
            "step_kind": "intro",
            "instructional_type": None,
            "kc_type": None,
            "lesson_objective_id": None,
            "title": "Introduction",
            "content": "Recall sharing objects equally.",
            "estimated_minutes": 5,
            "activities": [],
            "blocks": [],
        },
        "evaluation_step": {
            "step_id": "step-evaluation",
            "step_kind": "evaluation",
            "instructional_type": "check",
            "kc_type": None,
            "lesson_objective_id": None,
            "title": "Evaluation",
            "content": "Classwork on fraction notation.",
            "estimated_minutes": 10,
            "activities": [],
            "blocks": [
                {
                    "id": "block-eval-01",
                    "type": "practice",
                    "question": "State what a fraction represents.",
                    "answer": "A fraction represents equal parts of a whole.",
                    "lesson_objective_id": "lop01",
                },
                {
                    "id": "block-eval-02",
                    "type": "practice",
                    "question": "Write one-half as a symbol.",
                    "answer": "$\\frac{1}{2}$",
                    "lesson_objective_id": "lop02",
                },
            ],
        },
    }

    candidate_kcs = [
        CandidateKC.model_validate(candidate_payload)
        for candidate_payload in kc_plan["candidate_kcs"]
    ]
    planning_result, combined_kc_plan = _planning_fixture(
        candidate_kcs=candidate_kcs,
        curriculum_objectives=[
            {
                "curriculum_objective_id": "cur_obj01",
                "objective_text": "Explain the meaning of a fraction",
                "objective_order": 1,
            }
        ],
        step_evidence_plans=all_step_evidence_plans,
    )
    fake_lesson_plan_module = _AsyncResponder(
        LessonGenerationArtifacts(
            planning_result=planning_result,
            kc_plan=combined_kc_plan,
            resolved_kcs=candidate_kcs,
            lesson_plan_objectives=planning_result.lesson_structure.objectives,
            core_step_blueprints=planning_result.lesson_structure.blueprints,
            assessment_items=[],
            step_evidence_plans=all_step_evidence_plans,
            core_steps=[PlannerPlanStep.model_validate(core_step) for core_step in core_steps],
            global_steps=GlobalStepSet.model_validate(global_steps),
            evidence_summaries=[
                {
                    "lesson_objective_id": "lop01",
                    "records": [
                        {
                            "title": "Meaning of a fraction",
                            "section_ref": "tb-fractions-01",
                            "record_type": "explanation",
                            "asset_refs": [],
                        }
                    ],
                },
                {
                    "lesson_objective_id": "lop02",
                    "records": [
                        {
                            "title": "Writing fractions",
                            "section_ref": "tb-fractions-02-item",
                            "record_type": "exercise_item",
                            "asset_refs": [],
                        }
                    ],
                },
            ],
            planning_duration_ms=0,
            drafting_duration_ms=0,
            drafting_llm_call_estimate=0,
        )
    )

    generator = LessonGenerationService()
    generator.generation_program = fake_lesson_plan_module

    result = asyncio.run(
        generator.generate(
            session_context={
                "session_id": "S2",
                "subject": "Mathematics",
                "track": "General",
                "grade": "JSS1",
                "term": "First Term",
                "week": 1,
                "topic": "Fractions",
                "subtopic": "Meaning of fraction",
                "duration_minutes": 40,
                "session_objectives": ["Explain the meaning of a fraction"],
            },
            curriculum_context={
                "curriculum_objectives": [
                    {
                        "curriculum_objective_id": "cur_obj01",
                        "objective_text": "Explain the meaning of a fraction",
                        "objective_order": 1,
                    }
                ],
                "teacher_activities": ["Use objects to explain fractions"],
                "student_activities": ["Write fractions"],
            },
            reference_context=[
                {
                    "type": "textbook_record",
                    "title": "Meaning of a fraction",
                    "section_ref": "tb-fractions-01",
                    "record_id": "tb-fractions-01",
                    "retrieval_text": "A fraction is part of a whole.",
                    "content": "A fraction is part of a whole.",
                    "record_type": "note",
                },
                {
                    "type": "textbook_record",
                    "title": "Writing fractions note",
                    "section_ref": "tb-fractions-02-note",
                    "record_id": "tb-fractions-02-note",
                    "retrieval_text": "Fractions can be written in words and symbols.",
                    "content": "Fractions can be written in words and symbols.",
                    "record_type": "note",
                },
                {
                    "type": "textbook_record",
                    "title": "Writing fractions",
                    "section_ref": "tb-fractions-02-item",
                    "record_id": "tb-fractions-02-item",
                    "retrieval_text": "Write fractions in words and symbols.",
                    "content": "Write fractions in words and symbols.",
                    "record_type": "exercise_item",
                },
            ],
            evidence_selection_strategy="global_rlm",
        )
    )

    prompt_inputs = cast(dict[str, object], result.run_metadata.get("prompt_inputs") or {})
    session_plan = cast(dict[str, object], result.session_plan)
    lesson_objectives = cast(list[object], session_plan.get("lesson_plan_objectives") or [])
    assert prompt_inputs.get("evidence_selection_strategy") == "cached"
    assert len(lesson_objectives) == 2
    assert fake_lesson_plan_module.calls
    assert "request" in fake_lesson_plan_module.calls[0]
