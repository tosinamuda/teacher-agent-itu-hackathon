"""No-LLM tests for the bake-off generation backends (architecture axis).

The LLM call is not exercised; these cover the deterministic glue: the monolithic
output->artifacts adapter, the synthetic cold-start record, and the backend factory.
"""

from __future__ import annotations

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonCurriculumContext,
    LessonGenerationSession,
    PreparedGenerationInputs,
    TextbookRecordPayload,
    build_scope_context,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import (
    normalize_textbook_records,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    CandidateKC,
    LessonPlanObjective,
    StepEvidencePlan,
)
from experiments.strategy_bakeoff.backends import (
    COLD_START_RECORD_ID,
    MonolithicScoredService,
    StagedScoredService,
    build_scored_service,
    synthetic_curriculum_record,
)
from experiments.strategy_bakeoff.monolithic_signature import (
    MonolithicArtifacts,
    adapt_prediction,
)


class _FakePrediction:
    """Stand-in for a dspy.Prediction with the monolithic output fields."""

    def __init__(self, **fields: object) -> None:
        self.__dict__.update(fields)


def _objective(oid: str, order: int) -> LessonPlanObjective:
    return LessonPlanObjective(
        lesson_objective_id=oid,
        objective_text=f"objective {oid}",
        objective_order=order,
        curriculum_objective_id=f"cur_{oid}",
        curriculum_objective_text=f"curriculum {oid}",
        kc_type="concept",
        kc_focus=f"focus {oid}",
    )


def _kc(oid: str) -> CandidateKC:
    return CandidateKC(
        kc_id=f"kc_{oid}",
        kc_type="concept",
        objective_text=f"objective {oid}",
        curriculum_objective_id=f"cur_{oid}",
        kc_focus=f"focus {oid}",
        supporting_record_ids=[COLD_START_RECORD_ID],
    )


def _evidence(oid: str) -> StepEvidencePlan:
    return StepEvidencePlan(
        lesson_objective_id=oid,
        selected_record_ids=[COLD_START_RECORD_ID],
        concept_record_ids=[COLD_START_RECORD_ID],
    )


def _inputs(records: list[TextbookRecordPayload]) -> PreparedGenerationInputs:
    session = LessonGenerationSession.model_validate(
        {
            "session_id": "s1",
            "subject": "Mathematics",
            "track": "core",
            "grade": "JSS1",
            "term": "First Term",
            "week": 1,
            "topic": "Fractions",
            "subtopic": "Convert fractions to decimals",
        }
    )
    curriculum = LessonCurriculumContext.model_validate(
        {
            "subject": "Mathematics",
            "track": "core",
            "grade": "JSS1",
            "term": "First Term",
            "week": 1,
            "topic": "Fractions",
            "subtopic": "Convert fractions to decimals",
            "theme": "Number",
            "entry_behaviour": ["knows fractions"],
            "instructional_materials": ["number cards"],
        }
    )
    return PreparedGenerationInputs(
        session=session,
        scope=build_scope_context(session),
        curriculum=curriculum,
        textbook_records=records,
        evidence_selection_strategy="cached",
    )


def test_adapt_prediction_maps_outputs_to_artifacts() -> None:
    prediction = _FakePrediction(
        lesson_plan_objectives=[_objective("lo1", 1), _objective("lo2", 2)],
        resolved_kcs=[_kc("lo1"), _kc("lo2")],
        step_evidence_plans=[_evidence("lo1"), _evidence("lo2")],
        core_steps=["core1", "core2"],
        global_steps="global_step_set",
        assessments=[
            AssessmentItem(
                kc_id="kc_lo1",
                question="q?",
                expected_answer="a",
                bloom_justification="recall",
            )
        ],
        misconceptions=["confuses numerator/denominator"],
    )
    artifacts = adapt_prediction(prediction, _inputs([]))

    assert isinstance(artifacts, MonolithicArtifacts)
    # list -> dict keyed by lesson_objective_id
    assert set(artifacts.step_evidence_plans) == {"lo1", "lo2"}
    # one evidence summary per objective
    assert len(artifacts.evidence_summaries) == 2
    assert {s["lesson_objective_id"] for s in artifacts.evidence_summaries} == {"lo1", "lo2"}
    # kc_plan pulls misconceptions from the prediction and context from curriculum
    assert artifacts.kc_plan.misconceptions == ["confuses numerator/denominator"]
    assert artifacts.kc_plan.theme == "Number"
    assert artifacts.kc_plan.instructional_materials == ["number cards"]
    # passthroughs
    assert artifacts.core_steps == ["core1", "core2"]
    assert len(artifacts.resolved_kcs) == 2
    assert len(artifacts.assessment_items) == 1


