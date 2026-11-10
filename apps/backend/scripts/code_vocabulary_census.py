"""Measure every number `docs/code-vocabulary.md` states about the tree.

Two kinds of number live in that table and they want opposite treatment.

**Debt** counts what the vocabulary has not finished renaming or unpicking. Each trends to
zero, so it is a ceiling: a cleanup lowers it, and only a regression raises it.
``tests/test_code_vocabulary_census.py`` fails when one rises.

**Population** counts how many Stores, Readers, and port modules exist. These grow with the
product and have no target, so asserting them would tax every feature branch that adds a
reader with a markdown edit. They are regenerated on demand and never asserted.

Refresh the table with ``uv run python -m scripts.code_vocabulary_census --write``.
"""

from __future__ import annotations

import argparse
import ast
import re
from collections import defaultdict
from functools import cache
from pathlib import Path

import tomllib

from scripts.layer_paths import BACKEND_DIR, DOMAINS, application_files

VOCABULARY = BACKEND_DIR / "docs" / "code-vocabulary.md"
PYPROJECT = BACKEND_DIR / "pyproject.toml"

CENSUS_ROW = re.compile(r"^\|\s*`(?P<key>[a-z_]+)`\s*\|\s*(?P<value>\d+)\s*\|")
# A debt row carries a fourth column naming the story that deletes it.
DEBT_ROW = re.compile(r"^\|\s*`(?P<key>[a-z_]+)`\s*\|\s*\d+\s*\|[^|]*\|(?P<exit>[^|]*)\|")
STORY_ID = re.compile(r"\b(?:[A-Z]{3,6}-\d{3}[A-Z]?)\b")
BACKLOG = BACKEND_DIR.parent.parent / ".internal" / "backlog.yaml"

# Debt still carried, and the ceiling each may not exceed. Lower these; never raise them.
DEBT_CEILINGS = {
    "port_suffixed_names": 8,
    "port_suffixed_references": 67,
    "port_suffixed_files": 25,
    "persistence_suffixed_protocols": 1,
    "domain_wide_port_modules": 2,
    "application_to_infrastructure_exemptions": 111,
    "application_to_transport_exemptions": 11,
    "application_signatures_returning_orm": 276,
    "duplicated_reader_signatures": 15,
    "artefact_types_under_a_sorting_dir": 2,
}

# Counts that track the product's size. Regenerated, never asserted.
POPULATION_KEYS = (
    "store_protocols",
    "reader_protocols",
    "bare_name_protocols",
    "port_modules",
)

# The two domain-wide `ports.py` buckets that predate the rule. No third may appear.
GRANDFATHERED_PORT_BUCKETS = {
    "artefacts/core/application/ports.py",
    "artefacts/types/lesson_plan/application/ports.py",
}


def _python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))


@cache
def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _protocols(tree: ast.Module) -> list[ast.ClassDef]:
    return [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(isinstance(base, ast.Name) and base.id == "Protocol" for base in node.bases)
    ]


def _protocols_by_suffix() -> dict[str, int]:
    counts = {"store": 0, "reader": 0, "port": 0, "persistence": 0, "bare": 0}
    suffixes = (("Store", "store"), ("Reader", "reader"), ("Port", "port"))
    for path in application_files():
        for protocol in _protocols(_parse(path)):
            bucket = next(
                (key for suffix, key in suffixes if protocol.name.endswith(suffix)),
                "persistence" if protocol.name.endswith("Persistence") else "bare",
            )
            counts[bucket] += 1
    return counts


def orm_model_names() -> set[str]:
    """Every SQLAlchemy model class name, from the `models` modules that may define them."""
    names: set[str] = set()
    for path in _python_files(BACKEND_DIR / "src" / "app"):
        if "models" not in path.parts and path.stem != "models":
            continue
        names.update(node.name for node in ast.walk(_parse(path)) if isinstance(node, ast.ClassDef))
    return names


def _names_pattern(names: set[str]) -> re.Pattern[str] | None:
    if not names:
        return None
    return re.compile(r"\b(?:" + "|".join(re.escape(name) for name in sorted(names)) + r")\b")


