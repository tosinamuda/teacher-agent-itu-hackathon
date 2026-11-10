"""Read values back out of a rendered prompt.

Every check in this package reads the message rather than the request, because the request
is where a leak hides: a label and an excerpt are both a populated string, and a field a
condition should not receive looks identical to one it simply had no value for.
"""

from __future__ import annotations

import json
import re

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prepared_call import (
    PreparedCall,
)

_FIELD_MARKER = re.compile(r"\[\[ ## (\w+) ## \]\]")


def user_message(call: PreparedCall) -> str:
    """The message carrying this call's values, as sent."""
    return next(message["content"] for message in call.messages() if message["role"] == "user")


def field_blocks(call: PreparedCall) -> dict[str, str]:
    """The user message split on its field markers.

    The adapter closes with a sentence naming the output markers, so the final block holds
    prose rather than a value. Readers take the leading value and ignore the rest.
    """
    parts = _FIELD_MARKER.split(user_message(call))
    return dict(zip(parts[1::2], parts[2::2], strict=True))


def json_value(block: str) -> object:
    """The leading JSON value of a block, ignoring the adapter's trailing instruction."""
    value, _ = json.JSONDecoder().raw_decode(block.strip())
    return value
