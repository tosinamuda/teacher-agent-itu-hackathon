import dspy


class AtomizeObjectiveSignature(dspy.Signature):
    """Split a compound curriculum objective into atomic objectives."""

    performance_objective: str = dspy.InputField()
    evaluation_guide: list[str] = dspy.InputField()
    subtopic_title: str = dspy.InputField()

    atomic_texts: list[str] = dspy.OutputField()
    bloom_verbs: list[str] = dspy.OutputField()
