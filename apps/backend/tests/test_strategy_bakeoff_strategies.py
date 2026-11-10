"""No-LLM tests for the bake-off strategy cells.

The generation service is stubbed with scripted ScoredGeneration outputs, so the
strategy control flow (best-by-OPT-reward selection, early stop, cost
aggregation) is tested deterministically without any LLM call.
"""

from __future__ import annotations

import pytest

from experiments.strategy_bakeoff.generation import ScoredGeneration
from experiments.strategy_bakeoff.strategies import (
    run_baseline,
    run_best_of_n,
    run_refine,
)


class _StubService:
    """Returns scripted ScoredGeneration objects in order, counting calls."""

    def __init__(self, scripted: list[ScoredGeneration]) -> None:
        self._scripted = scripted
        self.calls = 0

    async def generate_scored(self, **_kwargs: object) -> ScoredGeneration:
        result = self._scripted[min(self.calls, len(self._scripted) - 1)]
        self.calls += 1
        return result


class _RecordingService:
    """Like _StubService, but records the prior_violations each call received."""

    def __init__(self, scripted: list[ScoredGeneration]) -> None:
        self._scripted = scripted
        self.calls = 0
        self.prior_violations_seen: list[list[str] | None] = []

    async def generate_scored(
        self, *, prior_violations: list[str] | None = None, **_kwargs: object
    ) -> ScoredGeneration:
        self.prior_violations_seen.append(prior_violations)
        result = self._scripted[min(self.calls, len(self._scripted) - 1)]
        self.calls += 1
        return result


def _gen(violations: list[str], *, llm_calls: int = 5, latency: float = 100.0) -> ScoredGeneration:
    # Mirror the real generate_scored contract: a crash sets BOTH error and the
    # generation_error violation, and yields no plan.
    errored = bool(violations) and "generation_error" in violations[0]
    return ScoredGeneration(
        session_plan=None if errored else {"ok": True},
        violations=violations,
        latency_ms=latency,
        llm_calls=llm_calls,
        error="boom" if errored else None,
    )


_PAYLOADS = ({"s": 1}, {"c": 1}, [{"r": 1}])


@pytest.mark.asyncio
async def test_baseline_single_attempt() -> None:
    service = _StubService([_gen([])])
    result = await run_baseline(service=service, payloads=_PAYLOADS)  # type: ignore[arg-type]
    assert service.calls == 1
    assert result.attempts == 1
    assert result.fully_passed is True
    assert result.opt_reward == 1.0


@pytest.mark.asyncio
async def test_best_of_n_stops_early_when_clean() -> None:
    # First attempt already OPT-clean -> should stop after 1 despite n=3.
    service = _StubService([_gen([]), _gen(["reused_modeling_record: x"])])
    result = await run_best_of_n(service=service, payloads=_PAYLOADS, n=3)  # type: ignore[arg-type]
    assert service.calls == 1
    assert result.attempts == 1
    assert result.opt_passed is True


@pytest.mark.asyncio
async def test_best_of_n_keeps_best_when_none_clean() -> None:
    # Two OPT violations, then one, then two -> best is the middle (reward higher).
    service = _StubService(
        [
            _gen(["reused_modeling_record: a", "mixed_direction_evidence: b"]),
            _gen(["reused_modeling_record: a"]),
            _gen(["reused_modeling_record: a", "mixed_direction_evidence: b"]),
        ]
    )
    result = await run_best_of_n(
        service=service,  # type: ignore[arg-type]
        payloads=_PAYLOADS,
        n=3,
        stop_when_clean=True,
    )
    assert service.calls == 3  # never clean -> uses all N
    assert result.attempts == 3
    assert result.opt_passed is False
    # best kept attempt has exactly one OPT violation
    assert len(result.split.opt) == 1
    # cost aggregates across all attempts
    assert result.total_llm_calls == 15


@pytest.mark.asyncio
async def test_held_out_violation_does_not_block_opt_pass() -> None:
    # OPT-clean but a held-out violation present: opt passes, fully does not.
    service = _StubService([_gen(["ungrounded_evaluation_material: worksheet"])])
    result = await run_best_of_n(service=service, payloads=_PAYLOADS, n=3)  # type: ignore[arg-type]
    assert service.calls == 1  # opt-clean -> early stop
    assert result.opt_passed is True
    assert result.held_out_passed is False
    assert result.fully_passed is False


@pytest.mark.asyncio
async def test_errored_attempt_scores_as_non_pass() -> None:
    # A crashed generation must never read as a pass, even though generation_error
    # carries no OPT code (the bug this fix closes).
    service = _StubService([_gen(["generation_error: ValueError: boom"])])
    result = await run_baseline(service=service, payloads=_PAYLOADS)  # type: ignore[arg-type]
    assert result.error is not None
    assert result.opt_reward == 0.0
    assert result.opt_passed is False
    assert result.held_out_passed is False
    assert result.fully_passed is False


@pytest.mark.asyncio
async def test_best_of_n_prefers_clean_attempt_over_errored() -> None:
    # Errored first (reward 0), clean second: the clean plan must be chosen.
    service = _StubService([_gen(["generation_error: ValueError: boom"]), _gen([])])
    result = await run_best_of_n(
        service=service,  # type: ignore[arg-type]
        payloads=_PAYLOADS,
        n=2,
        stop_when_clean=False,
    )
    assert service.calls == 2
    assert result.fully_passed is True
    assert result.session_plan == {"ok": True}
    assert result.error is None


@pytest.mark.asyncio
async def test_refine_feeds_opt_violations_into_next_attempt() -> None:
    # attempt 1 has an OPT violation, attempt 2 is clean.
    service = _RecordingService([_gen(["reused_modeling_record: x"]), _gen([])])
    result = await run_refine(service=service, payloads=_PAYLOADS, n=3)  # type: ignore[arg-type]
    assert service.calls == 2  # stops after the clean attempt
    assert service.prior_violations_seen[0] is None  # first attempt: no feedback
    # second attempt receives the OPT violation as feedback
    assert service.prior_violations_seen[1] == ["reused_modeling_record: x"]
    assert result.fully_passed is True


@pytest.mark.asyncio
async def test_refine_early_stops_on_clean_first_attempt() -> None:
    service = _RecordingService([_gen([])])
    result = await run_refine(service=service, payloads=_PAYLOADS, n=3)  # type: ignore[arg-type]
    assert service.calls == 1
    assert result.opt_passed is True


@pytest.mark.asyncio
async def test_refine_does_not_feed_held_out_violations_forward() -> None:
    # Held-out violations must NOT leak into the optimisation signal (§4b).
    service = _RecordingService([_gen(["ungrounded_evaluation_material: worksheet"]), _gen([])])
    await run_refine(
        service=service,  # type: ignore[arg-type]
        payloads=_PAYLOADS,
        n=2,
        stop_when_clean=False,
    )
    # OPT set is empty for a held-out-only attempt -> no feedback fed forward.
    assert service.prior_violations_seen[1] is None


@pytest.mark.asyncio
async def test_best_of_n_does_not_early_stop_on_errored_attempt() -> None:
    # An errored attempt has reward 0.0, so it must NOT satisfy the clean
    # early-stop condition; the loop continues to the clean attempt.
    service = _StubService([_gen(["generation_error: ValueError: boom"]), _gen([])])
    result = await run_best_of_n(
        service=service,  # type: ignore[arg-type]
        payloads=_PAYLOADS,
        n=3,
        stop_when_clean=True,
    )
    assert service.calls == 2  # stops on the clean attempt, not the errored one
    assert result.opt_passed is True
