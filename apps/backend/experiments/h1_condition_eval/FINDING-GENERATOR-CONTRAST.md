# The same plan, two generators: C1 converges, C0 does not

Runs `full-v3-deepseek` / `full-v7-deepseek` against `full-v3-enriched` / `full-v7-enriched`,
2026-08-24. Identical inputs — same frozen eval set, same conditions, same variants, three
draws, two Sonnet 4.6 passes. Only the generator differs.

## The direction replicates on all four dimensions

| rubric | gpt-oss C1−C0 | DeepSeek C1−C0 |
|---|---:|---:|
| Objective and curriculum alignment | +0.58 | +0.14 |
| **Taught-lesson alignment** | **+0.78** | **+0.39** |
| Scope and conceptual correctness | +0.36 | +0.14 |
| Student-facing clarity and usefulness | +0.31 | +0.14 |

Every sign agrees. Conditioning on her plan helps both models, so the direction is a
property of the treatment rather than of one model. Both put C1 ahead on 3 of 6 lessons.

## The smaller effect is not a worse C1 — it is a better C0

| rubric | gpt-oss C0 | gpt-oss C1 | DeepSeek C0 | DeepSeek C1 |
|---|---:|---:|---:|---:|
| Objective and curriculum alignment | 4.36 | 4.94 | **4.78** | 4.92 |
| **Taught-lesson alignment** | 3.36 | **4.14** | **3.75** | **4.14** |
| Scope and conceptual correctness | 3.94 | 4.31 | **4.67** | 4.81 |
| Student-facing clarity and usefulness | 4.31 | 4.61 | **4.86** | 5.00 |

On the endpoint the two C1s land on the same number — **4.14 and 4.14**. The C0s do not:
3.36 against 3.75. DeepSeek's advantage is spent before the plan arrives, and the plan
carries both models to the same place.

That is the finding. **The plan's measured value shrinks as the base model improves, not
because the plan does less but because the objectives-only baseline does more.** A study
that reports C1−C0 on one generator is reporting a difference that depends on which
generator sat underneath it.

## What does not replicate: the per-lesson pattern

| lesson | gpt-oss | DeepSeek |
|---|---:|---:|
| t2-w09 | +2.67 | +1.33 |
| t3-w02 | +0.00 | +0.00 |
| t3-w04 | +0.00 | +0.00 |
| t3-w05 | +0.50 | +1.00 |
| **t3-w06** | **−0.17** | **+0.17** |
| **t3-w09** | **+1.67** | **−0.17** |

Four of six agree in sign; two flip. **A prediction of ours is falsified here.** t3-w06 was
read as a lesson where C1 must lose because a text pack cannot represent a lesson taught
by drawing — a claim about the lesson, so it should have held for any model. DeepSeek puts
C1 ahead there. It was the model, not the lesson.

## The endpoint cannot reach significance at this n

| generator | per-lesson differences | non-zero pairs | two-sided p |
|---|---|---:|---:|
| gpt-oss | +2.67, 0, 0, +0.50, −0.17, +1.67 | 4 | 0.250 |
| DeepSeek | +1.33, 0, 0, +1.00, +0.17, −0.17 | 4 | 0.375 |

Wilcoxon discards ties, and both generators tie on the same two lessons — t3-w02 and
t3-w04, where C0 and C1 are both at ceiling. Four non-zero pairs put the floor at
**p = 0.125**, so no arrangement of these six lessons can reach 0.05. This is a limit of
the design, not of the result, and it does not move by re-running.

## Caveats that belong with the numbers

**Transport is confounded with model.** DeepSeek ran on `/responses` with JSONAdapter;
gpt-oss ran on chat completions with ChatAdapter. Each is the configuration that model
actually works under — forcing DeepSeek back to ChatAdapter costs it 13 recovered parse
failures we know are ours — but the comparison is model-plus-transport, not model alone.

**And this caveat carried a claim that was wrong.** It said mantle does not serve
`/responses`, so the confound could not be separated cheaply. That was asserted, never
tested, and it is false: mantle answers `POST /v1/responses` for gpt-oss with 200, and
returns a native `function_call {name: read_draft, arguments: {}}` for a sent tools list.
So the confound IS separable — gpt-oss can be run on the same transport as DeepSeek — and
the reason it has not been is a decision about disturbing a frozen arm, not a limit of the
endpoint. Measured 2026-08-24, after the claim had already been used to justify leaving
the confound in place.

