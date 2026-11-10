"""A spec's reference to a skill it is written with, pinned at a revision."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.shared.json_types import JsonObject

SKILL_SLUG = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


class SkillRefError(ValueError):
    """A skill reference that does not name a skill and a revision."""


@dataclass(frozen=True)
class SkillRef:
    """One skill a spec is written with, at the revision it pins."""

    slug: str
    revision: int

    @classmethod
    def from_record(cls, record: object) -> SkillRef:
        if not isinstance(record, dict):
            raise SkillRefError("a skill reference is an object with skill and revision")
        fields = {str(key): value for key, value in record.items()}
        slug, revision = fields.get("skill"), fields.get("revision")
        if not isinstance(slug, str) or not SKILL_SLUG.match(slug):
            raise SkillRefError(f"a skill is named by its slug: {slug!r}")
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
            raise SkillRefError(f"skill {slug} needs the revision it is pinned at")
        return cls(slug, revision)

    def to_record(self) -> JsonObject:
        return {"skill": self.slug, "revision": self.revision}
