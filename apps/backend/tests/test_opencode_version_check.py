"""The version check must not need a home the API's user can write in."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable

import pytest

from app.domains.content_engine.infrastructure.harness import opencode_server
from app.domains.content_engine.infrastructure.harness.opencode_server import (
    OPENCODE_VERSION,
    OpenCodeUnavailableError,
    check_version,
)

pytestmark = pytest.mark.asyncio


class _Process:
    def __init__(self, output: str) -> None:
        self._output = output

    async def communicate(self) -> tuple[bytes, None]:
        return self._output.encode(), None


def _answering(output: str, seen: list[dict[str, str]]) -> Callable[..., Awaitable[_Process]]:
    async def start(*_command: str, env: dict[str, str], **_options: object) -> _Process:
        seen.append(env)
        return _Process(output)

    return start


async def test_the_version_is_read_with_its_folders_in_the_adapters_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[dict[str, str]] = []
    monkeypatch.setattr(asyncio, "create_subprocess_exec", _answering(OPENCODE_VERSION, seen))

    await check_version()

    cache = str(opencode_server._CACHE)
    for name in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME"):
        assert seen[0][name].startswith(cache)


async def test_another_release_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(asyncio, "create_subprocess_exec", _answering("1.0.0", []))

    with pytest.raises(OpenCodeUnavailableError, match="needs"):
        await check_version()
