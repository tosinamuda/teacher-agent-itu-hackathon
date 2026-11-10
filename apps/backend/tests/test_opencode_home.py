"""The folders of a kept OpenCode agent: named by the thread's key, found again, and pruned."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from app.domains.content_engine.infrastructure.harness.opencode_home import (
    home_of,
    prune,
    remember_session,
    remembered_session,
)


def test_a_home_is_named_by_its_key_and_a_key_cannot_leave_the_folder(tmp_path: Path) -> None:
    assert home_of("RT-1", tmp_path) == tmp_path / "RT-1"
    for key in ("", "../x", "a/b", "a b"):
        with pytest.raises(ValueError, match="key"):
            home_of(key, tmp_path)


def test_the_session_a_home_holds_is_remembered(tmp_path: Path) -> None:
    home = home_of("RT-1", tmp_path)
    home.mkdir()
    assert remembered_session(home) is None

    remember_session(home, "ses_1")

    assert remembered_session(home) == "ses_1"


def test_prune_removes_the_homes_not_used_lately_and_keeps_the_rest(tmp_path: Path) -> None:
    for key in ("old", "recent"):
        home_of(key, tmp_path).mkdir()
        remember_session(home_of(key, tmp_path), f"ses_{key}")
    long_ago = time.time() - 40 * 24 * 3600
    os.utime(home_of("old", tmp_path) / "session", (long_ago, long_ago))

    removed = prune(tmp_path)

    assert removed == 1
    assert [path.name for path in tmp_path.iterdir()] == ["recent"]


def test_prune_of_a_folder_that_does_not_exist_removes_nothing(tmp_path: Path) -> None:
    assert prune(tmp_path / "none") == 0
