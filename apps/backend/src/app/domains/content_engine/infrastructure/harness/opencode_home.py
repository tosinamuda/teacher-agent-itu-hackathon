"""The folders of a kept OpenCode agent: its home, which holds its sessions, and its workspace.

OpenCode keeps a session's messages in its data folder, and a new server started on that folder
finds the session again. A conversation that outlives its server (closed when idle, closed for
another to take its place, or cut by a restart of the app) keeps its folders under the thread's
key, with the id of its session beside them, so the next message continues the same session.
"""

from __future__ import annotations

import re
import shutil
import time
from pathlib import Path

from app.config import BACKEND_DIR

#: Where kept agents' folders live: outside the checkout's tracked files, so a deploy keeps them.
SESSIONS_DIR = BACKEND_DIR / "var" / "engine-sessions"
#: How long a thread's folders are kept after its last message.
KEEP_SECONDS = 30 * 24 * 3600.0
_KEY = re.compile(r"[A-Za-z0-9_-]{1,100}")
_SESSION_FILE = "session"


def home_of(key: str, root: Path | None = None) -> Path:
    """The folder of the agent kept under ``key``, in ``root`` or the sessions folder."""
    if not _KEY.fullmatch(key):
        raise ValueError(f"a kept agent's key is letters, digits, hyphens and underscores: {key!r}")
    return (SESSIONS_DIR if root is None else root) / key


def remembered_session(home: Path) -> str | None:
    """The id of the session kept in ``home``, if one was opened there."""
    try:
        return (home / _SESSION_FILE).read_text().strip() or None
    except FileNotFoundError:
        return None


def remember_session(home: Path, session_id: str) -> None:
    """Record ``session_id`` as the session of ``home``; the write also marks the home as used."""
    (home / _SESSION_FILE).write_text(session_id)


def prune(root: Path | None = None, *, keep_seconds: float = KEEP_SECONDS) -> int:
    """Remove the folders not used for ``keep_seconds``; how many were removed."""
    root = SESSIONS_DIR if root is None else root
    if not root.is_dir():
        return 0
    cutoff = time.time() - keep_seconds
    stale = [home for home in root.iterdir() if home.is_dir() and _last_used(home) < cutoff]
    for home in stale:
        shutil.rmtree(home, ignore_errors=True)
    return len(stale)


def _last_used(home: Path) -> float:
    try:
        return (home / _SESSION_FILE).stat().st_mtime
    except FileNotFoundError:
        return home.stat().st_mtime
