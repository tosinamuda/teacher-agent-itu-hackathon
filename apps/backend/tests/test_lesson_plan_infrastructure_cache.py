"""Cache invalidation invariants for ``InfrastructureArtifactCache``.

Pins the contract documented at the top of ``cache.py``: an entry is a HIT
only when every input matches. Each test below changes one dimension and
asserts a miss; the suite is the executable form of the contract.

Why this exists
---------------

The cache is content-addressed: change any input and the next ``get`` is a
miss, so the planning pipeline recomputes. That contract is invisible
unless tested — drift in either ``cache.get``'s comparison logic or
``cache.put``'s metadata-writing would silently start returning stale
entries. These tests make every dimension of the contract a failing test
under drift.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.cache import (
    INFRASTRUCTURE_VERSION,
    InfrastructureArtifactCache,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.types import (
    KCPlanningResult,
    Violation,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    LessonStructure,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    AtomicObjective,
    CandidateKC,
    CandidateKCPlan,
    CoreStepBlueprint,
    LessonPlanObjective,
    StepEvidencePlan,
)

_SUBTOPIC_ID = "jss1-math-percentages-meaning"
_TOPIC_KEY = "jss1-math-percentages"
_TEXTBOOK_HASH = "textbook-hash-v1"
_CURRICULUM_HASH = "curriculum-hash-v1"


def _planning_result() -> KCPlanningResult:
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
    lesson_structure = LessonStructure(
        objectives=[lesson_objective],
        blueprints=[blueprint],
        objectives_by_id={"lop01": lesson_objective},
        kcs_by_objective_id={"lop01": candidate_kc},
    )

    return KCPlanningResult(
        subtopic_id=_SUBTOPIC_ID,
        topic_key=_TOPIC_KEY,
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
        lesson_structure=lesson_structure,
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


def _put(cache: InfrastructureArtifactCache) -> None:
    cache.put(
        subtopic_id=_SUBTOPIC_ID,
        textbook_hash=_TEXTBOOK_HASH,
        curriculum_hash=_CURRICULUM_HASH,
        planning_result=_planning_result(),
    )


# --- Baseline: a matching read is a hit -------------------------------------


def test_get_matching_returns_cached_result(tmp_path: Path) -> None:
    cache = InfrastructureArtifactCache(tmp_path)
    _put(cache)
    assert (
        cache.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is not None
    )


# --- Hash dimensions invalidate ---------------------------------------------


def test_textbook_hash_mismatch_is_miss(tmp_path: Path) -> None:
    cache = InfrastructureArtifactCache(tmp_path)
    _put(cache)
    assert (
        cache.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash="textbook-hash-v2",  # changed
            curriculum_hash=_CURRICULUM_HASH,
        )
        is None
    )


def test_curriculum_hash_mismatch_is_miss(tmp_path: Path) -> None:
    cache = InfrastructureArtifactCache(tmp_path)
    _put(cache)
    assert (
        cache.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash="curriculum-hash-v2",  # changed
        )
        is None
    )


# --- Code-version bump invalidates ALL --------------------------------------


def test_infrastructure_version_bump_is_miss(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache = InfrastructureArtifactCache(tmp_path)
    _put(cache)
    monkeypatch.setattr(
        "app.domains.artefacts.types.lesson_plan.drafting.application.precompute.cache.INFRASTRUCTURE_VERSION",
        "v3",
    )
    assert (
        cache.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is None
    )


# --- Model swap invalidates -------------------------------------------------


def test_model_swap_is_miss(tmp_path: Path) -> None:
    """Switching LLM models must invalidate.

    Previously stored entries via model A must not be served back to a
    pipeline running model B. Before this contract was enforced, the cache
    silently returned stale model-A outputs when the pipeline switched to
    model B.
    """
    written = InfrastructureArtifactCache(tmp_path, model_name="gpt-4o-mini")
    _put(written)

    swapped = InfrastructureArtifactCache(tmp_path, model_name="gpt-4o")
    assert (
        swapped.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is None
    )


def test_model_match_is_hit(tmp_path: Path) -> None:
    """The model_name check must NOT over-invalidate when the model matches."""
    written = InfrastructureArtifactCache(tmp_path, model_name="gpt-4o")
    _put(written)

    same = InfrastructureArtifactCache(tmp_path, model_name="gpt-4o")
    assert (
        same.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is not None
    )


def test_baseline_uses_default_infrastructure_version(tmp_path: Path) -> None:
    """A no-op safety check: ``INFRASTRUCTURE_VERSION`` is the value the cache
    is testing against. If this ever drifts away from ``"v2"`` without
    updating the metadata on disk, the suite will tell you exactly where.
    """
    assert INFRASTRUCTURE_VERSION == "v2"


# --- Explicit invalidate(...) API -------------------------------------------


def test_invalidate_subtopic_makes_next_get_miss(tmp_path: Path) -> None:
    cache = InfrastructureArtifactCache(tmp_path)
    _put(cache)
    assert cache.invalidate(_SUBTOPIC_ID) is True
    assert (
        cache.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is None
    )


def test_invalidate_unknown_subtopic_returns_false(tmp_path: Path) -> None:
    """Idempotent: invalidating a subtopic that was never cached is not an error."""
    cache = InfrastructureArtifactCache(tmp_path)
    assert cache.invalidate("no-such-subtopic") is False


def test_model_name_propagates_through_module_chain() -> None:
    """``model_name`` reaches the cache via the runtime module chain.

    Closes the gap flagged at #5 landing time: ``InfrastructurePlanningModule``
    and its outer ``LessonGenerationModule`` previously had no model_name kwarg,
    so the cache was always constructed with ``self._model_name = None`` and
    the (now-enforced) model_name invalidation never fired in practice.
    """
    from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.generator import (  # noqa: E501
        InfrastructurePlanningModule,
        LessonGenerationModule,
    )

    inner = InfrastructurePlanningModule(model_name="gpt-4o-mini")
    assert inner.infrastructure_builder._cache._model_name == "gpt-4o-mini"

    outer = LessonGenerationModule(model_name="gpt-4o")
    assert outer.infrastructure_planner.infrastructure_builder._cache._model_name == "gpt-4o"


def test_invalidate_all_clears_every_subtopic(tmp_path: Path) -> None:
    cache = InfrastructureArtifactCache(tmp_path)
    _put(cache)
    # write a second entry under a different subtopic
    cache.put(
        subtopic_id="jss1-math-percentages-conversion",
        textbook_hash=_TEXTBOOK_HASH,
        curriculum_hash=_CURRICULUM_HASH,
        planning_result=_planning_result(),
    )
    cache.invalidate_all()
    assert (
        cache.get(
            subtopic_id=_SUBTOPIC_ID,
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is None
    )
    assert (
        cache.get(
            subtopic_id="jss1-math-percentages-conversion",
            topic_key=_TOPIC_KEY,
            textbook_hash=_TEXTBOOK_HASH,
            curriculum_hash=_CURRICULUM_HASH,
        )
        is None
    )
