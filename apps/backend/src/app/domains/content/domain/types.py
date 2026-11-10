"""The content types the API names: registered data, each with who it is for and how it is built."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactScope

_SLUG = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


class Audience(str, Enum):
    """Teaching content is for the teacher; learning material is for learners."""

    TEACHER = "teacher"
    LEARNER = "learner"


class Engine(str, Enum):
    """How content of a type is built: its own generator, or the content engine over MCP."""

    BUILTIN = "builtin"
    MCP = "mcp"


class BuiltIn(str, Enum):
    """The types with generators of their own, by slug."""

    LESSON_PLAN = "lesson-plan"
    LESSON_NOTE = "lesson-note"
    CLASS_TEST = "class-test"
    REVISION_NOTE = "revision-note"


@dataclass(frozen=True)
class ContentTypeDefinition:
    """One registered content type."""

    slug: str
    #: The artefact kind its content and its specs are stored under.
    kind: str
    #: What a person calls it.
    label: str
    audience: Audience
    engine: Engine
    #: Whether a frozen plan version generates it; a lesson plan is made from its lesson.
    made_from_a_plan_version: bool
    #: Where it sorts: the built-in types in the order a lesson makes them, then the rest.
    position: int

    def __post_init__(self) -> None:
        """Refuse a slug that cannot sit in a URL, and a type without a name."""
        if not _SLUG.match(self.slug) or len(self.slug) > 64:
            raise ValueError(f"a type slug is lowercase words joined by hyphens: {self.slug!r}")
        if not self.label.strip():
            raise ValueError(f"{self.slug}: a type has a label")

    def is_(self, built_in: BuiltIn) -> bool:
        return self.slug == built_in.value

    def check(self, spec: ContentSpecification) -> None:
        """Refuse a spec this type cannot be built from.

        The engine builds a type part by part at class level only, so its spec declares
        the unit and parts. A built-in type's generator reads neither; its spec declares them
        when it is also drafted part by part, as a lesson plan is from a teacher's document.
        """
        if spec.kind != self.kind:
            raise ValueError(f"{self.slug}: a spec of {spec.kind} is not this type's")
        if self.engine is Engine.MCP and spec.parts is None:
            raise ValueError(f"{self.slug}: an engine type's spec declares unit and parts")
        if spec.parts is not None and spec.levels != frozenset({ArtefactScope.CLASS_LEVEL}):
            raise ValueError(f"{self.slug}: content drafted part by part is class level only")

    @staticmethod
    def kind_for(slug: str) -> str:
        """The stored kind of an engine type: its slug in snake case."""
        return slug.replace("-", "_")


class Level(str, Enum):
    CLASS = "class"
    LEARNER = "learner"

    @property
    def stored_as(self) -> ArtefactScope:
        return ArtefactScope.CLASS_LEVEL if self is Level.CLASS else ArtefactScope.LEARNER_LEVEL

    @classmethod
    def of(cls, scope: str) -> Level:
        return Level.CLASS if scope == ArtefactScope.CLASS_LEVEL.value else Level.LEARNER
