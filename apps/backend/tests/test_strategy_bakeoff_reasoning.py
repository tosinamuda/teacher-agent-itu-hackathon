"""No-LLM tests for the reasoning-module selector (architecture axis B/C).

Module construction does not call the LLM (and RLM creates its Deno interpreter
lazily per forward()), so these run offline.
"""

from __future__ import annotations

import dspy
import pytest

from experiments.strategy_bakeoff.monolithic_signature import DraftWholeLessonPlanSignature
from experiments.strategy_bakeoff.reasoning import (
    build_reasoning_module,
    normalize_reasoning,
)


def test_normalize_reasoning_aliases_and_rejects() -> None:
    assert normalize_reasoning(None) == "cot"
    assert normalize_reasoning("chain_of_thought") == "cot"
    assert normalize_reasoning("RLM") == "rlm"
    assert normalize_reasoning("Predict") == "predict"
    with pytest.raises(ValueError):
        normalize_reasoning("bogus")


def test_build_predict_cot_rlm_modules() -> None:
    predict = build_reasoning_module(DraftWholeLessonPlanSignature, reasoning="predict")
    cot = build_reasoning_module(DraftWholeLessonPlanSignature, reasoning="cot")
    rlm = build_reasoning_module(DraftWholeLessonPlanSignature, reasoning="rlm")
    assert isinstance(predict, dspy.Predict)
    assert isinstance(cot, dspy.ChainOfThought)
    assert isinstance(rlm, dspy.RLM)


def test_rlm_loops_are_bounded() -> None:
    rlm = build_reasoning_module(DraftWholeLessonPlanSignature, reasoning="rlm")
    # Bounded per pre-reg §7.4 (latency was the original blocker).
    assert rlm.max_iters <= 10
    assert rlm.max_llm_calls <= 20


def test_react_is_not_a_dropin_reasoner() -> None:
    # react is wired as a self-correction strategy cell, not a drop-in reasoner.
    with pytest.raises(NotImplementedError):
        build_reasoning_module(DraftWholeLessonPlanSignature, reasoning="react")
