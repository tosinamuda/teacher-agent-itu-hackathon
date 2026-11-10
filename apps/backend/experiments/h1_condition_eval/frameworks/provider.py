"""One model, one provider, four frameworks.

A bake-off between harnesses measures harnesses only if every candidate reaches the same
model the same way. The dspy arms reach it through litellm carrying a per-call timeout, a
retry budget sized for a shared upstream pool that 429s with `Retry-After: 59`, an
OpenRouter provider block, and whatever sampling the run pinned.

So the request below is READ OFF the LM `build_dspy_lm` returns rather than rebuilt from
the same rules. A second copy of those rules would drift, and the drift would arrive
looking like a difference between frameworks.
"""

from __future__ import annotations

from typing import Any

from app.infra.dspy_lm import build_dspy_lm

NO_LITELLM_CACHE = {"no-cache": True, "no-store": True}
"""What dspy sends litellm on every call. Its own cache sits a layer above, and a replayed
draw is the documented way an experiment reports a stochastic arm as reproducible."""


def litellm_request() -> dict[str, Any]:
    """The litellm call the dspy arms make, as keyword arguments.

    Raises:
        ValueError: when the configured model is not served over chat completions, which
            is the only endpoint these arms speak.
    """
    lm = build_dspy_lm()
    if lm.model_type != "chat":
        raise ValueError(
            f"{lm.model} reaches dspy over the {lm.model_type!r} endpoint and these arms "
            "call chat completions. Running both would compare endpoints, not frameworks."
        )
    return {
        "model": lm.model,
        "num_retries": lm.num_retries,
        "retry_strategy": "exponential_backoff_retry",
        "cache": dict(NO_LITELLM_CACHE),
        **{key: value for key, value in lm.kwargs.items() if value is not None},
    }
