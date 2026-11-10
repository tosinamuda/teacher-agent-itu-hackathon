"""Every kind of background job, by the name a job row carries.

A handler is named by its module path and imported only in the process that runs it, so
code that queues a job never imports the code that does it.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.shared.worker_delivery import MAX_TASK_DELIVERIES

RUN_CONDITIONED_EXECUTION = "experiments.run_conditioned_execution"
RETRY_CONDITION_RUN = "experiments.retry_condition_run"
GENERATE_STUDENT_PACK = "assessments.generate_student_pack"
SYNTHETIC_STUDENTS = "assessments.synthetic_students"
SYNTHETIC_RATE = "evaluation.synthetic_rate"
SYNTHETIC_TEACHER = "evaluation.synthetic_teacher"
SYNTHETIC_LOOP = "evaluation.synthetic_loop"
GENERATE_CONTENT = "content.generate"
GENERATE_LESSON_PLAN = "lesson_plans.generate"
AUTHOR_EXPERIMENT_PLAN = "experiments.author_plan"
IMPORT_LESSON_PLAN = "content_engine.import_lesson_plan"

#: A job whose run is interrupted is run again, up to this many runs. The domain's own claim
#: stops at MAX_TASK_DELIVERIES; the run after that is what lets it record the job as poison.
DURABLE_RUNS = MAX_TASK_DELIVERIES + 1
#: A teacher's generation cut short (a deploy, a crash) is made again once; one that dies
#: twice is reported, so the teacher is not left waiting on a loop.
TEACHER_RUNS = 2


@dataclass(frozen=True)
class JobKind:
    """Where a kind's handler lives and how a run of it is treated."""

    #: ``module:function``, an async function taking the job's args.
    handler: str
    #: How many runs an interrupted job gets: one for best-effort work.
    runs: int = DURABLE_RUNS
    #: Whether the handler is told that a run follows one that was interrupted.
    told_of_rerun: bool = False


KINDS: dict[str, JobKind] = {
    RUN_CONDITIONED_EXECUTION: JobKind(
        "app.domains.experiments.application.conditioned_execution:conduct_conditioned_execution",
        told_of_rerun=True,
    ),
    RETRY_CONDITION_RUN: JobKind(
        "app.domains.experiments.application.condition_retry:retry_failed_condition"
    ),
    GENERATE_STUDENT_PACK: JobKind("app.domains.assessments.jobs:generate_student_pack"),
    SYNTHETIC_STUDENTS: JobKind("app.domains.assessments.jobs:synthetic_students", runs=1),
    SYNTHETIC_RATE: JobKind("app.domains.evaluation.jobs:synthetic_rate", runs=1),
    SYNTHETIC_TEACHER: JobKind("app.domains.evaluation.jobs:synthetic_teacher", runs=1),
    SYNTHETIC_LOOP: JobKind("app.domains.evaluation.jobs:synthetic_loop", runs=1),
    GENERATE_CONTENT: JobKind("app.domains.content.jobs:generate_content", runs=TEACHER_RUNS),
    GENERATE_LESSON_PLAN: JobKind(
        "app.domains.content_engine.jobs:generate_lesson_plan", runs=TEACHER_RUNS
    ),
    AUTHOR_EXPERIMENT_PLAN: JobKind(
        "app.domains.experiments.jobs:draft_experiment_plan", runs=TEACHER_RUNS
    ),
    IMPORT_LESSON_PLAN: JobKind(
        "app.domains.content_engine.jobs:import_lesson_plan", runs=TEACHER_RUNS
    ),
}
