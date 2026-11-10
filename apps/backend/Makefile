# Backend quality gate. Run `make quality` for the full suite, or any single
# target (e.g. `make complexity`) in isolation. Everything runs through `uv run`
# so the pinned dev-dependency versions are used — never a global install.
#
# A small stack of focused tools, each catching a different class of problem:
#   ruff      style, bugs, bad patterns, import hygiene, annotations
#   radon     cyclomatic complexity + maintainability index (reporting)
#   xenon     fails the build when complexity exceeds the threshold (gate)
#   mypy      type-level mistakes (deeper than ty)
#   coverage  branch coverage — which risky paths are actually tested
#   bandit    common security smells
#   vulture   dead code
#   pylint    inference + design smells ruff can't do (duplicate-code,
#             cyclic-import, no-member/not-callable, useless-return); curated
#             to a complementary set in [tool.pylint.*] so it never echoes ruff
#   imports   import-linter — dependency DIRECTION (pylint finds cycles, not
#             direction); contracts in [tool.importlinter]

.PHONY: quality lint imports format complexity metrics types coverage security deadcode pylint

quality: lint imports complexity types coverage security deadcode pylint

lint:
	uv run ruff check .
	uv run ruff format --check .

# Enforce dependency DIRECTION. Every contract passes today; the
# application-does-not-import-infrastructure one passes against a SHRINK-ONLY
# baseline of pre-existing imports (see [tool.importlinter]) — a new one fails
# here, and so does a baseline line left behind after its import is fixed.
imports:
	uv run lint-imports

format:
	uv run ruff format .

# Reporting view of complexity + maintainability (does not fail the build).
metrics:
	uv run radon cc src/app -a -s
	uv run radon mi src/app -s

# Gate: no single block worse than rank C; module + repo averages capped. Green as
# of the complexity burn-down — see docs/audit-remediation-todo.md.
complexity:
	uv run xenon src/app --max-absolute C --max-modules B --max-average A

types:
	uv run mypy

coverage:
	uv run coverage run --branch -m pytest
	uv run coverage report -m

security:
	uv run bandit -c pyproject.toml -r src/app -q

deadcode:
	uv run vulture

# Complementary to ruff: only the pylint-unique checks (inference + cross-file
# design smells) are enabled — see [tool.pylint.*] in pyproject.toml.
pylint:
	uv run pylint src/app
