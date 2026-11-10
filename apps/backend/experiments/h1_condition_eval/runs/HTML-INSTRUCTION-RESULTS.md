# Does telling the model "NEVER HTML" stop it writing HTML?

**Yes — completely, once it is actually told.** Two pairs of runs, six lessons × C0–C3 × one
draw each, measured on the model's own tool-call arguments in the traces (`raw_markup.py`):

| generator | no format line on the wire | the line on the tools it writes through |
|---|---|---|
| deepseek-v4-flash, native tools | 27–56% of units wrote HTML (8 draws) | **0 of 68 units, 0 tags in 293,419 chars** |
| gpt-oss-120b, text-channel tools | 0% (every run) | 0% |

The 28-Aug "Markdown only, NEVER HTML" line on `DraftBlock.text` never reached generation: the
compose loop's `make_signature` contract never outputs a `DraftSection`, and the trace of every
generation run carries no `DraftSection`, no `DraftBlock`, and the word "HTML" nowhere. The text
goes through `add_block`, `revise_block`, `add_practice` and `revise_practice`, whose docstrings
are the only prompt the composer reads for it. With one sentence on those four (`d98df16f`),
verified on the provider-side schema dspy sends, DeepSeek stopped entirely.

The first pair of runs below was reported the same morning as "tested, no effect". It was
neither: the line was not on the wire, and those runs are baseline draws.

## What the baseline actually is — measured before reading the new runs

Eleven DeepSeek runs carry a trace. The share of units in which the model wrote any HTML:

| run | committed 24 Aug | units | with HTML |
|---|---|---:|---|
| t3w06-deepseek | 14:01 | 30 | **0%** |
| t3w06-deepseek-responses — JSONAdapter, `/responses` | 15:23 | 30 | **0%** |
| full-v3-deepseek | — | 102 | **0%** |
| full-v7-deepseek | 16:16 | 51 | **0%** |
| *native function calling switched on — `4869cfd8`* | *17:35* | | |
| full-v7-deepseek-b | 18:11 | 51 | 43% |
| full-v7-deepseek-native | 18:11 | 51 | 33% |
| full-v3-deepseek-native | 18:11 | 102 | 53% |
| t3w05-prism-declared | 25 Aug | 26 | 27% |
| t3w05-prism-objective | 25 Aug | 24 | 42% |
| c0c3-deepseek-native | 21:50 | 221 | 53% |
| c0c3-prism-objective | 25 Aug | 224 | 48% |

Four runs before the native-tools commit, all at 0% — one of them on JSONAdapter and
`/responses`. Seven after, 27–53%. Within a leaking run the HTML units interleave from the
second unit onward, per-unit chance around 45%; nothing spreads through the shared draft.

So the leak is neither the adapter nor the model's general habit. **DeepSeek writes rich text
into a function-call string argument as HTML, and writes the same text as markdown when it is
a completion.** gpt-oss takes its tool calls through the text channel and has never written a
tag in any run; it leaks the other way, bare LaTeX commands in prose.

## Decision rule, fixed before any instruction run is read

The native-tools baseline is seven runs at 27–53% of units. A single new run of ~70 units:

- **at or under 10%** — the instruction works on this generator;
- **27–53%** — it does not; the repair is carrying the surface alone;
- **between** — inconclusive at one draw, and a second draw is the next step.

## gpt-oss-120b, Bedrock mantle, ChatAdapter — no instruction on the wire (baseline draw)

24 cells, 68 loops, none abandoned.

| | HTML units | HTML tags | bare LaTeX / 1,000 chars |
|---|---|---:|---:|
| pre-instruction runs (full-v3, full-v7, clean-six) | 0% | 0 | 0.66, 0.67, 0.34 |
| **this draw** | **0%** | **0** | **0.71** |

Another baseline draw. gpt-oss has never written a tag in any run; its bare-LaTeX rate here,
109 commands in 153,651 characters, sits at the top of its 0.34–0.67 range.

## deepseek-v4-flash, `/responses`, native tools — no instruction on the wire (baseline draw)

24 cells, 71 loops, none abandoned.

| | units | with HTML | HTML tags | tags / 1,000 chars |
|---|---:|---|---:|---:|
| native-tools baseline, seven runs | 26–224 | 27–53% | — | 5.4–6.3 |
| **this draw** | **71** | **40 (56%)** | **1,875** | **7.15** |

An eighth native-tools baseline point, at the top of the range: 56% of units, 7.15 tags per
1,000 characters. No lesson came in under 25%; the two whose content invites tables and bolded
steps went to 83% (t2-w09) and 100% (t3-w09). This is what the harness produces with no format
instruction anywhere in the compose path.

Same run, other leak: bare LaTeX 0 in 262,143 characters, as in every DeepSeek run.

## The instruction runs — the line on the wire

Same six lessons × C0–C3 × one draw, commit `d98df16f`.

**deepseek-v4-flash, `/responses`, native tools:** 24 cells, 68 loops, none abandoned.

| | units | with HTML | HTML tags | tags / 1,000 chars | bare LaTeX |
|---|---:|---|---:|---:|---:|
| baseline, eight draws | 26–224 | 27–56% | — | 5.4–7.2 | 0–35 |
| **with the line** | **68** | **0 (0%)** | **0** | **0.00** | 2 |

Every lesson at zero. Against eight draws that never fell below 27% of units, a 0-of-68 draw
is not chance. By the rule above: the instruction works on this generator.

**gpt-oss-120b, mantle, ChatAdapter:** 24 cells, 69 loops, none abandoned.

| | HTML units | bare LaTeX / 1,000 chars |
|---|---|---:|
| baseline, four draws | 0% | 0.34, 0.66, 0.67, 0.71 |
| **with the line** | **0%** | **0.35** |

Nothing to test on HTML. On its own leak the draw sits at the bottom of the baseline range —
consistent with the `$LaTeX$` half of the line helping, not evidence of it at one draw.

## The two surfaces read the same packs differently

The tags reached the two instruments in different states, which is a finding in its own right:

| instrument | what it saw | evidence |
|---|---|---|
| LLM judge (144 H1 + 208 H2 ratings) | **literal** `<strong>` — `rater_packets._reader_ready` had no HTML step | this audit |
| human raters (40 published Part 1 sets) | **rendered** — the .docx pipeline round-trips markdown→HTML→docx through pandoc | 0 literal tags, 893 real Word tables |

So the same pack says different things depending on which instrument reads it. The LLM passes
are not a clean proxy for the human ones on anything presentation-sensitive, clarity above all.

`demote_html` never enters a math run: 7,496 runs across block text, captions and all three
practice fields, 0 changed. The .docx layer renders practice fields as OMML equations, so that
guarantee is load-bearing there, and is pinned as `TestMathIsNeverEntered`.

## What follows

The line stays: it removes the HTML at source on the generator that produced it, and it is
now part of the generation prompt, declared as such. `reader_ready` stays too — it is the
guarantee for every pack stored before the line, for gpt-oss's bare commands, and for the day
a model ignores it. `html_markers` and `raw_markup` make each of those a number per run.

And the method finding, which cost a false result to learn: **an instruction is tested on
the trace, not on the schema.** The schema said it; the wire did not carry it.
