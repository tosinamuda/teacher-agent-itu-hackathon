"""The plugin library: plugins the app has on hand but does not install until someone adds one.

The folders under the checkout's ``plugin-library/``. They are apart from ``plugins/``, which a
deploy installs, so a plugin here stays out until a teacher adds it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import BACKEND_DIR
from app.domains.content.plugins.plugin import Plugin
from app.domains.content.plugins.problems import errors_in
from app.domains.content.plugins.reader import folder_digest, read_plugins

LIBRARY_DIR = BACKEND_DIR.parents[1] / "plugin-library"


@dataclass(frozen=True)
class LibraryPlugin:
    folder: str
    plugins: list[Plugin]
    digest: str

    @property
    def description(self) -> str:
        return (self.plugins[0].manifest.description or "") if self.plugins else ""

    @property
    def version(self) -> str:
        return (self.plugins[0].manifest.version or "") if self.plugins else ""


def _read(folder: Path) -> LibraryPlugin | None:
    plugins, problems = read_plugins(folder)
    if not plugins or errors_in(problems):
        return None
    return LibraryPlugin(folder.name, plugins, folder_digest(folder))


def in_library() -> list[LibraryPlugin]:
    """Every valid plugin in the library, by folder name; none when the folder is missing."""
    if not LIBRARY_DIR.is_dir():
        return []
    found = [_read(folder) for folder in sorted(LIBRARY_DIR.iterdir()) if folder.is_dir()]
    return [plugin for plugin in found if plugin is not None]


def library_plugin(folder: str) -> LibraryPlugin | None:
    """The library's plugin of this folder name; a name is looked up, never joined to a path."""
    return next((plugin for plugin in in_library() if plugin.folder == folder), None)
