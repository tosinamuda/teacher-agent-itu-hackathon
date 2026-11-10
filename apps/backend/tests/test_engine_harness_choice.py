"""The app's engine runs on OpenCode with native skills, and the server installs that release."""

from __future__ import annotations

from pathlib import Path

import yaml

from app.domains.content_engine.infrastructure.harness.choice import (
    ENGINE_LOOP,
    ENGINE_SKILLS,
    EngineLoop,
    SkillsMode,
    loop_for,
)
from app.domains.content_engine.infrastructure.harness.opencode import (
    OpenCodeChecker,
    OpenCodeWriter,
)
from app.domains.content_engine.infrastructure.harness.opencode_server import OPENCODE_VERSION

REPO = Path(__file__).resolve().parents[3]


def test_the_app_writes_and_checks_on_opencode_with_native_skills() -> None:
    loop = loop_for()

    assert (ENGINE_LOOP, ENGINE_SKILLS) == (EngineLoop.OPENCODE, SkillsMode.NATIVE)
    assert isinstance(loop.writer(), OpenCodeWriter)
    assert isinstance(loop.checker(), OpenCodeChecker)


def test_another_loop_keeps_its_skills_in_the_brief_unless_asked_otherwise() -> None:
    loop_for(EngineLoop.DEEP_AGENTS)
    loop_for(EngineLoop.PI, skills=SkillsMode.NATIVE)


def test_the_playbook_installs_the_release_the_adapter_was_traced_on() -> None:
    variables = yaml.safe_load((REPO / "deploy/ansible/group_vars/all.yml").read_text())

    assert variables["opencode_version"] == OPENCODE_VERSION
