"""The note's limits, read from ``config.json`` beside the rules."""

from __future__ import annotations

import json
from pathlib import Path

_LIMITS = json.loads((Path(__file__).resolve().parent / "config.json").read_text("utf-8"))["limits"]

MIN_EXPLANATION_CHARS: int = _LIMITS["min_explanation_chars"]
MIN_WORKED_EXAMPLES: int = _LIMITS["min_worked_examples"]
MIN_PRACTICE_QUESTIONS: int = _LIMITS["min_practice_questions"]
