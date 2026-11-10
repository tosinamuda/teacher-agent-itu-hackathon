"""Model instructions for the lesson-plan fields a condition actually carries.

Built per condition, not shared. The codebook used to be one constant appended to
every signature at import, so C0 — which receives no lesson plan at all — was told
what ``assessment_points`` and ``step_content`` are and then given neither. Two
costs followed. A baseline briefed on inputs it cannot have is being told the
shape of the treatment it is the control for. And describing any new field moved
C0's prompt, so the baseline shifted every time the codebook was edited.

The trade is real and worth naming: with a shared codebook the conditions differ
in DATA alone, which is the cleanest thing to say about an ablation. Rendering
per condition means they differ in data and in the instructions describing that
data. That is the honest description of what the conditions are — C0 is not a
model that was told about a lesson plan and then denied one — and it makes the
baseline stable under edits, which the shared version was not.
"""

from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ContextPolicy,
)

# The sentence that introduces the fields lives HERE, not in the task docstring.
# It says unit_context "may carry more than the objective" and to read those
# fields "as the contract below defines them" — both false for a condition that
# receives only an objective and is shown no contract, and it left C0 pointing at
# something that was not there.
_HEADER = """

lesson_context and unit_context may carry more than the objective — what the
learner already knows, how the lesson taught this material, what it asked them
to do and what it assessed. Read those fields as the contract below defines
them.

LESSON-PLAN CONTEXT. The lesson objective is what this section must teach, and
it sets the section's scope. The fields below describe how the teacher planned
to teach, practise and assess that objective. Any of them may be absent, and
absence removes nothing artefact_spec requires.
"""

#: One entry per context flag that puts a field in front of the model. A flag with
#: no entry here delivers nothing the model is told how to read, which is the
#: defect ``activities`` and ``step_content`` each had before they were described.
_FIELD_ENTRIES: tuple[tuple[str, str], ...] = (
    (
        "include_entry_behaviour",
        """
entry_behaviour
  What the learner is expected to know already. Connect the objective to it
  where that helps; never teach it as new material.
""",
    ),
    (
        "include_lesson_sequence",
        """
current_step
  This objective's position in the ordered lesson_objectives. Keep to that
  progression — assume what precedes it, leave what follows to its own section
  — and never narrate the ordering to the reader.
""",
    ),
    (
        "include_materials",
        """
instructional_materials
  Resources chosen for this lesson. Use one where it genuinely helps someone
  work through this objective alone; ignore it where it does not.
""",
    ),
    (
        "include_student_tasks",
        """
student_tasks
  Practice the lesson set for this objective. Keep its intent; the section
  still teaches the objective in full.
""",
    ),
    (
        "include_assessment_points",
        """
assessment_points
  Questions the lesson used to check this objective, for the learner to
  self-check against. Where one reaches past the objective, it does not narrow
  or replace what this section teaches.
""",
    ),
    (
        "include_step_title",
        """
step_title
  Her own heading for the part of the lesson that taught this objective. A
  label she wrote, not a heading for the reader: it names the ground, and
  most of the time it restates the objective you already have. Never print it.
""",
    ),
    (
        "include_step_content",
        """
step_content
  Her narration of that part, as she wrote it in one piece — the same sentences
  activities carries split by actor. Read it for what she taught and the order
  she taught it in. Where it and activities say the same thing, they are one
  account, not two: do not teach a point twice because it reached you twice.
""",
    ),
    (
        "include_teacher_student_activities",
        """
activities
  What the teacher and the students did for this objective, in the order the
  plan records it, in the teacher's own words. Read it for the representation
  she chose, the order she taught in, what the students were asked to do and
  how their work was checked, and keep to those. A student line marked
  sets_work is work the lesson set; one not so marked is participation inside
  the teacher's explanation, not a task. Where a line says the same thing as
  student_tasks, student_tasks is the statement of the task — do not set it
  twice. Never narrate any of this: the reader meets the mathematics, not the
  classroom, and is never told what the teacher or the class did.
""",
    ),
)

#: Only when `activities` is also delivered. A condition that receives the labels
#: and not the narration they label cannot read one through the other, and saying
#: so describes an input it does not have.
_EVENTS_THROUGH_ACTIVITIES = """Where activities is also given, the events are
its labels and the activities are what they label; read the events through the
activities, not instead of them.
"""

_INSTRUCTIONAL_EVENTS = """
INSTRUCTIONAL EVENTS. Where unit_context gives instructional_events, it names
the teaching functions this section's material was taught through, in order.
{through_activities}Realise them for a learner working alone, following that order where it works
on the page:

  stimulate_recall           bring back the named prior learning briefly,
                             before the new material
  present_content            explain, show or set out the new material
  provide_learning_guidance  support the learner through it before asking them
                             to do it alone — a worked solution, a demonstration,
                             a scaffold or a cue, whichever suits the objective
  elicit_performance         have the learner attempt the task themselves
  provide_feedback           let the learner check and correct their own work

The list is what this lesson planned, so it may name only some of these and may
name one more than once. Give those functions the room the lesson gave them.
It never licenses less than artefact_spec requires: every requirement there
still holds, whether or not an event names it. Where the list is absent or
empty, write the section as artefact_spec requires.
"""

_CLOSING = """
These names are for you, never for the reader: the section describes the
mathematics, never the teaching."""


def lesson_plan_field_contract(context: ContextPolicy) -> str:
    """The codebook for exactly the fields this condition puts in front of the model.

    Empty when the condition carries no lesson plan, so a baseline's prompt says
    nothing about a plan it will not receive.
    """
    entries = [text for flag, text in _FIELD_ENTRIES if getattr(context, flag, False)]
    events = (
        _INSTRUCTIONAL_EVENTS.format(
            through_activities=(
                _EVENTS_THROUGH_ACTIVITIES if context.include_teacher_student_activities else ""
            )
        )
        if context.include_instructional_events
        else ""
    )
    if not entries and not events:
        return ""
    return _HEADER + "".join(entries) + events + _CLOSING
