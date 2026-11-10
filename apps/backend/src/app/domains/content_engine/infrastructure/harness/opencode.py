"""The writer and checker on OpenCode: its agent loop, run as a server in its own process.

The writer reaches the draft through the relay, so the model is offered the DSPy writer's
three tools and nothing else. The checker has no tools; it answers through OpenCode's
structured output, which OpenCode asks for as a tool call.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from mcp import Client

from app.domains.content_engine.infrastructure.checker import CheckerStoppedError
from app.domains.content_engine.infrastructure.harness.brief import (
    CHECKER_PROMPT,
    CHECKER_STEPS,
    NATIVE_SKILLS_WRITER_PROMPT,
    WRITER_PROMPT,
    Verdict,
    answer_again,
    as_named_by,
    checker_message,
    entry_skill,
    follow_up_message,
    refusal,
    turns_for,
    verdict_of,
    writer_message,
    written_answer,
)
from app.domains.content_engine.infrastructure.harness.opencode_feed import TOOL_PREFIX
from app.domains.content_engine.infrastructure.harness.opencode_home import home_of
from app.domains.content_engine.infrastructure.harness.opencode_server import Agent, served
from app.domains.content_engine.infrastructure.harness.opencode_session import (
    Model,
    Session,
    Steps,
)
from app.domains.content_engine.infrastructure.harness.relay import relayed
from app.domains.content_engine.infrastructure.harness.workspace import (
    WorkspaceSkill,
    manifest,
    pinned_skills,
    without_skills,
)
from app.domains.content_engine.infrastructure.writer import WriterStoppedError
from app.domains.generation_log.application.recorder import Generation, GenerationLog, current_tags
from app.shared.json_types import JsonObject, JsonValue


def _entries(value: JsonValue | None) -> list[JsonObject]:
    return [entry for entry in value if isinstance(entry, dict)] if isinstance(value, list) else []


def _info(message: JsonObject) -> JsonObject:
    info = message.get("info")
    return info if isinstance(info, dict) else {}


def _text(reply: JsonObject) -> str:
    """What the agent said last, as its summary."""
    parts = _entries(reply.get("parts"))
    return "\n".join(str(part["text"]) for part in parts if part.get("type") == "text").strip()


def _elapsed_ms(info: JsonObject) -> float | None:
    time = info.get("time")
    started = time.get("created") if isinstance(time, dict) else None
    ended = time.get("completed") if isinstance(time, dict) else None
    return float(ended - started) if isinstance(started, int) and isinstance(ended, int) else None


def _step(
    model: Model, message: JsonObject, tags: dict[str, object], workspace: JsonObject | None
) -> Generation:
    """One assistant message of the session, with the tokens OpenCode counted for it."""
    info = _info(message)
    tokens = info.get("tokens")
    request: JsonObject = {
        "harness": "opencode",
        "message_id": info.get("id"),
        "parent_id": info.get("parentID"),
    }
    if workspace is not None:
        request["workspace"] = workspace
    response = {
        "parts": message.get("parts"),
        "finish": info.get("finish"),
        "error": info.get("error"),
    }
    usage = tokens if isinstance(tokens, dict) else None
    return Generation(f"openai/{model.id}", dict(tags), request, response, _elapsed_ms(info), usage)


class _Recorded:
    def __init__(self, model: Model, log: GenerationLog | None) -> None:
        self._model = model
        self._log = log

    def _record(self, steps: Steps, workspace: JsonObject | None = None) -> None:
        """Log every model call of the session: OpenCode makes one assistant message each."""
        if self._log is None:
            return
        tags = current_tags()
        for step in steps.each():
            self._log.record(_step(self._model, step, tags, workspace))


def _answer(reply: JsonObject) -> object:
    """The checker's answer: through structured output, else what it wrote as text.

    OpenCode reports the text of a model that ignored the answer tool as a
    ``StructuredOutputError``, though the text is often a valid verdict.
    """
    structured = _info(reply).get("structured")
    return structured if structured is not None else written_answer(_text(reply))


def _failure(reply: JsonObject) -> str:
    error = _info(reply).get("error")
    return str(error) if error else ""


@dataclass(frozen=True)
class _Prepared:
    """What a run of the writer is set up with: its skills, its agent and its first skill."""

    skills: list[WorkspaceSkill]
    agent: Agent
    entry: str | None


class OpenCodeWriter(_Recorded):
    def __init__(
        self,
        model: Model,
        log: GenerationLog | None = None,
        *,
        temperature: float | None = None,
        native_skills: bool = False,
    ) -> None:
        """With ``native_skills`` the skills are files in the workspace, found by OpenCode."""
        super().__init__(model, log)
        self._temperature = temperature
        self._native_skills = native_skills

    async def _prepare(self, client: Client, draft: JsonObject) -> _Prepared:
        skills = await pinned_skills(client, draft) if self._native_skills else []
        prompt = as_named_by(
            NATIVE_SKILLS_WRITER_PROMPT if self._native_skills else WRITER_PROMPT, TOOL_PREFIX
        )
        entry = entry_skill(draft) if self._native_skills else None
        allowed = ("engine_*",)
        if self._native_skills:
            allowed += ("skill", *(("read",) if any(s.has_references for s in skills) else ()))
        return _Prepared(skills, Agent(prompt, turns_for(draft), allowed, self._temperature), entry)

    def _opening(
        self, draft: JsonObject, lesson: JsonObject, feedback: str, entry: str | None
    ) -> str:
        given = without_skills(draft) if self._native_skills else draft
        return as_named_by(writer_message(given, lesson, feedback, entry=entry), TOOL_PREFIX)

    @asynccontextmanager
    async def _served(
        self, client: Client, prepared: _Prepared, kept: Path | None = None
    ) -> AsyncIterator[Session]:
        async with relayed(client, skills_hidden=self._native_skills) as relay:
            mcp: JsonObject = {
                "type": "remote",
                "url": relay.url,
                "headers": {"Authorization": "Bearer {env:ENGINE_RELAY_TOKEN}"},
                "enabled": True,
            }
            token = {"ENGINE_RELAY_TOKEN": relay.token}
            async with served(
                self._model, prepared.agent, mcp=mcp, env=token, skills=prepared.skills, kept=kept
            ) as session:
                yield session

    def _outcome(self, reply: JsonObject, steps: Steps, prepared: _Prepared) -> str:
        self._record(steps, manifest(prepared.skills) if self._native_skills else None)
        if _failure(reply):
            raise WriterStoppedError(f"the writer stopped: {_failure(reply)}")
        return _text(reply)

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        """Fill the draft through ``client``. Returns the writer's summary of what it did."""
        prepared = await self._prepare(client, draft)
        async with self._served(client, prepared) as session:
            reply, steps = await session.run(
                self._opening(draft, lesson, feedback, prepared.entry), report=True
            )
        return self._outcome(reply, steps, prepared)

    @asynccontextmanager
    async def keep(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, key: str
    ) -> AsyncIterator[_KeptWriter]:
        """One agent for several messages: the first brings the brief, the rest only the news.

        The agent and its relay stay until the block ends. OpenCode keeps the session's history
        in the folders kept under ``key``, so each message continues from the last, including
        the first message after the agent was closed and opened again.
        """
        prepared = await self._prepare(client, draft)
        async with self._served(client, prepared, home_of(key)) as session:
            yield _KeptWriter(self, session, prepared)


