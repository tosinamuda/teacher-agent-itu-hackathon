"""Artefact plugins over HTTP: list them, install one, update it, and remove it."""

from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.content.application.errors import ContentError
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.plugins import PluginRevision
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.plugins.library import in_library, library_plugin
from app.domains.content.plugins.problems import PluginError
from app.domains.content.plugins.shipped import shipped_names
from app.domains.content.plugins.upload import plugins_from_files
from app.shared.auth import Actor
from app.shared.authz import requires
from app.shared.schema_base import StrictRequest

router = APIRouter(prefix="/content/plugins", tags=["content"])


class PluginFiles(StrictRequest):
    """A plugin folder as files: each path inside the folder, and its text."""

    files: dict[str, str]


class PluginResponse(BaseModel):
    name: str
    #: The plugin folder it belongs to; one plugin may make several things, each a row.
    plugin: str
    revision: int
    version: str
    type: str
    spec_revision: int
    status: str
    #: The plugin adds a generator to ``type`` instead of adding the type.
    implements: bool
    installed_by: str | None
    #: Whether the plugin ships with the app, so only a deploy changes it.
    system: bool

    @classmethod
    def of(cls, plugin: PluginRevision) -> PluginResponse:
        return cls(
            name=plugin.name,
            plugin=plugin.plugin or plugin.name,
            revision=plugin.revision,
            version=plugin.version,
            type=plugin.type_slug,
            spec_revision=plugin.spec_revision,
            status=plugin.status.value,
            implements=plugin.implements,
            installed_by=plugin.installed_by,
            system=plugin.name in shipped_names(),
        )


def _installer() -> PluginInstaller:
    return PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins())


def _refuse_shipped(name: str) -> None:
    if name in shipped_names():
        raise ContentError(409, f"plugin_ships_with_the_app:{name}")


def _raise(error: ContentError | PluginError) -> NoReturn:
    if isinstance(error, PluginError):
        raise HTTPException(status_code=422, detail=[str(problem) for problem in error.problems])
    raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("", response_model=list[PluginResponse])
async def list_plugins(
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[PluginResponse]:
    """Every plugin at its latest revision."""
    return [PluginResponse.of(plugin) for plugin in await _installer().installed(db)]


class LibraryPluginResponse(BaseModel):
    folder: str
    description: str
    version: str
    #: The types it adds, by label.
    adds: list[str]
    installed: bool


@router.get("/library", response_model=list[LibraryPluginResponse])
async def list_library(
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[LibraryPluginResponse]:
    """The plugins on hand to add, each saying whether it is already installed."""
    installed = {found.name for found in await _installer().installed(db) if found.installed}
    return [
        LibraryPluginResponse(
            folder=plugin.folder,
            description=plugin.description,
            version=plugin.version,
            adds=[p.definition.label for p in plugin.plugins if p.definition is not None],
            installed=all(p.name in installed for p in plugin.plugins),
        )
        for plugin in in_library()
    ]


@router.post("/library/{folder}", response_model=list[PluginResponse], status_code=201)
async def add_from_library(
    folder: str,
    actor: Actor = Depends(requires(obj="content:*", act="create")),
    db: AsyncSession = Depends(get_db),
) -> list[PluginResponse]:
    """Install a plugin from the library. Any teacher may: the plugins in it are the app's own."""
    plugin = library_plugin(folder)
    if plugin is None:
        raise HTTPException(status_code=404, detail="plugin_not_in_the_library")
    try:
        added = [
            await _installer().install(db, each, plugin.digest, actor.display_name)
            for each in plugin.plugins
        ]
    except (ContentError, PluginError) as error:
        _raise(error)
    await db.commit()
    return [PluginResponse.of(each) for each in added]


@router.post("", response_model=list[PluginResponse], status_code=201)
async def install_plugin(
    body: PluginFiles,
    actor: Actor = Depends(requires(obj="content_type:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> list[PluginResponse]:
    """Register each content type or generator the folder makes, with its skills and servers."""
    try:
        plugins, digest = plugins_from_files(body.files)
        for plugin in plugins:
            _refuse_shipped(plugin.name)
        installed = [
            await _installer().install(db, plugin, digest, actor.display_name) for plugin in plugins
        ]
    except (ContentError, PluginError) as error:
        _raise(error)
    await db.commit()
    return [PluginResponse.of(plugin) for plugin in installed]


@router.put("/{name}", response_model=list[PluginResponse])
async def update_plugin(
    name: str,
    body: PluginFiles,
    actor: Actor = Depends(requires(obj="content_type:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> list[PluginResponse]:
    """Store what changed in the folder's artefacts; ``name`` is one of them."""
    try:
        _refuse_shipped(name)
        plugins, digest = plugins_from_files(body.files)
        if name not in {plugin.name for plugin in plugins}:
            raise ContentError(422, f"plugin_name_differs:{name}")
        updated = [
            await _installer().update(db, plugin, digest, actor.display_name) for plugin in plugins
        ]
    except (ContentError, PluginError) as error:
        _raise(error)
    await db.commit()
    return [PluginResponse.of(plugin) for plugin in updated]


@router.delete("/{name}", response_model=PluginResponse)
async def remove_plugin(
    name: str,
    actor: Actor = Depends(requires(obj="content_type:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> PluginResponse:
    """Stop new drafts of the plugin's type. Content already made stays readable."""
    try:
        _refuse_shipped(name)
        removed = await _installer().remove(db, name, actor.display_name)
    except ContentError as error:
        _raise(error)
    await db.commit()
    return PluginResponse.of(removed)
