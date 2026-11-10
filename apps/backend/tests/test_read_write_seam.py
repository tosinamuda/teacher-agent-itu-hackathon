"""Read/write seam: view-services never write.

Codifies the rule that read-side application services (the ones whose job is
to shape a DTO for the dashboard) never call write methods on a repository
or directly mutate the session. This rule already holds across every
view-service in the codebase as of the audit pass; this test pins it so
future drift fails CI loudly rather than slipping in silently.

Why the rule
------------

The application layer has two distinct shapes:

- **Write services** orchestrate one use-case-level mutation:
  ``ExperimentApplicationService.create_or_get_experiment``,
  ``end_experiment``, ``update_focal_learners``, etc. Each loads the row,
  mutates it, persists. They DO read — to load — but their reason-to-change
  is "the lifecycle of one aggregate".

- **View services** assemble a DTO from many tables for one consumer
  (dashboard endpoint, story rollup, statistics page). Their reason-to-change
  is "what the dashboard wants to show". They MUST NOT write.

Mixing the two means a view-service starts taking on lifecycle concerns
(when does it persist? what happens on partial failure of the view build?)
that don't belong there. The audit pass verified every view-service is
write-free; this test guards against regression.

What's NOT enforced here
------------------------

Write-services routinely DO read (load-then-mutate is unavoidable with an
ORM). The asymmetric rule "view-services never write" is the meaningful
half of the read/write seam; the inverse isn't.

How additions work
------------------

When you add a new view-style service, append it to ``VIEW_SERVICE_FILES``.
If your new service legitimately needs to write, it isn't a view-service —
name it ``*_service.py`` (write-side) and don't add it here.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.architecture

# Files classified as VIEW services — their job is to assemble a DTO for a
# specific dashboard endpoint or rollup. Adding a file here is a promise
# that it has no write calls and will keep it that way.
VIEW_SERVICE_FILES = (
    # experiments domain
    "src/app/domains/experiments/application/experiment_views/execution.py",
    "src/app/domains/experiments/application/experiment_views/experiment.py",
    "src/app/domains/experiments/application/experiment_views/experiment_response.py",
    "src/app/domains/experiments/application/experiment_views/options.py",
    "src/app/domains/experiments/application/experiment_views/readiness.py",
    "src/app/domains/experiments/application/experiment_views/synthetic_students.py",
    "src/app/domains/experiments/application/experiment_context_service.py",
    "src/app/domains/experiments/application/experiment_story_service.py",
    "src/app/domains/experiments/application/results_summary_query.py",
    # evaluation domain
    "src/app/domains/evaluation/application/reporting_queries.py",
    "src/app/domains/evaluation/application/dataset_queries.py",
    "src/app/domains/evaluation/application/packet_payloads.py",
)

# Patterns that constitute a "write" — repository methods that mutate state
# OR direct session writes. Repository method names follow a stable verb
# convention (save_/update_/delete_/set_); session writes are db.add /
# .commit / .delete / .flush.
WRITE_PATTERNS = (
    # repo-level writes
    re.compile(r"\brepository\.(save_|update_|delete_|set_)\w*\("),
    # session-level writes (commit/refresh excluded — refresh re-READS;
    # commit is a transaction boundary, allowed in write-services and
    # by-construction absent from view-services since they have nothing
    # to commit).
    re.compile(r"\bdb\.add\("),
    re.compile(r"\bdb\.delete\("),
    re.compile(r"\bdb\.flush\("),
)

_BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("relative_path", VIEW_SERVICE_FILES)
def test_view_service_does_not_write(relative_path: str) -> None:
    file_path = _BACKEND_DIR / relative_path
    assert file_path.is_file(), f"view-service file not found: {relative_path}"
    source = file_path.read_text(encoding="utf-8")
    violations: list[tuple[str, str]] = []
    for pattern in WRITE_PATTERNS:
        for match in pattern.finditer(source):
            line = source.count("\n", 0, match.start()) + 1
            violations.append((str(line), match.group()))
    assert not violations, (
        f"View-service {relative_path} contains write calls:\n"
        + "\n".join(f"  line {line}: {snippet}" for line, snippet in violations)
        + "\n\nView-services must not write. If this service legitimately "
        "needs to mutate state, it isn't a view-service — remove it from "
        "VIEW_SERVICE_FILES and rename to indicate write-side intent."
    )


def test_every_view_service_path_exists() -> None:
    """Guard against typos in VIEW_SERVICE_FILES — every entry must resolve."""
    missing = [p for p in VIEW_SERVICE_FILES if not (_BACKEND_DIR / p).is_file()]
    assert not missing, f"VIEW_SERVICE_FILES contains non-existent paths: {missing}"
