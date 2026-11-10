"""Freeze the P1 prompt-eval dataset from real focal cases in the dev DB.

One case per focal case with a succeeded P0 run: the approved base sections,
the lesson's session plan, and the learner's DOMAIN state rebuilt from their
actual diagnostic (so counts ride in) and enriched with the missed-item answer
evidence queried from the items + responses tables (bucket-era snapshots
predate evidence recording). Session survey is included only when the learner
actually answered one for THAT lesson — no borrowed signals.

Usage:
    cd apps/backend
    uv run python -m experiments.p1_prompt_eval.dataset
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.db.metadata  # noqa: F401  (register ORM models for standalone use)
from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_sources import (
    resolve_lesson_sources,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
)
from app.domains.learner_state.application.service import LearnerStateService
from app.domains.learner_state.domain.models import AnswerEvidence, LearnerState
from app.domains.learners.models import LearnerProfile
from app.shared.session_plan_view import SessionPlanView

EVAL_SET_PATH = Path(__file__).parent / "eval_set.json"


async def _answer_evidence(
    db: AsyncSession, *, student_id: str, plan_version_id: str
) -> dict[str, list[AnswerEvidence]]:
    """The learner's missed items per objective (canonical domain vocabulary)."""
    rows = (
        await db.execute(
            select(ExitTicketItem, StudentItemResponse)
            .join(StudentItemResponse, StudentItemResponse.item_id == ExitTicketItem.id)
            .where(
                StudentItemResponse.student_id == student_id,
                ExitTicketItem.plan_version_id == plan_version_id,
            )
            .order_by(ExitTicketItem.lesson_objective_id)
        )
    ).all()
    by_objective: dict[str, list[AnswerEvidence]] = {}
    for item, response in rows:
        if response.is_correct or not item.lesson_objective_id:
            continue
        misconceptions = item.option_misconceptions or {}
        by_objective.setdefault(item.lesson_objective_id, []).append(
            AnswerEvidence(
                stem=item.stem,
                options=dict(item.options or {}),
                correct_option=item.correct_option,
                chosen_option=response.choice,
                misconception_code=misconceptions.get(response.choice),
            )
        )
    return by_objective


async def _learner_state_for_case(
    db: AsyncSession, *, student_id: str, plan_version_id: str, diagnostic_id: str | None
) -> LearnerState | None:
    """Rebuild the domain state from the case's actual diagnostic + evidence."""
    query = (
        select(ExitTicketSubmission)
        .where(ExitTicketSubmission.student_id == student_id)
        .where(ExitTicketSubmission.plan_version_id == plan_version_id)
        .order_by(ExitTicketSubmission.created_at.desc())
    )
    if diagnostic_id:
        query = select(ExitTicketSubmission).where(
            ExitTicketSubmission.diagnostic_id == diagnostic_id
        )
    submission = (await db.execute(query)).scalars().first()
    if submission is None:
        return None
    profile = (
        (await db.execute(select(LearnerProfile).where(LearnerProfile.student_id == student_id)))
        .scalars()
        .first()
    )
    state = LearnerStateService().build(
        student_id=student_id,
        student_profile=profile,
        diagnostic_id=submission.diagnostic_id,
        diagnostic_results=submission.results,
    )
    evidence = await _answer_evidence(db, student_id=student_id, plan_version_id=plan_version_id)
    for objective in state.objective_states:
        if not objective.evidence:
            objective.evidence = evidence.get(objective.lesson_objective_id, [])
    return state


async def build() -> Path:
    cases = []
    async with AsyncSessionLocal() as db:
        focal_cases = (await db.execute(select(ExperimentFocalCase))).scalars().all()
        for focal_case in focal_cases:
            p0_run = (
                (
                    await db.execute(
                        select(ExperimentConditionRun).where(
                            ExperimentConditionRun.focal_case_db_id == focal_case.id,
                            ExperimentConditionRun.condition_code == ConditionCode.P0.value,
                            ExperimentConditionRun.status == "succeeded",
                        )
                    )
                )
                .scalars()
                .first()
            )
            if p0_run is None or not (p0_run.generated_pack or {}).get("sections"):
                continue
            execution = (
                await db.execute(
                    select(ExperimentExecution).where(
                        ExperimentExecution.id == focal_case.execution_db_id
                    )
                )
            ).scalar_one()
            experiment = (
                await db.execute(
                    select(Experiment).where(Experiment.id == execution.experiment_db_id)
                )
            ).scalar_one()
            plan_version = (
                await db.execute(
                    select(PlanVersion).where(PlanVersion.version_id == experiment.plan_version_id)
                )
            ).scalar_one()
            snapshot = focal_case.learner_state_snapshot or {}
            learner_state = await _learner_state_for_case(
                db,
                student_id=focal_case.student_id,
                plan_version_id=experiment.plan_version_id,
                diagnostic_id=snapshot.get("diagnostic_id"),
            )
            if learner_state is None:
                continue
            session_plan = SessionPlanView.model_validate(plan_version.session_plan)
            sources = await resolve_lesson_sources(db, session_plan)
            cases.append(
                {
                    "case_id": focal_case.experiment_focal_case_id,
                    "student_id": focal_case.student_id,
                    "experiment_id": experiment.experiment_id,
                    "plan_version_id": experiment.plan_version_id,
                    "session_plan": plan_version.session_plan,
                    "base_sections": p0_run.generated_pack["sections"],
                    "learner_state": learner_state.model_dump(mode="json"),
                    # The plan citations and their resolved content are frozen
                    # together so runs do not depend on the live database.
                    "sources": [
                        {
                            "citation": source.citation,
                            "content": source.content,
                            "record_id": source.record_id,
                        }
                        for source in sources.items
                    ],
                }
            )
    EVAL_SET_PATH.write_text(json.dumps({"cases": cases}, indent=2))
    return EVAL_SET_PATH


def main() -> None:
    path = asyncio.run(build())
    data = json.loads(path.read_text())
    print(f"froze {len(data['cases'])} cases -> {path}")
    for case in data["cases"]:
        states = case["learner_state"]["objective_states"]
        n_evidence = sum(len(s.get("evidence", [])) for s in states)
        print(
            f"  {case['case_id']} {case['student_id']}: "
            f"{len(case['base_sections'])} base sections, "
            f"{len(states)} objective states, {n_evidence} evidence items"
        )


if __name__ == "__main__":
    main()
