import dspy

from app.shared.json_types import JsonObject


class DesignAssessmentSignature(dspy.Signature):
    """Design one assessment item that proves mastery of a knowledge item."""

    knowledge_name: str = dspy.InputField()
    knowledge_description: str = dspy.InputField()
    knowledge_type: str = dspy.InputField(
        desc="'concept' = a definition/idea; 'procedure' = a method; "
        "'representation' = reading/drawing a form."
    )
    bloom_level: str = dspy.InputField()
    source_content: str = dspy.InputField(
        desc="Grounding textbook content. The question must be answerable from this only."
    )
    existing_exercises: list[JsonObject] = dspy.InputField(
        desc="Grounded textbook exercises to adapt when possible."
    )

    question: str = dspy.OutputField()
    expected_answer: str = dspy.OutputField()
    bloom_justification: str = dspy.OutputField()
