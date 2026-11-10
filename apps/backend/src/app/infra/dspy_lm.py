"""Build the shared DSPy LM: one model, one endpoint, one set of quirks.

Centralised so the API process (``app.dspy_setup``), each job's process
(``app.infra.jobs.process``) and the experiments construct identical LMs instead of
drifting ``dspy.LM(...)`` call sites.

Which model each role runs, where it is served, and what it cannot be sent are declared
in ``app.infra.llm_models`` — in code, because they are experimental conditions and a
gitignored ``.env`` cannot record what a run used. The environment holds secrets only.
"""

from __future__ import annotations

import os
from typing import Any

import dspy

from app.infra.llm_models import for_role, host_of, recorded

# Per-LLM-call wall-clock cap (seconds). litellm's default is 6000s (100 min), so without
# this one hung provider request would hold a job's slot for that long, and a multi-call
# H1/H2 generation could run past the job time limit and be stopped. 300s is far above a
# healthy call (~15–30s), so it bounds the pathological case without failing legitimate
# generations: worst-case job wall-time is ~timeout × calls (a few thousand seconds),
# comfortably under the 2h job time limit.
LLM_REQUEST_TIMEOUT_SECONDS = 300

# gpt-oss-120b is served to us through a shared upstream pool that 429s with
# ``Retry-After: 59``. dspy's default of 3 retries backs off nowhere near that, so a
# transient limit killed a 40-minute experiment run outright. Eight rides out a
# minute-long window; the per-call timeout still bounds the pathological case.
LLM_RATE_LIMIT_RETRIES = 8

#: Where the bedrock-runtime judge is called, when nothing in the environment says.
DEFAULT_AWS_REGION = "us-east-1"


#: The wire formats litellm can be told to speak, which is all a provider is here.
#: ``openai`` and ``anthropic`` are the two Bedrock mantle serves, and DeepSeek serves the
#: first. ``bedrock`` is the runtime endpoint, which is not a URL at all — litellm signs
#: with SigV4 through boto3, so it takes a region instead of a base and a key.
PROVIDERS = ("openai", "anthropic", "bedrock")


def configured_model(role: str) -> str:
    """The model *role* runs: the environment's override, else ``llm_models.ROLES``.

    The assignment lives in code because it is an experimental condition — see ``ROLES``.
    The environment overrides it for a one-off without editing the repository.

    Composed rather than duplicated: the provider IS the wire format litellm picks, so
    setting them separately keeps one source for each half. A model given with a prefix
    already ("anthropic/us.anthropic.claude-sonnet-5") is taken as-is, so either style
    works and neither can contradict itself.
    """
    model = os.environ.get(f"{role.upper()}_MODEL", "").strip()
    if not model:
        return for_role(role)
    if model.partition("/")[0] in PROVIDERS:
        return model
    provider = os.environ.get(f"{role.upper()}_PROVIDER", "").strip().lower()
    if not provider:
        raise RuntimeError(
            f"{role.upper()}_MODEL is set without {role.upper()}_PROVIDER, and the "
            f"provider is how litellm picks the wire format. One of: {', '.join(PROVIDERS)}"
        )
    if provider not in PROVIDERS:
        raise RuntimeError(f"{role.upper()}_PROVIDER={provider!r} — expected one of {PROVIDERS}")
    return f"{provider}/{model}"


def active_model_name(role: str = "generator") -> str:
    """The model an LM built now would use — what a run records as its provenance.

    Harness arms set an override per process, so the configured model is not
    necessarily the one that answered.
    """
    return _MODEL_OVERRIDE or configured_model(role)


#: An escape hatch, not the configuration. A role's host normally comes from its model's
#: record in ``llm_models``; this only exists so a one-off can be pointed at another
#: endpoint without editing the repository.
_ENDPOINT_ENV = {
    "generator": ("GENERATOR_API_BASE", "LLM_API_BASE", "BEDROCK_ENDPOINT"),
    "engine": ("ENGINE_API_BASE",),
    "judge": ("JUDGE_API_BASE",),
}


#: Where each wire format lives, relative to a host root. Probed, not assumed: on Bedrock
#: mantle a routed path rejects a bad body with 400 and an unrouted one 404s with an empty
#: body, and ``/v1/messages`` — the obvious guess, and what litellm builds from a ``/v1``
#: base — 404s. Anthropic sits under ``/anthropic``. DeepSeek is the same shape, which is
#: why one rule covers both hosts.
_WIRE_ROOT = {"openai": "/v1", "anthropic": "/anthropic"}

#: Everything a host root may already have appended, longest first so a full path is
#: stripped before its prefix is.
_WIRE_PATHS = (
    "/v1/chat/completions",
    "/anthropic/v1/messages",
    "/v1/messages",
    "/chat/completions",
    "/messages",
    "/v1/responses",
    "/responses",
    "/anthropic",
    "/v1",
)


