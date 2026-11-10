"""Unit tests for the synthetic LLM-as-teacher review gate.

Covers the pure helpers (decision parsing, lesson-context rendering) and the bounded
review loop (review -> request change -> revise -> re-review -> approve), with the LLM,
revision pipeline, and artefact store all faked so the control flow is deterministic.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.evaluation.application import synthetic_teacher as st

DB = cast(AsyncSession, object())


# --- pure helpers ----------------------------------------------------------------


def test_parse_decision_maps_text_to_two_outcomes() -> None:
    assert st._parse_decision("approve") == "approve"
    assert st._parse_decision("Approve — looks good.") == "approve"
    assert st._parse_decision("request_changes") == "request_changes"
    assert st._parse_decision("Please revise the second section.") == "request_changes"
    assert st._parse_decision("reject") == "request_changes"
    assert st._parse_decision("") == "approve"  # ambiguous defaults to approve (loop terminates)


def test_lesson_context_renders_header_and_objectives() -> None:
    manifest = {
        "subject": "Mathematics",
        "grade": "JSS1",
        "topic": "Area of plane shapes",
        "lesson_plan_objectives": [
            {"objective_text": "Find the area of rectangles."},
            {"text": "Find the area of real-life objects."},
        ],
    }
    rendered = st._lesson_context(manifest)
    assert "Mathematics" in rendered and "Area of plane shapes" in rendered
    assert "- Find the area of rectangles." in rendered
    assert "- Find the area of real-life objects." in rendered


def test_lesson_context_handles_non_dict() -> None:
    assert st._lesson_context(None) == "(lesson context unavailable)"


# --- review loop -----------------------------------------------------------------


class _FakeReviewer:
    """Returns a scripted decision per call (oldest first)."""

    def __init__(self, decisions: list[str]) -> None:
        self._decisions = list(decisions)
        self.calls = 0

    def __call__(self, **kwargs: object) -> SimpleNamespace:
        self.calls += 1
        decision = self._decisions.pop(0)
        return SimpleNamespace(
            decision=decision,
            feedback="Add a worked example for objective 1.",
            rationale="needs a worked example",
        )


class _FakeRevision:
    def __init__(self) -> None:
        self.threads: list[tuple[str, str, str | None]] = []
        self.turns: list[tuple[str, str, object]] = []

    async def get_or_create_thread(
        self, *, db: AsyncSession, artefact_type: str, subject_id: str, created_by: str | None
    ) -> SimpleNamespace:
        self.threads.append((artefact_type, subject_id, created_by))
        return SimpleNamespace(revision_thread_id="RT-1")

    async def submit_turn(
        self, *, db: AsyncSession, thread_id: str, instruction: str, highlight: object
    ) -> tuple[object, object]:
        self.turns.append((thread_id, instruction, highlight))
        return SimpleNamespace(), SimpleNamespace(validation_passed=True)


class _FakeArtefacts:
    def __init__(self) -> None:
        self.approved: list[tuple[object, str | None]] = []

    async def approve_artefact(
        self, *, db: AsyncSession, artefact: object, reviewed_by: str | None
    ) -> object:
        self.approved.append((artefact, reviewed_by))
        return artefact


def _patch_loop(
    monkeypatch: pytest.MonkeyPatch, *, decisions: list[str]
) -> tuple[_FakeReviewer, _FakeRevision, _FakeArtefacts]:
    reviewer = _FakeReviewer(decisions)
    revision = _FakeRevision()
    artefacts = _FakeArtefacts()

    @contextlib.contextmanager
    def _ctx(**kwargs: object):  # type: ignore[no-untyped-def]
        yield

    # Replace the whole `dspy` reference: its real `settings` is an async-task-owned
    # proxy that ignores attribute patches and rejects cross-task use between tests.
    fake_dspy = SimpleNamespace(
        LM=lambda **kwargs: object(),
        ChainOfThought=lambda signature: reviewer,
        settings=SimpleNamespace(context=_ctx),
    )
    monkeypatch.setattr(st, "dspy", fake_dspy)
    monkeypatch.setattr(st, "build_artefact_revision_service", lambda: revision)
    monkeypatch.setattr(st, "build_artefact_service", lambda: artefacts)

    async def _pending(db: AsyncSession, experiment_id: str) -> list[str]:
        return ["AT-1"]

    async def _load(db: AsyncSession, artefact_id: str) -> SimpleNamespace:
        return SimpleNamespace(
            artefact_id=artefact_id,
            manifest={
                "subject": "Mathematics",
                "topic": "Area",
                "lesson_plan_objectives": [{"objective_text": "Find area"}],
                "steps": [{"title": "Area", "blocks": [{"content": "len × width"}]}],
            },
        )

    monkeypatch.setattr(st, "_pending_experiment_artefact_ids", _pending)
    monkeypatch.setattr(st, "_load_artefact", _load)
    return reviewer, revision, artefacts


@pytest.mark.asyncio
async def test_approves_immediately_when_pack_is_good(monkeypatch: pytest.MonkeyPatch) -> None:
    reviewer, revision, artefacts = _patch_loop(monkeypatch, decisions=["approve"])
    result = await st.review_experiment(DB, experiment_id="EXP-1")
    assert result == {"approved": 1, "revisions": 0, "pending_reviewed": 1}
    assert reviewer.calls == 1
    assert revision.turns == []  # no revision requested
    assert len(artefacts.approved) == 1
    assert artefacts.approved[0][1] == st.SYNTHETIC_REVIEWER


@pytest.mark.asyncio
async def test_requests_change_then_approves(monkeypatch: pytest.MonkeyPatch) -> None:
    reviewer, revision, artefacts = _patch_loop(
        monkeypatch, decisions=["request_changes", "approve"]
    )
    result = await st.review_experiment(DB, experiment_id="EXP-1")
    assert result == {"approved": 1, "revisions": 1, "pending_reviewed": 1}
    assert reviewer.calls == 2
    # The requested change went through the real revision-thread API on the right subject.
    assert revision.threads == [("post_class_review_pack", "AT-1", "synthetic_teacher")]
    assert revision.turns == [("RT-1", "Add a worked example for objective 1.", None)]
    assert len(artefacts.approved) == 1


@pytest.mark.asyncio
async def test_forced_approval_after_max_rounds(monkeypatch: pytest.MonkeyPatch) -> None:
    # The teacher never approves; after max_rounds revisions the pack is released anyway.
    reviewer, revision, artefacts = _patch_loop(
        monkeypatch, decisions=["request_changes", "request_changes", "request_changes"]
    )
    result = await st.review_experiment(DB, experiment_id="EXP-1", max_rounds=2)
    assert result == {"approved": 1, "revisions": 2, "pending_reviewed": 1}
    assert reviewer.calls == 3  # initial + 2 re-reviews, then break on round cap
    assert len(revision.turns) == 2
    assert len(artefacts.approved) == 1  # forced final approval
