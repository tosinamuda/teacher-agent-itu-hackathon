"""An installed artefact plugin: one row for each install, update or removal, never edited."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PluginStatus(str, Enum):
    INSTALLED = "installed"
    REMOVED = "removed"


@dataclass(frozen=True)
class PluginRevision:
    """What one install, update or removal of a plugin recorded."""

    name: str
    revision: int
    version: str
    #: A hash of the plugin folder's files, so the same folder installed twice is one revision.
    digest: str
    #: The content type the plugin adds. A plugin keeps its type for good.
    type_slug: str
    #: The spec revision of the type when this was recorded.
    spec_revision: int
    status: PluginStatus
    installed_by: str | None = None
    #: The plugin adds a generator to ``type_slug``, which another source registered.
    implements: bool = False
    #: The plugin folder this belongs to, which may make more than one thing: its manifest's
    #: name. A removal keeps no files, so it falls back to ``name``.
    plugin: str = ""

    @property
    def installed(self) -> bool:
        return self.status is PluginStatus.INSTALLED


@dataclass(frozen=True)
class PluginFiles:
    """The files a plugin revision was installed with, as text by their paths in the folder."""

    name: str
    revision: int
    files: dict[str, str]
