"""The note's step names, limits and field names, read from ``config.json`` beside the rules."""

from __future__ import annotations

import json
from pathlib import Path

_CONFIG = json.loads((Path(__file__).resolve().parent / "config.json").read_text("utf-8"))

#: The step that keeps the plan's own questions, so another step changes its question instead.
EVALUATION_STEP: str = _CONFIG["steps"]["evaluation"]
MIN_NOTE_CHARS: int = _CONFIG["limits"]["min_note_chars"]
#: ``(field, name)``: the text called ``name`` in each item of the part's ``field`` list.
ASKED: list[tuple[str, str]] = [(field, name) for field, name in _CONFIG["asked"]]
PRACTISED: list[tuple[str, str]] = [(field, name) for field, name in _CONFIG["practised"]]
WORKED: str = _CONFIG["worked"]
