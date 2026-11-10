"""The blinded rating pass as code, and the two properties that make it a measurement.

The study's 144 judgments were produced by hand-dispatched agents. Moving the pass
into the repository is only worth it if the pass is the same one, so these pin the
things that would quietly stop it being the same: the packet it reads, one candidate
per call, and a judge that is not the generator.

No API call — the LM boundary is replaced by the recorder, as in the leakage suite.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from recording_lm import RecordingLM, completion

from app.domains.evaluation.application.constants import H1_RUBRIC
from experiments.h1_condition_eval.collect_judgments import DIMENSIONS, _check_shape
from experiments.h1_condition_eval.judge import (
    JudgeModelError,
    RatePacket,
    build_judge_lm,
    judge_packet,
    judge_run,
)


def _rating(score: int = 4) -> dict[str, object]:
    return {"score": score, "evidence": ["a concrete observation"], "rationale": "because."}


def _answer(score: int = 4) -> str:
    return completion(**{dimension: _rating(score) for dimension in DIMENSIONS})


def test_the_judge_rates_every_frozen_dimension_and_nothing_else() -> None:
    """The signature IS the rubric — a dimension added to one and not the other shows here."""
    outputs = set(RatePacket.output_fields)
    assert outputs == set(DIMENSIONS)
    assert outputs == {str(criterion["criterion_id"]) for criterion in H1_RUBRIC}


def test_a_judgment_passes_the_collector_that_guards_a_hand_run() -> None:
    """An in-code pass meets the same refusals, so neither route can write a bad set."""
    lm = RecordingLM(_answer())
    judgment = asyncio.run(judge_packet({"candidate_id": "cand-1", "body": "packet"}, lm=lm))

    assert judgment["candidate_id"] == "cand-1"
    _check_shape(__import__("pathlib").Path("cand-1.json"), judgment)


def test_each_candidate_is_judged_in_its_own_call() -> None:
    """Two packs to one judge invites it to decide which is meant to win.

    That is the design's core blinding property, and it is the one a concurrency
    refactor would silently break — so it is asserted on the calls, not the docs.
    """
    packets = [{"candidate_id": f"cand-{n}", "body": f"packet {n}"} for n in range(3)]
    lm = RecordingLM(*(_answer() for _ in packets))

    async def run() -> list[dict[str, object]]:
        return [await judge_packet(packet, lm=lm) for packet in packets]

    judged = asyncio.run(run())

    assert len(lm.sent) == len(packets)
    assert {j["candidate_id"] for j in judged} == {"cand-0", "cand-1", "cand-2"}
    for index, body in enumerate(lm.prompts):
        assert f"packet {index}" in body
        for other in range(3):
            if other != index:
                assert f"packet {other}" not in body


def test_a_judge_may_not_be_the_model_that_wrote_the_packs(monkeypatch: pytest.MonkeyPatch) -> None:
    """A model marking its own homework is not a measurement."""
    monkeypatch.setattr(
        "experiments.h1_condition_eval.judge.active_model_name", lambda: "openrouter/some/model"
    )

    with pytest.raises(JudgeModelError):
        build_judge_lm("openrouter/some/model")

    assert build_judge_lm("openrouter/other/model").model == "openrouter/other/model"


def test_the_run_pass_judges_every_candidate_the_packets_contain(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packets = [{"candidate_id": f"cand-{n}", "body": f"packet {n}"} for n in range(4)]
    monkeypatch.setattr("experiments.h1_condition_eval.judge.build", lambda label: (packets, []))
    # A pass is refused unless the run's packets were built, because the key that
    # de-anonymises it is only read after every call has been paid for. The stub stands
    # in for the packets; the key has to be on disk like the real thing.
    monkeypatch.setattr("experiments.h1_condition_eval.judge.HERE", tmp_path)
    rating = tmp_path / "runs" / "any-run" / "rating"
    rating.mkdir(parents=True)
    (rating / "_key.json").write_text("[]")
    lm = RecordingLM(*(_answer() for _ in packets))

    judged = asyncio.run(judge_run("any-run", lm=lm, concurrency=2))

    assert {j["candidate_id"] for j in judged} == {p["candidate_id"] for p in packets}
    assert len(lm.sent) == len(packets)


def test_the_same_model_through_two_providers_is_refused():
    """One model, many provider ids — looked up, never inferred.

    Bedrock core, Bedrock mantle and OpenRouter each name a model differently, and this
    began as a regex trying to normalise them into a common shape. It was wrong three
    times: it fused a snapshot date into a version number, and it read `sonnet-4-5` as a
    subset of `sonnet-5`. A declared table cannot be wrong in a way nobody can see.
    """
    from app.infra.llm_models import MODELS, model_family
    from experiments.h1_condition_eval.judge import _same_model

    sonnet5 = sorted(MODELS["claude-sonnet-5"].ids)
    for other in sonnet5[1:]:
        assert _same_model(sonnet5[0], other), other

    gpt = "openai/openai.gpt-oss-120b-1:0"
    assert not _same_model(sonnet5[0], gpt)
    assert not _same_model(sonnet5[0], "openai/anthropic.claude-sonnet-4-5-v1:0")
    assert not _same_model(sonnet5[0], "openai/anthropic.claude-haiku-4-5-v1:0")

    # An id nobody has recorded is not claimed to match anything — build_judge_lm warns
    # rather than pretending it proved something.
    assert model_family("openai/anthropic.claude-sonnet-9-v1:0") is None
    assert not _same_model("openai/anthropic.claude-sonnet-9-v1:0", gpt)


def test_no_model_id_is_claimed_by_two_families():
    """A duplicate id would make the guard answer differently depending on dict order."""
    from app.infra.llm_models import MODELS

    seen: dict[str, str] = {}
    for family, model in MODELS.items():
        for name in model.ids:
            assert name not in seen, f"{name} claimed by {seen.get(name)} and {family}"
            seen[name] = family


def test_a_host_without_its_key_fails_loudly(monkeypatch):
    """A key belongs to a HOST, not to a role, and its absence must not be silent.

    Both roles sharing one key used to be a fallback chain from judge to generator; it is
    now simply the same host answering to the same variable. What must not happen is an
    LM built with no credential at all, which fails later and far less legibly.
    """
    monkeypatch.delenv("BEDROCK_MANTLE_API_KEY", raising=False)
    monkeypatch.setenv("JUDGE_PROVIDER", "anthropic")
    monkeypatch.setenv("JUDGE_MODEL", "anthropic.claude-sonnet-5")
    with pytest.raises(RuntimeError, match="BEDROCK_MANTLE_API_KEY"):
        build_judge_lm("anthropic/anthropic.claude-sonnet-5")


def test_the_judge_endpoint_comes_from_its_own_model(monkeypatch):
    """Not from the generator's. The two roles run on different hosts by default.

    The judge is on bedrock-runtime, which is SigV4 and has no URL; the generator is on
    mantle, which has both a URL and a bearer key. Inheriting either from the other would
    send one role's credential to the other's host.
    """
    from app.infra.dspy_lm import custom_endpoint

    generator, judge = custom_endpoint("generator"), custom_endpoint("judge")
    assert generator["api_base"].endswith("/v1") and generator["api_key"]
    assert judge == {"aws_region_name": "us-east-1"}


def test_provider_and_model_compose_into_the_litellm_name(monkeypatch):
    """Two halves, one source each, rather than a prefix duplicated in two places.

    The provider IS the wire format litellm picks, so it is not a second fact beside the
    model id — it is the front of it. A model already carrying a prefix is taken as-is,
    so both styles work and neither can contradict itself.
    """
    from app.infra.dspy_lm import active_model_name, configured_model

    monkeypatch.setenv("GENERATOR_MODEL", "openai.gpt-oss-120b-1:0")
    monkeypatch.setenv("GENERATOR_PROVIDER", "openai")
    monkeypatch.setenv("JUDGE_MODEL", "us.anthropic.claude-sonnet-5")
    monkeypatch.setenv("JUDGE_PROVIDER", "anthropic")
    assert active_model_name() == "openai/openai.gpt-oss-120b-1:0"
    assert configured_model("judge") == "anthropic/us.anthropic.claude-sonnet-5"

    monkeypatch.setenv("JUDGE_MODEL", "anthropic/us.anthropic.claude-sonnet-5")
    assert configured_model("judge") == "anthropic/us.anthropic.claude-sonnet-5"


def test_a_model_without_its_provider_is_refused(monkeypatch):
    """Silently guessing the wire format is how a run reaches the wrong endpoint."""
    from app.infra.dspy_lm import configured_model

    monkeypatch.setenv("JUDGE_MODEL", "us.anthropic.claude-sonnet-5")
    monkeypatch.delenv("JUDGE_PROVIDER", raising=False)
    with pytest.raises(RuntimeError, match="without JUDGE_PROVIDER"):
        configured_model("judge")

    monkeypatch.setenv("JUDGE_PROVIDER", "bedrock-mantle")
    with pytest.raises(RuntimeError, match="expected one of"):
        configured_model("judge")


def test_a_models_quirk_is_declared_not_inferred_from_its_name(monkeypatch) -> None:
    """The bug this exists to stop.

    ``drops_response_format`` used to be ``model.startswith("deepseek/")``. Pointing
    DeepSeek at its own OpenAI-compatible endpoint as ``openai/deepseek-v4-flash`` made
    that check stop firing, the param came back, and the first call of the frozen run
    would have failed. A quirk belongs to the model, not to the spelling of its name.
    """
    from app.infra.dspy_lm import build_dspy_lm, set_model_override
    from app.infra.llm_models import MODELS

    assert MODELS["deepseek-v4-flash"].drops_response_format
    assert MODELS["gpt-oss-120b"].drops_response_format
    assert not MODELS["claude-sonnet-5"].drops_response_format

    # Each model resolves its own host, and a host demands its own key before an LM
    # is built. The stand-in is for the build; nothing here is sent anywhere.
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key-not-a-real-one")
    for name in ("openai/deepseek-v4-flash", "openai/openai.gpt-oss-120b-1:0"):
        set_model_override(name)
        try:
            dropped = build_dspy_lm().kwargs.get("additional_drop_params") or []
            assert "response_format" in dropped, name
        finally:
            set_model_override(None)
