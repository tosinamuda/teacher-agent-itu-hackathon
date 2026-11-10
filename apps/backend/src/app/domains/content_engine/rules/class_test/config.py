"""The letters of a question's options, read from ``config.json`` beside the rules."""

from __future__ import annotations

import json
from pathlib import Path

_CONFIG = json.loads((Path(__file__).resolve().parent / "config.json").read_text("utf-8"))

LETTERS: list[str] = _CONFIG["letters"]
