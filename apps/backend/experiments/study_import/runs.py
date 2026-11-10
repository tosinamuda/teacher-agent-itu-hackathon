"""The study's two runs as the app's experiment records: one ended experiment per lesson.

Part 1 is three H1 executions per lesson, one per draw, each running C0–C3 under context
variant v7-full with pipeline 2026-08-25. Part 2 is one H2 execution per lesson it covered:
a focal case per learner, holding the learner state P1 read, with a P0 and a P1 run. P0 is
Part 1's C3 draw 1 reused, so it carries 2026-08-25; P1 was written by 2026-09-02.

Every revision note is stored the way the app's own runs store theirs: projected through the
request builder the run used, then the pack manifest adapter.

No teacher reviewed any of them. The researcher approved Part 2's base, C3's first draw, in the
teacher's place, so it and each learner's P0 made from it are approved by the researcher. Every
other note went to the raters unreviewed, and stays pending as the app's own research outputs do.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    sections_to_review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.evidence import (
    FigureSource,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_note_input import (  # noqa: E501
    with_lesson_note,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import ReviewPackPipeline
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.experiments.domain import FocalCaseType
from app.domains.experiments.domain.types import (
    ConditionCode,
    ConditionRunStatus,
    ExecutionStatus,
    ExperimentLifecycleStatus,
    Hypothesis,
    InvestigationStatus,
)
from app.domains.experiments.infrastructure.models import (
    Experiment,
    ExperimentConditionRun,
    ExperimentExecution,
    ExperimentFocalCase,
    Investigation,
)
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView
from app.shared.time import utc_now
from experiments.study_import.lessons import ImportedLesson, learner_id

INVESTIGATION_ID = "INV-STUDY-2026-09"
RESEARCHER_NAME = "The study researcher"


@dataclass
class Staged:
    """A run's rows in the order they reference each other; each stage is flushed in turn."""

    parents: list[object] = field(default_factory=list)
    runs: list[ExperimentConditionRun] = field(default_factory=list)
    notes: list[Artefact] = field(default_factory=list)

    @property
    def stages(self) -> tuple[list[Any], ...]:
        return (self.parents, list(self.runs), list(self.notes))


PART_1_VARIANT = "v7-full"
PART_1_FIGURES: FigureSource = "source"
_SPEC = {"kind": "post_class_review_pack", "revision": 1}
_WEAKEST_FIRST = ("remediate", "reinforce", "extend")


def _part_1_key(lesson: str, condition: str, draw: int) -> str:
    return f"{lesson}-{condition}-d{draw}"


def _part_2_key(lesson: str, pseudonym: str, condition: str) -> str:
    return f"{lesson}-{pseudonym}-{condition}"


def part_1_note_id(lesson: str, condition: str, draw: int) -> str:
    """A Part 1 class revision note, by the lesson, condition and draw that made it."""
    return f"AT-STUDY-{_part_1_key(lesson, condition, draw)}"


def part_2_note_id(lesson: str, pseudonym: str, condition: str) -> str:
    """A Part 2 learner's revision note, by lesson, the learner's pseudonym and P0 or P1."""
    return f"AT-STUDY-{_part_2_key(lesson, pseudonym, condition)}"


def base_note_id(lesson: str, base: dict[str, Any]) -> str:
    """The Part 1 note Part 2 reused as every learner's P0."""
    return part_1_note_id(lesson, str(base["condition"]), int(base["repeat"]))


def investigation_row() -> Investigation:
    return Investigation(
        id=uuid.uuid4(),
        investigation_id=INVESTIGATION_ID,
        investigation_code="msc-study-2026-09",
        title="MSc study: lesson-plan-driven revision notes, JSS1 Mathematics",
        description="Imported from the published datasets; concluded and read-only.",
        status=InvestigationStatus.ENDED,
        ended_at=utc_now(),
        ended_by="study import",
    )


def experiment_row(
    investigation: Investigation, lesson: ImportedLesson, learners: list[str]
) -> Experiment:
    return Experiment(
        id=uuid.uuid4(),
        experiment_id=f"EXP-STUDY-{lesson.lesson.lesson}",
        experiment_code=f"study-{lesson.lesson.lesson}",
        investigation_db_id=investigation.id,
        teacher_workspace_id=lesson.place.workspace_id,
        lesson_period_id=lesson.place.lesson_period_id,
        plan_version_id=lesson.plan_version_id,
        focal_learner_ids=[learner_id(pseudonym) for pseudonym in learners],
        lifecycle_status=ExperimentLifecycleStatus.ENDED,
        ended_at=utc_now(),
        ended_by="study import",
    )


