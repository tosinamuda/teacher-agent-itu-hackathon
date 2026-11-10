"""The writer and checker on DeepSeek Harness: dsh's agent loop, spoken to over ACP.

The writer reaches the draft through the relay, so the model is offered the DSPy writer's
three tools and nothing else. dsh has no structured output, so the checker answers through
a tool of one call, as DeepAgents' and OpenCode's checkers do; a verdict its schema does not
allow is refused there, and the model may answer again.
"""

from __future__ import annotations

from mcp import Client
from mcp.types import Tool

from app.domains.content_engine.infrastructure.harness.acp import Turn, http_server
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
from app.domains.content_engine.infrastructure.harness.dsh_agent import DshModel, Run, dsh_run
from app.domains.content_engine.infrastructure.harness.relay import relayed
from app.domains.content_engine.infrastructure.harness.workspace import (
    SkillError,
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


def _usage(call: JsonObject) -> JsonObject | None:
    usage = call.get("usage")
    if not isinstance(usage, dict):
        return None
    return {"input_tokens": usage.get("inputTokens"), "output_tokens": usage.get("outputTokens")}


class _Recorded:
    def __init__(self, model: DshModel, log: GenerationLog | None = None) -> None:
        self._model = model
        self._log = log

    def _record(self, run: Run, workspace: JsonObject | None = None) -> None:
        """Log every model call of the run, with the tokens dsh counted for it."""
        if self._log is None:
            return
        tags = current_tags()
        for call in run.model_calls():
            request: JsonObject = {
                "harness": "dsh",
                "turn": call.get("turn"),
                "step": call.get("step"),
            }
            if workspace is not None:
                request["workspace"] = workspace
            response = {"message": call.get("message")}
            model = f"openai/{self._model.id}"
            self._log.record(Generation(model, dict(tags), request, response, None, _usage(call)))


def _stopped(turn: Turn) -> str:
    """Why a turn ended short of its own end, or nothing when it ended by itself."""
    return "" if turn.stop_reason == "end_turn" else f"stop reason {turn.stop_reason!r}"


class DshWriter(_Recorded):
    def __init__(
        self, model: DshModel, log: GenerationLog | None = None, *, native_skills: bool = False
    ) -> None:
        """With ``native_skills`` the skills are files in the workspace, found by dsh."""
        super().__init__(model, log)
        self._native_skills = native_skills

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        """Fill the draft through ``client``. Returns the writer's summary of what it did."""
        skills = await pinned_skills(client, draft) if self._native_skills else None
        if any(skill.has_references for skill in skills or ()):
            raise SkillError("dsh has no tool to read a skill's reference files")
        prompt = NATIVE_SKILLS_WRITER_PROMPT if self._native_skills else WRITER_PROMPT
        entry = entry_skill(draft) if self._native_skills else None
        given = without_skills(draft) if self._native_skills else draft
        async with (
            relayed(client, skills_hidden=self._native_skills) as relay,
            dsh_run(self._model, prompt, skills=skills) as run,
        ):
            engine = http_server("engine", relay.url, relay.headers())
            session = await run.agent.new_session(run.workspace, (engine,))
            turn = await run.agent.prompt(
                session,
                writer_message(given, lesson, feedback, entry=entry),
                model_calls=turns_for(draft),
            )
            self._record(run, manifest(skills) if skills is not None else None)
        if _stopped(turn):
            raise WriterStoppedError(f"the writer stopped: {_stopped(turn)}")
        return turn.text


class DshChecker(_Recorded):
    async def errors(
        self, brief: JsonObject, unit: dict[str, object], part: JsonObject
    ) -> list[str]:
        """The part's real errors; empty when it has none."""
        async with (
            answering(VERDICT_TOOL, Verdict) as (endpoint, answer),
            dsh_run(self._model, CHECKER_PROMPT) as run,
        ):
            verdict = http_server("answer", endpoint.url, endpoint.headers())
            session = await run.agent.new_session(run.workspace, (verdict,))

            def answered() -> bool:
                return answer.arguments is not None

            message = checker_message(brief, unit, part)
            turn = await run.agent.prompt(
                session, message, model_calls=CHECKER_STEPS, done=answered
            )
            reason = None if answered() else refusal(written_answer(turn.text))
            if reason is not None and turn.model_calls < CHECKER_STEPS:
                left = CHECKER_STEPS - turn.model_calls
                turn = await run.agent.prompt(
                    session, answer_again(reason), model_calls=left, done=answered
                )
            self._record(run)
        if answer.arguments is not None:
            return verdict_of(answer.arguments)
        return verdict_of(written_answer(turn.text))
