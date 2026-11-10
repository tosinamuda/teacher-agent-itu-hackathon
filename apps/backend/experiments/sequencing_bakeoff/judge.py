"""LLM raters for a single lesson step: a quality judge and a grounding-fidelity checker.

The quality judge sees the rendered step (prose with `[TABLE]` and `[FIGURE: caption]`
markers) — blind to which strategy produced it. The fidelity checker compares the prose to
the figures' real captions and flags any statement about a figure that the caption does not
support (a hallucinated figure detail) — the dimension the first bake-off could not measure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import dspy

from app.shared.json_types import JsonObject
from experiments.content_repair.validators import block_list

_ARRAY_MATH = re.compile(r"\$\$\s*\\begin\{array\}.*?\\end\{array\}\s*\$\$", re.DOTALL)
_BARE_ARRAY = re.compile(r"\\begin\{array\}.*?\\end\{array\}", re.DOTALL)


def _figure_caption(block: JsonObject) -> str:
    return str(block.get("caption") or "").strip() or "figure (no caption)"


def render_for_judge(step: JsonObject) -> str:
    """Reading-order render: prose, with `[TABLE]` and `[FIGURE: caption]` where assets sit."""
    lines: list[str] = []
    for block in block_list(step):
        if str(block.get("type") or "") == "visual":
            lines.append(f"[FIGURE: {_figure_caption(block)}]")
            continue
        content = str(block.get("content") or "")
        content = _ARRAY_MATH.sub("[TABLE]", content)
        content = _BARE_ARRAY.sub("[TABLE]", content)
        lines.append(content.strip())
    return "\n\n".join(line for line in lines if line)


def prose_only(step: JsonObject) -> str:
    """The step's prose (tables collapsed to [TABLE], figures removed) for fidelity checking."""
    lines: list[str] = []
    for block in block_list(step):
        if str(block.get("type") or "") == "visual":
            continue
        raw = str(block.get("content") or "")
        content = _BARE_ARRAY.sub("[TABLE]", _ARRAY_MATH.sub("[TABLE]", raw))
        lines.append(content.strip())
    return "\n\n".join(line for line in lines if line)


def figure_captions(step: JsonObject) -> list[str]:
    captions = [
        str(b.get("caption") or "").strip()
        for b in block_list(step)
        if str(b.get("type")) == "visual"
    ]
    return [c for c in captions if c]


# ---- quality judge -------------------------------------------------------------------


class JudgeLessonStep(dspy.Signature):
    """You are an expert teacher reviewing ONE lesson step (a draft). Score it 1-5 on each
    axis. Judge only what you see; do not assume how it was produced. `[TABLE]` and
    `[FIGURE: caption]` mark where a visual appears in the flow."""

    objective: str = dspy.InputField()
    grade: str = dspy.InputField()
    rendered_step: str = dspy.InputField()
    sequencing_score: int = dspy.OutputField(
        desc="1-5: do tables/figures appear where the prose refers to them, in a sensible order?"
    )
    coherence_score: int = dspy.OutputField(desc="1-5: does it read as one connected lesson?")
    pedagogy_score: int = dspy.OutputField(desc="1-5: pedagogically sound for objective+grade?")
    rationale: str = dspy.OutputField(desc="2-3 sentences justifying the scores.")


@dataclass
class JudgeScore:
    sequencing: int
    coherence: int
    pedagogy: int
    rationale: str

    @property
    def mean(self) -> float:
        return round((self.sequencing + self.coherence + self.pedagogy) / 3, 2)


def _clamp(value: object) -> int:
    try:
        return max(1, min(5, int(str(value))))
    except (TypeError, ValueError):
        return 1


def judge_step(
    step: JsonObject, *, objective: str, grade: str, lm: dspy.LM | None = None
) -> JudgeScore:
    judge = dspy.Predict(JudgeLessonStep)
    kwargs = {"objective": objective, "grade": grade, "rendered_step": render_for_judge(step)}
    prediction = _run(judge, kwargs, lm)
    return JudgeScore(
        sequencing=_clamp(prediction.sequencing_score),
        coherence=_clamp(prediction.coherence_score),
        pedagogy=_clamp(prediction.pedagogy_score),
        rationale=str(prediction.rationale),
    )


# ---- grounding-fidelity checker ------------------------------------------------------


class CheckFigureFidelity(dspy.Signature):
    """Compare a lesson step's prose to the captions of the figures it includes. List every
    statement in the prose that describes what a figure shows but is NOT supported by, or
    contradicts, that figure's caption (a hallucinated figure detail, e.g. wrong numbers or
    ranges). Ignore general teaching prose that is not describing a figure. Return an empty
    list if there are none."""

    prose: str = dspy.InputField(desc="The step's prose (figures not inlined).")
    figure_captions: str = dspy.InputField(desc="One line per figure: its caption.")
    contradictions: list[str] = dspy.OutputField(
        desc="Each prose statement about a figure that its caption does not support."
    )


def check_fidelity(step: JsonObject, *, lm: dspy.LM | None = None) -> list[str]:
    """Return the prose statements about figures unsupported by their captions (empty = clean)."""
    captions = figure_captions(step)
    if not captions:
        return []
    checker = dspy.Predict(CheckFigureFidelity)
    kwargs = {"prose": prose_only(step), "figure_captions": "\n".join(f"- {c}" for c in captions)}
    prediction = _run(checker, kwargs, lm)
    raw = prediction.contradictions
    return [str(item) for item in raw] if isinstance(raw, list) else []


def _run(module: dspy.Module, kwargs: dict[str, str], lm: dspy.LM | None) -> dspy.Prediction:
    if lm is not None:
        with dspy.context(lm=lm):
            return module(**kwargs)
    return module(**kwargs)
