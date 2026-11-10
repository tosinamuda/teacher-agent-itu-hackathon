"""Regression: the synthetic-student diagnostic path is MySQL-safe.

Two Postgres-isms surfaced the first time this path actually ran on MySQL (live
E2E, 2026-06-17) — it had always no-op'd before:

* a ``str`` ``class_id`` bound against a ``uuid.UUID`` column, which the MySQL
  ``CHAR(32)`` coltype rejects with ``'str' object has no attribute 'hex'``
  (Postgres' driver had coerced it), and
* ``order_by(func.random())``, which compiles to ``random()`` — a function MySQL
  doesn't have (it's ``RAND()``).

Both lived in ``answer_diagnostic``'s candidate query. These tests pin it: the
query must accept a str ``class_id`` and run without ``random()``, reaching a
clean "0 candidates" instead of crashing. Runs against the MySQL test DB, so a
re-introduced PG-ism fails here rather than only in production.
"""

from __future__ import annotations

import uuid

import dspy
import pytest
from sqlalchemy import text

from app.domains.assessments.application.synthetic_student import answer_diagnostic
from app.domains.curriculum.models.exit_tickets import ExitTicketItem

pytestmark = pytest.mark.asyncio


async def _seed_one_item(db) -> None:
    """One diagnostic item so ``answer_diagnostic`` reaches the candidate query.

    FK checks off: the subtopic / plan_version FK targets are irrelevant to the
    query under test (it filters ``ExitTicketItem`` by ``plan_version_id`` only).
    """
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        ExitTicketItem(
            plan_version_id="LPV-REGRESS",
            subtopic_id="sub-x",
            lesson_objective_id="obj-1",
            stem="2 + 2 = ?",
            correct_option="A",
            options={"A": "4", "B": "5"},
        )
    )
    await db.flush()


@pytest.fixture(autouse=True)
def _stub_dspy(monkeypatch):
    # The DSPy LM + student are constructed up front but never invoked when there
    # are 0 candidates; stub construction so the test needs no configured model.
    monkeypatch.setattr(dspy, "LM", lambda *a, **k: object())
    monkeypatch.setattr(dspy, "ChainOfThought", lambda *a, **k: object())


async def test_str_class_id_binds_against_uuid_column(db) -> None:
    await _seed_one_item(db)
    # A str class_id matching no learner — exercises the UUID-column bind that was
    # the '.hex' crash on MySQL, then returns cleanly with no candidates.
    result = await answer_diagnostic(
        db, plan_version_id="LPV-REGRESS", n_students=3, class_id=str(uuid.uuid4())
    )
    assert result["created"] == 0


async def test_candidate_query_has_no_random_function(db) -> None:
    await _seed_one_item(db)
    # No class filter → the candidate query runs unfiltered; before the fix the
    # ``order_by(func.random())`` would have hit MySQL's missing ``random()``.
    result = await answer_diagnostic(db, plan_version_id="LPV-REGRESS", n_students=3)
    assert result["created"] == 0
