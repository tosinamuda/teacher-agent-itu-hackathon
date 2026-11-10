"""Install, update and remove artefact plugins.

A plugin adds one content type, or a generator for a type that exists. Its skills are stored as
skill revisions named by their folders, so a skill name is global: equal text is shared and
different text is refused. Its spec is stored as the type's spec revision, and each step is
recorded as a plugin revision. Everything is checked before anything is written, so a plugin
the reader accepted and the catalogue would refuse writes nothing.

A plugin that implements a type stores its spec under its own name. The type's current spec does
not change, and the generator is available until a person makes it the default.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.errors import ContentError
from app.domains.content.application.plugin_store import PluginStore
from app.domains.content.domain.plugins import PluginRevision, PluginStatus
from app.domains.content.domain.skills import Skill
from app.domains.content.plugins.plugin import Plugin


def _same(a: Skill, b: Skill) -> bool:
    return (a.name, a.description, a.instructions, a.files) == (
        b.name,
        b.description,
        b.instructions,
        b.files,
    )


class PluginInstaller:
    def __init__(self, catalogue: ContentCatalogue, store: PluginStore) -> None:
        self._catalogue = catalogue
        self._store = store

    async def installed(self, db: AsyncSession) -> list[PluginRevision]:
        return await self._store.all_latest(db)

    async def install(
        self, db: AsyncSession, plugin: Plugin, digest: str, by: str | None
    ) -> PluginRevision:
        """Register the plugin's type with its skills pinned; refuse a type or skill name in use."""
        name = plugin.name
        if await self._store.latest(db, name) is not None:
            raise ContentError(409, f"plugin_installed:{name}")
        if plugin.definition is None:
            return await self._install_generator(db, plugin, digest, by)
        slug = plugin.definition.slug
        if await self._catalogue.exists(db, slug):
            raise ContentError(409, f"content_type_exists:{slug}")
        fields = await self._fields(db, plugin, await self._pinned_by(db, slug))
        _, spec = await self._catalogue.register(
            db,
            slug=slug,
            label=plugin.definition.label,
            audience=plugin.definition.audience,
            made_from_a_plan_version=plugin.definition.made_from_a_plan_version,
            spec_fields=fields,
            created_by=by,
        )
        return await self._record(db, plugin, digest, spec.revision, PluginStatus.INSTALLED, by)

    async def sync(
        self, db: AsyncSession, plugin: Plugin, digest: str, by: str | None
    ) -> PluginRevision:
        """Install the plugin if it is new, else update it, so a deploy can always call it."""
        if await self._store.latest(db, plugin.name) is None:
            return await self.install(db, plugin, digest, by)
        return await self.update(db, plugin, digest, by)

    async def update(
        self, db: AsyncSession, plugin: Plugin, digest: str, by: str | None
    ) -> PluginRevision:
        """Store what changed: new skill revisions, and a new spec revision if the spec changed."""
        name = plugin.name
        latest = await self._store.latest(db, name)
        if latest is None:
            raise ContentError(404, f"unknown_plugin:{name}")
        if latest.installed and latest.digest == digest:
            return latest
        slug = plugin.slug
        if latest.implements != (plugin.definition is None):
            raise ContentError(422, f"plugin_type_is_fixed:{name}")
        if latest.implements:
            return await self._update_generator(db, plugin, latest, digest, by)
        await self._refuse_a_changed_type(db, plugin, latest)
        fields = await self._fields(db, plugin, await self._pinned_by(db, slug))
        current = await self._catalogue.current(db, slug)
        revision = current.revision
        if _spec_fields(current.to_record()) != _spec_fields({**fields}):
            revision = (await self._catalogue.add(db, slug, fields, by)).revision
        return await self._record(db, plugin, digest, revision, PluginStatus.INSTALLED, by)

    async def remove(self, db: AsyncSession, name: str, by: str | None) -> PluginRevision:
        """Stop new drafts of the plugin's type. Content already made stays readable."""
        latest = await self._store.latest(db, name)
        if latest is None:
            raise ContentError(404, f"unknown_plugin:{name}")
        if not latest.installed:
            return latest
        if latest.implements:
            await self._catalogue.retire_generator(db, latest.type_slug, name, by)
        removed = PluginRevision(
            name, 0, latest.version, latest.digest, latest.type_slug, latest.spec_revision,
            PluginStatus.REMOVED, by, latest.implements,
        )  # fmt: skip
        return await self._store.add(db, removed)

    async def _refuse_a_changed_type(
        self, db: AsyncSession, plugin: Plugin, latest: PluginRevision
    ) -> None:
        definition = await self._catalogue.type(db, latest.type_slug)
        new = plugin.definition
        assert new is not None
        if (new.slug, new.label, new.audience, new.made_from_a_plan_version) != (
            definition.slug,
            definition.label,
            definition.audience,
            definition.made_from_a_plan_version,
        ):
            raise ContentError(422, f"plugin_type_is_fixed:{plugin.name}")

    async def _pinned_by(self, db: AsyncSession, type_slug: str) -> set[str]:
        """The skill names the type's current spec pins; none while the type is not registered."""
        if not await self._catalogue.exists(db, type_slug):
            return set()
        return {ref.slug for ref in (await self._catalogue.current(db, type_slug)).skills}

    async def _install_generator(
        self, db: AsyncSession, plugin: Plugin, digest: str, by: str | None
    ) -> PluginRevision:
        """Register the plugin as a generator of a type that exists, available and not default."""
        slug = plugin.slug
        fields = await self._fields(db, plugin, set())
        binding = await self._catalogue.add_generator(db, slug, plugin.name, fields, by)
        assert binding.spec_revision is not None
        return await self._record(
            db, plugin, digest, binding.spec_revision, PluginStatus.INSTALLED, by
        )

    async def _update_generator(
        self, db: AsyncSession, plugin: Plugin, latest: PluginRevision, digest: str, by: str | None
    ) -> PluginRevision:
        slug = plugin.slug
        previous = await self._catalogue.revision(db, slug, latest.spec_revision)
        fields = await self._fields(db, plugin, {ref.slug for ref in previous.skills})
        changed = _spec_fields(previous.to_record()) != _spec_fields({**fields})
        revision = await self._catalogue.update_generator(
            db, slug, plugin.name, fields if changed else None, by
        )
        return await self._record(db, plugin, digest, revision, PluginStatus.INSTALLED, by)

    async def _fields(self, db: AsyncSession, plugin: Plugin, own: set[str]) -> dict[str, object]:
        """The spec's fields with each skill pinned at the revision it is stored at.

        ``own`` is the skill names the plugin's earlier spec already pinned.
        """
        pinned = []
        for skill in plugin.skills:
            latest = await self._catalogue.skills.find(db, skill.slug)
            stored = latest if latest is not None and _same(latest, skill) else None
            if stored is None:
                if latest is not None and skill.slug not in own:
                    raise ContentError(409, f"skill_name_in_use:{skill.slug}")
                stored = await self._catalogue.skills.add(db, skill, None)
            pinned.append(stored.ref().to_record())
        record = plugin.spec.to_record()
        return {**record, "skills": pinned}

    async def _record(
        self,
        db: AsyncSession,
        plugin: Plugin,
        digest: str,
        spec_revision: int,
        status: PluginStatus,
        by: str | None,
    ) -> PluginRevision:
        revision = PluginRevision(
            plugin.name, 0, plugin.manifest.version, digest,
            plugin.slug, spec_revision, status, by, plugin.definition is None,
        )  # fmt: skip
        return await self._store.add(db, revision, plugin.files)


def _spec_fields(record: dict[str, object]) -> dict[str, object]:
    """A spec record without the fields that differ by revision."""
    return {name: value for name, value in record.items() if name not in ("revision", "kind")}
