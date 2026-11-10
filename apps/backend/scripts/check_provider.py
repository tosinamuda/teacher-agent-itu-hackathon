"""Check a provider can actually run the arms before spending a run on it.

Swapping provider is not just a credentials change. The generation arms need two things
that providers differ on, and both fail late and confusingly:

  * a section returned against a schema (``packed``), and
  * a ReAct loop whose every turn parses into fields (``compose``) — the failure that
    killed a Bedrock run mid-flight was ``Adapter JSONAdapter failed to parse the LM
    response. LM Response: We need to call read_draft.``

    uv run python -m scripts.check_provider
    uv run python -m scripts.check_provider bedrock/converse/openai.gpt-oss-120b-1:0
"""

from __future__ import annotations

import sys

import dspy
from dotenv import load_dotenv
from pydantic import BaseModel

from app.infra.dspy_lm import (
    build_dspy_lm,
    configured_model,
    set_model_override,
    set_sampling_override,
)

REACT_TURNS = 3


class Section(BaseModel):
    title: str
    blocks: list[str]


class WriteSection(dspy.Signature):
    """Write a two-block section for a school revision pack."""

    topic: str = dspy.InputField()
    section: Section = dspy.OutputField()


class Compose(dspy.Signature):
    """Compose a section by calling add_block for each block, then finish."""

    topic: str = dspy.InputField()
    summary: str = dspy.OutputField()


def _structured(topic: str) -> str:
    result = dspy.Predict(WriteSection)(topic=topic).section
    return f"{len(result.blocks)} blocks, title {result.title[:32]!r}"


def _react(topic: str) -> str:
    written: list[str] = []

    def add_block(text: str) -> str:
        """Append one block of prose to the draft."""
        written.append(text)
        return f"draft now has {len(written)} blocks"

    def read_draft() -> str:
        """Return the draft so far."""
        return "\n".join(written) or "(empty)"

    dspy.ReAct(Compose, tools=[add_block, read_draft], max_iters=REACT_TURNS)(topic=topic)
    return f"{len(written)} blocks written through tools"


def main() -> int:
    load_dotenv(override=False)
    model = sys.argv[1] if len(sys.argv) > 1 else configured_model("generator")
    set_model_override(model)
    set_sampling_override(cache=False, temperature=0.0)
    dspy.configure(lm=build_dspy_lm())
    print(f"checking {model}\n")

    failures = 0
    for name, check in (
        ("structured output (packed)", _structured),
        ("ReAct loop (compose)", _react),
    ):
        try:
            print(f"  {name:28} OK   {check('the area of a rectangle')}")
        except Exception as error:  # noqa: BLE001 — the point is to report any failure
            failures += 1
            print(f"  {name:28} FAIL {type(error).__name__}: {str(error)[:150]}")
    print("\n" + ("usable for both arms" if not failures else f"{failures} arm(s) unusable"))
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
