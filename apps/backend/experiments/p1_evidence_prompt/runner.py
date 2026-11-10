"""Run the v1-vs-v2 P1 prompt comparison on a real focal case.

Replays a real H2 focal case (default: the dress-rehearsal case for Ngozi):

  * v1 = the EXACT production path — ``PersonalisedReviewPackRequestBuilder`` +
    ``SectionPersonalisation`` with the distilled state card;
  * v2 = the same policy / lesson context / base sections / model, but the
    learner state carries the spec's full internal LLM input (answer evidence,
    1-5 scores, plain-words misconception, session signals).

Both run live against the configured generator and write paired outputs + the
captured rendered prompts to ``experiments/p1_evidence_prompt/out/`` for the
independent comparison step (one assessor per approach + a blinded comparer).

Usage:
    cd apps/backend
    uv run python -m experiments.p1_evidence_prompt.runner \
      --focal-case EFC-caa170f9905345e1aff3cb06d0e3a658 --session 4,2
"""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

import dspy
from sqlalchemy import select

import app.db.metadata  # noqa: F401  (register ORM models for standalone use)
from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.post_class_review_pack.application.learner_state_input import (
    to_session_signals,
    to_spec_objective_state,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_sources import (
    resolve_lesson_sources,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.learner_state.domain.models import LearnerState, SessionSurvey
from app.infra.dspy_lm import active_model_name, build_dspy_lm
from app.shared.experiment_enums import Hypothesis
from app.shared.session_plan_view import SessionPlanView
from experiments.p1_evidence_prompt.evidence import (
    evidence_states_for_learner,
    load_answer_evidence,
)
from experiments.p1_evidence_prompt.requests_v2 import (
    PersonaliseReviewPackSectionV2Signature,
)

OUT_DIR = Path(__file__).parent / "out"
DEFAULT_FOCAL_CASE = "EFC-caa170f9905345e1aff3cb06d0e3a658"


def _last_prompt(lm: dspy.LM) -> str:
    """The rendered messages of the LM's most recent call, for the report."""
    if not lm.history:
        return ""
    entry = lm.history[-1]
    messages = entry.get("messages") or []
    return "\n\n".join(f"[{m.get('role')}]\n{m.get('content')}" for m in messages)


async def _load_case(db, focal_case_id: str):
    """Focal case + execution + experiment + session plan + P0 base sections."""
    focal_case = (
        await db.execute(
            select(ExperimentFocalCase).where(
                ExperimentFocalCase.experiment_focal_case_id == focal_case_id
            )
        )
    ).scalar_one()
    execution = (
        await db.execute(
            select(ExperimentExecution).where(ExperimentExecution.id == focal_case.execution_db_id)
        )
    ).scalar_one()
    experiment = (
        await db.execute(select(Experiment).where(Experiment.id == execution.experiment_db_id))
    ).scalar_one()
    p0_run = (
        await db.execute(
            select(ExperimentConditionRun).where(
                ExperimentConditionRun.focal_case_db_id == focal_case.id,
                ExperimentConditionRun.condition_code == ConditionCode.P0.value,
            )
        )
    ).scalar_one()
    from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion

    plan_version = (
        await db.execute(
            select(PlanVersion).where(PlanVersion.version_id == experiment.plan_version_id)
        )
    ).scalar_one()
    session_plan = SessionPlanView.model_validate(plan_version.session_plan)
    base_sections = [
        ReviewPackSection.model_validate(section)
        for section in (p0_run.generated_pack or {}).get("sections", [])
    ]
    return focal_case, experiment, session_plan, base_sections, p0_run


async def run(focal_case_id: str, session: tuple[int, int], session_provenance: str) -> Path:
    profile = profile_for(Hypothesis.H2, ConditionCode.P1)
    builder = PersonalisedReviewPackRequestBuilder()

    async with AsyncSessionLocal() as db:
        focal_case, experiment, session_plan, base_sections, p0_run = await _load_case(
            db, focal_case_id
        )
        learner_state = LearnerState.model_validate(focal_case.learner_state_snapshot)
        answer_evidence = await load_answer_evidence(
            db,
            student_id=focal_case.student_id,
            plan_version_id=experiment.plan_version_id,
        )
        sources = await resolve_lesson_sources(db, session_plan)

    spec_states = {
        s.lesson_objective_id: to_spec_objective_state(s) for s in learner_state.objective_states
    }
    v2_states = evidence_states_for_learner(learner_state, answer_evidence)
    # Through the production mapper, so both arms read the anchor phrases a real
    # run renders ("interested (4/5)") rather than bare 1-5 numbers.
    surveyed = learner_state.model_copy(
        update={"session_survey": SessionSurvey(interest=session[0], affect=session[1])}
    )
    session_signals = to_session_signals(surveyed)
    request = builder.build(
        session_plan=session_plan,
        base_pack_id=p0_run.experiment_condition_run_id,
        focal_learner_id=focal_case.student_id,
        learner_states=spec_states,
        policy=profile,
        session_signals=session_signals,
        sources=sources,
    )
    units_by_objective = {u.lesson_objective_id: u for u in request.units}

    # v1 — the exact production personaliser.
    v1 = PersonaliseSection(lm=build_dspy_lm())
    # v2 — same model, evidence-rich signature.
    v2_lm = build_dspy_lm()
    v2_personalise = dspy.ChainOfThought(PersonaliseReviewPackSectionV2Signature)

    sections_report = []
    for base_section in base_sections:
        objective_id = base_section.lesson_objective_id
        state = spec_states.get(objective_id)
        unit = units_by_objective.get(objective_id)
        if state is None or unit is None:
            continue
        v1_out = await v1.personalise_section(
            request=request, unit=unit, base_section=base_section, learner_state=state
        )
        v1_prompt = _last_prompt(v1.lm)
        with dspy.settings.context(lm=v2_lm):
            v2_result = await v2_personalise.acall(
                policy=request.policy,
                lesson_context=request.lesson_context,
                base_section=base_section,
                learner_state=v2_states[objective_id],
                session_signals=session_signals,
                source_evidence=unit.source_evidence,
            )
        v2_prompt = _last_prompt(v2_lm)
        sections_report.append(
            {
                "lesson_objective_id": objective_id,
                "objective_text": unit.objective_text,
                "base_section": base_section.model_dump(mode="json"),
                "v1": {
                    "learner_state_input": state.model_dump(mode="json"),
                    "output": v1_out.model_dump(mode="json"),
                    "prompt": v1_prompt,
                },
                "v2": {
                    "learner_state_input": v2_states[objective_id].model_dump(mode="json"),
                    "session_signals_input": (
                        session_signals.model_dump(mode="json") if session_signals else None
                    ),
                    "output": v2_result.output.model_dump(mode="json"),
                    "prompt": v2_prompt,
                },
            }
        )

    OUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = OUT_DIR / f"run-{stamp}.json"
    out_path.write_text(
        json.dumps(
            {
                "focal_case_id": focal_case_id,
                "student_id": focal_case.student_id,
                "experiment_id": experiment.experiment_id,
                "plan_version_id": experiment.plan_version_id,
                "model": active_model_name(),
                "provenance": {
                    "v1": "production request builder + SectionPersonalisation",
                    "v2": "experiments.p1_evidence_prompt.requests_v2 (evidence-rich)",
                    "numeric_survey_scores": (
                        "bucket-era diagnostic; numerics derived via the production "
                        "legacy coercion low->2 / medium->3 / high->4"
                    ),
                    "session_signals": session_provenance,
                },
                "sections": sections_report,
            },
            indent=2,
        )
    )
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--focal-case", default=DEFAULT_FOCAL_CASE)
    parser.add_argument(
        "--session",
        default="4,2",
        help="interest,affect 1-5 (default: Ngozi's real week-6 session survey)",
    )
    args = parser.parse_args()
    interest, affect = (int(part) for part in args.session.split(","))
    provenance = (
        f"interest={interest}, affect={affect} via --session; default values are the same "
        "student's most recent REAL session survey (a later lesson — the rehearsal "
        "diagnostic predates the session survey)"
    )
    out_path = asyncio.run(run(args.focal_case, (interest, affect), provenance))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
