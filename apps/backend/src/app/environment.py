"""The process environment the API needs before any of its modules load."""

from __future__ import annotations

from dotenv import load_dotenv

from app.infra.litellm_worker import disable_litellm_telemetry


def prepare_environment() -> None:
    """Read ``.env`` (a variable already set wins), and switch LiteLLM telemetry off.

    Telemetry left on keeps a background logger alive that hangs Uvicorn on shutdown.
    """
    load_dotenv(override=False)
    disable_litellm_telemetry()
