"""Deterministic metrics for each variant: validity, character economy, ref faithfulness."""

from __future__ import annotations

from dataclasses import dataclass

from app.shared.json_types import JsonObject
from experiments.content_repair.validators import block_list, validate_step


@dataclass
class VariantMetrics:
    latex_valid: bool
    latex_issue: str
    llm_authored_chars: int  # characters the LLM actually generated (prose + markers/refs)
    final_total_chars: int  # size of the final assembled step content (incl spliced verbatim)
    refs_valid: list[str]  # referenced ids that exist in the manifest
    refs_hallucinated: list[str]  # referenced ids NOT in the manifest
    refs_missed: list[str]  # manifest ids the variant never placed

    @property
    def ref_faithful(self) -> bool:
        return not self.refs_hallucinated


def latex_verdict(step: JsonObject) -> tuple[bool, str]:
    issues = validate_step(step, []).issues
    latex_issues = [i for i in issues if "hline" in i or "begin/\\end" in i or "$$" in i]
    return (not latex_issues), (latex_issues[0] if latex_issues else "")


def step_content_chars(step: JsonObject) -> int:
    """Total characters of all block contents in the final assembled step."""
    total = 0
    for block in block_list(step):
        total += len(str(block.get("content") or ""))
        total += len(str(block.get("url") or ""))
    return total


def score_variant(
    *,
    step: JsonObject,
    llm_authored_text: str,
    referenced_ids: list[str],
    manifest_ids: list[str],
) -> VariantMetrics:
    valid, issue = latex_verdict(step)
    manifest_set = set(manifest_ids)
    referenced_set = set(referenced_ids)
    return VariantMetrics(
        latex_valid=valid,
        latex_issue=issue,
        llm_authored_chars=len(llm_authored_text),
        final_total_chars=step_content_chars(step),
        refs_valid=sorted(referenced_set & manifest_set),
        refs_hallucinated=sorted(referenced_set - manifest_set),
        refs_missed=sorted(manifest_set - referenced_set),
    )
