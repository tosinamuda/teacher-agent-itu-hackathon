"""The generator as a LangChain chat model: the model, endpoint and sampling DSPy's LM uses."""

from __future__ import annotations

from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.infra.dspy_lm import (
    LLM_RATE_LIMIT_RETRIES,
    LLM_REQUEST_TIMEOUT_SECONDS,
    active_model_name,
    custom_endpoint,
    sampling_settings,
    wire_format,
)


class UnsupportedGeneratorError(RuntimeError):
    """The generator is not served on an OpenAI-compatible chat endpoint."""


#: The role the harness's writers and checkers run as: ``llm_models.ROLES``.
ENGINE_ROLE = "engine"


def generator_route() -> tuple[str, str, str]:
    """The engine's model ID, base URL and key, on its OpenAI-compatible endpoint."""
    model = active_model_name(ENGINE_ROLE)
    endpoint = custom_endpoint(ENGINE_ROLE, model)
    if wire_format(ENGINE_ROLE, model) != "openai" or "api_base" not in endpoint:
        raise UnsupportedGeneratorError(f"{model} is not on an OpenAI-compatible endpoint")
    return model.partition("/")[2], endpoint["api_base"], endpoint["api_key"]


def generator_chat_model() -> ChatOpenAI:
    """Chat completions, as DSPy's LM calls them, with native tool calls."""
    model, base_url, key = generator_route()
    temperature = sampling_settings().get("temperature")
    # Validated from its aliases: type checkers disagree on which names the constructor takes.
    return ChatOpenAI.model_validate(
        {
            "model": model,
            "base_url": base_url,
            "api_key": SecretStr(key),
            "timeout": LLM_REQUEST_TIMEOUT_SECONDS,
            "max_retries": LLM_RATE_LIMIT_RETRIES,
            "use_responses_api": False,
            "temperature": float(temperature) if isinstance(temperature, (int, float)) else None,
        }
    )
