"""The provider boundary, replaced by a recorder.

Every leak assertion until now read a prompt the TEST assembled, by calling the
same input mappers production calls and formatting them with a ChatAdapter of
its own. That is one `acall` argument list away from the truth, and the gap is
not hypothetical: a jargon check assembled its own inputs, passed for months,
and C0 was being handed the fields it is denied the whole time.

This closes the gap. Substituting the LM — the real boundary — leaves every line
of the generator in the call path, so what gets asserted is the bytes the
pipeline actually sends.
"""

from __future__ import annotations

import json
from typing import Any

import dspy
from pydantic import BaseModel

# What the ChatAdapter reads back out of a completion.
FIELD_MARKER = "[[ ## {name} ## ]]"
COMPLETED = FIELD_MARKER.format(name="completed")


def _jsonable(value: object) -> object:
    return value.model_dump(mode="json") if isinstance(value, BaseModel) else value


def completion(**fields: object) -> str:
    """One completion in the adapter's field-marker format.

    ``reasoning`` leads unless given: every module here is a ChainOfThought, so
    it is an output field, and a completion missing one is a parse error rather
    than the interesting failure.
    """
    ordered: dict[str, object] = {"reasoning": "because.", **fields}
    parts = [
        f"{FIELD_MARKER.format(name=name)}\n"
        + (value if isinstance(value, str) else json.dumps(_jsonable(value)))
        for name, value in ordered.items()
    ]
    return "\n\n".join([*parts, COMPLETED])


class RecordingLM(dspy.BaseLM):
    """Records what was sent; answers from a fixed script.

    ``sent`` holds one entry per call, in call order, each the full message list
    the adapter built — which is what a provider would have received.
    """

    forward_contract = "typed_lm"

    def __init__(self, *replies: str, model: str = "recording/test") -> None:
        # cache=False: a cached second call never reaches forward, so the
        # recording would silently miss it.
        super().__init__(model=model, cache=False)
        self.replies = list(replies)
        self.sent: list[list[Any]] = []

    @property
    def messages_per_call(self) -> list[list[str]]:
        """Each call's messages as text, in order — the adapter puts values last."""
        return [[_content(message) for message in call] for call in self.sent]

    def messages(self, index: int = 0) -> list[str]:
        return self.messages_per_call[index]

    @property
    def prompts(self) -> list[str]:
        """Each call's messages flattened to the text that went on the wire."""
        return ["\n".join(call) for call in self.messages_per_call]

    def prompt(self, index: int = 0) -> str:
        return self.prompts[index]

    def forward(self, request: dspy.LMRequest) -> dspy.LMResponse:
        self.sent.append(list(request.messages))
        if not self.replies:
            raise AssertionError(
                f"call {len(self.sent)} has no scripted reply; "
                "an unexpected extra LM call is itself the finding"
            )
        return dspy.LMResponse.from_text(self.replies.pop(0), model=self.model)

    async def aforward(self, request: dspy.LMRequest) -> dspy.LMResponse:
        return self.forward(request)


def _content(message: object) -> str:
    """The text of one message, however the request happens to carry it.

    A typed request splits a message into parts, so the text has to be gathered
    from them; a plain dict still arrives on some paths.
    """
    if isinstance(message, dict):
        return str(message.get("content", ""))
    parts = getattr(message, "parts", None)
    if parts is None:
        return str(getattr(message, "content", message))
    return "\n".join(str(getattr(part, "text", "") or "") for part in parts)
