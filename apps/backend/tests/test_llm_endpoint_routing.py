"""Where a role's requests are actually sent, and which id they name.

Both halves have been wrong in a way no unit test would have caught, because both look
right until a real call is made:

- The judge was pointed at ``<host>/v1`` for the Anthropic protocol. litellm appends
  ``/v1/messages`` to what it is given, so the request went to ``/v1/v1/messages`` and
  came back 404 — read as a dead endpoint, not as a base URL with one segment too many.
- Two of five model ids were the AWS console's spelling rather than the endpoint's
  (``us.anthropic.claude-sonnet-5``, ``openai.gpt-oss-120b-1:0``). Neither is served.

Nothing here calls out. The path arithmetic and the declared ids are what these pin;
``endpoint --check`` and ``endpoint --callable`` verify the rest against the live host.
"""

from __future__ import annotations

import pytest

from app.infra.dspy_lm import _host_root, configured_model, custom_endpoint, wire_format
from app.infra.llm_models import MODELS, hosted_at, model_family

MANTLE = "https://bedrock-mantle.us-east-1.api.aws"


@pytest.mark.parametrize(
    "pasted",
    [
        MANTLE,
        f"{MANTLE}/",
        f"{MANTLE}/v1",
        f"{MANTLE}/v1/chat/completions",
        f"{MANTLE}/anthropic",
        f"{MANTLE}/anthropic/v1/messages",
        f"{MANTLE}/v1/responses",
    ],
)
def test_any_shape_a_console_hands_out_reduces_to_the_host(pasted: str) -> None:
    """An operator pastes whatever the console showed them; all of it is the same host."""
    assert _host_root(pasted) == MANTLE


@pytest.mark.parametrize(
    ("provider", "model", "expected"),
    [
        ("openai", "openai.gpt-oss-120b", f"{MANTLE}/v1"),
        ("anthropic", "anthropic.claude-sonnet-5", f"{MANTLE}/anthropic"),
    ],
)
def test_each_wire_format_gets_its_own_base(
    monkeypatch: pytest.MonkeyPatch, provider: str, model: str, expected: str
) -> None:
    """The two protocols do NOT share a base, which is what the 404 was.

    litellm appends the rest — ``/chat/completions`` or ``/v1/messages`` — so the base
    must stop one segment earlier for Anthropic than the OpenAI-shaped URL suggests.
    """
    monkeypatch.setenv("GENERATOR_API_BASE", f"{MANTLE}/v1")
    monkeypatch.setenv("GENERATOR_API_KEY", "k")
    monkeypatch.setenv("GENERATOR_PROVIDER", provider)
    monkeypatch.setenv("GENERATOR_MODEL", model)
    assert wire_format("generator") == provider
    assert custom_endpoint("generator")["api_base"] == expected


def test_two_roles_on_one_host_share_its_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """The key is the host's, so naming it once serves both roles and both protocols."""
    monkeypatch.setenv("BEDROCK_MANTLE_API_KEY", "shared")
    monkeypatch.setenv("GENERATOR_PROVIDER", "openai")
    monkeypatch.setenv("GENERATOR_MODEL", "openai.gpt-oss-120b")
    monkeypatch.setenv("JUDGE_PROVIDER", "anthropic")
    monkeypatch.setenv("JUDGE_MODEL", "anthropic.claude-sonnet-5")
    assert custom_endpoint("generator") == {"api_base": f"{MANTLE}/v1", "api_key": "shared"}
    assert custom_endpoint("judge") == {"api_base": f"{MANTLE}/anthropic", "api_key": "shared"}


