"""The plugins that ship with the app: the folders under the checkout's ``plugins/``.

A deploy installs and updates them, so the API leaves them alone: the app needs them, and a
change made through the API would be undone by the next deploy.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.config import BACKEND_DIR

SHIPPED_DIR = BACKEND_DIR.parents[1] / "plugins"


def shipped_names() -> frozenset[str]:
    """The names the plugins in ``SHIPPED_DIR`` install under; none when the folder is missing."""
    if not SHIPPED_DIR.is_dir():
        return frozenset()
    return frozenset(name for folder in SHIPPED_DIR.iterdir() for name in _names_in(folder))


def _json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _names_in(folder: Path) -> list[str]:
    """What each artefact of the folder installs under: its ``name``, else the plugin's own."""
    manifest = _json(folder / "plugin.json")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("name"), str):
        return []
    ours = manifest.get("extensions", {}).get("com.tosinamuda.lpcg", {})
    paths = ours.get("artefacts", []) if isinstance(ours, dict) else []
    names = []
    for path in paths if isinstance(paths, list) else []:
        artefact = _json(folder / str(path))
        given = artefact.get("name") if isinstance(artefact, dict) else None
        names.append(given if isinstance(given, str) else manifest["name"])
    return names