def application_signatures_returning_orm() -> int:
    """Public application callables that hand an ORM row outward.

    This is the outward crossing that matters. `api/` not importing a model module does not
    establish that no ORM row reaches transport: a route can consume one through duck typing
    without naming its class. The return annotation is where the crossing is visible.
    """
    pattern = _names_pattern(orm_model_names())
    if pattern is None:
        return 0
    total = 0
    for path in application_files():
        for node in ast.walk(_parse(path)):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            if node.name.startswith("_") or node.returns is None:
                continue
            if pattern.search(ast.unparse(node.returns)):
                total += 1
    return total


def duplicated_reader_signatures() -> int:
    """Read signatures repeated verbatim across three or more readers in one domain.

    Exact method name and identical return annotation only. Overlaps that need judgment are
    left to review; this catches the literal copy that says two operations wanted one
    capability package.
    """
    shared: defaultdict[tuple[str, str, str], set[str]] = defaultdict(set)
    for path in application_files():
        domain = path.relative_to(DOMAINS).parts[0]
        for protocol in _protocols(_parse(path)):
            if not protocol.name.endswith("Reader"):
                continue
            for member in protocol.body:
                if not isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef):
                    continue
                if member.name.startswith("_"):
                    continue
                returns = ast.unparse(member.returns) if member.returns else "None"
                shared[(domain, member.name, returns)].add(protocol.name)
    return sum(1 for readers in shared.values() if len(readers) >= 3)


def port_suffixed_class_names() -> set[str]:
    return {
        node.name
        for path in _python_files(BACKEND_DIR / "src" / "app")
        for node in ast.walk(_parse(path))
        if isinstance(node, ast.ClassDef) and node.name.endswith("Port")
    }


def _port_suffix_reach() -> tuple[int, int]:
    pattern = _names_pattern(port_suffixed_class_names())
    if pattern is None:
        return 0, 0
    references = 0
    files = 0
    for root in ("src/app", "tests", "scripts", "experiments"):
        for path in _python_files(BACKEND_DIR / root):
            hits = len(pattern.findall(path.read_text(encoding="utf-8")))
            if hits:
                references += hits
                files += 1
    return references, files


def artefact_types_under_a_sorting_dir() -> list[str]:
    """Artefact-type packages filed under a `types/` directory rather than named directly.

    `types/` sorts siblings by what they are instead of naming what they do, which is the
    directory form of a `services/` bucket. The target is `artefacts/<type>/`.
    """
    sorting_dir = DOMAINS / "artefacts" / "types"
    if not sorting_dir.is_dir():
        return []
    return sorted(
        path.name
        for path in sorting_dir.iterdir()
        if path.is_dir() and (path / "__init__.py").exists()
    )


def port_modules() -> list[Path]:
    return sorted(DOMAINS.rglob("*ports.py"))


def domain_wide_port_buckets() -> set[str]:
    """Port modules named exactly `ports.py` — scoped to a domain rather than a capability."""
    return {str(path.relative_to(DOMAINS)) for path in port_modules() if path.name == "ports.py"}


def _contract_exemptions(name: str) -> int:
    config = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    for contract in config["tool"]["importlinter"]["contracts"]:
        if contract["name"] == name:
            return len(contract.get("ignore_imports", []))
    raise AssertionError(f"no import-linter contract named {name!r}")


@cache
def _measured() -> tuple[tuple[str, int], ...]:
    protocols = _protocols_by_suffix()
    references, files = _port_suffix_reach()
    counts = {
        "store_protocols": protocols["store"],
        "reader_protocols": protocols["reader"],
        "bare_name_protocols": protocols["bare"],
        "port_modules": len(port_modules()),
        "port_suffixed_names": len(port_suffixed_class_names()),
        "port_suffixed_references": references,
        "port_suffixed_files": files,
        "persistence_suffixed_protocols": protocols["persistence"],
        "domain_wide_port_modules": len(domain_wide_port_buckets()),
        "application_to_infrastructure_exemptions": _contract_exemptions(
            "application does not import infrastructure directly"
        ),
        "application_to_transport_exemptions": _contract_exemptions(
            "application does not import api transport"
        ),
        "application_signatures_returning_orm": application_signatures_returning_orm(),
        "duplicated_reader_signatures": duplicated_reader_signatures(),
        "artefact_types_under_a_sorting_dir": len(artefact_types_under_a_sorting_dir()),
    }
    return tuple(counts.items())


