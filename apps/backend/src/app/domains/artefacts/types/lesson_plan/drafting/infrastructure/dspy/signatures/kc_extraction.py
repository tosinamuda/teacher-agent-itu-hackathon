import dspy

from app.shared.json_types import JsonObject


class ExtractKCsSignature(dspy.Signature):
    """Extract knowledge components from textbook records for one atomic objective."""

    objective_text: str = dspy.InputField()
    target_bloom_level: str = dspy.InputField()
    prior_objectives: list[str] = dspy.InputField()
    textbook_records: list[JsonObject] = dspy.InputField(
        desc=(
            "Records with record_id, record_type, and content. "
            "These are the only records you may reference."
        )
    )

    knowledge_names: list[str] = dspy.OutputField()
    knowledge_descriptions: list[str] = dspy.OutputField()
    knowledge_types: list[str] = dspy.OutputField()
    knowledge_bloom_levels: list[str] = dspy.OutputField()
    knowledge_source_record_ids: list[list[str]] = dspy.OutputField()
    knowledge_prerequisite_indices: list[list[int]] = dspy.OutputField()
    knowledge_is_prior: list[bool] = dspy.OutputField()
    knowledge_focuses: list[str] = dspy.OutputField()
    exercise_record_ids: list[str] = dspy.OutputField()