def _host_root(base: str) -> str:
    """*base* with any API path taken off, leaving the host to hang a format on."""
    base = base.rstrip("/")
    for path in _WIRE_PATHS:
        if base.endswith(path):
            return base[: -len(path)].rstrip("/")
    return base


def wire_format(role: str, model: str = "") -> str:
    """The protocol a call speaks — the prefix of the model being called.

    *model* wins over the environment because the model is what is actually on the wire.
    ``--judge-model openai/zai.glm-5`` against ``JUDGE_PROVIDER=anthropic`` sent an
    OpenAI-shaped request to the Anthropic base and 404'd; the flag is documented, so
    that was reachable from the CLI as written.
    """
    return (model or configured_model(role)).partition("/")[0]


def custom_endpoint(role: str = "generator", model: str = "") -> dict[str, str]:
    """The endpoint a *role* calls through, or empty when none is configured.

    One host serves both protocols but NOT at one base, which cost a run to learn: a
    Claude judge on ``.../v1`` had litellm build ``/v1/v1/messages`` and 404. So the
    configured URL is reduced to its host and the role's own format is appended —
    ``/v1`` for OpenAI, ``/anthropic`` for Anthropic — and any of the shapes a console
    hands out can be pasted in.

    Secrets stay in env; ``AppConfig`` reads code defaults only, deliberately.

        GENERATOR_API_BASE=https://bedrock-mantle.us-east-1.api.aws/v1
        GENERATOR_API_KEY=<bedrock api key>
        # JUDGE_API_BASE / JUDGE_API_KEY only when the judge is somewhere else
    """
    if wire_format(role, model) == "bedrock":
        # Not a URL. litellm signs with SigV4 via boto3's own credential chain, so the
        # region is the whole configuration and AWS_PROFILE (or the usual AWS_* vars)
        # carries the credentials. Returning a base or a key here would be ignored.
        return {"aws_region_name": os.environ.get("AWS_REGION") or DEFAULT_AWS_REGION}
    host = host_of(model or configured_model(role))
    # An explicit base still wins, so a one-off can be pointed anywhere without a code
    # change; otherwise the host comes from the model's own record.
    override = next((os.environ[name] for name in _ENDPOINT_ENV[role] if os.environ.get(name)), "")
    base = _host_root(override or host.base)
    if not base:
        return {}
    key = next((os.environ[name] for name in host.key_env if os.environ.get(name)), "")
    if not key:
        raise RuntimeError(
            f"{role}: {base} needs a key. Set {host.key_env[0] if host.key_env else '?'}. "
            "The AWS access key/secret pair is NOT used on this route — that is the "
            "bedrock/ SigV4 path, which the judge takes and this one does not."
        )
    return {"api_base": base + _WIRE_ROOT.get(wire_format(role, model), "/v1"), "api_key": key}


def _declare_native_tools(model: str) -> None:
    """Tell litellm what we measured, for ids its registry has never seen.

    Without this `lm.supports_function_calling` is False, and dspy's adapter drops the
    `tools` list on the floor rather than sending it — so the model is asked for tool
    calls as text and is free to answer in a text format of its own choosing.
    """
    known = recorded(model)
    if not (known and known.supports_native_tools):
        return
    import litellm

    # `supports_response_schema` decides json_schema against json_object in JSONAdapter,
    # and litellm infers it from the provider — so it is already True here by accident of
    # `litellm_provider: openai`. Stated anyway: the two capabilities are what put this
    # arm on native tools AND an enforced schema, and an inferred one can change under us
    # on a litellm upgrade without anything failing loudly.
    entry = {
        "supports_function_calling": True,
        "supports_response_schema": True,
        "litellm_provider": "openai",
        "mode": "chat",
    }
    litellm.register_model({name: entry for name in (model, model.rsplit("/", 1)[-1])})


