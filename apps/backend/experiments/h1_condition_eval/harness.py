"""The harness that produced a run, as a dimension rather than a name.

An arm name is a label; `compose-v2` says nothing about what varies. Five things do, and
each has changed a result on its own: which framework drives the call, which generator
module runs, which agent loop drives it, which contract family it renders, and how
evidence reaches it.

The sixth is the one that cost most. A half-adopted dspy upgrade turned prompt-parsed
`ReAct` into native tool calling and produced five duds out of six before anyone noticed,
because the arm name did not move and nothing recorded the library version. So the version
is captured at run time and travels with the run — of whichever framework produced it,
since a run is no longer necessarily a dspy run.

Nothing here defaults. An arm with no declared harness raises, and a run whose harness is
unrecorded is refused — a silent default is exactly the failure this exists to prevent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Literal

Delivery = Literal["in_prompt", "read_tools", "workspace_files"]
"""How the teaching evidence reaches the model: serialized into the prompt, fetched by a
tool call, or read off disk."""

Framework = Literal["dspy", "langgraph", "google-adk", "deepagents"]
"""Which agent framework drives the call. The outermost dimension: it decides what a loop
name even means, so `ReActV2` and `create_react_agent` are not comparable strings."""

Loop = Literal[
    "none",
    "ReAct",
    "ReActV2",
    "StateGraph",
    "create_deep_agent",
    "LlmAgent",
]
"""The agent loop, or none for a single-shot predictor. Each name belongs to one
framework: dspy's three, langgraph's own graph, deepagents' harness, ADK's agent."""

DISTRIBUTIONS: dict[Framework, str] = {
    "dspy": "dspy",
    "langgraph": "langgraph",
    "google-adk": "google-adk",
    "deepagents": "deepagents",
}
"""The installed distribution whose version a run of each framework must record."""


@dataclass(frozen=True)
class Harness:
    """What produced a pack, other than the condition and the model."""

    framework: Framework
    """Whose agent loop ran: dspy, langgraph, google-adk, deepagents."""
    module: str
    """The generator class: GenerateSection, ComposeSection, LangGraphComposeSection..."""
    loop: Loop
    contract_family: Literal["shared", "leveled", "composed", "from_sources"]
    evidence_delivery: Delivery

    def recorded(self) -> dict[str, str]:
        """The harness as it is written into a run, with the library version resolved."""
        return {**asdict(self), "framework_version": framework_version(self.framework)}


def framework_version(framework: Framework) -> str:
    """The installed version of the framework that produced the run.

    Resolved per framework rather than per package name: reading dspy's version off a
    langgraph run would record a library that never ran, which is the same blindness as
    recording nothing. A point release of any of them has changed behaviour here.
    """
    try:
        return version(DISTRIBUTIONS[framework])
    except PackageNotFoundError:  # pragma: no cover - every framework is a hard dependency
        return "unknown"


def require_harness(arm_name: str, harness: Harness | None) -> Harness:
    """Refuse an arm that has not declared what produced it."""
    if harness is None:
        raise ValueError(
            f"generator arm {arm_name!r} declares no harness. Every arm states its framework, "
            "module, loop, contract family and evidence delivery; a silent default is how the "
            "dspy 3.1.3 to 3.3.0b1 upgrade produced five duds out of six."
        )
    return harness


def require_recorded(record: dict[str, object], where: str) -> dict[str, str]:
    """Refuse a run record whose harness is missing or partial."""
    harness = record.get("harness")
    expected = {
        "framework",
        "module",
        "loop",
        "contract_family",
        "evidence_delivery",
        "framework_version",
    }
    if not isinstance(harness, dict) or expected - set(harness):
        missing = expected - set(harness) if isinstance(harness, dict) else expected
        raise ValueError(f"{where} records no harness; missing {sorted(missing)}")
    return {key: str(value) for key, value in harness.items()}
