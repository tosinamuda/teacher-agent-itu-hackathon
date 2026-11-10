"""No-LLM tests for the GEPA optimiser plumbing (split, metric, inputs).

The GEPA run itself needs the LLM; these cover the deterministic helpers: the
disjoint train/test split, the signature-input projection, and the metric's
robust handling of a malformed prediction.
"""

from __future__ import annotations

from types import SimpleNamespace

import dspy

from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonCurriculumContext,
    LessonGenerationSession,
    PreparedGenerationInputs,
    build_scope_context,
)
from experiments.strategy_bakeoff.optimize import (
    _gepa_metric,
    _signature_inputs,
    _train_test_split,
)


def _request() -> PreparedGenerationInputs:
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
        }
    )
    return PreparedGenerationInputs(
        session=session,
        scope=build_scope_context(session),
        curriculum=curriculum,
        textbook_records=[],
        evidence_selection_strategy="cached",
    )


def test_train_test_split_is_disjoint_and_excludes_s3() -> None:
    eval_set = {
        "selected": {
            "S1_grounded": [{"subtopic_id": f"s1-{i}"} for i in range(4)],
            "S2_partial": [{"subtopic_id": f"s2-{i}"} for i in range(3)],
            "S3_no_records": [{"subtopic_id": "s3-0"}],
        }
    }
    train, test = _train_test_split(eval_set)
    train_ids = {r["subtopic_id"] for r in train}
    test_ids = {r["subtopic_id"] for r in test}
    assert train_ids.isdisjoint(test_ids)  # no leakage
    assert len(train) == 4  # 2 S1 + 2 S2
    assert len(test) == 3  # 2 S1 + 1 S2
    # S3 never appears in either split (too few; pre-reg §5)
    assert not any("s3" in i for i in train_ids | test_ids)


def test_signature_inputs_projects_the_five_fields() -> None:
    keys = set(_signature_inputs(_request()))
    assert keys == {
        "scope_context",
        "curriculum_context",
        "curriculum_objectives",
        "textbook_records",
        "prior_violations",
    }


def test_gepa_metric_scores_malformed_prediction_zero_with_feedback() -> None:
    gold = dspy.Example(request=_request())
    # step_evidence_plans as a string -> adapt_prediction crashes -> caught.
    bad_pred = SimpleNamespace(
        step_evidence_plans="not-a-list",
        lesson_plan_objectives=[],
        resolved_kcs=[],
        core_steps=[],
        global_steps=None,
        assessments=[],
        misconceptions=[],
    )
    result = _gepa_metric(gold, bad_pred)
    assert result.score == 0.0
    assert isinstance(result.feedback, str) and result.feedback  # non-empty guidance