def test_deepseek_takes_the_same_two_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    """The frozen run's host, which is why one rule covers both rather than a special case."""
    monkeypatch.setenv("DEEPSEEK_API_KEY", "k")
    monkeypatch.setenv("GENERATOR_MODEL", "deepseek-v4-flash")
    for provider, expected in (("openai", "/v1"), ("anthropic", "/anthropic")):
        monkeypatch.setenv("GENERATOR_API_BASE", "https://api.deepseek.com/v1")
        monkeypatch.setenv("GENERATOR_PROVIDER", provider)
        assert custom_endpoint("generator")["api_base"] == "https://api.deepseek.com" + expected


def test_every_declared_call_as_is_one_of_the_ids_it_answers_to() -> None:
    """A ``call_as`` outside its own ``ids`` would defeat the same-model guard."""
    for family, model in MODELS.items():
        assert model.call_as in model.ids, family
        assert model_family(model.call_as) == family


def test_each_model_is_declared_on_exactly_one_host() -> None:
    """``hosted_at`` selects by substring, so two hosts sharing a token would double-count.

    OpenRouter is empty now that both Sonnets are reached through bedrock-runtime, and
    that is the point: nothing should be attributed to a host merely because an old id
    for it survives in ``ids``.
    """
    for base, expected in (
        (f"{MANTLE}/v1", {"claude-sonnet-5", "claude-haiku-4.5", "gpt-oss-120b"}),
        ("https://api.deepseek.com/v1", {"deepseek-v4-flash", "deepseek-v4-pro"}),
        ("https://openrouter.ai/api/v1", set()),
    ):
        assert set(hosted_at(base)) == expected


def test_an_explicit_judge_model_moves_the_base_with_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """``--judge-model`` overrides the model, so it has to override the path too.

    Reachable from the CLI as documented: an OpenAI-shaped judge against an Anthropic
    ``JUDGE_PROVIDER`` was posted to ``/anthropic/chat/completions`` and 404'd.
    """
    monkeypatch.setenv("GENERATOR_API_BASE", f"{MANTLE}/v1")
    monkeypatch.setenv("GENERATOR_API_KEY", "k")
    monkeypatch.setenv("JUDGE_PROVIDER", "anthropic")
    monkeypatch.setenv("JUDGE_MODEL", "anthropic.claude-sonnet-5")
    monkeypatch.delenv("JUDGE_API_BASE", raising=False)
    monkeypatch.delenv("JUDGE_API_KEY", raising=False)
    assert custom_endpoint("judge")["api_base"] == f"{MANTLE}/anthropic"
    assert custom_endpoint("judge", "openai/zai.glm-5")["api_base"] == f"{MANTLE}/v1"


def test_bedrock_runtime_is_a_region_not_a_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """The judge's endpoint. litellm signs with SigV4 through boto3, so there is no base
    URL and no bearer key — a base configured for the generator must not leak into it.
    """
    monkeypatch.setenv("GENERATOR_API_BASE", f"{MANTLE}/v1")
    monkeypatch.setenv("GENERATOR_API_KEY", "k")
    monkeypatch.setenv("JUDGE_PROVIDER", "bedrock")
    monkeypatch.setenv("JUDGE_MODEL", "converse/global.anthropic.claude-sonnet-4-6")
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    assert wire_format("judge") == "bedrock"
    assert custom_endpoint("judge") == {"aws_region_name": "eu-west-1"}


