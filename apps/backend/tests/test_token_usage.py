"""Every model call is recorded with the tokens it spent, the writer's and the checker's alike."""

from __future__ import annotations

from typing import Any

import dspy
import pytest
from dspy.utils import DummyLM
from dspy.utils.usage_tracker import track_usage
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content_engine.infrastructure.checker import PartChecker
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.writer import EngineWriter
from app.domains.generation_log.application.recorder import GenerationLogRecorder
from app.domains.generation_log.application.spend import billed, metered
from tests.content_engine_support import PLAN, TYPE, part, seed_lesson, server_over

SPENT = {"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150}


class MeteredLM(DummyLM):
    """A scripted model that reports the tokens each reply cost, as a provider does."""

    def __init__(self, answers: list[dict[str, Any]], *, name: str = "metered") -> None:
        super().__init__(answers)
        self.model = name

    def forward(
        self, prompt: str | None = None, messages: list[dict[str, Any]] | None = None, **kwargs: Any
    ) -> Any:
        response = super().forward(prompt=prompt, messages=messages, **kwargs)
        response.usage = dict(SPENT)
        return response


class CapturingRecorder(GenerationLogRecorder):
    """The recorder, with what it would persist kept in memory."""

    def __init__(self) -> None:
        super().__init__()
        self.events: list[dict[str, Any]] = []

    def _persist(self, **fields: Any) -> None:
        self.events.append(fields)


def test_a_call_is_recorded_with_its_tokens() -> None:
    recorder = CapturingRecorder()
    predict = dspy.Predict("question -> answer")

    with dspy.context(lm=MeteredLM([{"answer": "4"}]), callbacks=[recorder]):
        predict(question="2 + 2?")

    assert [event["token_usage"] for event in recorder.events] == [SPENT]


def test_a_tracker_counting_the_calls_around_it_still_counts_them() -> None:
    lm = MeteredLM([{"answer": "4"}, {"answer": "6"}])
    predict = dspy.Predict("question -> answer")

    with dspy.context(lm=lm, callbacks=[CapturingRecorder()]), track_usage() as outer:
        predict(question="2 + 2?")
        predict(question="3 + 3?")

    assert outer.get_total_tokens()[lm.model]["total_tokens"] == 300


def _writer_turns(draft_id: str) -> list[dict[str, object]]:
    def turn(name: str, args: dict[str, object]) -> dict[str, object]:
        return {
            "next_thought": f"Call {name}.",
            "tool_calls": {"tool_calls": [{"name": name, "args": args}]},
        }

    return [
        turn("add_part", {"draft_id": draft_id, "unit_id": "s1", "part": part("A")}),
        turn("add_part", {"draft_id": draft_id, "unit_id": "s2", "part": part("B")}),
        turn("submit", {"summary": "Wrote both steps."}),
    ]


class _MeteredWriter:
    """The real writer, on a metered model scripted once the draft's ID is known."""

    async def write(self, client: Any, draft: Any, lesson: Any, *, feedback: str) -> str:
        writer = EngineWriter(MeteredLM(_writer_turns(str(draft["draft_id"])), name="writer"))
        return await writer.write(client, draft, lesson, feedback=feedback)


@pytest.mark.asyncio
async def test_every_writer_and_checker_call_of_a_draft_is_recorded_with_its_tokens(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    recorder = CapturingRecorder()
    checker_lm = MeteredLM([{"reasoning": "Both are right.", "errors": []}] * 2, name="checker")
    engine = Engine(lambda: server_over(db), _MeteredWriter, lambda: PartChecker(checker_lm))

    with dspy.context(callbacks=[recorder]), metered() as spend:
        await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    models = [event["model"] for event in recorder.events]
    assert models == ["writer"] * 3 + ["checker"] * 2
    assert all(event["token_usage"] == SPENT for event in recorder.events)
    assert {event["kind"] for event in recorder.events} == {"engine_content"}
    assert (spend.calls, spend.prompt_tokens, spend.completion_tokens) == (5, 600, 150)


@pytest.mark.parametrize(
    "usage",
    [
        {"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150},
        {"input_tokens": 120, "output_tokens": 30, "total_tokens": 150},
        {"input": 100, "output": 10, "reasoning": 20, "cache": {"read": 20, "write": 0}},
    ],
)
def test_a_call_is_billed_the_same_however_its_usage_is_reported(usage: dict[str, Any]) -> None:
    assert billed(usage) == (120, 30)


def test_model_calls_are_not_logged_unless_asked():
    from app.config import AppConfig

    assert AppConfig().log_model_calls is False
