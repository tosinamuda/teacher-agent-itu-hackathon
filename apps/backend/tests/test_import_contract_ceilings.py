"""Hold every import-contract exemption list to an exact size.

An allowlist with no ratchet grows: entry 115 arrives with a reasonable justification and
nobody notices the count went up. These counts are exact, so adding an exemption fails and
removing one fails until the number is lowered in the same change.

Each exemption in ``pyproject.toml`` carries a comment naming the story that deletes it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import tomllib

pytestmark = pytest.mark.architecture

PYPROJECT = Path("pyproject.toml")
BACKLOG = Path("../../.internal/backlog.yaml")
STORY_REFERENCE = re.compile(r"\b(?:APP|EVAL|EXP)-\d{3}[A-Z]?\b")

# Contract name -> exemptions it is still allowed to carry. Lower these; never raise them.
EXEMPTION_CEILINGS = {
    "evaluation transport+persistence do not DIRECTLY import experiments (PR-1 win)": 2,
    "leaf/reference domains import no peer domain": 0,
    "api transport does not directly import peer-domain code": 0,
    "artefacts core domain imports no peer domain and no content type": 0,
    "post-class review-pack does not import experiments": 0,
    "generation reads condition profiles, never condition labels": 0,
    "application does not import infrastructure directly": 111,
    "application does not import api transport": 11,
}


def _contracts() -> list[dict]:
    config = tomllib.loads(PYPROJECT.read_text())
    return config["tool"]["importlinter"]["contracts"]


def _exemption_counts() -> dict[str, int]:
    return {contract["name"]: len(contract.get("ignore_imports", [])) for contract in _contracts()}


def test_every_contract_has_a_declared_ceiling() -> None:
    assert set(_exemption_counts()) == set(EXEMPTION_CEILINGS)


def test_no_contract_carries_more_exemptions_than_declared() -> None:
    assert _exemption_counts() == EXEMPTION_CEILINGS


def _exemption_blocks() -> list[str]:
    return re.findall(r"ignore_imports = \[\n(.*?)\n\]", PYPROJECT.read_text(), re.DOTALL)


def _exemption_comments() -> list[str]:
    """Each contiguous run of comment lines, joined: one heading per exemption group."""
    headings: list[str] = []
    for block in _exemption_blocks():
        current: list[str] = []
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                current.append(stripped.removeprefix("#").strip())
                continue
            if current:
                headings.append(" ".join(current))
                current = []
        if current:
            headings.append(" ".join(current))
    return headings


def _backlog_story_ids() -> set[str]:
    import yaml

    document = yaml.safe_load(BACKLOG.read_text())
    return {story["id"] for sprint in document["sprints"] for story in sprint.get("stories", [])}


def test_every_exemption_group_names_a_story_or_declares_itself_permanent() -> None:
    unattributed = [
        comment
        for comment in _exemption_comments()
        if not STORY_REFERENCE.search(comment) and not comment.startswith("permanent:")
    ]
    assert unattributed == []


@pytest.mark.skipif(
    not BACKLOG.exists(),
    reason="The backlog is deliberately untracked, so a clean checkout has none to check "
    "against. This guard runs where planning lives.",
)
def test_every_named_exit_story_exists_in_the_backlog() -> None:
    referenced = {
        story for comment in _exemption_comments() for story in STORY_REFERENCE.findall(comment)
    }
    assert referenced <= _backlog_story_ids()


def test_every_exemption_sits_under_a_group_comment() -> None:
    orphans: list[str] = []
    for block in _exemption_blocks():
        seen_comment = False
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                seen_comment = True
            elif stripped and not seen_comment:
                orphans.append(stripped)
    assert orphans == []


def test_every_exemption_is_a_single_named_import_edge() -> None:
    malformed = [
        exemption
        for contract in _contracts()
        for exemption in contract.get("ignore_imports", [])
        if exemption.count(" -> ") != 1 or "*" in exemption
    ]
    assert malformed == []
