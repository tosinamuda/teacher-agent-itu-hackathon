"""A traced draft keeps what reached the endpoint and what came back, streamed or not."""

from __future__ import annotations

import shutil
from collections.abc import Callable

import pytest
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content_engine.infrastructure.engine import Engine, Request, Writer
from app.domains.content_engine.infrastructure.harness.deep_agents import DeepAgentsWriter
from app.domains.content_engine.infrastructure.harness.dsh import DshWriter
from app.domains.content_engine.infrastructure.harness.dsh_agent import DshModel
from app.domains.content_engine.infrastructure.harness.opencode import OpenCodeWriter
from app.domains.content_engine.infrastructure.harness.opencode_session import Model
from experiments.lesson_note_engine.trace_summary import summary
from experiments.lesson_note_engine.wire import recording
from tests.content_engine_support import PLAN, TYPE, seed_lesson, server_over
from tests.harness_script import engine_script
from tests.openai_stub import stub_model

pytestmark = pytest.mark.asyncio


def _deep_agents(base_url: str) -> Writer:
    model = ChatOpenAI(model="stub-model", base_url=base_url, api_key=SecretStr("k"))
    return DeepAgentsWriter(model)


def _opencode(base_url: str) -> Writer:
    return OpenCodeWriter(Model("stub-model", base_url, "k"))


def _dsh(base_url: str) -> Writer:
    return DshWriter(DshModel("stub-model", base_url, "k"))


#: The program each writer's loop runs in, when it runs in one of its own.
_INSTALLS = {
    _opencode: ("opencode", "npm i -g opencode-ai@1.18.32"),
    _dsh: ("dsh", "npm i -g @deepseek-ai/dsh@0.1.5-rc.3"),
}


@pytest.mark.parametrize(
    "writer", [_deep_agents, _opencode, _dsh], ids=["deepagents", "opencode", "dsh"]
)
async def test_a_traced_draft_shows_the_tool_calls_and_refusals_on_the_wire(
    db: AsyncSession, writer: Callable[[str], Writer]
) -> None:
    program, install = _INSTALLS.get(writer, ("", ""))
    if program and shutil.which(program) is None:
        pytest.skip(install)
    await seed_lesson(db)
    with stub_model(engine_script()) as (_, stub_url):
        async with recording(stub_url.removesuffix("/v1")) as (proxy, base_url):
            engine = Engine(lambda: server_over(db), lambda: writer(base_url))
            await engine.build(Request(type=TYPE, plan_version_id=PLAN))

    shown = summary(proxy.exchanges)
    assert len(proxy.exchanges) == 4
    assert 'add_part` {"draft_id"' in shown
    assert "examples: is required" in shown.split("## Call 1")[0]
    assert '"plan_step": {"type": "object"' in shown
