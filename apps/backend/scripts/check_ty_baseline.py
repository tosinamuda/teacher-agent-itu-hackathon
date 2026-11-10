"""Fail when ty diagnostics differ from the checked-in debt baseline."""

from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "ty-baseline.txt"
DIAGNOSTIC = re.compile(r"^(?P<path>.*?):\d+:\d+: (?P<message>error\[[^]]+\].*)$")


def _diagnostics(output: str) -> Counter[str]:
    findings: Counter[str] = Counter()
    for line in output.splitlines():
        match = DIAGNOSTIC.match(line)
        if match:
            findings[f"{match.group('path')}|{match.group('message')}"] += 1
    return findings


def _print_difference(title: str, findings: Counter[str]) -> None:
    if not findings:
        return
    print(f"{title}:")
    for diagnostic, count in sorted(findings.items()):
        suffix = f" x{count}" if count > 1 else ""
        print(f"  {diagnostic}{suffix}")


def main() -> int:
    completed = subprocess.run(
        ["ty", "check", "--output-format", "concise", "--color", "never"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    observed = _diagnostics(completed.stdout + completed.stderr)
    expected = Counter(line for line in BASELINE.read_text().splitlines() if line)

    new = observed - expected
    resolved = expected - observed
    if new or resolved:
        _print_difference("New ty diagnostics", new)
        _print_difference("Resolved diagnostics still present in ty-baseline.txt", resolved)
        print("Update ty-baseline.txt only after reviewing the diagnostic change.")
        return 1
    if completed.returncode not in (0, 1):
        print(completed.stdout, end="")
        print(completed.stderr, end="")
        return completed.returncode

    print(f"ty ratchet passed: {sum(observed.values())} known diagnostics, 0 new")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
