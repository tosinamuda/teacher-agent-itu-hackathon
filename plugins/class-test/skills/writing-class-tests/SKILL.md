---
name: writing-class-tests
description: Use when creating a class test, exit ticket or multiple-choice questions on a lesson objective for a Nigerian secondary school class such as JSS1. Write two questions for each objective, each with four options keyed A-D, one correct option, a misconception code for each wrong option, and a difficulty, and check every question against what the lesson taught.
---
Write the test for one lesson objective at a time. The class takes it after the lesson. These
rules apply to every question.

## What the lesson taught

The lesson is the approved lesson note, or the plan's steps when the note is not approved.

- Test the objective only. Use nothing from another objective of the lesson, and nothing from a
  later lesson.
- Judge every option by the lesson's own definitions and examples, not by a definition from
  elsewhere. If the lesson defines an improper fraction as one whose numerator is greater than
  or equal to its denominator, then $\frac{4}{4}$ is improper.
- Use the method and the names the lesson uses, such as BODMAS for the order of operations.

## Each question

- Write two questions for the objective.
- Write a stem that asks one thing and can be answered from the stem and the options alone.
  Write "Which of these is an improper fraction?", never "Answer the question on fractions."
- Print every number the question is about in the stem. To order or compare numbers, name them
  in the stem and let the options be the possible answers: "Arrange 36 million, 3.6 billion and
  360 million from smallest to largest." Never write "Arrange the following numbers" or "Which
  number is larger?" with the numbers only inside the options. The app sends such a question
  back.
- Never put a lettered list of your own in a stem. The options are the only A-D list.
- A question is text only. Never refer to a diagram, figure or table that the stem does not
  hold.
- Give exactly four options. In the part, the options group has the lowercase fields a, b, c
  and d; `correct_option` and each distractor's `option` use the capitals A, B, C and D.
- Give each question a difficulty: easy, medium or hard.
- Never ask the same question twice. The two questions test different parts of the objective,
  not the same skill with other numbers.
- Test at the size the objective names. If it names billions and trillions, at least one
  question for it uses numbers that large; a set of four-digit numbers does not test it. The
  app sends such a set back.
- Never teach or test a comparison rule as "the larger unit wins" or "the larger leading digit
  wins": 0.08 trillion is less than 800 billion. Convert both numbers to the same unit, or
  write them in full, then compare digit by digit from the left.
- Test the objective's own skill. Do not set division, percentage or other arithmetic unless
  the objective names it.
- Mark a question medium at least when it mixes sizes (millions with billions) or writes a size
  as a decimal (0.055 trillion). The app raises an "easy" label that these stems cannot have.
- Set the difficulty by the work: easy is one step in one unit; medium needs a conversion
  between units or two steps; hard needs several steps.
- Write numbers, units and amounts as plain text: 3,600 million, 0.36 trillion, ₦435.01 billion.
  Use $ signs only for maths that needs a symbol, such as a fraction or a power, and never
  around a plain number, a unit or an amount. Never write \( \) or \text.
- An option is the answer and nothing else: no reason, no "because".

## The classroom

- Keep numbers and language right for the class's grade.
- Use Nigerian contexts, and naira where money is involved.

## When a part needs more

- Before you choose the correct option, read `references/answer-key.md`.
- Before you write a wrong option or a misconception code, read `references/distractors.md`.

## Check before you submit

Once every part is written, the app checks the draft for the faults that a program can check: a question whose options repeat or whose key is not one of A to D, a stem that leaves out the numbers it asks about, a wrong option without a snake_case misconception code, two questions with one stem, and an objective that names a size no question reaches. The faults come back in the result of the last part you add, and again if you submit; a draft that has any is not saved, so mend each with `revise_part`.