def _execution(
    experiment: Experiment, hypothesis: Hypothesis, attempt: int, run: str
) -> ExperimentExecution:
    return ExperimentExecution(
        id=uuid.uuid4(),
        execution_id=f"EXE-STUDY-{experiment.experiment_code.removeprefix('study-')}-{hypothesis.value.lower()}-{attempt}",
        experiment_db_id=experiment.id,
        hypothesis=hypothesis.value,
        attempt_number=attempt,
        status=ExecutionStatus.SUCCEEDED,
        runtime_snapshot={"study_run": run},
        created_at=utc_now(),
        updated_at=utc_now(),
    )


class _Projection:
    """A lesson as Part 1's request builder saw it: its lesson context and objectives."""

    def __init__(self, lesson: ImportedLesson) -> None:
        plan = SessionPlanView.model_validate(
            with_lesson_note(lesson.lesson.plan, dict(lesson.lesson.note_sections))
        )
        request = BaseReviewPackRequestBuilder(figures=PART_1_FIGURES).build(
            session_plan=plan,
            policy=profiles_for_variant(PART_1_VARIANT)[ConditionCode.C3].generation_policy(),
            sources=LessonSources.unresolved(plan.references),
        )
        self.context = request.lesson_context
        self.objectives: list[JsonObject] = [
            {"lesson_objective_id": unit.lesson_objective_id, "objective_text": unit.objective_text}
            for unit in request.units
        ]

    def pack(
        self,
        run: ExperimentConditionRun,
        plan_version_id: str,
        sections: list[dict[str, Any]],
        refs: dict[str, Any],
        *,
        student: str | None = None,
        bands: dict[str, str] | None = None,
        approved_by_the_researcher: bool = False,
    ) -> Artefact:
        artefact_id = f"AT-{run.experiment_condition_run_id.removeprefix('ECR-')}"
        scope = ArtefactScope.LEARNER_LEVEL if student else ArtefactScope.CLASS_LEVEL
        manifest = sections_to_review_pack_manifest(
            sections=[ReviewPackSection.model_validate(section) for section in sections],
            artefact_id=artefact_id,
            plan_version_id=plan_version_id,
            scope=scope,
            lesson_context=self.context,
            created_at=utc_now(),
            lesson_plan_objectives=self.objectives,
            student_id=student,
            personalisation_bands=bands,
        )
        return Artefact(
            artefact_id=artefact_id,
            artefact_type="post_class_review_pack",
            scope=scope.value,
            plan_version_id=plan_version_id,
            student_id=student,
            experiment_condition_run_id=run.experiment_condition_run_id,
            manifest=manifest,
            artefact_refs={"origin": "generated", "specification": _SPEC, **refs},
            review_status=ArtefactReviewStatus.APPROVED
            if approved_by_the_researcher
            else ArtefactReviewStatus.PENDING,
            reviewed_by=RESEARCHER_NAME if approved_by_the_researcher else None,
        )


def _run(
    execution: ExperimentExecution,
    code: ConditionCode,
    suffix: str,
    profile: Any,
    model: str,
    pipeline: ReviewPackPipeline,
) -> ExperimentConditionRun:
    return ExperimentConditionRun(
        id=uuid.uuid4(),
        experiment_condition_run_id=f"ECR-STUDY-{suffix}",
        execution_db_id=execution.id,
        hypothesis=execution.hypothesis,
        condition_code=code.value,
        status=ConditionRunStatus.SUCCEEDED,
        condition_profile=profile.model_dump(mode="json"),
        model_name=model,
        prompt_version=pipeline.value,
        created_at=utc_now(),
        updated_at=utc_now(),
    )