def test_synthetic_record_is_a_valid_curriculum_only_exposition() -> None:
    record = synthetic_curriculum_record(
        {"subtopic": "Sum of angles of a triangle"},
        {
            "subtopic": "Sum of angles of a triangle",
            "curriculum_objectives": [
                {"objective_text": "State that angles in a triangle sum to 180"},
                {"objective_text": "Find a missing angle"},
            ],
        },
    )
    assert record["record_id"] == COLD_START_RECORD_ID
    assert record["record_type"] == "exposition"
    # content is curriculum-derived, and the dict parses as a real record payload
    parsed = TextbookRecordPayload.model_validate(record)
    assert parsed.record_id == COLD_START_RECORD_ID
    assert "missing angle" in parsed.content
    # REGRESSION GUARD: it must survive normalize_textbook_records (needs
    # type="textbook_record"), else the empty-records guard fires on S3.
    assert normalize_textbook_records([record]), "synthetic record was filtered out"


def test_synthetic_record_falls_back_when_no_objectives() -> None:
    record = synthetic_curriculum_record({"subtopic": "Topic X"}, {"subtopic": "Topic X"})
    assert "Topic X" in record["content"]


def test_factory_builds_each_architecture() -> None:
    assert isinstance(build_scored_service("staged", reasoning="cot"), StagedScoredService)
    assert isinstance(build_scored_service("staged", reasoning="predict"), StagedScoredService)
    assert isinstance(build_scored_service("monolithic", reasoning="cot"), MonolithicScoredService)
    assert isinstance(build_scored_service("monolithic", reasoning="rlm"), MonolithicScoredService)


def test_monolithic_react_builds_request_bound_agent() -> None:
    svc = build_scored_service("monolithic", reasoning="react")
    module = svc.generation_program
    # react has no static writer; the ReAct agent (with record-lookup tools) is
    # built per forward() because its tools need the request context.
    assert module.reasoning == "react"
    assert module.writer is None


_SESSION_CTX = {
    "session_id": "s1",
    "subject": "Mathematics",
    "track": "core",
    "grade": "JSS1",
    "term": "First Term",
    "week": 1,
    "topic": "Angles",
    "subtopic": "Sum of angles of a triangle",
}
# Curriculum context fields only (LessonCurriculumContext is extra="forbid", so no
# session-only keys like session_id).
_CURRICULUM_CTX = {
    "subject": "Mathematics",
    "track": "core",
    "grade": "JSS1",
    "term": "First Term",
    "week": 1,
    "topic": "Angles",
    "subtopic": "Sum of angles of a triangle",
    "curriculum_objectives": [{"objective_text": "State that angles in a triangle sum to 180"}],
}


def test_cold_start_injects_synthetic_when_only_nonrecord_refs_present() -> None:
    # S3 arrives with a subject-level ref (type "textbook", no chunks) that
    # normalize_textbook_records drops -> the synthetic record must still be added.
    nonrecord_refs = [{"type": "textbook", "source_id": "x", "title": "Maths", "chunk_refs": []}]
    for arch in ("staged", "monolithic"):
        service = build_scored_service(arch, reasoning="cot")
        inputs = service._prepare_inputs(
            session_context=_SESSION_CTX,
            curriculum_context=_CURRICULUM_CTX,
            reference_context=nonrecord_refs,
            requested_strategy=None,
        )
        ids = [r.record_id for r in inputs.textbook_records]
        assert ids == [COLD_START_RECORD_ID], f"{arch}: expected synthetic record, got {ids}"


def test_cold_start_does_not_inject_when_real_records_present() -> None:
    real_refs = [
        {
            "type": "textbook_record",
            "record_id": "ch01-b001",
            "section_ref": "ch01-b001",
            "content": "Angles in a triangle add up to 180 degrees.",
            "record_type": "exposition",
        }
    ]
    service = build_scored_service("staged", reasoning="cot")
    inputs = service._prepare_inputs(
        session_context=_SESSION_CTX,
        curriculum_context=_CURRICULUM_CTX,
        reference_context=real_refs,
        requested_strategy=None,
    )
    ids = [r.record_id for r in inputs.textbook_records]
    assert ids == ["ch01-b001"]  # no synthetic record added


def test_factory_rejects_unwired_and_unknown_combinations() -> None:
    with pytest.raises(NotImplementedError):
        build_scored_service("staged", reasoning="react")  # multi-sig react: Phase 2
    with pytest.raises(ValueError):
        build_scored_service("nonsense", reasoning="cot")
    with pytest.raises(ValueError):
        build_scored_service("monolithic", reasoning="bogus")
