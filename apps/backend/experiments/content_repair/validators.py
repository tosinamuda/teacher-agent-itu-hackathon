"""Deterministic content validators — no LLM. These are the contract.

Each returns a list of concrete, human-readable issue strings (empty = clean). They are
usable three ways without change: as ReAct tool output, as a Refine reward, or as a hard
gate. The agent's job is to drive these to empty; the gate's job is to confirm it did.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import cast

from app.shared.json_types import JsonObject


def block_list(step: JsonObject) -> list[JsonObject]:
    """The step's content blocks, coerced to a typed list of dicts (drops non-dicts)."""
    raw = step.get("blocks")
    if not isinstance(raw, list):
        return []
    return [cast(JsonObject, item) for item in raw if isinstance(item, dict)]


# Tabular / aligned math environments that use `\\` row terminators.
_MATH_ENVS = (
    "array",
    "matrix",
    "pmatrix",
    "bmatrix",
    "Bmatrix",
    "vmatrix",
    "Vmatrix",
    "aligned",
    "cases",
)
_ENV_ALT = "|".join(_MATH_ENVS)
# \begin{env}{optional col spec} BODY \end{env}  (backref keeps begin/end paired)
_ENV_BLOCK = re.compile(
    r"\\begin\{(" + _ENV_ALT + r")\}(\{[^}]*\})?([\s\S]*?)\\end\{\1\}",
)
# A prose reference to a visual that points somewhere ("the diagram below", "as shown").
_DANGLING_VISUAL = re.compile(
    r"\b(diagram|figure|chart|illustration|picture|image|graph)\b[^.<>\n]{0,40}\b"
    r"(below|above|shown|here|opposite|following)\b|\bas shown\b",
    re.IGNORECASE,
)


@dataclass
class Report:
    """A validation result: empty issues == clean."""

    issues: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def validate_latex(content: str) -> list[str]:
    """Structural LaTeX checks for the defect classes the drafter actually produces."""
    issues: list[str] = []

    for env in _MATH_ENVS:
        begins = len(re.findall(r"\\begin\{" + env + r"\}", content))
        ends = len(re.findall(r"\\end\{" + env + r"\}", content))
        if begins != ends:
            issues.append(f"unbalanced \\begin/\\end for '{env}' ({begins} vs {ends})")

    for match in _ENV_BLOCK.finditer(content):
        body = match.group(3)
        segments = re.split(r"\s*\\hline\s*", body)
        for index in range(1, len(segments)):
            previous = segments[index - 1].strip()
            if previous and not previous.endswith("\\\\"):
                issues.append(
                    r"array row not terminated with \\ before \hline "
                    "(MathJax will reject this as 'Misplaced \\hline')"
                )
                break

    if content.count("$$") % 2 != 0:
        issues.append("unbalanced $$ display-math delimiters")

    return issues


def validate_grounded_figures(step: JsonObject, grounded_images: list[JsonObject]) -> list[str]:
    """Every grounded source figure must be embedded as a visual block, or it's missing."""
    embedded = {
        str(block.get("url") or "").strip()
        for block in block_list(step)
        if str(block.get("type") or "") == "visual"
    }
    issues: list[str] = []
    for image in grounded_images:
        url = str(image.get("url") or "").strip()
        if url and url not in embedded:
            name = url.rsplit("/", 1)[-1]
            issues.append(
                f"grounded figure not embedded: {name} (from {image.get('source_record_id')})"
            )
    return issues


def detect_dangling_visual_refs(step: JsonObject, grounded_images: list[JsonObject]) -> list[str]:
    """Heuristic: prose points at a visual, but there's no visual block and no source
    figure available to embed — so embedding can't fix it; the prose must be rewritten."""
    blocks = block_list(step)
    has_visual = any(str(b.get("type") or "") == "visual" for b in blocks)
    if has_visual or grounded_images:
        return []  # there IS (or can be) a visual — not dangling; embed_figures handles it

    # Report each offending location separately, naming the exact rewrite target — a vague
    # "prose references a visual" leaves a ReAct agent unable to localize the fix.
    sources: list[tuple[str, str, str]] = [("step content", "step", str(step.get("content") or ""))]
    for block in blocks:
        if str(block.get("type") or "") == "explanation":
            block_id = str(block.get("id") or "")
            sources.append((f"block {block_id}", block_id, str(block.get("content") or "")))

    issues: list[str] = []
    for label, target_id, text in sources:
        match = _DANGLING_VISUAL.search(text)
        if match:
            issues.append(
                f"{label} references a visual that does not exist "
                f'("{match.group(0).strip()}") and has no source figure to embed — '
                f"rewrite it with rewrite_explanation(block_id={target_id!r}, ...) so it "
                "does not depend on a missing visual"
            )
    return issues


def _block_text_fields(block: JsonObject) -> list[str]:
    out: list[str] = []
    for key in ("content", "problem", "final_answer", "question", "answer"):
        value = block.get(key)
        if isinstance(value, str):
            out.append(value)
    raw_steps = block.get("steps")
    for sub in raw_steps if isinstance(raw_steps, list) else []:
        if isinstance(sub, dict):
            content = sub.get("content")
            if isinstance(content, str):
                out.append(content)
    return out


def validate_step(step: JsonObject, grounded_images: list[JsonObject]) -> Report:
    """Run all validators over a step and its blocks; aggregate concrete issues."""
    issues: list[str] = []

    step_content = step.get("content")
    if isinstance(step_content, str):
        issues += [f"step content: {msg}" for msg in validate_latex(step_content)]
    for block in block_list(step):
        block_id = block.get("id")
        for text in _block_text_fields(block):
            issues += [f"block {block_id}: {msg}" for msg in validate_latex(text)]

    issues += validate_grounded_figures(step, grounded_images)
    issues += detect_dangling_visual_refs(step, grounded_images)
    return Report(issues=issues)