def build_dspy_lm() -> dspy.LM:
    """The process-wide DSPy LM (model + provider routing + per-call timeout)."""
    model = active_model_name()
    _declare_native_tools(model)
    kwargs: dict[str, Any] = {
        "timeout": LLM_REQUEST_TIMEOUT_SECONDS,
        "num_retries": LLM_RATE_LIMIT_RETRIES,
    }
    kwargs.update(custom_endpoint("generator", model))
    known = recorded(model)
    if known and known.speaks_responses_api and _USE_RESPONSES_API:
        # No output ceiling here, and that is a decision with a measurement behind it.
        # Reasoning and answer DO share one budget on `/responses`, where chat
        # completions returned no reasoning at all, and a loop that reasons until
        # nothing is left returns `text: None` and is abandoned. An 8,000-token ceiling
        # was added to leave room for both. It made it SEVEN TIMES WORSE — 1 abandoned
        # loop in 102 without it, 7 in 102 with it, every one "the LM returned an empty
        # or null response". The provider's own default is evidently larger, so naming a
        # number tightened the budget rather than protecting it. Do not add one back
        # without measuring the default first.
        # `/responses` enforces a json_schema — including one shaped like a real section,
        # measured — and returns tool calls as `function_call` objects rather than
        # `[[ ## tool_calls ## ]]` written into prose. That removes the whole class of
        # parse failure where a model omits the newline before a field marker.
        kwargs["model_type"] = "responses"
    elif known and known.drops_response_format:
        # Declared per model in llm_models, not inferred from the name. These checks used
        # to read `model.startswith("deepseek/")`, and pointing DeepSeek at its own
        # OpenAI-compatible endpoint as `openai/deepseek-v4-flash` silently stopped them
        # firing — the param came back and the first call would have failed.
        #
        # Chat path only. DeepSeek's rejection is endpoint-shaped, not schema-shaped:
        # `/v1/chat/completions` 400s on any json_schema, flat or nested, while
        # `/responses` accepts and enforces both.
        kwargs["additional_drop_params"] = ["response_format"]
    kwargs.update(_SAMPLING_OVERRIDE)
    return dspy.LM(model=model, **kwargs)


# Harness arms override the model per process (e.g. --model deepseek/…); the
# API/worker never set this, so production behaviour is unchanged.
_MODEL_OVERRIDE: str | None = None
# Whether a model that declares `speaks_responses_api` is called on `/responses`. Off by
# default because the framework arms speak chat only — `provider.litellm_request` refuses
# anything else — so a run with this on would compare dspy against nothing. The dspy arms
# turn it on for themselves.
_USE_RESPONSES_API = False
# dspy caches LM responses to disk by default. In production that is free speed; in
# an experiment it is fatal — a repeated run replays the first sample instead of
# drawing a new one, so a stochastic arm reports as perfectly reproducible. `packed`
# appeared deterministic across eight cells for exactly this reason.
_SAMPLING_OVERRIDE: dict[str, Any] = {}


def set_responses_api(wanted: bool) -> None:
    """Call models that declare ``speaks_responses_api`` on ``/responses``.

    What it buys: schemas the endpoint actually enforces, native ``function_call`` tool
    calls instead of field markers parsed out of prose, and DeepSeek's
    ``reasoning_content``, which chat completions does not return.

    What it costs: the framework arms. They call chat completions and refuse anything
    else, so a run with this on compares dspy against nothing. Hence off by default and
    turned on per run by the arms that can use it.
    """
    global _USE_RESPONSES_API  # noqa: PLW0603 — deliberate process-wide switch
    _USE_RESPONSES_API = wanted


def transport_for(model: str = "") -> dspy.Adapter:
    """The endpoint and output contract a model's own record says it works on.

    One decision, not two. ``/responses`` is worth taking for the enforced schema and the
    native ``function_call`` — and those are exactly what makes ``JSONAdapter`` safe. With
    no enforced schema its "reply in JSON" is a request in the prompt and nothing more, so
    a model is free to add a field and pydantic then rejects the whole object rather than
    the field. gpt-oss did that the first time it was run through DeepSeek's adapter:
    ``additional_info: null`` on a block, and a ``RevisedSection`` refused for it.

    So a model that does not speak ``/responses`` gets ``ChatAdapter``, whose field markers
    it has a measured record on. Pairing them by hand is how one model's transport ends up
    imposed on another's.
    """
    known = recorded(model or active_model_name())
    on_responses = bool(known and known.speaks_responses_api)
    set_responses_api(on_responses)
    return dspy.JSONAdapter() if on_responses else dspy.ChatAdapter()


def set_model_override(model: str | None) -> None:
    """Route every subsequently built LM to *model* (None restores the config)."""
    global _MODEL_OVERRIDE  # noqa: PLW0603 — deliberate process-wide switch for harness arms
    _MODEL_OVERRIDE = model


def set_sampling_override(*, cache: bool | None = None, temperature: float | None = None) -> None:
    """Pin cache and temperature for every subsequently built LM.

    Experiments call this so that what was sampled is recorded rather than
    inherited from a provider default, and so repeats draw fresh samples.
    """
    global _SAMPLING_OVERRIDE  # noqa: PLW0603 — deliberate process-wide switch for harness arms
    _SAMPLING_OVERRIDE = {
        key: value
        for key, value in (("cache", cache), ("temperature", temperature))
        if value is not None
    }


def sampling_settings() -> dict[str, Any]:
    """What sampling this process is pinned to — recorded in the run fingerprint."""
    return dict(_SAMPLING_OVERRIDE)