def census() -> dict[str, int]:
    """Every number `code-vocabulary.md` states about the current tree."""
    return dict(_measured())


def documented_exit_stories() -> dict[str, list[str]]:
    """Debt row -> the story IDs its Gap column names.

    A measured number with no owner is reported forever, which is how a metric becomes
    decoration. Every debt row names the story that deletes it, the same rule
    `test_import_contract_ceilings.py` already applies to each import exemption.
    """
    exits: dict[str, list[str]] = {}
    for line in VOCABULARY.read_text(encoding="utf-8").splitlines():
        row = DEBT_ROW.match(line)
        if row is not None and row["key"] in DEBT_CEILINGS:
            exits[row["key"]] = STORY_ID.findall(row["exit"])
    return exits


def exit_story_must_be_plannable(count: int) -> bool:
    """Whether a row's exit story still has to exist in the backlog.

    A row still carrying debt names work someone can pick up, so that story must be there. A
    row at zero names the story that closed it — history, not a plan. Requiring the closed
    story to stay in the backlog forever would make archiving it fail CI on a table that is
    more correct than it was the day before.
    """
    return count > 0


def backlog_story_ids() -> set[str] | None:
    """Every story ID in the backlog, or None when it is not checked out.

    The backlog is untracked, so a clone without it skips the cross-check rather than failing.
    """
    if not BACKLOG.exists():
        return None
    import yaml

    document = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    return {story["id"] for sprint in document["sprints"] for story in sprint.get("stories", [])}


def documented_census() -> dict[str, int]:
    lines = VOCABULARY.read_text(encoding="utf-8").splitlines()
    rows = (CENSUS_ROW.match(line) for line in lines)
    return {row["key"]: int(row["value"]) for row in rows if row is not None}


def rewrite_table() -> list[str]:
    """Rewrite each census row to its measured count, and re-sort debt by size.

    Debt rows read largest-first so the table ranks what is worth attention. Counts move, so
    the order is generated rather than typed — a hand-kept order drifts the moment a row
    shrinks past its neighbour.
    """
    measured = census()
    changed: list[str] = []
    lines = VOCABULARY.read_text(encoding="utf-8").splitlines(keepends=True)

    debt_slots: list[int] = []
    for index, line in enumerate(lines):
        row = CENSUS_ROW.match(line)
        if row is None or row["key"] not in measured:
            continue
        if row["key"] in DEBT_CEILINGS:
            debt_slots.append(index)
        current = int(row["value"])
        if current == measured[row["key"]]:
            continue
        head, _, tail = line.partition(f"| {current} |")
        lines[index] = f"{head}| {measured[row['key']]} |{tail}"
        changed.append(f"{row['key']}: {current} -> {measured[row['key']]}")

    def rank(line: str) -> tuple[int, str]:
        key = CENSUS_ROW.match(line)["key"]  # type: ignore[index]
        return -measured[key], key  # name breaks ties, so a tail of zeros stops churning

    ranked = sorted((lines[slot] for slot in debt_slots), key=rank)
    if [lines[slot] for slot in debt_slots] != ranked:
        changed.append("debt rows re-sorted by count")
    for slot, line in zip(debt_slots, ranked, strict=True):
        lines[slot] = line

    VOCABULARY.write_text("".join(lines), encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="update the table in place")
    if parser.parse_args().write:
        changed = rewrite_table()
        print("\n".join(changed) if changed else "table already matches the tree")
        return
    for key, value in census().items():
        ceiling = DEBT_CEILINGS.get(key)
        marker = f"  (ceiling {ceiling})" if ceiling is not None else "  (population)"
        print(f"{key:44} {value:>5}{marker}")


if __name__ == "__main__":
    main()
