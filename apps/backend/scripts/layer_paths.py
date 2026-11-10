"""One answer to "which files are in this layer".

Every guard that walks a layer needs this, and each one that spells the glob itself is a
chance to spell it slightly differently. `*/application/**` is the mistake that keeps
happening: it reads as "every application module" but stops at a top-level domain, so it
silently skips every artefact type — a quarter of the layer. A subdomain has its own layers
by definition, so a layer walk is `rglob`, never one `*` of depth.

`tests/test_layer_paths.py` fails any guard that goes back to spelling its own.
"""

from __future__ import annotations

from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
DOMAINS = BACKEND_DIR / "src" / "app" / "domains"

# The layers named by `domain-architecture-baseline.md`, each present at any nesting depth.
LAYERS = ("api", "application", "domain", "infrastructure")


def layer_files(layer: str, root: Path = DOMAINS) -> list[Path]:
    """Every `.py` under any `<layer>/` directory, nested subdomains included."""
    if layer not in LAYERS:
        raise ValueError(f"{layer!r} is not a layer; expected one of {LAYERS}")
    return sorted(root.rglob(f"{layer}/**/*.py"))


def application_files(root: Path = DOMAINS) -> list[Path]:
    return layer_files("application", root)


def api_files(root: Path = DOMAINS) -> list[Path]:
    return layer_files("api", root)
