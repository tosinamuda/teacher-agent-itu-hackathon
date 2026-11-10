"""A plugin sent as files instead of read from a folder: the API's form of an install."""

from __future__ import annotations

import tempfile
from pathlib import Path, PurePosixPath

from app.domains.content.plugins.plugin import Plugin
from app.domains.content.plugins.problems import PluginError, Problem, errors_in
from app.domains.content.plugins.reader import folder_digest, read_plugins

MAX_FILES = 200
MAX_BYTES = 1_000_000


def _refused(files: dict[str, str]) -> list[Problem]:
    """Why these files cannot be written into a plugin folder, if they cannot."""
    problems: list[Problem] = []
    if not files or len(files) > MAX_FILES:
        problems.append(Problem("files", f"send 1 to {MAX_FILES} files"))
    if sum(len(text.encode()) for text in files.values()) > MAX_BYTES:
        problems.append(Problem("files", f"send at most {MAX_BYTES} bytes in all"))
    for path in files:
        parts = PurePosixPath(path).parts
        if PurePosixPath(path).is_absolute() or not parts or ".." in parts or "" in path.split("/"):
            problems.append(Problem(path, "is a path inside the plugin folder"))
    return problems


def plugins_from_files(files: dict[str, str]) -> tuple[list[Plugin], str]:
    """Read the plugins the files make, one for each artefact, with the folder's digest.

    Every problem found is raised otherwise.
    """
    if problems := _refused(files):
        raise PluginError(problems)
    with tempfile.TemporaryDirectory(prefix="plugin-upload-") as scratch:
        folder = Path(scratch)
        for path, text in files.items():
            target = folder / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        plugins, found = read_plugins(folder)
        if not plugins or errors_in(found):
            raise PluginError(found)
        return plugins, folder_digest(folder)
