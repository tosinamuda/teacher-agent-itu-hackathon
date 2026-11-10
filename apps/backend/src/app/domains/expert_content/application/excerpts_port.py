"""Reading textbook passages, as a port.

Lesson sources are resolved by both the experiments pipeline and the artefacts
student-pack path, so the query cannot live on either domain's repository. It is
a port here, next to the records it reads.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol


class ExcerptsPort(Protocol):
    """The textbook passages behind a set of plan-reference citations."""

    async def excerpts_for(self, references: Sequence[str]) -> dict[str, str]:
        """``record_id -> passage text``, omitting references that resolve to nothing."""
        ...
