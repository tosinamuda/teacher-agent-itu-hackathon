"""The generators that can make content of a type: which exist, and which is the default."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.domains.content.domain.types import Level
from app.shared.json_types import JsonObject


class GeneratorKind(str, Enum):
    """Which kind of generator made content: a fixed DSPy program, or a plugin run by the engine.

    Not the engine's ``EngineLoop``, which is the loop it runs a plugin with. Stored and
    sent as ``harness``, the name content records already carry.
    """

    DSPY_PIPELINE = "dspy-pipeline"
    ENGINE = "engine"


class SchemaSource(str, Enum):
    """Where the content's schema lives: written in the program, or read from a spec."""

    CODE = "code"
    SPEC = "spec"


class GeneratorStatus(str, Enum):
    """A generator that can be pinned, the one used when none is pinned, or one set aside."""

    AVAILABLE = "available"
    DEFAULT = "default"
    RETIRED = "retired"


@dataclass(frozen=True)
class GeneratorBinding:
    """One generator of one type at one level."""

    type_slug: str
    level: Level
    harness: GeneratorKind
    schema: SchemaSource
    #: A pipeline name such as ``2026-09-02``, or what holds the spec for an engine generator.
    ref: str
    status: GeneratorStatus
    #: For a generator that reads a spec: the revision it builds from.
    spec_revision: int | None = None

    def provenance(self) -> JsonObject:
        """What an item records of the generator that made it."""
        recorded: JsonObject = {
            "harness": self.harness.value,
            "schema": self.schema.value,
            "ref": self.ref,
        }
        if self.spec_revision is not None:
            recorded["spec_revision"] = self.spec_revision
        return recorded