class _KeptWriter:
    """The writer of one kept agent."""

    def __init__(self, owner: OpenCodeWriter, session: Session, prepared: _Prepared) -> None:
        self._owner = owner
        self._session = session
        self._prepared = prepared
        #: Whether the agent has its brief and what came after: it has spoken, or is resumed.
        self.briefed = session.resumed

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        text = (
            as_named_by(follow_up_message(draft, feedback), TOOL_PREFIX)
            if self.briefed
            else self._owner._opening(draft, lesson, feedback, self._prepared.entry)
        )
        self.briefed = True
        reply, steps = await self._session.run(text, report=True)
        return self._owner._outcome(reply, steps, self._prepared)

    async def stop(self) -> None:
        """Stop the agent's run in progress."""
        await self._session.abort()


class OpenCodeChecker(_Recorded):
    def __init__(
        self, model: Model, log: GenerationLog | None = None, *, temperature: float | None = None
    ) -> None:
        super().__init__(model, log)
        self._temperature = temperature

    async def errors(
        self, brief: JsonObject, unit: dict[str, object], part: JsonObject
    ) -> list[str]:
        """The part's real errors; empty when it has none."""
        agent = Agent(CHECKER_PROMPT, CHECKER_STEPS, ("StructuredOutput",), self._temperature)
        answer: JsonObject = {"type": "json_schema", "schema": Verdict.model_json_schema()}
        async with served(self._model, agent) as session:
            reply, steps = await session.run(checker_message(brief, unit, part), format=answer)
            self._record(steps)
            used = len(steps.each())
            reason = refusal(_answer(reply))
            # OpenCode fixes an agent's step limit per prompt, so the answer sent back is
            # asked for only while the checker has steps left, not capped at those left.
            if reason is not None and used < CHECKER_STEPS:
                reply, steps = await session.run(answer_again(reason), format=answer)
                self._record(steps)
        answered = _answer(reply)
        if answered is None:
            raise CheckerStoppedError(f"the checker gave no answer: {_failure(reply)}")
        return verdict_of(answered)
