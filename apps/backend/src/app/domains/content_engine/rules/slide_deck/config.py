"""The plugin's step names and limits, read from ``config.json`` beside the rules."""

from __future__ import annotations

import json
from pathlib import Path

_CONFIG = json.loads((Path(__file__).resolve().parent / "config.json").read_text("utf-8"))

#: The step that opens the lesson: the recall question, the aim, the idea the lesson builds on.
INTRO_STEP: str = _CONFIG["steps"]["intro"]
#: The step that keeps the plan's own questions, so another step changes its question instead.
EVALUATION_STEP: str = _CONFIG["steps"]["evaluation"]
LIMITS: dict[str, int] = _CONFIG["limits"]
#: The symbols after a number that make it a measure, such as ``2 km``.
MEASURE_UNITS: list[str] = _CONFIG["measure_units"]
