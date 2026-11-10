"""Which loop the engine writes and checks with: DSPy's, DeepAgents', OpenCode's, dsh's or pi's.

The loop is an experimental condition, so it is chosen in code, where a run records it,
not in an environment a run cannot record.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

import dspy

from app.config import CONFIG
from app.domains.content_engine.infrastructure.checker import PartChecker
from app.domains.content_engine.infrastructure.engine import Checker, Writer
from app.domains.content_engine.infrastructure.harness.chat_log import ChatModelLog
from app.domains.content_engine.infrastructure.harness.deep_agents import (
    DeepAgentsChecker,
    DeepAgentsWriter,
)
from app.domains.content_engine.infrastructure.harness.dsh import DshChecker, DshWriter
from app.domains.content_engine.infrastructure.harness.dsh_agent import DshModel
from app.domains.content_engine.infrastructure.harness.models import (
    generator_chat_model,
    generator_route,
)
from app.domains.content_engine.infrastructure.harness.opencode import (
    OpenCodeChecker,
    OpenCodeWriter,
)
from app.domains.content_engine.infrastructure.harness.opencode_session import Model
from app.domains.content_engine.infrastructure.harness.pi import PiChecker, PiWriter
from app.domains.content_engine.infrastructure.harness.pi_agent import PiModel
from app.domains.content_engine.infrastructure.writer import EngineWriter
from app.domains.generation_log.application.recorder import GenerationLog
from app.infra.dspy_lm import build_dspy_lm, sampling_settings


class EngineLoop(str, Enum):
    """The loop the engine runs a plugin with, not a generator's ``GeneratorKind``.

    A run records the loop as ``harness``, the name its stored runs already carry.
    """

    DSPY = "dspy"
    DEEP_AGENTS = "deepagents"
    OPENCODE = "opencode"
    DEEPSEEK = "dsh"
    PI = "pi"


class SkillsMode(str, Enum):
    """Where the writer gets the skills its type pins."""

    #: In the brief, as text, on every call.
    PINNED = "pinned"
    #: As files in the workspace the harness starts in, which it loads as it needs them.
    NATIVE = "native"


#: The loop the app's engine runs, and where its writer gets the skills a type pins: OpenCode
#: loading them from its workspace, as compared against DSPy's loop (experiments/lesson_note_engine/
#: HARNESSES.md).
ENGINE_LOOP = EngineLoop.OPENCODE
ENGINE_SKILLS = SkillsMode.NATIVE


@dataclass(frozen=True)
class Loop:
    """A fresh writer and checker for each draft, on the chosen harness."""

    writer: Callable[[], Writer]
    checker: Callable[[], Checker]


def _dspy(lm: dspy.BaseLM | None) -> Loop:
    return Loop(
        lambda: EngineWriter(lm or build_dspy_lm()), lambda: PartChecker(lm or build_dspy_lm())
    )


def _deep_agents() -> Loop:
    def log() -> list[ChatModelLog]:
        model = generator_chat_model().model_name
        return [ChatModelLog(f"openai/{model}")] if CONFIG.log_model_calls else []

    return Loop(
        lambda: DeepAgentsWriter(generator_chat_model(), log()),
        lambda: DeepAgentsChecker(generator_chat_model(), log()),
    )


def _opencode(skills: SkillsMode) -> Loop:
    def model() -> Model:
        return Model(*generator_route())

    log = GenerationLog() if CONFIG.log_model_calls else None
    temperature = sampling_settings().get("temperature")
    heat = float(temperature) if isinstance(temperature, (int, float)) else None
    native = skills is SkillsMode.NATIVE
    return Loop(
        lambda: OpenCodeWriter(model(), log, temperature=heat, native_skills=native),
        lambda: OpenCodeChecker(model(), log, temperature=heat),
    )


def _dsh(skills: SkillsMode) -> Loop:
    def model() -> DshModel:
        return DshModel(*generator_route())

    log = GenerationLog() if CONFIG.log_model_calls else None
    native = skills is SkillsMode.NATIVE
    return Loop(
        lambda: DshWriter(model(), log, native_skills=native), lambda: DshChecker(model(), log)
    )


def _pi(skills: SkillsMode) -> Loop:
    def model() -> PiModel:
        return PiModel(*generator_route())

    log = GenerationLog() if CONFIG.log_model_calls else None
    native = skills is SkillsMode.NATIVE
    return Loop(
        lambda: PiWriter(model(), log, native_skills=native), lambda: PiChecker(model(), log)
    )


def loop_for(
    harness: EngineLoop = ENGINE_LOOP,
    *,
    lm: dspy.BaseLM | None = None,
    skills: SkillsMode | None = None,
) -> Loop:
    """The writer and checker of ``harness``; ``lm`` is DSPy's model, when it is given.

    ``skills`` is native for the app's own loop and pinned for another unless it says otherwise.
    Only OpenCode, dsh and pi load skills from a workspace; asking it of another loop is an error.
    """
    if skills is None:
        skills = ENGINE_SKILLS if harness is ENGINE_LOOP else SkillsMode.PINNED
    if skills is SkillsMode.NATIVE and harness not in (
        EngineLoop.OPENCODE,
        EngineLoop.DEEPSEEK,
        EngineLoop.PI,
    ):
        raise ValueError(f"{harness.value} does not load skills from a workspace")
    if harness is EngineLoop.DEEP_AGENTS:
        return _deep_agents()
    if harness is EngineLoop.OPENCODE:
        return _opencode(skills)
    if harness is EngineLoop.DEEPSEEK:
        return _dsh(skills)
    if harness is EngineLoop.PI:
        return _pi(skills)
    return _dspy(lm)
