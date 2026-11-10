"""The dspy.ReAct content-repair agent and its tools.

The step under repair lives in a `RepairSession` closure, so the tools mutate real
structured state and the LLM only orchestrates (it never has to serialise/round-trip the
step JSON — which would be expensive and error-prone). The agent's text output is just a
summary; the authoritative repaired step is `session.step`, scored afterwards by an
independent gate.
"""

from __future__ import annotations

from collections.abc import Callable

import dspy

from app.shared.json_types import JsonObject

from .repairs import embed_missing_figures, repair_step_latex
from .validators import block_list, validate_step


class RepairSession:
    """Mutable state the tools operate on: one step + its grounded source figures."""

    def __init__(self, step: JsonObject, grounded_images: list[JsonObject]) -> None:
        self.step = step
        self.grounded_images = grounded_images
        self.tool_calls: list[str] = []


def build_tools(session: RepairSession) -> list[Callable[..., str]]:
    """Build the agent's tools, closed over `session`. Docstrings are what the agent reads."""

    def check_content() -> str:
        """Validate the current step for content problems: malformed LaTeX, grounded
        source figures referenced but not embedded, and prose pointing at a visual that
        does not exist. Returns 'PASS' or a numbered list of concrete issues. ALWAYS call
        this first, and again after every fix, until it returns PASS."""
        session.tool_calls.append("check_content")
        report = validate_step(session.step, session.grounded_images)
        if report.ok:
            return "PASS - no content issues remain."
        return "ISSUES:\n" + "\n".join(f"{i + 1}. {msg}" for i, msg in enumerate(report.issues))

    def fix_latex() -> str:
        """Deterministically repair malformed LaTeX (e.g. table/array rows missing the
        '\\\\' terminator before \\hline). Use for any LaTeX issue. Returns which parts changed."""
        session.tool_calls.append("fix_latex")
        changed = repair_step_latex(session.step)
        return f"repaired LaTeX in: {', '.join(changed)}" if changed else "no LaTeX changes needed"

    def embed_figures() -> str:
        """Embed any grounded source figures the step references but hasn't included, as
        image blocks. Use for 'grounded figure not embedded' issues. Returns what was added."""
        session.tool_calls.append("embed_figures")
        added = embed_missing_figures(session.step, session.grounded_images)
        return f"embedded figures: {', '.join(added)}" if added else "no figures needed embedding"

    def rewrite_explanation(block_id: str, new_markdown: str) -> str:
        """Replace the markdown of an explanation block (pass block_id='step' for the
        step's own content). Use ONLY for issues no other tool can fix - e.g. prose that
        references a visual that does not exist: rewrite it so it does not depend on the
        missing visual. Returns confirmation."""
        session.tool_calls.append(f"rewrite_explanation({block_id})")
        if block_id == "step":
            session.step["content"] = new_markdown
            return "rewrote step content"
        for block in block_list(session.step):
            if str(block.get("id")) == block_id:
                if str(block.get("type") or "") != "explanation":
                    return f"block {block_id!r} is not an explanation block; cannot rewrite"
                block["content"] = new_markdown
                return f"rewrote block {block_id}"
        return f"no block with id {block_id!r}"

    return [check_content, fix_latex, embed_figures, rewrite_explanation]


class RepairLessonStep(dspy.Signature):
    """Fix every content-quality problem in a lesson step so it renders correctly and has
    no dangling references.

    Call check_content to find issues, then use the repair tools to fix them, re-checking
    after each fix until check_content returns PASS. Prefer the deterministic tools
    (fix_latex, embed_figures); use rewrite_explanation ONLY for problems no other tool can
    fix. Stop as soon as check_content returns PASS."""

    step_title: str = dspy.InputField(desc="Title of the lesson step being repaired.")
    known_problem: str = dspy.InputField(
        desc="A one-line hint about what looked wrong (may be vague; verify with check_content)."
    )
    outcome: str = dspy.OutputField(desc="One-line summary of the fixes applied.")


def build_agent(session: RepairSession, *, max_iters: int = 8) -> dspy.ReAct:
    """A ReAct agent whose tools repair `session.step` in place."""
    return dspy.ReAct(RepairLessonStep, tools=build_tools(session), max_iters=max_iters)
