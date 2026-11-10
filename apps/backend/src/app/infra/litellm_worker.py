"""Configure LiteLLM globals for a job's own process and its fresh event loop."""

from __future__ import annotations

import os


def disable_litellm_telemetry() -> None:
    """Disable telemetry before task modules import generation dependencies."""
    os.environ["LITELLM_TELEMETRY"] = "False"
    import litellm

    # LiteLLM does not publish these module globals in its type surface. Keep
    # that dynamic boundary isolated here instead of erasing caller types.
    module_state = vars(litellm)
    module_state["telemetry"] = False
    module_state["success_callback"] = []
    module_state["failure_callback"] = []


def reset_litellm_logging_worker() -> None:
    """Clear litellm's global logging-worker singleton so the per-task loop owns it."""
    try:
        from litellm.litellm_core_utils.logging_worker import GLOBAL_LOGGING_WORKER

        GLOBAL_LOGGING_WORKER._queue = None
        GLOBAL_LOGGING_WORKER._worker_task = None
        GLOBAL_LOGGING_WORKER._sem = None
        GLOBAL_LOGGING_WORKER._running_tasks = set()
    except ImportError:
        pass
