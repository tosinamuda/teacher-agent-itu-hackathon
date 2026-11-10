"""Composition root for the content catalogue: the registered types, their specs and skills."""

from __future__ import annotations

from app.domains.artefacts.core.infrastructure.specifications import (
    SqlAlchemyContentSpecifications,
)
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.skill_library import SkillLibrary
from app.domains.content.infrastructure.generator_store import SqlAlchemyGeneratorBindings
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.skills import SqlAlchemySkills
from app.domains.content.infrastructure.type_registry import SqlAlchemyContentTypes


def build_content_catalogue() -> ContentCatalogue:
    return ContentCatalogue(
        SqlAlchemyContentTypes(),
        SqlAlchemyContentSpecifications(),
        SkillLibrary(SqlAlchemySkills()),
        SqlAlchemyPlugins(),
        SqlAlchemyGeneratorBindings(),
    )
