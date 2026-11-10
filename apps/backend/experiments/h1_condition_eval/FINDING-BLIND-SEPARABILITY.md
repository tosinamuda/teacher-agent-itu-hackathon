# Finding: a blinded reader cannot separate C1 from C0

Two passes over the packs H1a was judged on (`runs/c0c3-worksheet`), cheapest first.
Reproduce with:

```bash
uv run python -m experiments.h1_condition_eval.blind_separability --surface
uv run python -m experiments.h1_condition_eval.blind_separability --read
```

Per-comparison verdicts, with the reason the reader gave for each, are written to
`runs/c0c3-worksheet/blind-separability.json`.

## Surface pass — no model

Vocabulary overlap between two packs of the same lesson and draw, against the overlap
between two **draws of the same arm**. The second is the floor: if re-running one condition
changes a pack as much as changing the condition does, there is no arm signal to find.

| Comparison | median overlap |
| --- | --- |
| C0 vs C1 | 0.440 |
| C1 vs C2 | 0.447 |
| C0 vs C2 | 0.394 |
| C2 vs C3 | 0.564 |
| **within C0 (floor)** | **0.505** |
| **within C1 (floor)** | **0.543** |
| **within C2 (floor)** | **0.582** |
| **within C3 (floor)** | **0.561** |

Two packs from the *same* arm share about half their vocabulary; two packs from *different*
arms share about 0.44. The whole between-arm effect is roughly 0.06–0.11 of overlap, sitting
on a redraw that moves the pack by about 0.45. Changing the condition does a little more
than re-rolling the same condition, and not much more.

Note also that C0-vs-C1 (0.440) and C1-vs-C2 (0.447) are the same to within noise, although
C2 adds the evidence step and C1 adds only plan fields. Surface vocabulary is not tracking
whatever separated the arms for the raters.

## Reader pass — forced choice, chance is 50%

Each pair anonymised, order fixed by a hash of lesson and draw, and the reader asked which
pack was written with more knowledge of how the lesson was actually taught. A discrimination
task rather than a rating, so it needs no scale and never touches the 0.45 judge floor —
a reader who cannot beat chance has answered the question directly.

| Comparison | correct | one-sided p |
| --- | --- | --- |
| **C0 vs C1** | **8/18 (44%)** | 0.76 |
| C0 vs C3 (positive control) | 12/18 (67%) | 0.12 |

**C0 versus C1 is at chance, slightly below it.** On the packs the study was judged on, a
blinded reader given both and asked to pick the one written with knowledge of the taught
lesson does no better than a coin.

## The caveat that keeps this from being the whole answer

**The positive control is weak.** C0 versus C3 — the arm that topped every rated dimension
and is the only one with no maths error — reaches 67%, in the right direction but not
significant at n = 18. So this pass is *consistent with* C1 and C0 being indistinguishable,
but it does not establish that the reader could have found a difference had one existed. A
stronger control, or more pairs, would be needed to separate "the arms are the same" from
"this reader is not sensitive enough".

**And this is an LLM reader, not the expert-teacher instrument.** It is a screen. It does
not replace a human blind pass, and no rating in the thesis should rest on it.

## The methodological observation, which may matter more

The reader was explicitly offered `neither` and told that a forced guess would be
indistinguishable from a real judgement in the tally.

**It used `neither` zero times out of 36.**

Yet on C0 versus C1 it was at chance. So it produced a confident distinguishing reason for
every pair while detecting nothing — and the reasons given for wrong answers read exactly
like the reasons given for right ones:

> *[wrong]* "Pack A follows a detailed lesson-style sequence with specific worked examples
> and practice questions, showing knowledge of the teacher's actual plan."

> *[right]* "Pack A follows a specific lesson flow with explanatory sections, worked
> examples, and concrete practice questions matching a teacher-planned lesson."

A rater asked to justify a choice will produce a justification whether or not they detected
anything. That is worth carrying into how the human rating is read, and it is the same
shape as the measured 0.45 re-rate movement on identical prose.

## What this adds to the null

Read beside the delivery audit, the two findings fit together without either being the whole
story:

- [`FINDING-C1-DELIVERY.md`](FINDING-C1-DELIVERY.md) — C1 carried its manipulation
  incompletely and unevenly: three keys on every call, `student_tasks` on four of seventeen.
- Here — the packs that resulted are, to a blinded reader, not separable from C0.

So the null is not mysterious. A manipulation that arrived partially produced output that
does not read as different. What this does **not** establish is the counterfactual: whether
a fully delivered C1 would have separated. That question needs the delivery fix first
(sprint 18), then a fresh run and a fresh blind pass — in that order.
