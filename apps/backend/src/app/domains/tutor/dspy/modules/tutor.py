import dspy

from app.domains.tutor.dspy.signatures.answer_question import TutorAnswerSignature


class TutorModule(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.predict = dspy.Predict(TutorAnswerSignature)

    def forward(
        self,
        lesson_context: str,
        step_context: str,
        items_context: str,
        question: str,
        schema_hint: str,
    ) -> dspy.Prediction:
        return self.predict(
            lesson_context=lesson_context,
            step_context=step_context,
            items_context=items_context,
            question=question,
            schema_hint=schema_hint,
        )

    async def aforward(
        self,
        lesson_context: str,
        step_context: str,
        items_context: str,
        question: str,
        schema_hint: str,
    ) -> dspy.Prediction:
        return await self.predict.acall(
            lesson_context=lesson_context,
            step_context=step_context,
            items_context=items_context,
            question=question,
            schema_hint=schema_hint,
        )
