# What each condition sends, and what the pack is built from

```sh
uv run python -m experiments.h1_condition_eval.condition_trace
```

Writes to `../input-output/`: one PDF per lesson and condition — the exact payload
the model received, the sections it produced, and a layer-by-layer verdict — plus
`LAYER-ANALYSIS.pdf` across the cohort.

## Why layers

"C1 receives the lesson plan" is too coarse to explain a null result. A pack is
not one thing: a title, an explanation, worked examples, sometimes a figure, and
practice with answers. Each needs a *different kind* of input to be written from
the lesson rather than from what the model already knows about the topic — and
the conditions differ in which of those kinds they carry.

So each output layer is traced to the input layer that could have supplied it:

- **grounded** — that input layer is present
- **substituted** — it is absent and a different layer stood in
- **unsourced** — nothing in the input supplies it, so the model wrote it from
  its own knowledge of the topic

`unsourced` is not a defect report. A model with no worked examples in its input
still writes worked examples; they are simply not from the lesson that was taught.
Distinguishing those two is what H1 exists to measure.

## What it found

**The enacted-content layer reaches no condition from the plan.** `step_content`
is filled on 28/28 steps of the cohort and `include_step_content` is `False` in
C0, C1, C2 *and* C3. C2 and C3 recover content from the **note**, a different
artefact, under the field name `lesson_content`.

C1 therefore carries the lesson's *design* — position, Gagné event labels,
materials, entry behaviour, assessment — and none of its *substance*. Its whole
per-section pedagogical input is typically three event labels and one evaluation
question. Worked examples are `unsourced` in C1 exactly as in C0, and the
explanation is written from event labels rather than from what was explained.

Set work reaches only 8/17 units, and unevenly: 3/3 on t2-w09 and 4/5 on t3-w06,
but 0 on t3-w02, t3-w04 and t3-w09, where every question-shaped input the model
receives is the teacher's *evaluation*. That is the same content the raters see on
the reference sheet.

## Two things worth knowing before editing

**The payload is not reconstructed.** `assemble.py` calls
`ComposeSection.inputs`, the method the generator itself calls, so what the PDF
shows and what the model received cannot drift. Rebuilding the payload here would
give a document that is right the day it is written and quietly wrong after.

**Presence is probed over more than the payload.** Figures reach C2/C3 through a
composition tool, not the prompt — the payload carries only `figure_ref` and
`caption` — so availability is probed on the unit and the channel is labelled in
the table. The rendered fields stay exactly what the contract declares.
