"""Request-model contracts keep H1 and H2 workflows structurally distinct."""

import pytest
from condition_plan_inputs import build_request, example_plan
from pydantic import ValidationError

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    GenerationPolicyContext,
    LessonContextForGeneration,
    PersonalisedReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for


def _common(hypothesis: Hypothesis) -> dict[str, object]:
    return {
        "generation_policy": profile_for(
            hypothesis,
            ConditionCode.C0 if hypothesis == Hypothesis.H1 else ConditionCode.P1,
        ).generation_policy(),
        "artefact_spec": revision_pack_spec("JSS1"),
        "policy": GenerationPolicyContext(
            require_source_refs=False,
            use_only_provided_sources=False,
            preserve_lesson_objective=True,
            instruction_summary="",
        ),
        "lesson_context": LessonContextForGeneration(
            subject="Mathematics",
            grade_level="JSS1",
            topic="Fractions",
            lesson_objectives=["Add fractions"],
        ),
        "units": [
            SectionGenerationUnit(
                unit_id="objective:one",
                lesson_objective_id="one",
                objective_text="Add fractions",
            )
        ],
    }


def test_h1_rejects_h2_only_fields() -> None:
    with pytest.raises(ValidationError, match="base_pack_id"):
        BaseReviewPackRequest(
            **_common(Hypothesis.H1),
            base_pack_id="PACK-1",
            focal_learner_id="LEARNER-1",
        )


def test_h2_requires_its_workflow_identifiers() -> None:
    with pytest.raises(ValidationError, match="base_pack_id"):
        PersonalisedReviewPackRequest(**_common(Hypothesis.H2))


def test_product_requests_contain_no_experiment_identifiers() -> None:
    request = BaseReviewPackRequest(**_common(Hypothesis.H1))

    assert "experiment_id" not in type(request).model_fields
    assert "lesson_id" not in type(request).model_fields
    assert "hypothesis" not in type(request.generation_policy).model_fields
    assert "condition_code" not in type(request.generation_policy).model_fields


def test_h1_and_h2_builders_return_their_concrete_request_types() -> None:
    h1 = build_request(example_plan(), profile_for(Hypothesis.H1, ConditionCode.C0))
    h2 = build_request(example_plan(), profile_for(Hypothesis.H2, ConditionCode.P1))

    assert isinstance(h1, BaseReviewPackRequest)
    assert isinstance(h2, PersonalisedReviewPackRequest)