def test_a_slash_alone_does_not_mean_the_provider_is_already_there(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bedrock ids embed a slash of their own.

    ``converse/global.anthropic.claude-sonnet-4-6`` is a model, not a prefixed one, and
    treating any slash as "already prefixed" dropped the provider and produced a string
    litellm cannot route.
    """
    monkeypatch.setenv("JUDGE_PROVIDER", "bedrock")
    monkeypatch.setenv("JUDGE_MODEL", "converse/global.anthropic.claude-sonnet-4-6")
    assert configured_model("judge") == "bedrock/converse/global.anthropic.claude-sonnet-4-6"
    monkeypatch.setenv("JUDGE_MODEL", "bedrock/converse/global.anthropic.claude-sonnet-4-6")
    assert configured_model("judge") == "bedrock/converse/global.anthropic.claude-sonnet-4-6"


def test_the_judge_models_resolve_to_the_family_they_are_configured_as() -> None:
    """A judged run records the model string; it has to name a family we can identify.

    Without this the same-model guard cannot prove the judge is not the generator, and
    ``build_judge_lm`` degrades to a warning.
    """
    for family in ("claude-sonnet-4.6", "claude-sonnet-4.5"):
        assert model_family(MODELS[family].call_as) == family
        assert MODELS[family].host == "bedrock-runtime"
        assert MODELS[family].call_as.startswith("bedrock/converse/")


def test_every_role_is_callable_as_declared(monkeypatch: pytest.MonkeyPatch) -> None:
    """Switching a role must be a one-line edit, so every candidate has to be complete.

    A role names a family; the family has to exist, resolve to itself, and sit on a host
    that either has a key variable or is the SigV4 one. Without this, swapping the
    generator to deepseek-v4-flash for the frozen run fails at its first call rather than
    here.
    """
    from app.infra.dspy_lm import custom_endpoint
    from app.infra.llm_models import HOSTS, ROLES, for_role

    monkeypatch.setenv("BEDROCK_MANTLE_API_KEY", "k")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "k")
    for role, family in ROLES.items():
        assert family in MODELS, f"{role} names an unknown model {family!r}"
        assert model_family(for_role(role)) == family
        host = HOSTS[MODELS[family].host]
        assert host.key_env or not host.base, f"{family} sits on a host with no key"

    for family, model in MODELS.items():
        monkeypatch.setenv("GENERATOR_MODEL", model.call_as)
        connection = custom_endpoint("generator")
        assert connection, f"{family} resolves to no endpoint at all"
        assert "api_key" in connection or "aws_region_name" in connection, family


def test_gemma_4_is_called_under_the_openai_root_of_the_mantle_host(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BEDROCK_MANTLE_API_KEY", "k")

    connection = custom_endpoint("generator", "openai/google.gemma-4-31b")

    assert connection["api_base"] == f"{MANTLE}/openai/v1"
    assert custom_endpoint("generator", "openai/openai.gpt-oss-120b")["api_base"] == f"{MANTLE}/v1"


def test_opencode_turns_deepseeks_thinking_off_and_leaves_other_models_alone() -> None:
    from app.domains.content_engine.infrastructure.harness.opencode_session import Model

    def models(model_id: str) -> dict[str, object]:
        provider = Model(model_id, "https://example.test/v1", "k").provider()
        listed = provider["models"]
        assert isinstance(listed, dict)
        return listed

    assert models("deepseek-v4-flash")["deepseek-v4-flash"] == {
        "name": "deepseek-v4-flash",
        "tool_call": True,
        "options": {"thinking": {"type": "disabled"}},
    }
    assert "options" not in models("openai.gpt-oss-120b")["openai.gpt-oss-120b"]


def test_the_engine_runs_deepseek_and_the_studys_generator_stays_on_gpt_oss(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.domains.content_engine.infrastructure.harness.models import generator_route

    monkeypatch.delenv("ENGINE_MODEL", raising=False)
    monkeypatch.delenv("GENERATOR_MODEL", raising=False)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")

    assert generator_route() == (
        "deepseek-v4-flash",
        "https://api.deepseek.com/v1",
        "deepseek-key",
    )
    assert configured_model("generator") == "openai/openai.gpt-oss-120b"


def test_a_machine_without_deepseek_points_the_engine_at_bedrock_by_its_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.domains.content_engine.infrastructure.harness.models import generator_route

    monkeypatch.setenv("ENGINE_MODEL", "openai/openai.gpt-oss-120b")
    monkeypatch.setenv("BEDROCK_MANTLE_API_KEY", "mantle-key")

    assert generator_route() == ("openai.gpt-oss-120b", f"{MANTLE}/v1", "mantle-key")
