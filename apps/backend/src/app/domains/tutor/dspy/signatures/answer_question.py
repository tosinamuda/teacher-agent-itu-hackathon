import dspy


class TutorAnswerSignature(dspy.Signature):
    """Answer student questions using only the current step context."""

    lesson_context = dspy.InputField(
        desc=("JSON with lesson metadata: subject, grade, term, week, topic, subtopic, objectives.")
    )
    step_context = dspy.InputField(
        desc="JSON with step metadata: step_id, type, title, estimated_minutes."
    )
    items_context = dspy.InputField(
        desc=(
            "JSON list of items available in the step. Each includes item_id, type, "
            "content, answer, hints. Use item_ids as citations."
        )
    )
    question = dspy.InputField(desc="Student question about the current step.")
    schema_hint = dspy.InputField(
        desc=(
            'Return JSON: {"answer": string, "citations": ["ITEM_ID"], "refusal": boolean, '
            '"reason": string|null}. If question is off-scope, refusal=true.'
        )
    )

    response_json: str = dspy.OutputField(
        desc=(
            "JSON response following schema_hint. Keep answer concise, friendly, and "
            "grounded in items."
        )
    )
