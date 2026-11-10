"""Job handlers for the runner's tests: each leaves a trace in a file its test reads.

They run in the job's own process, so a file is the one thing both sides can see.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path


def _note(path: str, line: str) -> None:
    with Path(path).open("a", encoding="utf-8") as trace:
        trace.write(f"{line}\n")


async def record(path: str) -> dict[str, str]:
    _note(path, "ran")
    return {"trace": path}


async def record_rerun(path: str, *, redelivered: bool) -> None:
    _note(path, f"rerun={redelivered}")


async def raise_error(path: str) -> None:
    _note(path, "ran")
    raise ValueError("the handler failed")


async def refuse(path: str) -> None:
    from app.domains.experiments.application.errors import ExperimentApplicationError

    _note(path, "ran")
    raise ExperimentApplicationError(409, "approve_the_lesson_note_first")


async def die(path: str) -> None:
    _note(path, "ran")
    os._exit(3)


async def hang(path: str) -> None:
    _note(path, "ran")
    await asyncio.sleep(3600)


async def hang_telling_pid(path: str) -> None:
    _note(path, f"pid={os.getpid()}")
    await asyncio.sleep(3600)
