"""Hallucination audit over harness runs: source-attribution claims in outputs.

Scans every generated section for phrases that attribute content to the
textbook/source, splits them into HARD provenance claims (problems/answers/
solutions attributed to the source — the failure mode caught by manual
judging) and SOFT attributions (method/definition references — often
legitimate now that excerpts are real, but worth eyeballing), and prints
per-run counts with the offending lines. Deterministic flagging for a human
read — not a verdict by itself.

Usage:
    uv run python -m experiments.p1_prompt_eval.audit <run-label> [<run-label> ...]
"""

from __future__ import annotations

import json
import re
import sys

from experiments.p1_prompt_eval.runner import RUNS_DIR

# Problems/answers/solutions attributed to the source — never legitimate for
# generated items (inherited base claims show up here too; check the base).
_HARD = re.compile(
    r"(?:drawn from|taken from|given in|provided in|available in|are in)"
    r"\s+the\s+(?:textbook|source)"
    r"|textbook (?:exercise|solution|answer)"
    r"|(?:solution|answer)s?[^.\n]{0,60}?\b(?:in|from)\s+the\s+(?:textbook|source)"
    r"|(?:check|verify|compare)[^.\n]{0,60}?\b(?:against|with|in|using)\s+the\s+(?:textbook|source)",
    re.IGNORECASE,
)
# Method/definition attributions — legitimate when the cited excerpt contains
# them, drift risk when it doesn't.
_SOFT = re.compile(
    r"(?:described|illustrated|shown|explained|appears|presented|defined|follows?|mirrors?)"
    r"[^.\n]{0,40}?\bthe\s+textbook"
    r"|textbook(?:'s)?\s+(?:description|illustration|example|method|chapter|activity)",
    re.IGNORECASE,
)


def _sections(label: str):
    data = json.loads((RUNS_DIR / label / "run.json").read_text())
    for case in data["cases"]:
        for section in case["sections"]:
            yield case["case_id"], section


def audit(label: str) -> dict:
    hard, soft, n_sections = [], [], 0
    for case_id, section in _sections(label):
        n_sections += 1
        text = "\n".join(block.get("text") or "" for block in section.get("blocks", []))
        for match in _HARD.finditer(text):
            line = text[max(0, match.start() - 60) : match.end() + 40].replace("\n", " ")
            hard.append((case_id, section["lesson_objective_id"], line.strip()))
        for match in _SOFT.finditer(text):
            line = text[max(0, match.start() - 60) : match.end() + 40].replace("\n", " ")
            soft.append((case_id, section["lesson_objective_id"], line.strip()))
    return {"sections": n_sections, "hard": hard, "soft": soft}


def usage_summary(label: str) -> str:
    data = json.loads((RUNS_DIR / label / "run.json").read_text())
    ins, outs = [], []
    for case in data["cases"]:
        for usage in case.get("usage", []):
            if usage.get("input_tokens"):
                ins.append(usage["input_tokens"])
            if usage.get("output_tokens"):
                outs.append(usage["output_tokens"])
    if not ins:
        return "no recorded usage"
    return (
        f"calls={len(ins)} mean input={sum(ins) / len(ins):,.0f} "
        f"mean output={sum(outs) / len(outs):,.0f} "
        f"total={sum(ins) + sum(outs):,.0f} tokens"
    )


def main() -> None:
    for label in sys.argv[1:]:
        result = audit(label)
        print(f"\n== {label} ({result['sections']} sections) — {usage_summary(label)}")
        print(f"HARD provenance claims: {len(result['hard'])}")
        for case_id, objective, line in result["hard"]:
            print(f"  [{case_id[-6:]}/{objective}] …{line}…")
        print(f"SOFT attributions: {len(result['soft'])}")
        for case_id, objective, line in result["soft"][:8]:
            print(f"  [{case_id[-6:]}/{objective}] …{line}…")
        if len(result["soft"]) > 8:
            print(f"  … and {len(result['soft']) - 8} more")


if __name__ == "__main__":
    main()
