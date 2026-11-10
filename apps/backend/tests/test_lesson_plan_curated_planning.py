"""No-LLM tests for the authoritative curated planning path (Phase 10A).

Covers build_curated_planning -> curated_artifacts_to_kc_planning_result: the
KCPlanningResult the drafting stage consumes is correctly keyed (lopNN), evidence
is re-keyed from ao_id, modeling records stay distinct per objective, and the
all-ungrounded case raises (so the generator falls back to LLM planning).
"""

from __future__ import annotations

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.curated_planning import (  # noqa: E501
    build_curated_planning,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.curated_planning_adapter import (  # noqa: E501
    curated_artifacts_to_kc_planning_result,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.session_plan_rules import (
    MAX_LESSON_OBJECTIVES,
)

_SCOPE = {
    "subject": "Mathematics",
    "track": "core",
    "grade": "JSS1",
    "term": "First Term",
    "week": 1,
    "topic": "Fractions",
    "subtopic": "Convert fractions to decimals",
}


def _curated_objectives() -> list[dict]:
    return [
        {
            "ao_id": "ao-convert",
            "ao_order": 1,
            "curriculum_objective_id": "co-1",
            "objective_text": "Convert fractions to decimals",
            "bloom_level": "apply",
            "assessment": {"question": "Convert 1/2", "expected_answer": "0.5"},
            "record_links": [
                {"record_id": "r-concept", "role": "instruction", "link_order": 1},
                {"record_id": "r-model", "role": "worked_example", "link_order": 2},
                {"record_id": "r-ex", "role": "exercise", "link_order": 3},
            ],
            "practice_record_ids": [],
        },
        {
            "ao_id": "ao-define",
            "ao_order": 2,
            "curriculum_objective_id": "co-2",
            "objective_text": "Define a decimal fraction",
            "bloom_level": "understand",
            "assessment": None,
            "record_links": [
                {"record_id": "r-def", "role": "foundation", "link_order": 1},
            ],
            "practice_record_ids": [],
        },
    ]


_CURRICULUM = [
    {"curriculum_objective_id": "co-1", "objective_text": "Convert fractions to decimals"},
    {"curriculum_objective_id": "co-2", "objective_text": "Define decimal fractions"},
]


def test_curated_adapter_produces_aligned_kc_planning_result() -> None:
    artifacts = build_curated_planning(curated_objectives=_curated_objectives(), theme="Number")
    kpr = curated_artifacts_to_kc_planning_result(
        artifacts, scope_context=_SCOPE, curriculum_objectives=_CURRICULUM
    )

    objective_ids = [o.lesson_objective_id for o in kpr.lesson_structure.objectives]
    assert objective_ids == ["lop01", "lop02"]  # re-keyed by build_lesson_structure_from_kcs
    # evidence + assessments re-keyed to match the lesson structure ids
    assert set(kpr.step_evidence_plans) == {"lop01", "lop02"}
    assert all(plan.lesson_objective_id == key for key, plan in kpr.step_evidence_plans.items())
    # only the objective that carried a curated assessment yields one
    assert set(kpr.assessment_items) == {"lop01"}
    assert kpr.assessment_items["lop01"].lesson_objective_id == "lop01"
    # deterministic curated path: no LLM, no violations
    assert kpr.from_cache is False
    assert kpr.violations == []
    assert kpr.llm_calls_planning == 0


def test_curated_kc_types_and_distinct_modeling() -> None:
    artifacts = build_curated_planning(curated_objectives=_curated_objectives(), theme=None)
    kpr = curated_artifacts_to_kc_planning_result(
        artifacts, scope_context=_SCOPE, curriculum_objectives=_CURRICULUM
    )
    kc_by_obj = kpr.lesson_structure.kcs_by_objective_id
    # AO with a worked_example -> procedure; concept-only AO -> concept
    assert kc_by_obj["lop01"].kc_type == "procedure"
    assert kc_by_obj["lop02"].kc_type == "concept"
    # each objective's modeling records are its own (no reuse across objectives)
    modeling = [tuple(p.modeling_record_ids) for p in kpr.step_evidence_plans.values()]
    non_empty = [m for m in modeling if m]
    assert len(set(non_empty)) == len(non_empty)


def _trillions_like_curated_objectives() -> list[dict]:
    """5 atomic objectives across 2 performance objectives (the real 'Trillions' shape).

    po01 carries 2 distinct skills (count, write); po02 over-decomposes one
    "apply ... in everyday life" objective into 3. The lesson cap is 4, so po02 must
    collapse for the request to succeed.
    """

    def ao(ao_id: str, order: int, co: str, text: str, record_id: str) -> dict:
        return {
            "ao_id": ao_id,
            "ao_order": order,
            "curriculum_objective_id": co,
            "objective_text": text,
            "bloom_level": "apply",
            "assessment": {"question": f"Q: {text}", "expected_answer": "A"},
            "record_links": [{"record_id": record_id, "role": "instruction", "link_order": 1}],
            "practice_record_ids": [],
        }

    return [
        ao("trillions-ao-count-trillions", 1, "po01", "Count in trillions.", "r-count"),
        ao("trillions-ao-write-trillions", 2, "po01", "Write in trillions.", "r-write"),
        ao("apply-counting", 3, "po02", "Apply counting of large numbers.", "r-apply-count"),
        ao("apply-writing", 4, "po02", "Apply writing of large numbers.", "r-apply-write"),
        ao("apply-reading", 5, "po02", "Apply reading of large numbers.", "r-apply-read"),
    ]


def test_curated_planning_caps_objectives_at_four() -> None:
    artifacts = build_curated_planning(curated_objectives=_trillions_like_curated_objectives())

    # 5 curated AOs (2 under po01, 3 under po02): the over-decomposed po02 group
    # collapses so the lesson defines at most the cap — no strict-validator 422.
    assert len(artifacts.resolved_kcs) <= MAX_LESSON_OBJECTIVES
    ao_ids = [objective.atomic_objective_id for objective in artifacts.atomic_objectives]
    assert ao_ids == [
        "trillions-ao-count-trillions",  # po01 stays granular
        "trillions-ao-write-trillions",
        "apply-counting",  # po02 collapsed onto its first member's id
    ]

    # The merged po02 objective unions every apply record (curation is preserved).
    merged_kc = artifacts.resolved_kcs[2]
    assert {"r-apply-count", "r-apply-write", "r-apply-read"} <= set(
        merged_kc.supporting_record_ids
    )
    merged_evidence = artifacts.step_evidence_plans["apply-counting"]
    assert {"r-apply-count", "r-apply-write", "r-apply-read"} <= set(
        merged_evidence.selected_record_ids
    )


_TRILLIONS_CURRICULUM = [
    {"curriculum_objective_id": "po01", "objective_text": "Count and write in trillions"},
    {
        "curriculum_objective_id": "po02",
        "objective_text": "Apply the counting, writing, and reading of large numbers",
    },
]


def test_a_merged_group_reads_as_its_curriculum_objective() -> None:
    artifacts = build_curated_planning(
        curated_objectives=_trillions_like_curated_objectives(),
        curriculum_objectives=_TRILLIONS_CURRICULUM,
    )

    assert [kc.objective_text for kc in artifacts.resolved_kcs] == [
        "Count in trillions.",
        "Write in trillions.",
        "Apply the counting, writing, and reading of large numbers",
    ]


def test_each_lesson_objective_carries_its_curriculum_objective_s_own_words() -> None:
    artifacts = build_curated_planning(
        curated_objectives=_trillions_like_curated_objectives(),
        curriculum_objectives=_TRILLIONS_CURRICULUM,
    )
    kpr = curated_artifacts_to_kc_planning_result(
        artifacts, scope_context=_SCOPE, curriculum_objectives=_TRILLIONS_CURRICULUM
    )

    assert [o.curriculum_objective_text for o in kpr.lesson_structure.objectives] == [
        "Count and write in trillions",
        "Count and write in trillions",
        "Apply the counting, writing, and reading of large numbers",
    ]


def test_curated_planning_keeps_all_objectives_within_cap() -> None:
    # At or under the cap nothing is merged — granularity is preserved verbatim.
    objectives = _trillions_like_curated_objectives()[:MAX_LESSON_OBJECTIVES]
    artifacts = build_curated_planning(curated_objectives=objectives)
    assert len(artifacts.resolved_kcs) == MAX_LESSON_OBJECTIVES


def test_all_ungrounded_curated_objectives_raise() -> None:
    # An AO with no record links cannot be grounded; build_curated_planning raises
    # so the generator falls back to LLM planning.
    ungrounded = [
        {
            "ao_id": "ao-x",
            "ao_order": 1,
            "curriculum_objective_id": "co-1",
            "objective_text": "Do something",
            "bloom_level": "apply",
            "assessment": None,
            "record_links": [],
            "practice_record_ids": [],
        }
    ]
    with pytest.raises(ValueError):
        build_curated_planning(curated_objectives=ungrounded)


def test_prepare_inputs_preserves_curated_curriculum_ids() -> None:
    """The curated path carries the AUTHORITATIVE curriculum_objective_id, and the plan's
    curriculum_objectives expose those same ids (the application layer builds them from the
    curated linkage), so curated lesson objectives match the plan's curriculum objectives
    by construction — no synthetic id + heuristic remap."""
    from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
        prepare_generation_inputs,
    )

    inputs = prepare_generation_inputs(
        session_context={
            "session_id": "s1",
            "subject": "Mathematics",
            "track": "core",
            "grade": "JSS1",
            "term": "First Term",
            "week": 1,
            "topic": "Plane shapes",
            "subtopic": "Area of plane shapes",
        },
        curriculum_context={
            # The application layer (SessionContextPayloadBuilder) now exposes the
            # canonical curriculum_objective_ids here, sourced from the curated linkage.
            "curriculum_objectives": [
                {
                    "curriculum_objective_id": "jss1-...-area-po01",
                    "objective_text": "Find the area of plane shapes",
                    "objective_order": 1,
                },
                {
                    "curriculum_objective_id": "jss1-...-area-po02",
                    "objective_text": "Find the area of real life objects",
                    "objective_order": 2,
                },
            ],
            "instructional_materials": ["ruler"],
        },
        reference_context=[
            {
                "type": "textbook_record",
                "record_id": "r1",
                "record_type": "exposition",
                "content": "area of shapes",
                "retrieval_text": "area of shapes",
            }
        ],
        requested_strategy=None,
        default_strategy="cached",
        grounding_mode="manual_linkage",
        curated_objectives=[
            {
                "ao_id": "ao1",
                "ao_order": 1,
                "curriculum_objective_id": "jss1-...-area-po01",
                "objective_text": "Find the area of plane shapes",
            },
            {
                "ao_id": "ao2",
                "ao_order": 2,
                "curriculum_objective_id": "jss1-...-area-po02",
                "objective_text": "Find the area of real life objects",
            },
        ],
    )
    plan_ids = {ref.curriculum_objective_id for ref in inputs.curriculum_objectives}
    curated_ids = {obj["curriculum_objective_id"] for obj in inputs.curated_objectives}
    assert plan_ids == {"jss1-...-area-po01", "jss1-...-area-po02"}
    # Preserved verbatim (NOT remapped), and present in the plan set → they validate.
    assert curated_ids == {"jss1-...-area-po01", "jss1-...-area-po02"}
    assert curated_ids <= plan_ids
