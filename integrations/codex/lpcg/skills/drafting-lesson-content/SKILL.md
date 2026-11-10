---
name: drafting-lesson-content
description: Use when a teacher asks to write, create, draft, revise or change a lesson plan, lesson note, class test, revision note or slide deck for one of their own lessons with the Plan-to-Tutor (lpcg) tools. It covers finding the lesson, opening a draft, writing it one part at a time, and saving it for the teacher to review.
---
The `lpcg` MCP server writes lesson content for a teacher's own classes. You write a draft one
part at a time with its tools, and the teacher approves it in the app. Nothing you do reaches a
learner.

## Steps

1. **Find the lesson.** Call `find_lessons` with words from the teacher's request, such as a
   topic, a week or a class. If more than one lesson matches, ask which one. Do not guess. A
   lesson has a `lesson_id`, and a `plan_id` when it already has a plan.
2. **Pick the type.** Call `list_content_types`. Use a type whose `draftable` is true. Its
   `made_from` says which id `start_draft` takes: `session_id` is the lesson's `lesson_id`, and
   `plan_version_id` is the id of a plan version.
3. **Open the draft.** Call `start_draft` with the type and the id. To change a plan the lesson
   already has, also pass `content_id` with its `plan_id`. The result has the brief, the units
   to write a part for, the schema of each kind of part, and a `draft_id`.
4. **Read the lesson.** Call `read_lesson` with the `draft_id`.
5. **Read the skill for the type.** It says how to write the content. The skills are
   `drafting-lesson-plans`, `writing-lesson-notes`, `writing-class-tests`,
   `writing-revision-notes` (and `writing-learner-revision-notes` for one learner's note) and
   `writing-lesson-slides`.
6. **Write one part for each unit.** Call `add_part` with the `draft_id`, the `unit_id` and a
   part that matches the schema. The result lists the units still missing and, when none is
   missing, the issues that stop the draft being saved. Fix an issue with `revise_part`, and
   send the whole part with your change made.
7. **Save it.** When no unit is missing and there is no issue, call `submit_draft`. Tell the
   teacher the content is saved for their review, and that they approve it in the app. Never
   say it is approved.

## Keep the context small

`read_draft` returns the whole draft, and it is long. Name the fields you need, such as
`["parts", "missing", "issues"]`.

## When the teacher points at text

When the teacher quotes a line to change, call `locate_text` with the draft and the quoted
text. It returns the unit and the path of each field that holds it, and the line when the
field has several. Then `revise_part` for that unit. If the text is in no part, tell the
teacher, because the page may draw it from other details.

## Limits

- You reach only the teacher's own lessons. If a tool says a lesson is not one of their classes,
  say so and stop.
- A refusal from a tool says what to do instead. Do what it says.
- To show the content to the teacher, call `show_draft` or `show_content`.
