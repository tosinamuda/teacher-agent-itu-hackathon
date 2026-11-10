"""Reasoning-module axis for the bake-off (pre-registration §3 axis B/C).

A single place that maps a `reasoning` name to the DSPy module that wraps a
generation signature, so the architecture (single vs multi signature) and the
reasoning module (predict / cot / react / rlm) vary independently.

Phase 1 implements the two cheap, robust reasoners (`predict`, `cot`). The
agentic/long-context reasoners (`react`, `rlm`) are wired in Phase 2; they raise
a clear error until then so a runner that requests them fails loudly rather than
silently falling back.
"""

from __future__ import annotations

import dspy

# Names accepted on the reasoning axis. `react`/`rlm` are recognised here so the
# CLI/validation can list them, but only become runnable in Phase 2.
REASONERS: frozenset[str] = frozenset({"predict", "cot", "react", "rlm"})
_IMPLEMENTED: frozenset[str] = frozenset({"predict", "cot", "rlm"})

# Bounded RLM loops (pre-registration §7.4: engineer within a budget; latency was
# the original blocker). RLM drives a code-interpreter REPL with sub-LLM calls, so
# these caps keep cost/latency in check during the bake-off.
RLM_MAX_ITERS = 8
RLM_MAX_LLM_CALLS = 12

# Bounded ReAct loop (pre-reg §7.4). ReAct is built per-request inside the
# monolithic module (its tools need request context), not via build_reasoning_module.
REACT_MAX_ITERS = 4


def normalize_reasoning(reasoning: str | None) -> str:
    name = (reasoning or "cot").strip().lower()
    if name in {"chain_of_thought", "chainofthought"}:
        return "cot"
    if name not in REASONERS:
        raise ValueError(
            f"unknown reasoning module: {reasoning!r} (expected one of {sorted(REASONERS)})"
        )
    return name


def build_reasoning_module(
    signature: type[dspy.Signature],
    *,
    reasoning: str,
) -> dspy.Module:
    """Wrap a single signature in the requested reasoning module.

    Used by the monolithic (single-signature) backend, and by the multi-signature
    backend for its drafting signatures.
    """
    name = normalize_reasoning(reasoning)
    if name == "predict":
        return dspy.Predict(signature)
    if name == "cot":
        return dspy.ChainOfThought(signature)
    if name == "rlm":
        # Long-context recursive reasoner over a sandboxed REPL (Deno interpreter).
        return dspy.RLM(
            signature,
            max_iters=RLM_MAX_ITERS,
            max_llm_calls=RLM_MAX_LLM_CALLS,
        )
    # react is a tool-using self-correction module; it is wired as a strategy cell
    # (run_react) in the self-correction axis, not as a drop-in reasoner here.
    raise NotImplementedError(
        f"reasoning '{name}' is not a drop-in module here. Implemented: {sorted(_IMPLEMENTED)}."
    )
