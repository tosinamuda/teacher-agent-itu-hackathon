"""The writer and checker on pi: its agent loop, spoken to over RPC.

pi has no MCP client, so an extension gives it the tools of the run's servers: the writer's
three draft tools through the relay, and the checker's answer tool, of one call, as
DeepSeek Harness' checker has. A verdict its schema does not allow is refused there, and the
model may answer again.
"""

from __future__ import annotations

from mcp import Client
from mcp.types import Tool

from app.domains.content_engine.infrastructure.harness.answer_tool import answering
from app.domains.content_engine.infrastructure.harness.brief import (
    CHECKER_PROMPT,
    CHECKER_STEPS,
    NATIVE_SKILLS_WRITER_PROMPT,
    WRITER_PROMPT,
    Verdict,
    answer_again,
    checker_message,
    entry_skill,
    refusal,
    turns_for,
    verdict_of,
    writer_message,
    written_answer,
)
from app.domains.content_engine.infrastructure.harness.pi_agent import (
    McpServer,
    PiModel,
    Turn,
    pi_run,
)
from app.domains.content_engine.infrastructure.harness.relay import relayed
from app.domains.content_engine.infrastructure.harness.workspace import (
    manifest,
    pinned_skills,
    without_skills,
)
from app.domains.content_engine.infrastructure.writer import WriterStoppedError
from app.domains.generation_log.application.recorder import Generation, GenerationLog, current_tags
from app.shared.json_types import JsonObject

#: The checker's answer tool: the Verdict schema, called once.
VERDICT_TOOL = Tool(
    name="give_verdict",
    description="Answer with the part's real errors; an empty list when it has none.",
    input_schema=Verdict.model_json_schema(),
)


def _usage(message: JsonObject) -> JsonObject | None:
    usage = message.get("usage")
    if not isinstance(usage, dict):
        return None
    return {"input_tokens": usage.get("input"), "output_tokens": usage.get("output")}


class _Recorded:
    def __init__(self, model: PiModel, log: GenerationLog | None = None) -> None:
        self._model = model
        self._log = log

    def _record(self, turns: list[Turn], workspace: JsonObject | None = None) -> None:
        """Log every model call of the run, with the tokens pi counted for it."""
        if self._log is None:
            return
        tags = current_tags()
        model = f"openai/{self._model.id}"
        for turn in turns:
            for message in turn.messages:
                request: JsonObject = {"harness": "pi", "timestamp": message.get("timestamp")}
                if workspace is not None:
                    request["workspace"] = workspace
                response: JsonObject = {"message": message}
                generation = Generation(model, dict(tags), request, response, None, _usage(message))
                self._log.record(generation)


def _stopped(turn: Turn) -> str:
    """Why a turn ended short of its own end, or nothing when it ended by itself."""
    return "" if turn.stop_reason == "stop" else f"stop reason {turn.stop_reason!r}"


async def _offered(client: Client) -> tuple[str, ...]:
    """The names of the tools the writer is offered."""
    return tuple(tool.name for tool in (await client.list_tools()).tools)


class PiWriter(_Recorded):
    def __init__(
        self, model: PiModel, log: GenerationLog | None = None, *, native_skills: bool = False
    ) -> None:
        """With ``native_skills`` the skills are files in the workspace, found by pi."""
        super().__init__(model, log)
        self._native_skills = native_skills

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        """Fill the draft through ``client``. Returns the writer's summary of what it did."""
        skills = await pinned_skills(client, draft) if self._native_skills else None
        prompt = NATIVE_SKILLS_WRITER_PROMPT if self._native_skills else WRITER_PROMPT
        entry = entry_skill(draft) if self._native_skills else None
        given = without_skills(draft) if self._native_skills else draft
        async with relayed(client, skills_hidden=self._native_skills) as relay:
            engine = McpServer("engine", relay.url, relay.headers(), await _offered(client))
            async with pi_run(
                self._model, prompt, [engine], model_calls=turns_for(draft), skills=skills
            ) as agent:
                turn = await agent.prompt(
                    writer_message(given, lesson, feedback, entry=entry),
                    model_calls=turns_for(draft),
                )
        self._record([turn], manifest(skills) if skills is not None else None)
        if _stopped(turn):
            raise WriterStoppedError(f"the writer stopped: {_stopped(turn)}")
        return turn.text


class PiChecker(_Recorded):
    async def errors(
        self, brief: JsonObject, unit: dict[str, object], part: JsonObject
    ) -> list[str]:
        """The part's real errors; empty when it has none."""
        async with answering(VERDICT_TOOL, Verdict) as (endpoint, answer):
            verdict = McpServer(
                "answer", endpoint.url, endpoint.headers(), (VERDICT_TOOL.name,), final=True
            )
            async with pi_run(
                self._model, CHECKER_PROMPT, [verdict], model_calls=CHECKER_STEPS
            ) as agent:

                def answered() -> bool:
                    return answer.arguments is not None

                message = checker_message(brief, unit, part)
                turns = [await agent.prompt(message, model_calls=CHECKER_STEPS, done=answered)]
                reason = None if answered() else refusal(written_answer(turns[-1].text))
                spent = sum(turn.model_calls for turn in turns)
                if reason is not None and spent < CHECKER_STEPS:
                    turns.append(
                        await agent.prompt(
                            answer_again(reason), model_calls=CHECKER_STEPS - spent, done=answered
                        )
                    )
        self._record(turns)
        if answer.arguments is not None:
            return verdict_of(answer.arguments)
        return verdict_of(written_answer(turns[-1].text))
