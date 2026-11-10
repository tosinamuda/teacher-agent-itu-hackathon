"""Synthetic LLM-as-judge rater — shared core for the CLI script + browser-triggered job.

Scores each blinded packet's candidate pack against the H1/H2 rubric under several
expert-mathematics-teacher personas (for inter-rater variety), persisting clearly
labelled synthetic evaluation_ratings. Not a substitute for the expert-teacher
evaluation in the thesis design.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from statistics import mean
from typing import TYPE_CHECKING, cast

import dspy
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.evaluation.application.identity_ports import RaterRegistrationStore
from app.domains.evaluation.application.synthetic_support import (
    get_or_create_rater,
    load_experiment_executions,
)
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRating,
)
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.infra.dspy_lm import build_dspy_lm
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

if TYPE_CHECKING:
    from app.domains.experiments.infrastructure.models import ExperimentConditionRun

PERSONAS: dict[str, str] = {
    "veteran_examiner": (
        "a veteran NERDC mathematics examiner — exacting about curriculum coverage, "
        "correctness, and staying on scope; reserves top marks for excellent work"
    ),
    "constructivist": (
        "a constructivist mathematics educator who prizes conceptual understanding, "
        "clear scaffolding, and building from what the learner already knows"
    ),
    "exam_coach": (
        "an exam-focused mathematics tutor who values worked examples, practice, and "
        "efficient, unambiguous explanations students can apply under test conditions"
    ),
    "remediation_specialist": (
        "a remedial-mathematics specialist attuned to misconceptions and the right level "
        "of support for struggling learners; generous when support is well targeted"
    ),
}

H1_RUBRIC = (
    ("objective_curriculum_alignment", "Objective and curriculum alignment", 1, 5),
    ("taught_lesson_alignment", "Taught-lesson alignment", 1, 5),
    ("scope_conceptual_correctness", "Scope and conceptual correctness", 1, 5),
    ("clarity_usefulness", "Student-facing clarity and usefulness", 1, 5),
)
H2_RUBRIC = (
    ("learner_state_suitability", "Learner-state suitability", 1, 5),
    ("scaffolding_appropriateness", "Scaffolding appropriateness", 1, 5),
    ("challenge_calibration", "Challenge calibration", 1, 5),
    ("misconception_support", "Misconception support", 1, 5),
    ("objective_preservation", "Objective preservation", 1, 5),
)

# Hypothesis-keyed registry — replaces ``H1_RUBRIC if hyp == "H1" else H2_RUBRIC``.
_RUBRIC_BY_HYPOTHESIS: dict[str, tuple[tuple[str, str, int, int], ...]] = {
    "H1": H1_RUBRIC,
    "H2": H2_RUBRIC,
}

ProgressFn = Callable[[JsonObject], None]


def _emit(on_progress: ProgressFn | None, event: JsonObject) -> None:
    if on_progress is not None:
        on_progress(event)


class PackJudge(dspy.Signature):
    """Score a student review pack against a rubric as the described expert teacher-rater.

    Return ONLY a JSON object mapping each criterion_id to an integer within its scale.
    """

    persona: str = dspy.InputField(desc="the rater's disposition")
    rubric: str = dspy.InputField(desc="criteria: id, label, scale")
    pack_text: str = dspy.InputField(desc="the review pack content to evaluate")
    scores_json: str = dspy.OutputField(desc="JSON: {criterion_id: integer score}")


def _pack_text(manifest: object) -> str:
    if not isinstance(manifest, dict):
        return ""
    manifest_obj = cast(JsonObject, manifest)
    parts: list[str] = []
    steps = manifest_obj.get("steps")
    if not isinstance(steps, list):
        return ""
    for step in steps:
        if not isinstance(step, dict):
            continue
        title = step.get("title")
        if title:
            parts.append(str(title))
        blocks = step.get("blocks")
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            content = block.get("content")
            if content:
                parts.append(str(content))
    return "\n\n".join(parts)[:6000]


def _rubric_text(rubric: tuple) -> str:
    return "\n".join(f"- {cid} ({label}, scale {lo}-{hi})" for cid, label, lo, hi in rubric)


def _parse_scores(raw: str, rubric: tuple) -> dict[str, float]:
    try:
        parsed = json.loads(raw[raw.find("{") : raw.rfind("}") + 1])
    except json.JSONDecodeError:
        parsed = {}
    scores: dict[str, float] = {}
    for cid, _label, lo, hi in rubric:
        raw_score = parsed.get(cid)
        try:
            if raw_score is None:
                raise TypeError("missing score")
            num = float(raw_score)
        except (TypeError, ValueError):
            num = (lo + hi) / 2
        scores[cid] = float(max(lo, min(hi, round(num))))
    return scores


class SyntheticRatingResult(BaseModel):
    """Completion summary for a synthetic packet-rating run."""

    created: int
    packets: int
    personas: list[str]


async def rate_experiment(
    db: AsyncSession,
    *,
    identity_store: RaterRegistrationStore,
    experiment_id: str,
    personas: list[str] | None = None,
    on_progress: ProgressFn | None = None,
) -> JsonObject:
    """Synthetically rate every packet of an experiment under each persona."""
    judge = dspy.ChainOfThought(PackJudge)
    lm = build_dspy_lm()
    chosen = [p for p in (personas or list(PERSONAS)) if p in PERSONAS]

    repository = ExperimentRepository(db)
    executions = await load_experiment_executions(experiment_id, repository=repository)
    if executions is None:
        return {"created": 0, "note": "experiment not found"}
    run_by_id: dict[str, ExperimentConditionRun] = {}
    packets: list[EvaluationPacket] = []
    for execution in executions:
        for run in await repository.list_condition_runs(execution.id):
            run_by_id[run.experiment_condition_run_id] = run
        packets += (
            (
                await db.execute(
                    select(EvaluationPacket).where(EvaluationPacket.execution_db_id == execution.id)
                )
            )
            .scalars()
            .all()
        )

    raters = {
        persona: await get_or_create_rater(identity_store, f"Synthetic Judge — {persona}")
        for persona in chosen
    }
    total = len(packets) * len(chosen)
    _emit(
        on_progress,
        {
            "type": "start",
            "phase": "ratings",
            "done": 0,
            "total": total,
            "message": f"Expert raters scoring {len(packets)} packs × {len(chosen)} personas…",
        },
    )
    created = 0
    done = 0
    artefact_repository = ArtefactRepository()
    for packet in packets:
        condition_run = run_by_id.get(packet.primary_condition_run_id)
        if condition_run is None:
            continue
        # Resolve the run's current pack via the back-pointer (a run's output
        # points back at the run), not a stored forward id on the run.
        artefact = await artefact_repository.current_artefact_for_condition_run(
            db, condition_run.experiment_condition_run_id
        )
        if artefact is None:
            continue
        text = _pack_text(artefact.manifest)
        rubric = _RUBRIC_BY_HYPOTHESIS[packet.hypothesis]
        spec = _rubric_text(rubric)
        for persona, rater in raters.items():
            done += 1
            exists = (
                await db.execute(
                    select(EvaluationRating).where(
                        EvaluationRating.evaluation_packet_db_id == packet.id,
                        EvaluationRating.rater_db_id == rater.id,
                    )
                )
            ).scalar_one_or_none()
            if exists is not None:
                _emit(
                    on_progress,
                    {
                        "type": "progress",
                        "phase": "ratings",
                        "done": done,
                        "total": total,
                        "message": f"{packet.hypothesis} · {persona} (cached)",
                    },
                )
                continue
            with dspy.settings.context(lm=lm):
                out = judge(persona=PERSONAS[persona], rubric=spec, pack_text=text)
            scores = _parse_scores(out.scores_json, rubric)
            db.add(
                EvaluationRating(
                    rating_id=new_public_id(PublicIdPrefix.EVALUATION_RATING),
                    evaluation_packet_db_id=packet.id,
                    rater_db_id=rater.id,
                    hypothesis=packet.hypothesis,
                    overall_score=round(mean(scores.values()), 3),
                    rubric_scores=scores,
                    notes={"synthetic": True, "persona": persona},
                    created_at=utc_now(),
                    updated_at=utc_now(),
                    submitted_at=utc_now(),
                )
            )
            created += 1
            _emit(
                on_progress,
                {
                    "type": "progress",
                    "phase": "ratings",
                    "done": done,
                    "total": total,
                    "message": f"{packet.hypothesis} · {persona}: "
                    f"{round(mean(scores.values()), 2)}",
                },
            )
    await db.commit()
    _emit(
        on_progress,
        {
            "type": "done",
            "phase": "ratings",
            "done": done,
            "total": total,
            "message": f"{created} synthetic ratings across {len(packets)} packs",
        },
    )
    return SyntheticRatingResult(created=created, packets=len(packets), personas=chosen).model_dump(
        mode="json"
    )
