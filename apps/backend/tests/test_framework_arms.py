"""A framework arm may differ from `compose-v2` in its loop, and in nothing else.

The bake-off compares harnesses. That only holds if every arm reaches the same model the
same way, is set the same task, and returns through the one path that applies identity,
provenance, figures and the reader-ready pass. What is left over is the loop, which is the
thing being measured.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    GenerationPolicyContext,
    LessonContextForGeneration,
    SectionGenerationUnit,
    SourceEvidenceItem,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.section_draft import (  # noqa: E501
    SectionDraft,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from app.infra.dspy_lm import build_dspy_lm, set_sampling_override
from experiments.h1_condition_eval.frameworks.adk_arm import AdkComposeSection
from experiments.h1_condition_eval.frameworks.brief import composed_brief
from experiments.h1_condition_eval.frameworks.chat_model import _as_message
from experiments.h1_condition_eval.frameworks.composer import FrameworkComposer, superstep_budget
from experiments.h1_condition_eval.frameworks.deepagents_arm import DeepAgentsComposeSection
from experiments.h1_condition_eval.frameworks.langgraph_arm import LangGraphComposeSection
from experiments.h1_condition_eval.frameworks.provider import litellm_request
from experiments.h1_condition_eval.generator_arms import GENERATOR_ARMS, harness_for

ARMS = (LangGraphComposeSection, AdkComposeSection, DeepAgentsComposeSection)
FRAMEWORK_ARM_NAMES = ("langgraph", "adk", "deepagents")


def _unit() -> SectionGenerationUnit:
    return SectionGenerationUnit(
        unit_id="unit:lo-1",
        lesson_objective_id="lo-1",
        objective_text="identify multiples of a number",
        source_evidence=[
            SourceEvidenceItem(source_ref="s1", excerpt="The multiples of 4 are 4, 8, 12.")
        ],
    )


def _request(unit: SectionGenerationUnit) -> BaseReviewPackRequest:
    return BaseReviewPackRequest(
        artefact_spec=revision_pack_spec("JSS1"),
        generation_policy=H1_CONDITION_PROFILES[ConditionCode.C2].generation_policy(),
        policy=GenerationPolicyContext(
            require_source_refs=False,
            use_only_provided_sources=True,
            preserve_lesson_objective=True,
            instruction_summary="",
        ),
        lesson_context=LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="Number", lesson_objectives=[]
        ),
        units=[unit],
    )


async def _wrote_a_section(self, *, draft: SectionDraft, instructions: str, inputs: str) -> str:
    """Stand in for a loop: write the draft the composition tools would have written."""
    del instructions, inputs
    draft.title = "Multiples"
    draft.add("explanation", r"A multiple of 4 is 4 \times a whole number.")
    draft.add_practice("List three multiples of 4.", "4, 8, 12", None)
    return "submit"


@pytest.mark.parametrize("arm", ARMS, ids=lambda cls: cls.framework)
@pytest.mark.asyncio
async def test_a_framework_arm_assembles_through_the_one_assembly_path(arm, monkeypatch) -> None:
    """Identity, provenance and the reader-ready pass are applied to every arm alike."""
    monkeypatch.setattr(arm, "compose", _wrote_a_section)
    unit = _unit()

    section = await arm().generate_section(request=_request(unit), unit=unit)

    assert section.section_id == unit.unit_id
    assert section.lesson_objective_id == unit.lesson_objective_id
    assert [block.block_id for block in section.blocks] == ["unit:lo-1:b0"]
    assert section.blocks[0].source_refs == ["s1"]
    assert section.practice[0].item_id == "unit:lo-1:p0"
    # The model wrote a bare LaTeX command; only delimited maths is typeset, so a reader
    # would otherwise meet the backslash on the page.
    assert section.blocks[0].text == r"A multiple of 4 is 4 \(\times\) a whole number."


@pytest.mark.parametrize("name", FRAMEWORK_ARM_NAMES)
def test_a_framework_arm_differs_from_compose_v2_only_in_the_framework(name: str) -> None:
    composed, framework = harness_for("compose-v2"), harness_for(name)

    assert framework.framework != composed.framework
    assert framework.contract_family == composed.contract_family == "composed"
    assert framework.evidence_delivery == composed.evidence_delivery == "in_prompt"


@pytest.mark.parametrize("name", FRAMEWORK_ARM_NAMES)
def test_a_framework_arm_is_registered_and_builds(name: str) -> None:
    arm = GENERATOR_ARMS[name]
    built = arm.build(
        profile=H1_CONDITION_PROFILES[ConditionCode.C2],
        case={"lesson": "sel-rich", "plan": {"steps": []}},
        workspace_root=None,  # type: ignore[arg-type] - no arm here materialises files
        signatures="leveled",
    )

    assert isinstance(built, FrameworkComposer)
    assert hasattr(built, "generate_section")


def test_the_brief_is_compose_v2s_own_contract_and_inputs() -> None:
    """Re-authoring the task would make the comparison about the prompt, not the loop."""
    unit = _unit()
    request = _request(unit)
    composer = ComposeSection(lm=build_dspy_lm(), contract_mode="leveled")
    contract = composer.contract(request)

    instructions, rendered = composed_brief(request=request, unit=unit, signatures="leveled")

    assert instructions == contract.instructions
    assert "calling the tools" in instructions
    for field in composer.inputs(request, unit, contract):
        assert f"## {field}" in rendered
    assert "The multiples of 4 are 4, 8, 12." in rendered


def test_every_framework_reaches_the_model_the_dspy_arms_reach() -> None:
    """A framework arm must call the SAME model, the same way, or it is not a comparison.

    This is the check that would have caught the half-adopted dspy upgrade, where the
    ReAct arms went to a prompt-parsing path while the others used native tool calling
    and 5 of 6 came back duds.
    """
    set_sampling_override(cache=False, temperature=0.3)
    try:
        lm, request = build_dspy_lm(), litellm_request()
    finally:
        set_sampling_override()

    assert request["model"] == lm.model
    assert request["num_retries"] == lm.num_retries
    assert request["timeout"] == lm.kwargs["timeout"]
    assert request["temperature"] == lm.kwargs["temperature"]
    # The endpoint travels with the model now, so an arm pointed elsewhere is a real risk.
    assert request.get("api_base") == lm.kwargs.get("api_base")
    # A replayed sample is how a stochastic arm reports as perfectly reproducible.
    assert request["cache"] == {"no-cache": True, "no-store": True}


def test_a_langgraph_budget_counts_both_halves_of_a_turn() -> None:
    """A turn is the model then the tools, and one last turn calls no tool."""
    assert superstep_budget(16) == {"recursion_limit": 33}


def _reply(content: str, calls: list) -> object:
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content, tool_calls=calls))]
    )


def _call(name: str, arguments: str) -> object:
    return SimpleNamespace(id="call-1", function=SimpleNamespace(name=name, arguments=arguments))


def test_the_chat_model_reads_a_native_tool_call() -> None:
    message = _as_message(_reply("", [_call("add_block", '{"block_type": "explanation"}')]))

    assert message.tool_calls == [
        {
            "name": "add_block",
            "args": {"block_type": "explanation"},
            "id": "call-1",
            "type": "tool_call",
        }
    ]


def test_a_malformed_tool_call_is_handed_back_rather_than_raised() -> None:
    """The loop returns it to the model as an error; raising would score the draw a dud."""
    message = _as_message(_reply("", [_call("add_block", "{not json")]))

    assert message.tool_calls == []
    assert message.invalid_tool_calls[0]["name"] == "add_block"


def test_deepseek_can_still_run_the_framework_arms(monkeypatch) -> None:
    """The frozen generator must not silently exclude three of the four harnesses.

    DeepSeek speaks both OpenAI endpoints, and ``/responses`` is the better one: it
    enforces a json_schema and returns native ``function_call`` tool calls, where chat
    completions 400s on any json_schema and leaves dspy parsing ``[[ ## field ## ]]``
    markers out of prose. But ``provider.litellm_request`` refuses anything that is not
    chat completions, so making it the default would mean LangGraph, ADK and DeepAgents
    could never run on a deepseek generation. It is therefore off by default and turned
    on by the arms that can use it.
    """
    from app.infra.dspy_lm import build_dspy_lm, set_model_override, set_responses_api
    from experiments.h1_condition_eval.frameworks.provider import litellm_request

    # DeepSeek reached through its own OpenAI-compatible endpoint, which is how it is
    # configured now — `deepseek/` as a provider is gone. Its host demands its own key
    # to build an LM; the stand-in is for the build, nothing here is sent.
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key-not-a-real-one")
    set_model_override("openai/deepseek-v4-flash")
    try:
        set_responses_api(False)
        lm = build_dspy_lm()
        assert lm.model_type == "chat"
        # Chat completions 400s on json_schema, flat or nested, so it must not be sent.
        assert "response_format" in (lm.kwargs.get("additional_drop_params") or [])
        litellm_request()  # must not raise — the arms can run

        # On /responses the schema is accepted AND enforced, so it is NOT dropped —
        # which is the whole point of going there. It still costs the arms.
        set_responses_api(True)
        lm = build_dspy_lm()
        assert lm.model_type == "responses"
        assert "response_format" not in (lm.kwargs.get("additional_drop_params") or [])
        with pytest.raises(ValueError, match="chat completions"):
            litellm_request()
    finally:
        set_responses_api(False)
        set_model_override(None)
