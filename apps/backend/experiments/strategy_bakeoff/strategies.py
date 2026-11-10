"""Strategy cells for the lesson-plan generation bake-off.

Each strategy takes the three generation payloads + a ScoredLessonGenerationService
and returns a StrategyResult: the chosen plan, its violations (split into OPT /
HELD-OUT), and cost (attempts, llm_calls, latency). All strategies are scored by
the SAME deterministic check split (check_split.opt_reward) so they compete on
equal footing; the LLM-judge primary outcome is applied separately by the runner.

First-pass strategies (no production changes, no feedback-into-prompt channel —
prod drafter signatures have no prior_violations field and we are not modifying
prod):

  * baseline       — one generation attempt.
  * best_of_n      — N independent attempts, keep the one with the best OPT
                     reward (a faithful self-correction baseline that needs no
                     feedback channel; this is dspy.BestOfN semantics applied to
                     the whole pipeline).

A true feedback-injecting Refine cell is a later step (it requires a
prior_violations prompt channel; tracked separately).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from app.shared.json_types import JsonObject

from .check_split import SplitViolations, opt_reward, split_violations
from .generation import ScoredGeneration, ScoredLessonGenerationService


@dataclass
class StrategyResult:
    """Outcome of running one strategy on one subtopic."""

    strategy: str
    session_plan: JsonObject | None
    violations: list[str]
    split: SplitViolations
    opt_reward: float
    attempts: int
    total_llm_calls: int | None
    total_latency_ms: float
    attempt_rewards: list[float] = field(default_factory=list)
    error: str | None = None

    @property
    def opt_passed(self) -> bool:
        # A crashed attempt (error set) produced no plan -> never a pass, even
        # though a `generation_error` carries no OPT code.
        return self.error is None and self.split.opt_passed

    @property
    def held_out_passed(self) -> bool:
        return self.error is None and self.split.held_out_passed

    @property
    def fully_passed(self) -> bool:
        return self.error is None and self.split.fully_passed


GenPayloads = tuple[JsonObject, JsonObject, list[JsonObject]]
GenFn = Callable[[], Awaitable[ScoredGeneration]]


def _result_from(strategy: str, attempts: list[ScoredGeneration]) -> StrategyResult:
    """Pick the best attempt by OPT reward (ties -> earliest) and summarise cost."""
    best_index = 0
    best_reward = -1.0
    rewards: list[float] = []
    for index, attempt in enumerate(attempts):
        reward = opt_reward(attempt.violations)
        rewards.append(reward)
        if reward > best_reward:
            best_reward = reward
            best_index = index
    best = attempts[best_index]
    llm_calls_values = [a.llm_calls for a in attempts if a.llm_calls is not None]
    total_llm_calls = sum(llm_calls_values) if llm_calls_values else None
    return StrategyResult(
        strategy=strategy,
        session_plan=best.session_plan,
        violations=best.violations,
        split=split_violations(best.violations),
        opt_reward=best_reward,
        attempts=len(attempts),
        total_llm_calls=total_llm_calls,
        total_latency_ms=round(sum(a.latency_ms for a in attempts), 1),
        attempt_rewards=rewards,
        error=best.error,
    )


async def run_baseline(
    *,
    service: ScoredLessonGenerationService,
    payloads: GenPayloads,
    evidence_strategy: str | None = None,
) -> StrategyResult:
    """Single generation attempt — the control."""
    session_context, curriculum_context, reference_context = payloads
    attempt = await service.generate_scored(
        session_context=session_context,
        curriculum_context=curriculum_context,
        reference_context=reference_context,
        evidence_selection_strategy=evidence_strategy,
    )
    return _result_from("baseline", [attempt])


async def run_best_of_n(
    *,
    service: ScoredLessonGenerationService,
    payloads: GenPayloads,
    n: int = 3,
    evidence_strategy: str | None = None,
    stop_when_clean: bool = True,
) -> StrategyResult:
    """Up to N independent attempts; keep the best by OPT reward.

    `stop_when_clean` short-circuits once an attempt is OPT-clean (reward == 1.0),
    so the cost axis reflects early stopping rather than always paying N draws.
    """
    session_context, curriculum_context, reference_context = payloads
    attempts: list[ScoredGeneration] = []
    for _ in range(max(1, n)):
        attempt = await service.generate_scored(
            session_context=session_context,
            curriculum_context=curriculum_context,
            reference_context=reference_context,
            evidence_selection_strategy=evidence_strategy,
        )
        attempts.append(attempt)
        if stop_when_clean and opt_reward(attempt.violations) >= 1.0:
            break
    return _result_from(f"best_of_{n}", attempts)


async def run_refine(
    *,
    service: ScoredLessonGenerationService,
    payloads: GenPayloads,
    n: int = 3,
    evidence_strategy: str | None = None,
    stop_when_clean: bool = True,
    seed_attempt: ScoredGeneration | None = None,
) -> StrategyResult:
    """Feedback-injecting self-correction (pre-reg axis A, hypothesis E1).

    Unlike best_of_n (blind re-sampling), each attempt's OPT-set violations are
    fed into the NEXT attempt as guidance, so the model can target what it got
    wrong. Bounded at N<=3 (pre-reg §7.4). Only OPT-set violations are fed forward
    — HELD-OUT checks never leak into the optimisation signal (§4b).

    The feedback channel is honoured by backends whose generation program accepts
    `prior_violations` (the monolithic arm). On the staged arm the prod signatures
    have no feedback field, so this degrades to best_of_n-style re-sampling.
    """
    session_context, curriculum_context, reference_context = payloads
    attempts: list[ScoredGeneration] = []
    prior: list[str] = []
    for index in range(max(1, n)):
        if index == 0 and seed_attempt is not None:
            attempt = seed_attempt  # pre-reg §7.3 shared initial draft, when provided
        else:
            attempt = await service.generate_scored(
                session_context=session_context,
                curriculum_context=curriculum_context,
                reference_context=reference_context,
                evidence_selection_strategy=evidence_strategy,
                prior_violations=prior or None,
            )
        attempts.append(attempt)
        if stop_when_clean and opt_reward(attempt.violations) >= 1.0:
            break
        prior = split_violations(attempt.violations).opt
    return _result_from(f"refine_{n}", attempts)
