"""The job queue's bounds hold together, and every kind names a handler that exists.

No database and no processes: these read the configuration and the registry, as a drift
guard on what the runner will do with them.
"""

from __future__ import annotations

import importlib
import inspect

import pytest

from app.config import CONFIG
from app.infra.dspy_lm import LLM_REQUEST_TIMEOUT_SECONDS, build_dspy_lm
from app.infra.jobs.kinds import (
    AUTHOR_EXPERIMENT_PLAN,
    DURABLE_RUNS,
    GENERATE_CONTENT,
    GENERATE_LESSON_PLAN,
    GENERATE_STUDENT_PACK,
    IMPORT_LESSON_PLAN,
    KINDS,
    RETRY_CONDITION_RUN,
    RUN_CONDITIONED_EXECUTION,
    SYNTHETIC_LOOP,
    SYNTHETIC_RATE,
    SYNTHETIC_STUDENTS,
    SYNTHETIC_TEACHER,
    TEACHER_RUNS,
)
from app.shared.worker_delivery import MAX_TASK_DELIVERIES

# A single H1/H2 generation makes a bounded number of LLM calls (H1 ≤ ~5 conditions, H2 ≤ ~4
# focal learners × P0/P1, each with a validation retry). 16 is a generous ceiling.
_GENEROUS_LLM_CALL_CEILING = 16
#: The generations whose claim takes over a run that was cut short.
_DURABLE = (RUN_CONDITIONED_EXECUTION, RETRY_CONDITION_RUN, GENERATE_STUDENT_PACK)
#: What a teacher waits on: made again once if cut short, then reported.
_TEACHERS = (GENERATE_CONTENT, GENERATE_LESSON_PLAN, AUTHOR_EXPERIMENT_PLAN, IMPORT_LESSON_PLAN)
#: The synthetic runs a researcher triggers: one run, never repeated.
_BEST_EFFORT = (SYNTHETIC_STUDENTS, SYNTHETIC_RATE, SYNTHETIC_TEACHER, SYNTHETIC_LOOP)


def test_an_llm_call_has_a_bounded_timeout() -> None:
    assert build_dspy_lm().kwargs.get("timeout") == LLM_REQUEST_TIMEOUT_SECONDS > 0


def test_the_time_limit_sits_above_the_longest_legitimate_run() -> None:
    assert CONFIG.jobs.time_limit_seconds > LLM_REQUEST_TIMEOUT_SECONDS * _GENEROUS_LLM_CALL_CEILING


def test_a_claim_is_renewed_well_inside_its_lease() -> None:
    """Two missed beats still leave the claim held, so a slow beat is not taken for a death."""
    assert CONFIG.jobs.heartbeat_seconds * 3 <= CONFIG.jobs.lease_seconds


def test_a_durable_job_outlasts_the_claim_that_poisons_it() -> None:
    """The domain stops at MAX_TASK_DELIVERIES; one run more lets it record the poison."""
    assert 1 <= MAX_TASK_DELIVERIES <= 10
    assert DURABLE_RUNS == MAX_TASK_DELIVERIES + 1
    assert all(KINDS[kind].runs == DURABLE_RUNS for kind in _DURABLE)


def test_a_teacher_s_generation_cut_short_is_made_again_once() -> None:
    assert all(KINDS[kind].runs == TEACHER_RUNS == 2 for kind in _TEACHERS)


def test_best_effort_jobs_run_once() -> None:
    assert all(KINDS[kind].runs == 1 for kind in _BEST_EFFORT)


def test_every_kind_is_run_by_one_of_the_policies() -> None:
    assert set(KINDS) == {*_DURABLE, *_TEACHERS, *_BEST_EFFORT}


@pytest.mark.parametrize("name", sorted(KINDS))
def test_every_kind_names_an_async_handler_that_takes_what_it_is_given(name: str) -> None:
    kind = KINDS[name]
    module, function = kind.handler.split(":")
    handler = getattr(importlib.import_module(module), function)

    assert inspect.iscoroutinefunction(handler)
    takes_rerun = "redelivered" in inspect.signature(handler).parameters
    assert takes_rerun == kind.told_of_rerun
