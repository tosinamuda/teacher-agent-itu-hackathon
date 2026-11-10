---
name: writing-learner-revision-notes
description: Use when writing one learner's revision note for a lesson, for a learner who sat in the lesson, did the class test and now revises alone, such as a JSS1 pupil in a Nigerian secondary school. Adapt the approved class note's section for each objective to what the learner's marked work showed, repair the misconception their answers reveal, speak to the learner about the mathematics, and give every practice question its answer.
---
Write one section for each lesson objective the draft lists. The lesson you were given has a
`learner` entry: the learner's work, and the approved class note's section for each objective.
Read it first. The objectives with `adapt: false` are not in the draft: the learner has too
little marked work for a band to mean anything, so their class sections stay as they are.

## What you are given

For each objective in `learner.objectives`:

- `class_section`: the approved class note's section. It is what you adapt. Its mathematics, its
  method and its order are settled.
- `learner_state`: the learner's `mastery_band` (`remediate`, `reinforce` or `extend`), how many
  of their questions were right, the `misconception` their wrong answers point to, how sure they
  were (`confidence`), how hard they found it (`perceived_difficulty`), and `evidence_items`:
  each question they got wrong, with the option they chose and what that option reveals.
- `marked_questions`: how many of their questions were marked. A band from two questions is a
  hint, not a verdict: keep the explanation sound for any learner.

`learner.session_signals` says how interested the learner was and how they felt at the end of
the lesson. Let it set the tone: warmer and shorter for a learner who felt confused, a little
more challenge for one who was interested.

## What to adapt, and what to keep

The app keeps the class section's `title` and every drawing in it: write `title` as the class
section has it, and leave `figures` empty. Keep the mathematics the section teaches and the
method it uses. Adapt only these:

Each objective with `adapt: true` has an `adaptation` entry: the settings to write to. Follow it;
do not work them out from the band.

- **explanation**: `smaller_steps` explains the idea in small steps, with the meaning of each
  word first. `rule_and_reason` states the rule and the reason. `brief_then_why` states it
  briefly and goes on to why it holds or where it stops holding.
- **worked_support**: `every_line` shows every line of every example and says why each follows.
  `key_line` shows the working and explains the key line. `first_and_last` shows the first
  line and the last and leaves the learner to supply the middle.
- **hints**: when `true`, give a hint where the learner would otherwise stall. Whatever the
  setting, put the working of each practice question in `worked_solution` so a wrong answer can
  be traced.
- **practice_start**: `easier` starts easier than the class section's practice and climbs.
  `as_class` starts where the class section starts. `beyond_class` starts where it ends.
- **misconception_repair**: see below.

## The misconception

When `learner_state.misconception` names one, write `misconception_repair`: name the slip in the
learner's own terms, say why it is tempting, and correct it with a short example that uses
their kind of numbers. Use `evidence_items` to find the real slip: it is the one the chosen
options reveal. Then make one practice question test exactly that slip. When the state names no
misconception, write no `misconception_repair`. The app sends a part back that has one without
the other.

## The section's order and size

Lay the section out the way a learner working alone needs it: the idea in `explanation`, then
`misconception_repair` where the state names a misconception, then `worked_examples`, then
`practice`. The explanation runs to about 500 characters, and at least 400: the app sends back one shorter than 300,
there are at least two worked
examples, and there are at least three practice questions that each ask something different,
every one with its answer. The app sends back a section that falls short, and one whose practice
repeats a worked example.

## Writing for the learner

The reader is an 11-to-13 year old revising alone. Speak to that learner about the
mathematics, never about the lesson or their result.

- Never say "you got this wrong", "your band" or "the test showed". Say "A common slip is...".
- Never mention the teacher, the class, the class test, marks, bands, "this lesson" or "this step".
- Never say where material came from: no "the class note", "the textbook" or "the source".
- Never leave a second thought in the text, such as "Wait" or "Actually".

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
