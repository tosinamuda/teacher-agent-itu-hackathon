"""Give every unfinished generation the job that runs it.

A QUEUED or RUNNING experiment execution, and a QUEUED or RUNNING student-pack generation,
each always has an unfinished job — they are staged in one commit. Work that was queued
before jobs existed was a message in a broker instead, and is gone with it; this queues it
again. Idempotent: a generation that already has an unfinished job is left alone.

The job it queues counts as a second run, so the claim takes over an execution still marked
RUNNING by a run that was cut short.

CLI: ``uv run python -m migrations.data.requeue_unfinished_work``.
"""

from __future__ import annotations

import argparse
import json

import sqlalchemy as sa
from sqlalchemy.orm import Session

import app.db.metadata  # noqa: F401  (registers every ORM model; mappers need them all)
from app.db.config import get_sync_database_url
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.experiments.infrastructure.models import ExperimentExecution
from app.infra.jobs.kinds import GENERATE_STUDENT_PACK, RUN_CONDITIONED_EXECUTION
from app.infra.jobs.models import UNFINISHED, Job, JobState
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.time import utc_now

_UNFINISHED_WORK = ("queued", "running")


def _requeue(session: Session, kind: str, subjects: list[str]) -> int:
    held = set(
        session.scalars(
            sa.select(Job.subject).where(
                Job.kind == kind, Job.subject.in_(subjects), Job.state.in_(UNFINISHED)
            )
        )
    )
    for subject in (subject for subject in subjects if subject not in held):
        session.add(
            Job(
                job_id=new_public_id(PublicIdPrefix.JOB),
                kind=kind,
                args=[subject],
                subject=subject,
                active_subject=subject,
                state=JobState.QUEUED,
                attempts=1,
                last_error="queued again: its run was lost with the broker",
                created_at=utc_now(),
            )
        )
    return len(subjects) - len(held)


def run(database_url: str | None = None) -> dict[str, int]:
    """Queue a job for each unfinished generation that has none; return how many."""
    engine = sa.create_engine(database_url or get_sync_database_url(), future=True)
    with Session(engine) as session, session.begin():
        executions = list(
            session.scalars(
                sa.select(ExperimentExecution.execution_id).where(
                    ExperimentExecution.status.in_(_UNFINISHED_WORK)
                )
            )
        )
        generations = list(
            session.scalars(
                sa.select(StudentPackGeneration.generation_id).where(
                    StudentPackGeneration.status.in_(_UNFINISHED_WORK)
                )
            )
        )
        return {
            "executions": _requeue(session, RUN_CONDITIONED_EXECUTION, executions),
            "student_packs": _requeue(session, GENERATE_STUDENT_PACK, generations),
        }


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url", default=None, help="Database URL override.")
    args = parser.parse_args()
    print(json.dumps(run(args.database_url), indent=2))


if __name__ == "__main__":
    _main()
