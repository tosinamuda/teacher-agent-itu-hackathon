"""Part 1's own input, and the request Part 1 built from an input, for tests to compare against."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.note_editorial import clean_plan

#: Where the published datasets are on a machine that has fetched them.
RELEASE = Path(
    os.environ.get(
        "STUDY_DATASET_ROOT", Path.home() / "Documents/Unilag/Masters/Thesis/Dataset/public"
    )
)

PART_1 = Path("experiments/h1_condition_eval/runs/c0c3-prism-objective")
RUN = json.loads((PART_1 / "run.json").read_text())["arm"]
CONDITIONS = (ConditionCode.C0, ConditionCode.C1, ConditionCode.C2, ConditionCode.C3)


def part_1_request(plan: dict[str, Any], condition: ConditionCode) -> Any:
    """Part 1's request construction, as `experiments/h1_condition_eval/execution.py` makes it."""
    view = SessionPlanView.model_validate(plan)
    return BaseReviewPackRequestBuilder(figures=RUN["figures"]).build(
        session_plan=view,
        policy=profiles_for_variant(RUN["context_variant"])[condition].generation_policy(),
        sources=LessonSources.unresolved(view.references),
    )


def part_1_inputs() -> dict[str, dict[str, Any]]:
    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    return {
        case["lesson"]: clean_plan({**case["plan"], "lesson_key": case["lesson"]})[0]
        for case in cases
    }