What separating it would cost, also measured: mantle's `/responses` serves gpt-oss and
does native tool calls, but its structured output is broken there — `json_object` returns
prose in 1.0s, and `json_schema` hangs at 100s against a 1.1s control. So the move is not
free. It would mean ChatAdapter on `/responses` with native tools, keeping the field
markers gpt-oss has never once malformed in 306 loops while matching DeepSeek's transport
and tool channel. That is the shape of the experiment if it is ever run; it is not run
here.

A second correction rides on the first: DeepSeek's runs here did NOT use native tool
calls either, whatever this section originally implied. dspy gates tools on
`lm.supports_function_calling`, which litellm answers False for every id in this project,
so both arms were parsing tool calls out of text. See `FINDING-TOOL-CHANNEL.md`.

**One abandoned loop, inspected not waved through.** `full-v3-deepseek` lost a loop to a
parse error on `step-t3w02-04`, C1 repeat 1. The observer exists to catch silently
truncated sections, so the section was read: 13 blocks against siblings' 2 and 7, six
explanations and seven worked examples, no duplication. It is complete; the loop failed on
the turn that would have submitted it. Kept and judged rather than re-drawn, because
re-running until no loop fails is selection.

**Recall is not reported here.** DeepSeek's spread is much wider (0.27–1.0). Recall screens,
the rubric judges, and the coverage prompt flatters conditions that receive the note.

---

# Addendum, 2026-08-24: the same contrast on a defect-free harness

`full-v3-deepseek-native` / `full-v7-deepseek-native`. Same eval set, same conditions,
same two Sonnet passes. DeepSeek now on `/responses` with native tool calls and an
enforced json_schema — 153 loops, no abandonment, no parse failure of any kind.

## The direction holds a third time

| rubric | gpt-oss | DeepSeek, text tools | DeepSeek, native |
|---|---:|---:|---:|
| Objective and curriculum alignment | +0.58 | +0.14 | +0.17 |
| **Taught-lesson alignment** | **+0.78** | **+0.39** | **+0.50** |
| Scope and conceptual correctness | +0.36 | +0.14 | +0.39 |
| Student-facing clarity and usefulness | +0.31 | +0.14 | +0.19 |

Twelve positive signs out of twelve, across two models and three harnesses.

## The endpoint, for the first time, is unanimous

| harness | per-lesson C1 − C0 | non-zero | positive | p (two-sided) |
|---|---|---:|---:|---:|
| gpt-oss | +2.67, 0, 0, +0.50, **−0.17**, +1.67 | 4 | 3 | 0.250 |
| DeepSeek text | +1.33, 0, 0, +1.00, +0.17, **−0.17** | 4 | 3 | 0.375 |
| **DeepSeek native** | **+1.33, 0, +0.33, +0.50, +0.17, +0.67** | **5** | **5** | **0.0625** |

Every lesson that moves at all moves the same way, and 0.0625 is the FLOOR at five
non-zero pairs — the most evidence this design can produce. One-sided it is 0.031.

**This is not the study's endpoint and must not be reported as one.** The confirmatory
test is C1 vs C0 on the frozen generator, which is gpt-oss, and there it is p = 0.25.
This result comes from changing the generator AND the harness and then looking, which is
exactly the freedom that manufactures findings. It belongs in the writeup as a secondary
analysis with that stated, or not at all.

What it does support, honestly: the effect is REAL and its visibility depends on the
machinery. Three harnesses agree on direction on every dimension; they disagree on which
lessons reach significance, and the one with no known defects is the one where the
lessons stop disagreeing.

## The convergence claim, corrected

The original section said the two C1s "land on the same number — 4.14 and 4.14". On the
clean harness it is 4.14 against 4.22, so the identity was a coincidence of that run and
"the same number" was over-precise. The shape survives on two dimensions and fails on two:

| rubric | gpt-oss C0 | gpt-oss C1 | DeepSeek C0 | DeepSeek C1 |
|---|---:|---:|---:|---:|
| Objective | 4.36 | 4.94 | 4.83 | 5.00 |
| **Taught-lesson** | 3.36 | **4.14** | 3.72 | **4.22** |
| Scope | 3.94 | 4.31 | 4.58 | **4.97** |
| Clarity | 4.31 | 4.61 | 4.81 | **5.00** |

On objective and taught-lesson the C1s nearly meet while the C0s are half a point apart —
the plan closing a gap the baseline could not. On scope and clarity they do not meet:
DeepSeek's C1 is better by 0.66 and 0.39, so there the stronger model stays ahead and the
plan does not level it.

So the claim to carry forward is narrower than the original: **on the dimensions the plan
is about, a better baseline shrinks the plan's measured value. On correctness and
readability it does not** — those track the model.
