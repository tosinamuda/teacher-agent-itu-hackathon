"""The models this project calls, and what each one needs.

Two wire formats, and litellm picks by the provider prefix: ``openai/<id>`` speaks OpenAI
chat completions to whatever ``api_base`` is set, ``anthropic/<id>`` speaks Anthropic
messages to it. Everything we use is reachable one of those two ways — Bedrock mantle
serves both, DeepSeek serves the OpenAI one — so ``deepseek/`` and ``bedrock/`` as
providers are gone.

That is why the quirks live here rather than in a prefix check. They used to read
``model.startswith("deepseek/")``, and the moment DeepSeek was reached as
``openai/deepseek-v4-flash`` the check stopped firing and its ``response_format`` came
back — a run that would have failed at the first call. A quirk belongs to the model, not
to the spelling of its name.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class Model:
    """One model: how to call it, what it answers to, and what it cannot take."""

    call_as: str
    """``provider/id``. The provider is the wire format; see the module docstring."""
    ids: frozenset[str]
    """Every id this model has answered to. For the same-model guard, and for reading old
    runs: the ``openrouter/`` spellings are HISTORY ONLY — nothing routes there any more —
    but they still appear in fingerprints written before the move to Bedrock, and those
    have to keep resolving to a family."""
    host: str = "bedrock-mantle"
    """Which endpoint serves it — a token that appears in that endpoint's base URL.

    ``bedrock-runtime`` is the exception: it authenticates with SigV4 through boto3's
    credential chain rather than a base URL and a bearer key, so nothing matches it and
    ``endpoint --check`` skips those models. They are verified by calling them.

    Three hosts are in play and they serve different catalogues: Bedrock mantle has the
    Claudes and gpt-oss, DeepSeek's own platform has v4-flash (mantle stops at v3.2),
    and OpenRouter has the retired sonnet-4.5. So this is what tells an operator which
    ``*_API_BASE`` a model needs, and it is what lets ``endpoint --check`` verify a
    declared id against the host that should have it instead of against all of them.
    """
    drops_response_format: bool = False
    """Whether our json_schema ``response_format`` must not be sent on CHAT COMPLETIONS.

    Two different reasons, one treatment.

    DeepSeek rejects it outright there — ``400 "This response_format type is unavailable
    now"``. That was recorded as schema-shaped, "a small typed schema passes and the
    nested section schema does not". Re-measured 2026-08-24 and it is **endpoint**-shaped:
    flat and nested both 400 on ``/v1/chat/completions``, and both are accepted AND
    enforced on ``/responses`` — including a schema shaped like a real section, with
    nested block and practice arrays. See ``speaks_responses_api``.

    Bedrock's OpenAI compatibility layer ACCEPTS it and does not enforce it, which is
    worse: gpt-oss then answers a ReAct turn in prose where dspy expects field markers
    and the adapter gives up. Its ``json_schema`` returns 200 and then ```json fences
    that do not parse. (Its ``json_object`` alone does work; the flag drops both rather
    than carry a per-format exception for a path ChatAdapter never takes.)
    """
    supports_native_tools: bool = False
    """Whether the endpoint takes a `tools` list and answers with a tool-call object.

    litellm decides this from its own model registry, and our ids are not in it —
    `openai/deepseek-v4-flash`, `openai/openai.gpt-oss-120b` — so it answers False and
    dspy silently never sends `tools` at all. Every tool call this project has ever made
    was therefore TEXT: `[[ ## tool_calls ## ]]` parsed out of prose under ChatAdapter,
    a `tool_calls` field inside JSON under JSONAdapter. That is the channel a model
    wanders off, and DeepSeek wanders off it into its own `<|DSML|tool_calls>` markup.

    Declared here so a measured capability is not lost to a registry that has never
    heard of the id. Verified against the live API: `/responses` with a `tools` list
    returns `function_call {name: read_draft, arguments: {}}`.
    """
    speaks_responses_api: bool = False
    """Whether ``/responses`` is available, with enforced schemas and native tool calls.

    This is the way out of field-marker parsing, not a preference. ``ChatAdapter`` writes
    ``[[ ## tool_calls ## ]]`` into prose and reads it back by line, so a model that omits
    one newline before the marker produces an unparseable turn — 13 of them on one
    t3-w06 run, every one recovered by a second call. On ``/responses`` the tool call is
    a ``function_call`` object and there is no marker to malform.

    Declared, not assumed: measured against the live API, ``/responses`` returned a
    conformant nested section schema and ``function_call {name: read_draft, args: {}}``.
    """

    opencode_options: JsonObject = field(default_factory=dict)
    """Request options OpenCode adds to every call of this model, as its provider sees them.

    DeepSeek's thinking mode answers 400 "Thinking mode does not support this tool_choice"
    to the forced tool choice that OpenCode's structured output sends, so the checker of a
    run on it could never answer. Measured against api.deepseek.com on 2026-11-03: the
    same request is a 200 with ``thinking`` disabled.
    """


MODELS: dict[str, Model] = {
    # Every ``call_as`` below is a literal id the endpoint returned to
    # ``experiments.h1_condition_eval.endpoint``, not a guess. Guessing produced
    # "us.anthropic.claude-sonnet-5" and "openai.gpt-oss-120b-1:0" — the AWS console
    # spellings — and mantle serves neither. ``endpoint --check`` re-verifies.
    #
    # ``ids`` is wider on purpose: it holds every spelling a model has answered to,
    # including OpenRouter's and the console's, so an old run's fingerprint still
    # resolves and the same-model guard still fires across a provider change.
    #
    # Judge. The native Anthropic route, so structured output rides tool-use.
    "claude-sonnet-5": Model(
        call_as="anthropic/anthropic.claude-sonnet-5",
        ids=frozenset(
            {
                "anthropic/anthropic.claude-sonnet-5",
                "openai/anthropic.claude-sonnet-5",
                "anthropic/us.anthropic.claude-sonnet-5",
                "openrouter/anthropic/claude-sonnet-5",
            }
        ),
    ),
    "claude-haiku-4.5": Model(
        call_as="anthropic/anthropic.claude-haiku-4-5",
        ids=frozenset(
            {
                "anthropic/anthropic.claude-haiku-4-5",
                "openai/anthropic.claude-haiku-4-5",
                "anthropic/us.anthropic.claude-haiku-4-5-20251001-v1:0",
                "openrouter/anthropic/claude-haiku-4.5",
            }
        ),
    ),
    # The study's previous judge, which produced its 144 judgments. Mantle does not serve
    # it, but bedrock-runtime does, so a run directly comparable with the August ones is
    # still possible — that is why it stays callable rather than merely resolvable. Its
    # OpenRouter and console spellings stay in ``ids`` so old fingerprints still parse.
    "claude-sonnet-4.5": Model(
        call_as="bedrock/converse/global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        host="bedrock-runtime",
        ids=frozenset(
            {
                "bedrock/converse/global.anthropic.claude-sonnet-4-5-20250929-v1:0",
                "bedrock/converse/us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                "openrouter/anthropic/claude-sonnet-4.5",
                "anthropic/us.anthropic.claude-sonnet-4-5",
                "openai/us.anthropic.claude-sonnet-4-5-v1:0",
            }
        ),
    ),
    # Generator now. Bedrock's compatibility layer accepts the schema without enforcing —
    # re-measured 2026-08-24 and still true, so this flag stays. Structured output on
    # mantle is endpoint-dependent and no endpoint enforces it:
    #
    #   /v1/chat/completions  json_object   -> 200, valid conforming JSON
    #   /v1/chat/completions  json_schema   -> 200, then ```json fences that do not parse
    #   /v1/responses         json_object   -> 200 in 1.0s, PROSE — accepted and ignored
    #   /v1/responses         json_schema   -> HANGS; 100s against a 1.1s control
    #
    # A schema that is accepted and not enforced is worse than none because it reads as
    # enforcement, and one that hangs is worse still. So the flag stays and gpt-oss stays
    # on chat completions with ChatAdapter, whose field markers it has never once
    # malformed in 306 loops.
    #
    # `speaks_responses_api` is deliberately NOT set for it. Mantle does serve
    # `/v1/responses` — 200, and native `function_call` for a sent tools list, so the
    # transport CAN be matched to DeepSeek's if the confound in the generator contrast is
    # ever worth closing — but going there would trade a working output contract for a
    # broken one. It would have to be ChatAdapter on `/responses` with native tools, not
    # JSONAdapter, and that is a change to a frozen arm rather than a free win.
    "gpt-oss-120b": Model(
        call_as="openai/openai.gpt-oss-120b",
        ids=frozenset(
            {
                "openai/openai.gpt-oss-120b",
                "openai/openai.gpt-oss-120b-1:0",
                "openrouter/openai/gpt-oss-120b",
            }
        ),
        drops_response_format=True,
    ),
    # The judge, on bedrock-runtime. Mantle refuses every Anthropic model on this account
    # whatever its runtime agreement says, and the Claude 5 generation is refused on both
    # endpoints — agreement created, quota requested at the AWS default and auto-denied in
    # 85 seconds. Everything up to 4.6 answers. See AWS-SUPPORT-SONNET-5.md.
    #
    # ``global.``/``us.`` are cross-region INFERENCE PROFILES, and the bare id is rejected
    # with "on-demand throughput isn't supported" — a ValidationException that reads like
    # a missing model rather than a missing prefix.
    "claude-sonnet-4.6": Model(
        call_as="bedrock/converse/global.anthropic.claude-sonnet-4-6",
        host="bedrock-runtime",
        ids=frozenset(
            {
                "bedrock/converse/global.anthropic.claude-sonnet-4-6",
                "bedrock/converse/us.anthropic.claude-sonnet-4-6",
                "bedrock/global.anthropic.claude-sonnet-4-6",
                "anthropic/anthropic.claude-sonnet-4-6",
                "openrouter/anthropic/claude-sonnet-4.6",
            }
        ),
    ),
    # Generator for the frozen run, on DeepSeek's own OpenAI-compatible endpoint at
    # api.deepseek.com/v1. Mantle carries deepseek.v3.1 and v3.2 only, so this one does
    # not come from Bedrock. Both ids below were read from that API's /v1/models.
    #
    # `drops_response_format` on these two is a WORKAROUND THAT HAS OUTLIVED ITS REASON,
    # measured against the live API on 2026-08-24:
    #
    #   POST /v1/chat/completions  response_format {"type":"json_object"}  -> 200, valid JSON
    #   POST /responses            text.format json_schema                 -> 200, conformant
    #   POST /responses            tools + tool_choice                     -> 200, native
    #                                                                          function_call
    #
    # v4 supports all three. Kept set only because clearing it changes how the DeepSeek
    # arm behaves relative to the runs already recorded, and no result depends on it: the
    # study's generator is gpt-oss, which has produced zero parse failures in 306 loops.
    # What it costs today is one extra LM call per ChatAdapter recovery — 13 of them on
    # t3-w06, every one a missing newline before a `[[ ## field ## ]]` marker. The route
    # out is /responses with native tools, where there is no marker to malform; that path
    # already exists in dspy_lm as `model_type="responses"`, gated off because the
    # framework arms speak chat completions only.
    "deepseek-v4-pro": Model(
        call_as="openai/deepseek-v4-pro",
        host="deepseek",
        ids=frozenset({"openai/deepseek-v4-pro", "deepseek/deepseek-v4-pro"}),
        drops_response_format=True,  # chat completions only; see speaks_responses_api
        speaks_responses_api=True,
        supports_native_tools=True,
    ),
    "deepseek-v4-flash": Model(
        call_as="openai/deepseek-v4-flash",
        host="deepseek",
        ids=frozenset(
            {
                "openai/deepseek-v4-flash",
                "deepseek/deepseek-v4-flash",
                "openrouter/deepseek/deepseek-v4-flash",
            }
        ),
        drops_response_format=True,  # chat completions only; see speaks_responses_api
        speaks_responses_api=True,
        supports_native_tools=True,
        opencode_options={"thinking": {"type": "disabled"}},
    ),
    # Gemma 4 on Bedrock is served by mantle under ``/openai/v1`` only: ``/v1`` answers
    # "model isn't supported on this route". Tool calls are native, one per turn. The id was
    # read from that host's /v1/models and verified with a tool call on 2026-11-03.
    "gemma-4-31b": Model(
        call_as="openai/google.gemma-4-31b",
        host="api.aws/openai",
        ids=frozenset({"openai/google.gemma-4-31b"}),
    ),
}


def model_family(name: str) -> str | None:
    """Which model an id names, or None if nobody has recorded that id."""
    return next((family for family, model in MODELS.items() if name in model.ids), None)


def recorded(name: str) -> Model | None:
    """The record for an id, or None. Callers decide what an unknown model means."""
    family = model_family(name)
    return MODELS[family] if family else None


def call_as(family: str) -> str:
    """The id to call *family* by, on the wire format native to it."""
    if family not in MODELS:
        raise KeyError(f"no recorded ids for {family!r}. Known: {sorted(MODELS)}")
    return MODELS[family].call_as


def hosted_at(base_url: str) -> dict[str, Model]:
    """The models declared to live on *base_url*, keyed by family.

    Matched on the host token appearing in the URL, so
    ``https://bedrock-mantle.us-east-1.api.aws/v1`` selects the mantle models and not
    DeepSeek's. Empty when no declared host matches, which is itself worth reporting.
    """
    return {family: model for family, model in MODELS.items() if model.host in base_url.lower()}


@dataclass(frozen=True)
class Host:
    """Where a family of models is served, and which env var holds the secret.

    The URL is not a secret and belongs in git; only the key is environment-specific.
    Keys are per HOST rather than per role, because two roles on one host share one key —
    which is what the old ``JUDGE_* falls back to GENERATOR_*`` chain was working around.
    """

    base: str
    key_env: tuple[str, ...] = ()
    """Env vars holding the key, first is canonical and the rest are legacy spellings."""


HOSTS: dict[str, Host] = {
    "bedrock-mantle": Host(
        "https://bedrock-mantle.us-east-1.api.aws",
        ("BEDROCK_MANTLE_API_KEY", "GENERATOR_API_KEY", "LLM_API_KEY", "AWS_BEARER_TOKEN_BEDROCK"),
    ),
    # SigV4 through boto3's credential chain: no URL to call and no bearer token to hold.
    "bedrock-runtime": Host(""),
    "deepseek": Host("https://api.deepseek.com", ("DEEPSEEK_API_KEY",)),
    # The same mantle host and key, under the ``/openai`` root that Gemma 4 is served from.
    "api.aws/openai": Host(
        "https://bedrock-mantle.us-east-1.api.aws/openai",
        ("BEDROCK_MANTLE_API_KEY", "GENERATOR_API_KEY", "LLM_API_KEY", "AWS_BEARER_TOKEN_BEDROCK"),
    ),
}


#: Which model each role runs.
#:
#: This is an experimental condition, not a deployment detail, so it is versioned here
#: rather than set in ``.env``. A gitignored file cannot record what a run used, and the
#: study has already been bitten by exactly that: two judged runs were generated from RAW
#: notes and only a SHA-256 in a fingerprint said so. The same reasoning as declaring
#: dependencies in the lockfile — an undeclared choice is an unrecorded condition.
#:
#: Override per process for a bake-off arm (``--model``/``set_model_override``) or, for a
#: one-off, with ``{ROLE}_MODEL`` + ``{ROLE}_PROVIDER`` in the environment.
#: Switching a role is a one-line edit here, and the endpoint, key and quirks follow from
#: the model's own record — ``deepseek-v4-flash`` moves the generator to
#: api.deepseek.com/v1 on DEEPSEEK_API_KEY with response_format dropped, without touching
#: anything else. ``test_every_role_is_callable_as_declared`` guards that.
#:
#: ``generator`` is the study's frozen generator and the DSPy pipelines'. ``engine`` is the
#: writer of the plugin types, run by the harness: a different decision with its own model,
#: so choosing it never changes what a study run used. A machine that cannot reach
#: DeepSeek, such as a developer's laptop, sets ``ENGINE_MODEL=openai/openai.gpt-oss-120b``.
ROLES: dict[str, str] = {
    "generator": "gpt-oss-120b",
    "engine": "deepseek-v4-flash",
    "judge": "claude-sonnet-4.6",
}


def for_role(role: str) -> str:
    """The id *role* calls by, from the versioned assignment above."""
    if role not in ROLES:
        raise KeyError(f"no model assigned to role {role!r}. Known: {sorted(ROLES)}")
    return call_as(ROLES[role])


def host_of(model: str) -> Host:
    """Where *model* is served. Unrecorded models are assumed to be on mantle.

    That default is what makes ad-hoc probing work — ``endpoint --callable`` walks ids
    that are deliberately not in ``MODELS`` — and a wrong guess surfaces immediately as a
    404 or an auth error rather than silently.
    """
    known = recorded(model)
    return HOSTS[known.host] if known else HOSTS["bedrock-mantle"]