def part_1_rows(
    run: dict[str, Any],
    lessons: dict[str, ImportedLesson],
    experiments: dict[str, Experiment],
    base: dict[str, Any],
) -> Staged:
    """Each lesson's twelve class revision notes: C0–C3, three draws.

    ``base`` is Part 2's record of the note it reused, the one the researcher approved.
    """
    profiles, staged = profiles_for_variant(PART_1_VARIANT), Staged()
    projections = {name: _Projection(lesson) for name, lesson in lessons.items()}
    executions: dict[tuple[str, int], ExperimentExecution] = {}
    for case in run["cases"]:
        name, draw, code = case["lesson"], int(case["repeat"]), ConditionCode(case["condition"])
        key = (name, draw)
        if key not in executions:
            executions[key] = _execution(experiments[name], Hypothesis.H1, draw, run["label"])
            staged.parents.append(executions[key])
        condition_run = _run(
            executions[key],
            code,
            _part_1_key(name, code.value, draw),
            profiles[code],
            case["model"],
            ReviewPackPipeline.V2026_08_25,
        )
        staged.runs.append(condition_run)
        staged.notes.append(
            projections[name].pack(
                condition_run,
                lessons[name].plan_version_id,
                case["sections_json"],
                {
                    "pipeline": ReviewPackPipeline.V2026_08_25.value,
                    "study": {"run": run["label"], "condition": code.value, "draw": draw},
                },
                approved_by_the_researcher=(run["label"], code.value, draw)
                == (base["run"], base["condition"], int(base["repeat"])),
            )
        )
    return staged


def _focal_type(states: dict[str, Any]) -> FocalCaseType:
    bands = {state.get("mastery_band") for state in states.values()}
    for band in _WEAKEST_FIRST:
        if band in bands:
            return FocalCaseType(band)
    return FocalCaseType.MIXED_OR_MISCONCEPTION


def part_2_rows(
    run: dict[str, Any],
    lessons: dict[str, ImportedLesson],
    experiments: dict[str, Experiment],
) -> Staged:
    """Each covered learner's P0 and P1 notes, with the learner state P1 read."""
    staged = Staged()
    projections = {
        name: _Projection(lessons[name]) for name in {case["lesson"] for case in run["cases"]}
    }
    executions: dict[str, ExperimentExecution] = {}
    focal: dict[tuple[str, str], ExperimentFocalCase] = {}
    for case in run["cases"]:
        name, student, code = (
            case["lesson"],
            learner_id(case["student"]),
            ConditionCode(case["condition"]),
        )
        if name not in executions:
            executions[name] = _execution(experiments[name], Hypothesis.H2, 1, run["label"])
            staged.parents.append(executions[name])
        if (name, student) not in focal:
            focal[(name, student)] = ExperimentFocalCase(
                id=uuid.uuid4(),
                experiment_focal_case_id=f"EFC-STUDY-{name}-{case['student']}",
                execution_db_id=executions[name].id,
                student_id=student,
                focal_case_type=_focal_type(case["learner_states"]).value,
                learner_state_snapshot=case["learner_states"],
                selection_metadata={"study_pseudonym": case["student"]},
            )
            staged.parents.append(focal[(name, student)])
        pipeline = (
            ReviewPackPipeline.V2026_09_02
            if code is ConditionCode.P1
            else ReviewPackPipeline.V2026_08_25
        )
        condition_run = _run(
            executions[name],
            code,
            _part_2_key(name, case["student"], code.value),
            profile_for(Hypothesis.H2, code),
            run["model"],
            pipeline,
        )
        condition_run.focal_case_db_id = focal[(name, student)].id
        condition_run.student_id = student
        staged.runs.append(condition_run)
        staged.notes.append(
            projections[name].pack(
                condition_run,
                lessons[name].plan_version_id,
                case["sections"],
                {
                    "pipeline": pipeline.value,
                    "study": {"run": run["label"], "condition": code.value, "base": run["base"]},
                    **(
                        {"base_note": base_note_id(name, run["base"])}
                        if code is ConditionCode.P0
                        else {}
                    ),
                },
                student=student,
                bands=pitched(case),
                approved_by_the_researcher=code is ConditionCode.P0,
            )
        )
    return staged


def pitched(case: dict[str, Any]) -> dict[str, str] | None:
    """The band each objective was pitched at, for the objectives the record says P1 personalised.

    P0 is the class note reused unchanged, and an objective P1 had no evidence on was left as it
    was: neither was pitched at the learner, so neither carries a band.
    """
    personalised = {
        outcome["lesson_objective_id"]
        for outcome in case.get("personalisation") or []
        if outcome.get("outcome") == "personalised"
    }
    states = case["learner_states"]
    return {
        objective: states[objective]["mastery_band"] for objective in sorted(personalised)
    } or None
