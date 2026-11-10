"""DSPy contract for resolving line-anchored section findings."""

import dspy


class ResolveSectionFindings(dspy.Signature):
    """Fix exactly the review findings by editing the file through the tools.

    Each finding names the line it starts on and quotes the offending words.
    Read the surrounding lines first, then make the smallest edits that resolve
    each finding. Never touch block-marker or figure lines.
    """

    findings: list[str] = dspy.InputField(
        desc="Review comments, each as 'line N: quote - problem'."
    )
    done: bool = dspy.OutputField(desc="True once every finding is resolved by an edit.")
