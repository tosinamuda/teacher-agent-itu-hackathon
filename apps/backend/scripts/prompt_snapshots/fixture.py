"""The fixed lesson a prompt snapshot is rendered from.

Synthetic on purpose. The frozen eval set is the teacher's real work and re-freezing it is
a deliberate act; a snapshot that moved whenever that file moved would report dataset
churn as a prompt change. This plan exists to make the CONDITIONS legible, so it carries
every field some condition gates on and nothing a condition would not read:

* two lesson objectives, and two core steps that map one-to-one onto them, so the
  objective-unit and step-unit projections produce the same count and differ only in
  content;
* an evaluation step whose questions carry ``lesson_objective_id``, which is the only way
  ``assessment_points`` reaches a unit;
* activities phrased so the Gagne coder emits a known sequence — "explains" is
  present_content, "solves" by a student is elicit_performance;
* a practice block per core step, which is what ``student_tasks`` reads;
* a note per core step, which is what the retrieval conditions turn into evidence;
* ``entry_behaviour``, ``instructional_materials`` and a ``theme``, each gated separately.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    AnswerEvidenceItem,
    ObjectiveLearnerState,
    SessionSignals,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from app.shared.session_plan_view import SessionPlanView

FIRST_OBJECTIVE_ID = "obj-perimeter-rectangle"
SECOND_OBJECTIVE_ID = "obj-perimeter-triangle"

SESSION_PLAN = SessionPlanView.model_validate(
    {
        "subject": "Mathematics",
        "track": "core",
        "grade": "JSS1",
        "term": "Third Term",
        "week": 3,
        "topic": "Perimeter of plane shapes",
        "subtopic": "Perimeter of rectangles and triangles",
        "theme": "Mensuration and geometry",
        "entry_behaviour": [
            "Learners can add and multiply whole numbers.",
            "Learners can measure a straight line with a ruler.",
        ],
        "instructional_materials": ["Metre rule", "Cardboard rectangles and triangles"],
        "references": ["MAN Mathematics for Junior Secondary Schools 1, chapter 12"],
        "lesson_plan_objectives": [
            {
                "lesson_objective_id": FIRST_OBJECTIVE_ID,
                "objective_text": "Calculate the perimeter of a rectangle.",
            },
            {
                "lesson_objective_id": SECOND_OBJECTIVE_ID,
                "objective_text": "Calculate the perimeter of a triangle.",
            },
        ],
        "steps": [
            {
                "step_id": "step-1",
                "step_kind": "core",
                "lesson_objective_id": FIRST_OBJECTIVE_ID,
                "instructional_type": "explain_then_practise",
                "title": "STEP 1:",
                "content": "Teacher explains perimeter then sets two questions.",
                "estimated_minutes": 15,
                "activities": [
                    {"who": "teacher", "what": "Explains that perimeter is the distance round"},
                    {"who": "student", "what": "Solves two questions in their notes"},
                ],
                "note": (
                    "Perimeter is the total distance round a closed shape.\n"
                    "For a rectangle of length L and breadth B, perimeter = 2(L + B).\n"
                    "Example: L = 8 cm, B = 5 cm, perimeter = 2(8 + 5) = 26 cm."
                ),
                "blocks": [
                    {
                        "type": "practice",
                        "question": "Find the perimeter of a rectangle 7 cm by 4 cm.",
                    }
                ],
            },
            {
                "step_id": "step-2",
                "step_kind": "core",
                "lesson_objective_id": SECOND_OBJECTIVE_ID,
                "instructional_type": "explain_then_practise",
                "title": "Step II",
                "content": "Teacher works a triangle example on the board.",
                "estimated_minutes": 15,
                "activities": [
                    {"who": "teacher", "what": "Draws a triangle and labels its three sides"},
                    {"who": "student", "what": "Calculates the perimeter of the drawn triangle"},
                ],
                "note": (
                    "The perimeter of a triangle is the sum of its three sides.\n"
                    "Example: sides 3 cm, 4 cm and 5 cm give 3 + 4 + 5 = 12 cm."
                ),
                "blocks": [
                    {
                        "type": "practice",
                        "question": "A triangle has sides 6 cm, 6 cm and 9 cm. Find its perimeter.",
                    }
                ],
            },
            {
                "step_id": "step-eval",
                "step_kind": "evaluation",
                "blocks": [
                    {
                        "type": "question",
                        "lesson_objective_id": FIRST_OBJECTIVE_ID,
                        "question": "Find the perimeter of a rectangle 10 cm by 3 cm.",
                    },
                    {
                        "type": "question",
                        "lesson_objective_id": SECOND_OBJECTIVE_ID,
                        "question": "Find the perimeter of a triangle with sides 5 cm, 5 cm, 8 cm.",
                    },
                ],
            },
        ],
    }
)

LESSON_SOURCES = LessonSources.unresolved(SESSION_PLAN.references)

BASE_SECTION = ReviewPackSection(
    section_id="sec-1",
    title="Distance round a rectangle",
    lesson_objective_id=FIRST_OBJECTIVE_ID,
    blocks=[
        ReviewPackBlock(
            block_id="blk-1",
            block_type="explanation",
            lesson_objective_id=FIRST_OBJECTIVE_ID,
            text="The perimeter of a rectangle is 2 x (length + breadth).",
            source_refs=["the lesson note"],
        ),
        ReviewPackBlock(
            block_id="blk-2",
            block_type="worked_example",
            lesson_objective_id=FIRST_OBJECTIVE_ID,
            text="A rectangle 8 cm by 5 cm has perimeter 2 x (8 + 5) = 26 cm.",
            source_refs=["the lesson note"],
        ),
    ],
    practice=[
        ReviewPackPracticeItem(
            item_id="itm-1",
            prompt="Find the perimeter of a rectangle 7 cm by 4 cm.",
            answer="22 cm",
            worked_solution="2 x (7 + 4) = 2 x 11 = 22 cm.",
        )
    ],
    source_refs=["the lesson note"],
)

LEARNER_STATE = ObjectiveLearnerState(
    lesson_objective_id=FIRST_OBJECTIVE_ID,
    mastery_band="remediate",
    mastery="1 of 3 diagnostic questions correct",
    confidence="a little sure (2/5)",
    perceived_difficulty="very difficult (5/5)",
    misconception="Adds only the two labelled sides of a rectangle.",
    evidence_items=[
        AnswerEvidenceItem(
            question="Find the perimeter of a rectangle 10 cm by 3 cm.",
            options={"A": "13 cm", "B": "26 cm", "C": "30 cm"},
            correct_option="B",
            student_choice="A",
            chosen_option_misconception="Adds length and breadth once instead of twice.",
        )
    ],
)

SESSION_SIGNALS = SessionSignals(
    interest="quite interested (4/5)",
    end_of_lesson_feeling="a bit lost (2/5)",
)
