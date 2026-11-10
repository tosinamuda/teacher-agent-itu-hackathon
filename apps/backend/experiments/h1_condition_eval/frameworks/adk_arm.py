"""Compose a section with a Google ADK agent.

ADK is the one framework here that does not take a chat model object: it takes its own
`LiteLlm`, which calls the same `litellm.acompletion` with the same keyword arguments, so
this arm reaches the model over the route the dspy arms reach it by.

Two ADK details are load-bearing. Its budget is `max_llm_calls`, a count of model turns
rather than of graph steps, so this arm's cap is the one that means what dspy's
`max_iters` means. And a `str` instruction is a state template — `{name}` would be
substituted out of session state — so the brief is passed as a provider, which ADK
documents as bypassing injection.
"""

from __future__ import annotations

from collections.abc import Callable

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import LlmCallsLimitExceededError
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.run_config import RunConfig
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.section_draft import (  # noqa: E501
    SectionDraft,
    composition_tools,
)
from experiments.h1_condition_eval.frameworks.composer import (
    ITERATION_LIMIT,
    SUBMITTED,
    FrameworkComposer,
)
from experiments.h1_condition_eval.frameworks.provider import litellm_request

APP_NAME = "h1-harness-bakeoff"
USER_ID = "harness"


class AdkComposeSection(FrameworkComposer):
    """`compose-v2` with an ADK agent driving the composition tools."""

    framework = "google-adk"

    async def compose(self, *, draft: SectionDraft, instructions: str, inputs: str) -> str:
        agent = LlmAgent(
            name="compose_section",
            model=_model(),
            instruction=_instruction(instructions),
            tools=composition_tools(draft),
        )
        runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
        try:
            return await self._drive(runner, inputs)
        finally:
            await runner.close()

    async def _drive(self, runner: InMemoryRunner, inputs: str) -> str:
        session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
        message = types.Content(role="user", parts=[types.Part(text=inputs)])
        try:
            async for _event in runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=message,
                run_config=RunConfig(max_llm_calls=self.max_iterations),
            ):
                pass
        except LlmCallsLimitExceededError:
            return ITERATION_LIMIT
        return SUBMITTED


def _model() -> LiteLlm:
    """The dspy arms' litellm call, as ADK's model wrapper takes it."""
    request = dict(litellm_request())
    return LiteLlm(model=request.pop("model"), **request)


def _instruction(text: str) -> Callable[[ReadonlyContext], str]:
    """ADK's provider form, which bypasses `{state}` substitution over the brief."""
    return lambda _context: text
