---
name: writing-revision-notes
description: Use when creating a revision note, revision pack or take-home revision for a lesson, for a learner who sat in the lesson and now revises alone, such as a JSS1 pupil in a Nigerian secondary school. Write one section per lesson objective from what the lesson taught, speak to the learner about the mathematics, work examples line by line, and give every practice question its answer.
---
Write one section for each lesson objective. These rules apply to every part.

## What the lesson gives you

The lesson's approved lesson note and its plan say what this class was taught for the
objective. Teach from them.

- Teach only what the lesson's material supports, inside the lesson's topic and subtopic.
  Standard definitions, explanations and extra practice on that topic are welcome.
- Never invent a fact about the world, or a reason to explain the numbers in an example.
  Made-up numbers in an example or a question are fine.
- What the lesson note states is settled. Never correct it towards a more general or more
  advanced form.
- Keep the representation, method and order the lesson used. A procedure the lesson
  taught is kept step for step; never replace it with one of your own.
- Teach the objective in full. Assume what an earlier objective taught; leave what a later
  objective teaches to its own section.
- Connect to what the learner already knew before the lesson; never teach it as new.
- The work the lesson set for this objective shows the kind of practice to give. Keep its
  intent, and do not set the same task twice.
- The lesson's evaluation questions show what the learner must be able to do. Never let
  one narrow what the section teaches.

## The section's order

Lay the section out the way a learner working alone needs it:

1. Bring back the earlier idea the objective builds on, briefly, where the lesson did.
2. State the new mathematics in `explanation`, in full: the rule or idea, why it holds, one
   short instance with real numbers, and the slip learners most often make with it. Write
   about 500 characters, three or four full sentences. This is a minimum, not a limit: the app
   sends back an explanation shorter than 300 characters, so write at least 400.
3. Guide the learner through it in `worked_examples` before asking them to do it alone: at
   least two, the second harder than the first.
4. Give `practice` for the learner to attempt: at least three questions, each asking
   something different, from the easiest to the hardest. The app sends back fewer than three,
   or two that are the same.
5. Give each practice question the answer the learner checks against afterwards, and a
   `worked_solution` for every question that takes more than one step.

## Writing for the learner

The reader is an 11-to-13 year old revising alone. Speak to that learner about the
mathematics, never about the lesson.

- Write "To add two fractions with the same denominator, add the numerators and keep the
  denominator.", never "In class, the teacher showed us how to add fractions."
- Never mention the teacher, the class, "this lesson", "this step" or "pupils will".
- Never print an objective label, a step title or a planning term such as "evaluation" or
  "worked example step".
- Never say where any material came from: no "the lesson note", "the textbook", "the
  source" or "the evidence".
- Numbered steps inside a method and instructions to the reader ("Try these on your own")
  are how a method is taught. Use them.
- Write the `title` yourself, for the learner: "Adding fractions with the same
  denominator", never "Objective 2" or a step's heading copied over.
- Never refer to a picture, a space to write in, a partner or an answer key that the note
  does not hold.

## Correctness

- Every statement, worked answer and practice answer must be mathematically correct.
  Check each one before you write it.
- Test every rule you state on two numbers of your own before you write it. A rule that
  fails on either is wrong: for example, never state that a larger unit name, or a leading
  digit, decides which number is larger; compare by the number of digits first, then digit
  by digit from the left.
- Write the corrected version only. Never leave a second thought in the text, such as
  "Wait" or "Actually, we made a mistake".
- No table, number or example in a section may contradict another in it.
- A worked answer follows from its own working.

## Format and setting

- Write markdown: **bold**, *italic*, `-` lists, and maths in LaTeX between `$` signs.
  Never write HTML: a `<strong>` tag reaches the learner as the characters `<strong>`.
- Put every formula and every line of working between `$` signs. A line of working without
  them reaches the learner as raw code such as `\text{HCF}=2^{2}\times5`.
- Start a new line by starting a new line. Never type `\n` or `\;` as text: the learner
  would read those characters.
- A practice `question` is the question and nothing before it: no heading such as
  `### Exercise`.
- Keep numbers and language right for the class's grade.
- Use Nigerian contexts and naira for money. Use the names the class is taught, such as
  BODMAS for the order of operations.

## What the app checks

The app refuses a part that would show as code: a `working` line that is not a formula between
`$` signs, or is only a sentence in `\text{}`; a `$` that is never closed; `\n`, `\t` or `\;`
typed as text outside a formula. The refusal names the part and the line. Rewrite that line,
keep the rest as it is, and send the part again.

A lesson whose working is not a calculation, such as naming the kind of word each word is,
writes each `working` line as plain text: the app asks for `$` signs only where the lesson
is mathematics. Never put plain words in `\text{}` to look like a formula.

## When a part needs more

- Before you write `worked_examples` or `practice`, read
  `references/worked-examples-and-practice.md`.
- Before you write `figures`, or any text that depends on a drawing, a shape, an angle or a
  construction, read `references/figures.md`.

## Check before you submit

Once every part is written, the app checks the draft for the faults that a program can check: a section with too short an explanation, too few worked examples or practice questions, a practice question repeated or copied from a worked example, a false rule for comparing sizes, a wrong rounding, and a second thought left in the text. The faults come back in the result of the last part you add, and again if you submit; a draft that has any is not saved, so mend each with `revise_part`.
