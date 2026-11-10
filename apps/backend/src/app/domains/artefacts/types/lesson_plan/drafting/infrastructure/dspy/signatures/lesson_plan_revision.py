"""Revise a teacher-confirmed lesson plan from one piece of human feedback.

The human-in-the-loop revision chat hands the model the CURRENT plan plus a single
instruction (often anchored to a highlighted part) and asks for a focused edit:
change exactly what was asked and preserve everything else. The output is the full
revised ``SessionPlan`` (not a diff) so it can be validated and persisted as a new
version. ``prior_violations`` is the self-correction channel on retry.
"""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import SessionPlan


class ReviseLessonPlanSignature(dspy.Signature):
    """Apply ONE teacher instruction to an existing JSS1 lesson plan, minimally.

    You are an expert teacher revising a colleague's lesson plan in response to a
    single piece of feedback. Rules:
    - Apply EXACTLY the requested change and nothing else. Preserve every other
      objective, step, block and field verbatim, including their ids (step_id,
      block ids, lesson_objective_id) so unchanged parts stay stable.
    - Keep full curriculum coverage: do not drop or renumber curriculum_objectives
      or lesson_plan_objectives unless the instruction explicitly asks you to.
    - If a highlighted part is given, scope the change to it; if it is empty, the
      instruction applies to the plan as a whole.
    - Output the COMPLETE revised plan as a valid SessionPlan (not a diff, not a
      fragment).
    - Keep every step's blocks complete for its kind: a core step with
      knowledge_type='concept' needs an 'explanation' block and no 'worked_example'; a
      core step with knowledge_type='procedure' or 'representation' needs ALL THREE of
      'explanation', 'worked_example' and 'practice'; an 'evaluation' step holds
      only 'practice' blocks. If your edit touches a core step, keep all its
      required blocks present.
    - prior_violations (if non-empty) are schema/context errors from your previous
      attempt — fix every one while still honouring the instruction.
    """

    current_session_plan = dspy.InputField(
        desc="The full current lesson plan (SessionPlan JSON) to revise."
    )
    highlighted_part = dspy.InputField(
        desc="The part the teacher highlighted (anchor ids + selected text); may be "
        "empty when the instruction applies to the whole plan."
    )
    revision_instruction = dspy.InputField(desc="The teacher's free-text change request.")
    conversation_summary = dspy.InputField(
        desc="Summary of earlier revision turns in this chat (empty on the first turn)."
    )
    prior_violations = dspy.InputField(
        desc="Validation errors from your previous attempt (empty on the first). Fix every one."
    )

    revised_session_plan: SessionPlan = dspy.OutputField(
        desc="The complete revised lesson plan — same schema, focused change applied."
    )
    change_summary: str = dspy.OutputField(
        desc=(
            "One short, plain-language sentence a CLASSROOM TEACHER would understand, "
            "describing the pedagogical change you made (e.g. 'Simplified the opening "
            "explanation' or 'Added an objective on checking the order is reasonable'). "
            "Write ONLY about what changed in the lesson. Never mention any internal "
            "field name, any internal id code (short tokens like lop04, step04, exp01), "
            "JSON, schema, formatting, validation, or any technical repair you did to "
            "satisfy the format — the teacher only cares about the teaching change."
        )
    )
