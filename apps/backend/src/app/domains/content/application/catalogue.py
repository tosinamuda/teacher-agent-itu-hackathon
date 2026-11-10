"""The registered content types and the revisions of each type's spec."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.content.application.errors import ContentError, NoGeneratorError
from app.domains.content.application.generator_store import GeneratorBindings
from app.domains.content.application.plugin_store import PluginStore
from app.domains.content.application.skill_library import SkillLibrary
from app.domains.content.application.type_registry import ContentTypes
from app.domains.content.domain.generator_contract import refuse_unfit_spec
from app.domains.content.domain.generators import (
    GeneratorBinding,
    GeneratorKind,
    GeneratorStatus,
    SchemaSource,
)
from app.domains.content.domain.plugins import PluginFiles
from app.domains.content.domain.skills import Skill
from app.domains.content.domain.types import Audience, ContentTypeDefinition, Engine, Level


class ContentCatalogue:
    """Reads the types, and reads and adds spec revisions. A revision is added, never edited.

    A spec may pin skills; it is stored only when every skill it pins is in ``skills``.
    """

    def __init__(
        self,
        types: ContentTypes,
        specifications: ContentSpecifications,
        skills: SkillLibrary,
        plugins: PluginStore,
        generators: GeneratorBindings,
    ) -> None:
        self._types = types
        self._specifications = specifications
        self.skills = skills
        self._plugins = plugins
        self._generators = generators

    async def skills_of(self, db: AsyncSession, spec: ContentSpecification) -> list[Skill]:
        """The skills a spec is written with, each at the revision it pins."""
        return await self.skills.pinned(db, spec.skills)

    async def type(self, db: AsyncSession, slug: str) -> ContentTypeDefinition:
        found = await self._types.get(db, slug)
        if found is None:
            raise ContentError(404, f"unknown_content_type:{slug}")
        return found

    async def retired(self, db: AsyncSession, slug: str) -> bool:
        """Whether the plugin that added the type has been removed: no new drafts of it."""
        plugin = await self._plugins.of_type(db, slug)
        return plugin is not None and not plugin.installed

    async def plugin_files(
        self, db: AsyncSession, slug: str, spec_revision: int
    ) -> PluginFiles | None:
        """The files of the plugin that made the type's spec revision, when a plugin did."""
        return await self._plugins.files_for(db, slug, spec_revision)

    async def generator(
        self,
        db: AsyncSession,
        definition: ContentTypeDefinition,
        level: Level,
        pin: str | None = None,
    ) -> GeneratorBinding:
        """The generator that makes the type's content: the pinned one, else the default.

        An engine type needs no row: its generator is the engine, building from the type's
        current spec.
        """
        registered = await self._generators.of(db, definition.slug, level)
        if pin is not None:
            chosen = [
                b for b in registered if b.ref == pin and b.status is not GeneratorStatus.RETIRED
            ]
            if not chosen:
                raise ContentError(422, f"unknown_generator:{definition.slug}:{pin}")
            return chosen[0]
        defaults = [b for b in registered if b.status is GeneratorStatus.DEFAULT]
        if defaults:
            return defaults[0]
        if definition.engine is Engine.MCP:
            spec = await self.current(db, definition.slug)
            return GeneratorBinding(
                type_slug=definition.slug,
                level=level,
                harness=GeneratorKind.ENGINE,
                schema=SchemaSource.SPEC,
                ref=definition.slug,
                status=GeneratorStatus.DEFAULT,
                spec_revision=spec.revision,
            )
        raise NoGeneratorError(422, f"no_generator:{definition.slug}:{level.value}")

    async def add_generator(
        self,
        db: AsyncSession,
        slug: str,
        generator: str,
        fields: Mapping[str, object],
        created_by: str | None,
    ) -> GeneratorBinding:
        """Store a plugin's spec for the type and register the generator that builds from it.

        The spec must keep what the type's stored shape needs. The generator is available and
        never the default; a person makes it the default.
        """
        definition = await self.type(db, slug)
        specification = specification_for(
            definition, {**fields, "kind": definition.kind, "revision": 0}, engine_type=False
        )
        try:
            refuse_unfit_spec(slug, await self.current(db, slug), specification)
        except ValueError as error:
            raise ContentError(422, f"invalid_generator:{error}") from error
        await self.skills_of(db, specification)
        stored = await self._specifications.add_revision(db, specification, created_by, generator)
        binding = GeneratorBinding(
            type_slug=slug,
            level=(
                Level.LEARNER
                if specification.levels == frozenset({ArtefactScope.LEARNER_LEVEL})
                else Level.CLASS
            ),
            harness=GeneratorKind.ENGINE,
            schema=SchemaSource.SPEC,
            ref=generator,
            status=GeneratorStatus.AVAILABLE,
            spec_revision=stored.revision,
        )
        await self._generators.add(db, binding, created_by)
        return binding

    async def update_generator(
        self,
        db: AsyncSession,
        slug: str,
        generator: str,
        fields: Mapping[str, object] | None,
        by: str | None,
    ) -> int:
        """Bring a plugin's generator up to date; ``fields`` is a changed spec, if it changed.

        Returns the spec revision the generator builds from.
        """
        binding = await self._generator_of(db, slug, generator)
        revision = binding.spec_revision or 0
        if fields is not None:
            definition = await self.type(db, slug)
            specification = specification_for(
                definition, {**fields, "kind": definition.kind, "revision": 0}, engine_type=False
            )
            try:
                refuse_unfit_spec(slug, await self.current(db, slug), specification)
            except ValueError as error:
                raise ContentError(422, f"invalid_generator:{error}") from error
            await self.skills_of(db, specification)
            revision = (
                await self._specifications.add_revision(db, specification, by, generator)
            ).revision
        await self._generators.set_spec_revision(db, binding, revision, by)
        return revision

    async def make_default(
        self, db: AsyncSession, slug: str, level: Level, generator: str, by: str | None
    ) -> GeneratorBinding:
        """Make an available generator the one used when a request pins none.

        One native pipeline is never made the default in place of another; a plugin may take
        the default, and a native pipeline may take it back.
        """
        definition = await self.type(db, slug)
        binding = await self.generator(db, definition, level, generator)
        if binding.status is GeneratorStatus.DEFAULT:
            return binding
        current = await self.generator(db, definition, level)
        if binding.harness is current.harness is GeneratorKind.DSPY_PIPELINE:
            raise ContentError(409, f"native_generator_is_locked:{slug}")
        await self._generators.set_default(db, binding, by)
        return binding

    async def generators_of(
        self, db: AsyncSession, definition: ContentTypeDefinition
    ) -> list[GeneratorBinding]:
        """Every generator of the type at every level, the default first.

        An engine type without a row has the engine as its one generator.
        """
        found: list[GeneratorBinding] = []
        for level in Level:
            registered = await self._generators.of(db, definition.slug, level)
            if registered:
                found += sorted(registered, key=lambda b: b.status is not GeneratorStatus.DEFAULT)
        if not found and definition.engine is Engine.MCP:
            found.append(await self.generator(db, definition, Level.CLASS))
        return found

    async def generator_of_spec(
        self, db: AsyncSession, definition: ContentTypeDefinition, revision: int
    ) -> GeneratorBinding:
        """The generator whose spec is the type's revision: a plugin's, else the type's own."""
        registered = [
            b for level in Level for b in await self._generators.of(db, definition.slug, level)
        ]
        owner = [b for b in registered if b.spec_revision == revision]
        if owner:
            return owner[0]
        registered = [b for b in registered if b.level is Level.CLASS]
        own = [b for b in registered if b.spec_revision is None and b.schema is SchemaSource.SPEC]
        base = own[0] if own else await self.generator(db, definition, Level.CLASS)
        return replace(base, spec_revision=revision)

    async def drafting_spec(
        self, db: AsyncSession, slug: str, level: Level = Level.CLASS, pin: str | None = None
    ) -> ContentSpecification:
        """The spec a new draft is written to: the pinned generator's, else the default's."""
        definition = await self.type(db, slug)
        binding = await self.generator(db, definition, level, pin)
        if binding.schema is SchemaSource.SPEC and binding.spec_revision is not None:
            return await self.revision(db, slug, binding.spec_revision)
        return await self.current(db, slug)

    async def retire_generator(
        self, db: AsyncSession, slug: str, generator: str, by: str | None
    ) -> None:
        """Stop offering a plugin's generator. The default cannot be retired."""
        binding = await self._generator_of(db, slug, generator)
        if binding.status is GeneratorStatus.DEFAULT:
            raise ContentError(409, f"generator_is_default:{slug}:{generator}")
        await self._generators.retire(db, binding, by)

    async def _generator_of(self, db: AsyncSession, slug: str, generator: str) -> GeneratorBinding:
        found = [
            b
            for level in Level
            for b in await self._generators.of(db, slug, level)
            if b.ref == generator
        ]
        if not found:
            raise ContentError(404, f"unknown_generator:{slug}:{generator}")
        return found[0]

    async def exists(self, db: AsyncSession, slug: str) -> bool:
        return await self._types.get(db, slug) is not None

    async def type_of_kind(self, db: AsyncSession, kind: str) -> ContentTypeDefinition:
        found = await self._types.by_kind(db, kind)
        if found is None:
            raise ContentError(404, f"unknown_content_kind:{kind}")
        return found

    async def types(
        self, db: AsyncSession
    ) -> list[tuple[ContentTypeDefinition, ContentSpecification]]:
        """Every type with its current spec, in position order."""
        current = {spec.kind: spec for spec in await self._specifications.all_current(db)}
        return [
            (definition, current[definition.kind])
            for definition in await self._types.all(db)
            if definition.kind in current
        ]

    async def current(self, db: AsyncSession, slug: str) -> ContentSpecification:
        definition = await self.type(db, slug)
        try:
            return await self._specifications.current(db, definition.kind)
        except LookupError as error:
            raise ContentError(404, str(error)) from error

    async def history(self, db: AsyncSession, slug: str) -> list[ContentSpecification]:
        return await self._specifications.history(db, (await self.type(db, slug)).kind)

    async def revision(self, db: AsyncSession, slug: str, revision: int) -> ContentSpecification:
        definition = await self.type(db, slug)
        try:
            return await self._specifications.revision(db, definition.kind, revision)
        except LookupError as error:
            raise ContentError(404, str(error)) from error

    async def register(
        self,
        db: AsyncSession,
        *,
        slug: str,
        label: str,
        audience: Audience,
        made_from_a_plan_version: bool,
        spec_fields: Mapping[str, object],
        created_by: str | None,
    ) -> tuple[ContentTypeDefinition, ContentSpecification]:
        """Register an engine type with its first spec. It can be generated at once."""
        kind = ContentTypeDefinition.kind_for(slug)
        if await self._types.get(db, slug) is not None or await self._types.by_kind(db, kind):
            raise ContentError(409, f"content_type_exists:{slug}")
        try:
            definition = ContentTypeDefinition(
                slug=slug,
                kind=kind,
                label=label,
                audience=audience,
                engine=Engine.MCP,
                made_from_a_plan_version=made_from_a_plan_version,
                position=0,
            )
        except ValueError as error:
            raise ContentError(422, f"invalid_content_type:{error}") from error
        specification = specification_for(definition, {**spec_fields, "kind": kind, "revision": 0})
        await self.skills_of(db, specification)
        await self._types.add(db, definition, created_by)
        stored = await self._specifications.add_revision(db, specification, created_by)
        return await self.type(db, slug), stored

    async def add(
        self,
        db: AsyncSession,
        slug: str,
        fields: Mapping[str, object],
        created_by: str | None,
    ) -> ContentSpecification:
        """Store the fields as the type's next spec revision, if they form a valid spec."""
        definition = await self.type(db, slug)
        specification = specification_for(
            definition, {**fields, "kind": definition.kind, "revision": 0}
        )
        await self.skills_of(db, specification)
        return await self._specifications.add_revision(db, specification, created_by)


def specification_for(
    definition: ContentTypeDefinition, record: Mapping[str, object], *, engine_type: bool = True
) -> ContentSpecification:
    """The spec ``record`` describes, if it is valid and, for an engine type, fits the type.

    A generator's spec is checked against the type's contract instead (``engine_type=False``).
    """
    try:
        specification = ContentSpecification.from_record(record)
        if engine_type:
            definition.check(specification)
    except (KeyError, TypeError, ValueError) as error:
        raise ContentError(422, f"invalid_spec:{error}") from error
    return specification
