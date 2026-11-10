"""Which input layer is responsible for which layer of the pack.

A generated section is not one thing. It has a title, an explanation, worked
examples, sometimes a figure, and practice with answers — and each of those is a
different *kind* of content that needs a different *kind* of input to be written
truthfully rather than invented.

This module names both sides and states the correspondence, so that "C1 receives
the lesson plan" can be replaced by the sharper question the study actually turns
on: for each layer the reader sees, did anything in the input supply it?

The correspondence is a claim about grounding, not about what a language model
can produce. A model with no worked examples in its input will still write worked
examples; they just come from its own knowledge of the topic rather than from the
lesson that was taught. That is exactly the distinction H1 exists to measure, so
it is worth being able to see it per layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Verdict = Literal["grounded", "substituted", "unsourced", "absent"]

# Where a probe looks. The assembled inputs are the three containers the contract
# actually declares, so a layer is located by container and key rather than by a
# path expression — there is no nesting to walk.
Probe = tuple[str, str]


@dataclass(frozen=True)
class InputLayer:
    key: str
    name: str
    carries: str
    probes: tuple[Probe, ...]
    channel: str = "prompt"

    def present_in(self, inputs: dict) -> bool:
        return any(_filled(inputs.get(container), field) for container, field in self.probes)


@dataclass(frozen=True)
class OutputLayer:
    key: str
    name: str
    is_what: str
    source: str
    substitute: str | None = None
    substitute_note: str = ""


def _filled(container: object, field: str) -> bool:
    if isinstance(container, dict):
        return container.get(field) not in (None, "", [], {})
    if isinstance(container, list) and field == "*":
        return bool(container)
    return False


INPUT_LAYERS: tuple[InputLayer, ...] = (
    InputLayer(
        "scope",
        "Scope",
        "what is to be taught, and to whom",
        (("unit_context", "objective_text"), ("lesson_context", "topic")),
    ),
    InputLayer(
        "prior",
        "Prior knowledge",
        "what the learner already knew coming in",
        (("lesson_context", "entry_behaviour"),),
    ),
    InputLayer(
        "materials",
        "Materials",
        "what the lesson was represented with",
        (("lesson_context", "instructional_materials"),),
    ),
    InputLayer(
        "position",
        "Position",
        "where this objective sat in the sequence",
        (("unit_context", "current_step"),),
    ),
    InputLayer(
        "method",
        "Method",
        "the shape of the teaching, as event labels",
        (("unit_context", "instructional_events"),),
    ),
    InputLayer(
        "content",
        "Enacted content",
        "what was actually explained and worked through",
        # Three routes, because a grounded contract renames the field: the plan's own
        # step narration, and the note under either name a contract gives it.
        (
            ("unit_context", "step_content"),
            ("lesson_content", "*"),
            ("source_evidence", "*"),
        ),
    ),
    InputLayer(
        "tasks",
        "Set work",
        "what the learners were asked to do in class",
        (("unit_context", "student_tasks"),),
    ),
    InputLayer(
        "assessment",
        "Assessment",
        "the questions the lesson was checked with",
        (("unit_context", "assessment_points"),),
    ),
    InputLayer(
        "figures",
        "Figures",
        "the drawings the lesson used",
        # Not in the payload. The prompt carries only a figure_ref and a caption;
        # the drawing itself is attached by a composition tool, so availability is
        # a property of the unit rather than of the rendered fields.
        (("attachable", "source_figures"),),
        channel="tool",
    ),
)

OUTPUT_LAYERS: tuple[OutputLayer, ...] = (
    OutputLayer("title", "Title", "the reader-facing framing of the section", "scope"),
    OutputLayer(
        "explanation",
        "Explanation",
        "the principle, rule or relationship to review",
        "content",
        "method",
        "written from event labels — the shape of the teaching without its substance",
    ),
    OutputLayer(
        "worked_example",
        "Worked example",
        "a problem with its solution worked through",
        "content",
        None,
        "",
    ),
    OutputLayer("visual", "Figure", "a drawing the learner reads from", "figures"),
    OutputLayer(
        "practice",
        "Practice",
        "what the learner does",
        "tasks",
        "assessment",
        "written from the teacher's evaluation questions instead of her set work",
    ),
    OutputLayer(
        "answer",
        "Answer",
        "what the learner checks against",
        "content",
        "assessment",
        "checked against the evaluation answers rather than the taught method",
    ),
)

BY_KEY = {layer.key: layer for layer in INPUT_LAYERS}


@dataclass(frozen=True)
class LayerTrace:
    layer: OutputLayer
    produced: int
    source_present: bool
    substitute_present: bool

    @property
    def verdict(self) -> Verdict:
        if not self.produced:
            return "absent"
        if self.source_present:
            return "grounded"
        return "substituted" if self.substitute_present else "unsourced"

    @property
    def sourced_by(self) -> str:
        if self.verdict == "grounded":
            return BY_KEY[self.layer.source].name
        if self.verdict == "substituted" and self.layer.substitute:
            return BY_KEY[self.layer.substitute].name
        return "nothing in the input"


def count_produced(sections: list[dict]) -> dict[str, int]:
    """How many of each output layer the generator actually produced."""
    counts = dict.fromkeys((layer.key for layer in OUTPUT_LAYERS), 0)
    for section in sections:
        counts["title"] += bool(str(section.get("title") or "").strip())
        for block in section.get("blocks") or []:
            key = block.get("block_type")
            if key in counts:
                counts[key] += 1
        for item in section.get("practice") or []:
            counts["practice"] += 1
            counts["answer"] += bool(str(item.get("answer") or "").strip())
    return counts


def trace(inputs: dict, sections: list[dict]) -> list[LayerTrace]:
    produced = count_produced(sections)
    present = {layer.key: layer.present_in(inputs) for layer in INPUT_LAYERS}
    return [
        LayerTrace(
            layer=layer,
            produced=produced[layer.key],
            source_present=present[layer.source],
            substitute_present=bool(layer.substitute) and present[str(layer.substitute)],
        )
        for layer in OUTPUT_LAYERS
    ]
