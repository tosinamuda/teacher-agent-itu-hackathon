Write a take-home revision pack for the lesson described in `inputs/curriculum.json`.
If `inputs/lesson-plan.json` is present, use it as evidence of how the lesson was
planned — prior knowledge, instructional emphasis, the work set, and the expected
depth of assessment.

The reader is **a junior secondary student aged about 11-13 who sat in this
lesson and is revising alone at home**, with no one to ask. The artefact is a
take-home revision pack.

## Output

Write `sections.xml` in the workspace root: one `<section>` per objective, in the
order the objectives are given.

```xml
<sections>
  <section objective="OBJECTIVE-ID">
    <title>A reader-facing title, not the objective restated</title>
    <block type="explanation">Markdown. Maths in LaTeX, written normally.</block>
    <block type="worked_example">A problem, then its solution worked through.</block>
    <practice>
      <prompt>The question as the learner reads it.</prompt>
      <answer>What the learner checks against.</answer>
      <worked-solution>Optional: the steps, where the answer alone will not teach.</worked-solution>
    </practice>
  </section>
</sections>
```

**XML, not JSON, because of the maths.** Backslashes are ordinary characters
here: write `\frac{22}{7}`, `\times`, `\pi` exactly as you would in a document.
Nothing needs doubling or escaping.

Two characters are the exception, because XML reserves them:

- write `&lt;` for a less-than sign (`x &lt; 5`)
- write `&amp;` for an ampersand

Everything else is literal.

### What each part is for

Carried from the study's own field definitions, so this arm is briefed in the
same terms as the other one:

- **`<title>`** — the reader-facing section title.
- **`<block type="explanation">`** — the principle, relationship, rule or
  representation the learner needs to review this objective. Concise and
  relational, *not* a summary of the topic.
- **`<block type="worked_example">`** — one or more worked or modelled examples:
  the problem, then its solution worked through, demonstrating the knowledge or
  procedure being taught.
- **`<practice>`** — what the learner *does*, each with the answer they check
  against.

Rules for the shape, all of them load-bearing:

- At least one `explanation` block and at least one `worked_example` block per
  section. `type` is one of those two words exactly.
- **`<prompt>` and `<answer>` are separate elements and must stay separate.**
  Never put the answer inside the prompt. The renderer places questions in the
  pack and collects answers into a "Check your work" section at the end, which
  is what makes the pack usable for self-testing.
- `objective` is the objective's `id` from `inputs/curriculum.json`.
- Write nothing outside `sections.xml`. No other files in the workspace root.

## Writing rules

These are the artefact requirements, carried verbatim from the study's shared
`artefact_spec` so that this arm is held to exactly what the other one is held
to. A comparison where one generator has requirements the other lacks measures
the prompt, not the generator.

1. Speak directly to the learner about the mathematics, never about the lesson as
   an event: no mention of the teacher or what happened in class, no lesson step
   or objective labels, no mention of where any material came from.
2. Write your own learner-facing section title; nothing in the inputs is a
   heading for the reader.
3. Teach the objective inside this lesson's topic and subtopic: examples and
   practice must be of the kind the topic names (a lesson on algebraic
   expressions practises on algebraic terms, not on bare numbers).
4. Every practice question must have its answer in the section — answers at the
   end, so the learner attempts first and then checks. (Here that is structural:
   `<prompt>` and `<answer>` are separate, and the renderer places them.)
5. Never refer to a picture, space, partner or answer key that is not in the pack
   itself.

And one rule of this arm's own: do not invent content the inputs do not support.
Where the plan records nothing for an objective, teach it from the curriculum
alone.

## Check before you finish

Call the **`check_sections`** tool. Fix anything it reports and call it again,
until it returns OK.

It checks the things that would otherwise reach a reader broken: that the file
parses, that every objective has exactly one section in order, that each section
has an explanation and a worked example, and that no answer has been written
inside its own prompt. Do not stop while it still reports a problem.
