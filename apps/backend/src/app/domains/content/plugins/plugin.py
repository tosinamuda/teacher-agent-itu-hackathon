"""A plugin read from a folder: the type it adds, its spec, its skills and its servers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.domain.skills import Skill
from app.domains.content.domain.types import ContentTypeDefinition
from app.domains.content.plugins.manifest import PluginManifest


@dataclass(frozen=True)
class Plugin:
    """One artefact of a plugin folder: the type it adds, or the generator it adds to a type."""

    manifest: PluginManifest
    #: What the installed row and a generator's binding are called: the artefact's name.
    name: str
    #: The type the plugin adds; none when it implements a type that exists.
    definition: ContentTypeDefinition | None
    #: The slug of the type the plugin adds a generator to.
    implements: str | None
    #: The spec as written, its skills pinned at revision 1 until they are installed. For a
    #: plugin that implements a type its kind is a placeholder: installing sets the type's.
    spec: ContentSpecification
    skills: tuple[Skill, ...]
    servers: tuple[McpServerRef, ...]
    #: The folder's files by path, as text, so a run can copy them: those the artefact uses.
    files: Mapping[str, str]

    @property
    def slug(self) -> str:
        """The type the plugin adds, or the one it implements."""
        if self.definition is not None:
            return self.definition.slug
        assert self.implements is not None
        return self.implements
