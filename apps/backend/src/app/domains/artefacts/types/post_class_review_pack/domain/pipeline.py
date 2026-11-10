"""Versions of the revision pack's generation code path, named for the day each was fixed.

A version is code: which tool descriptions the composer reads, which instructions the critic
follows, which schema the repair step returns. The pack's spec — its brief — is data, and
every version injects the same stored spec. A version, once named, never changes; new code is
a new version. Leaving the version out means the latest. docs/pipeline-versions.md records
what each version generated in the study.
"""

from collections.abc import Mapping
from enum import Enum


class ReviewPackPipeline(str, Enum):
    #: The code at 5b43e968 that generated Part 1's C0-C3 packs, and so Part 2's P0 packs. No
    #: markdown note on the composer's tools or in the repair schema; the critic without its
    #: "fig-NN" sentence.
    V2026_08_25 = "2026-08-25"
    #: The code Part 2's P1 packs were generated with: its personalisation, critic and repair
    #: calls and its tool descriptions match the code that recorded that run (a3d6bb58).
    V2026_09_02 = "2026-09-02"


#: The latest version, used when a request names none.
CURRENT_PIPELINE = ReviewPackPipeline.V2026_09_02


def pipeline_that_wrote(refs: Mapping[str, object] | None) -> ReviewPackPipeline:
    """The version a pack records writing it; a pack that records none counts as the latest."""
    recorded = (refs or {}).get("pipeline")
    return ReviewPackPipeline(recorded) if isinstance(recorded, str) else CURRENT_PIPELINE
