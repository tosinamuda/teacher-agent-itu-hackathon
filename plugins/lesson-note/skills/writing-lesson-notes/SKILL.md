---
name: writing-lesson-notes
description: Use when writing the lesson note for a lesson plan step, or notes a teacher teaches from, for a Nigerian secondary school class such as JSS1. Say what to explain and in what order, work the examples line by line, give questions for the class with their expected answers, and end with what stays on the board.
---
Write the note for one plan step at a time. It is what the teacher teaches that step from: the
mathematics to explain, in the order to explain it, with worked examples and questions to ask
the class. These rules apply to every part.

## The teacher's material

Start from the material the teacher supplied. It is the teacher's own teaching. A lesson plan step
may carry blocks: explanations, worked examples with their working and figures, and practice.

- Keep what the material teaches, in its order, correct as it is. Expand around it.
- Keep a procedure the material gives, step for step; never replace it with one of your own.
- Where the material gives no blocks for a step, write from its title, objective and activities.
- Keep the evaluation step's questions for the evaluation: never use them as examples or
  classwork in another step.

## The step's type

Shape the note to the step, as the plan types it with step_kind, kc_type and
instructional_type. Each kind of step carries its own events of instruction.

- **Intro** (step_kind intro): recall what the lesson builds on. Give the earlier ideas as
  teaching points, each stated, then a few quick questions on them with their answers. Teach
  nothing new.
- **Concept** (kc_type concept): state each definition, property and fact in full, with
  instances of the idea, and a list, table or labelled figure where it helps. Give a worked
  calculation only if the objective asks for one.
- **Procedure** (kc_type procedure): state the rule briefly, then work at least three graded
  examples, from simple to harder.
- **Evaluation** (instructional_type check): the questions the class answers, each with its
  expected answer. The teaching points name what the questions check.

Teach only the step's objective. Use nothing a later step of the lesson teaches, and nothing
from a later lesson. Do not restate the objective or the step's title: the plan carries them.

## How much to write

A note a teacher can teach from is not a list of headings. Each part carries the mathematics.

- `teaching_points`: three to six for a concept or procedure step, two to four for an intro or
  evaluation step. Each is a full statement of one thing to explain, in the order to explain it,
  with the numbers or symbols themselves. "Place value" is a heading, not a teaching point;
  "In 3,600,000,000 the digit 3 stands for 3 billion because it is in the billions place" is.
- `questions_for_the_class`: two to four questions the teacher asks, each with its expected
  answer, at the size the objective names.
- `on_the_board`: one or two lines the class copies and keeps, such as the rule or the
  definition in its shortest correct form.
- A note that says no more than "Explain place value" or that repeats the plan's activities
  fails the teacher. The app does not check this; you do.

## Writing the teaching points

- Never state a comparison rule as "the number with the larger unit is larger" or "the larger
  leading digit decides": 0.08 trillion is less than 800 billion. Teach the rule that holds:
  convert both numbers to the same unit, or write them in full, then compare digit by digit from
  the left, and a number with more digits is larger when neither starts with zero.

State the mathematics itself. A short direction to the teacher is fine only when it carries
the mathematics too: "Remind the class that 1 billion is 1,000 million, so 3,600 million is
3.6 billion."

- Never describe the lesson as an event: no "in this step", no "pupils will".
- A definition is given in full, never only referred to.

## The classroom

- Keep numbers and language right for the class's grade.
- Use Nigerian contexts, and naira where money is involved.
- Use the names the class is taught, such as BODMAS for the order of operations.

## What the app checks

The app refuses a part that would show as code: a `working` line that is not a formula between
`$` signs, or is only a sentence in `\text{}`; a `$` that is never closed; `\n`, `\t` or `\;`
typed as text outside a formula. The refusal names the part and the line. Rewrite that line,
keep the rest as it is, and send the part again.

A lesson whose working is not a calculation, such as naming the kind of word each word is,
writes each `working` line as plain text: the app asks for `$` signs only where the lesson
is mathematics. Never put plain words in `\text{}` to look like a formula.

## The questions for the class

- Ask only what this note taught. A question on something no teaching point or example covers
  tests the class on what it was not taught, such as "seconds in ten years" or "write a number
  in words" in a lesson on comparing sizes.
- Give the question and its expected answer in the same size and form the note teaches.
- Never leave a second thought in the text: no "Wait" or "Actually, we made a mistake". Work it
  out first and write only the corrected version. The app sends such a step back.
- Never name a record id from the plan, such as ch01-b044-i01. Say "the textbook" instead.

## When a part needs more

- Before you write a worked example, a solution or an answer, read
  `references/worked-solutions.md`.
- Before you write a part that may carry a figure, a diagram, a shape, an angle or a
  construction, read `references/figures.md`.

## Check before you submit

Once every part is written, the app checks the draft for the faults that a program can check: a step with too little text to teach from, a second thought left in the text, a false rule for comparing sizes, a wrong rounding, a question asked in two steps, and a note that asks the class to round or estimate without having taught it. The faults come back in the result of the last part you add, and again if you submit; a draft that has any is not saved, so mend each with `revise_part`.
