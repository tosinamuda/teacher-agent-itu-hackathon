# The harness: which one ships, and why — 2026-08-18

A **harness** is what produced a pack, other than the condition and the model. Four things
vary and each has changed a result on its own — the generator module, the agent loop, the
contract family it renders, and how evidence reaches it — so `harness.py` records all four
plus the library version, and refuses a run that does not declare them.

This file settles which one the study and the product both use.

## The decision

**`ComposeSection` over `ReActV2`, leveled contracts, evidence in the prompt.** The
`compose-v2` arm. Production wires it in
[`generation_wiring.py`](../../src/app/domains/artefacts/types/post_class_review_pack/infrastructure/generation_wiring.py);
runs declare it with `--generator compose-v2 --signatures leveled`.

## Why — and it is not "it scored best"

**The bake-off cannot pick a winner, and says so.** Six DSPy harnesses over a held-out
4-lesson selection set, C2, 3 draws each ([HARNESS-BAKEOFF-2026-08-14.md](HARNESS-BAKEOFF-2026-08-14.md)):

| candidate | recall (median) | invention | duds |
| --- | ---: | ---: | ---: |
| `compose` | 1.000 | 0.136 | 0 |
| `compose-v2` | 1.000 | 0.224 | 0 |
| `compose-read` | 0.957 | 0.223 | 0 |
| `agentic2` | 0.832 | 0.107 | 0 |
| `agentic` | 0.788 | 0.126 | 0 |
| `packed` | 0.766 | 0.174 | 0 |

The margin a winner must clear is **0.667** — the movement these candidates showed across
their own draws. The full spread top to bottom is **0.234**. *The same harness on the same
lesson moves recall further between draws than any two harnesses differ*, so nothing in
that table separates from anything else.

**And invention is not a tiebreak either.** It is reported without a margin, so the
0.107–0.224 spread is not known to be larger than its own noise. Reading `agentic2` as
"less inventive" would be doing exactly what the recall column forbids. It is recorded as
an open question, not as a reason.

So the choice is made on grounds the bake-off does not supply:

1. **It is what the evidence base describes.** 72 packs, 144 judgments, 576
   dimension-scores, two blinded passes, the judge-noise measurement, the delivery audit
   and all four rendering fixes were produced and verified on `compose-v2`. Shipping
   `packed` instead would leave every one of those numbers describing a system that does
   not run.
2. **Nothing argues against it.** It ties for top recall and has no duds.
3. **A typed tool-call field, not prompt-parsed prose.** `ReActV2` receives the turn as a
   `tool_calls` field. *(Corrected 2026-08-24: this heading read "native tool calling",
   which it is not. Modelling the turn as a typed field is the improvement over parsing
   free prose, but whether the call TRAVELS natively is decided by
   `lm.supports_function_calling`, which litellm answers False for every id in this
   project. gpt-oss still parses its tool calls out of text. See
   `HARNESS-TRANSPORT.md`.)* Its predecessor parses tool calls out of prompt text, which is the
   failure mode that produced five duds in six on a half-adopted dspy 3.1.3→3.3.0b1
   upgrade — invisible because the arm name did not move. That is why the library version
   now travels with every run. *(This bake-off shows `compose` clean on its selection set,
   so the failure was not universal; the point is that the mechanism exists and `ReActV2`
   does not have it.)*

The honest one-line version: **the arms are indistinguishable on the evidence, so ship the
one the evidence was collected on.**

## What was rejected, and what would reopen it

`packed` (`GenerateSection`, single-shot) was what production wired until this decision. It
is the lowest recall in the table, but not distinguishably so. Re-running the study on it
was the alternative and was rejected on cost, not on quality: it means regenerating 72
packs and re-judging, to answer a question the bake-off says has no answer.

This reopens if a bake-off with a **bounded** invention margin separates the candidates, or
if the recall margin narrows enough for the 0.234 spread to clear it. Both need more draws
per cell, which is the cheap experiment.

## The comparison is no longer DSPy-only — 2026-08-19

LangGraph, Google ADK and DeepAgents are wired as arms (`langgraph`, `adk`, `deepagents`).
Each is `compose-v2` with its driver swapped: the same contract, the same inputs, the same
composition tools writing the same `SectionDraft`, returned through the same
`assemble_section`. The three blockers this file recorded are closed:

- `Harness` carries a **`framework`** beside the loop, and every arm declares it. A record
  written before the dimension existed is refused rather than read as dspy.
- `dspy_version()` is now `framework_version(framework)`, resolving the distribution that
  actually ran. A langgraph run recording dspy's version would name a library that did not.
- Every framework reaches the model through **one litellm request, read off the LM
  `build_dspy_lm` returns** — same model, same OpenRouter provider block, same timeout,
  same retry budget, same sampling. `langchain-litellm` was the obvious route and was not
  taken: it requires litellm >= 1.97 against the 1.82.6 every pack in this study was
  generated on, so adopting it would have moved the transport under the dspy arms too.

**And the arms are still indistinguishable.** 9 candidates, 4 held-out lessons, 3 draws,
107 packs, each rated twice on the study's own H1 rubric by a judge that is not the
generator's model ([HARNESS-JUDGED-2026-08-19.md](HARNESS-JUDGED-2026-08-19.md)):

| candidate | framework | rubric mean |
| --- | --- | ---: |
| `langgraph` | langgraph | 3.34 |
| `deepagents` | deepagents | 3.33 |
| `compose-v2` | dspy | 3.29 |
| `adk` | google-adk | 3.29 |
| `compose-read` | dspy | 3.25 |
| `agentic2` | dspy | 3.20 |
| `agentic` | dspy | 3.19 |
| `packed` | dspy | 3.01 |
| `compose` | dspy | 2.99 |

The margin to clear is **0.75** — what one harness does to its own row when only the draw
changes. The whole table spreads **0.35**, and the top four sit within 0.05 of each other,
inside even the 0.10 the judge moves a row it has already read. *No framework separates from
any other, and none separates from what ships.*

So the decision above stands, and now on wider evidence: `compose-v2` ships because the
study's 72 packs, 144 judgments and four rendering fixes were produced on it, and because
nothing — including three other frameworks — argues against it.

Two things did change, and both are about the instrument rather than the arms:

1. **Recall never had a chance and now neither metric is asked to do that job.** The
   generation pass screens for duds and floor; the rubric ranks. Invention is still
   reported without a margin and is still not a tiebreak.
2. **A floor has to be measured at the level it is applied.** The first judged report
   compared twelve-pack means against a single cell's spread across draws (2.12, from one
   lesson of `compose-read`) and concluded nothing separated — which was true, but not for
   that reason. Both floors are now measured on the candidate rows the table ranks.

## What this comparison still does not cover

**One judge, not a panel.** Two ratings bound what *this* judge does to prose that did not
change. They say nothing about a different judge, or about a human rater.

**Constructed lessons.** The selection set reproduces the structural shapes the cohort audit
found in her real plans, and nothing chosen on it has seen the frozen data — but a harness
chosen here is chosen on constructed lessons.

**The frameworks are bounded in their own units.** dspy and ADK cap model turns; langgraph
caps graph supersteps; deepagents spends supersteps on middleware the others do not have.
Each arm names its own cut-off `iteration_limit`, and the study runner captures that in the
run trace — but the bake-off opens no trace window, so a composition truncated by its cap
reached the judge as a short section and the judged table cannot say which ones. Giving the
screening pass a per-cell trace is the next cheap thing to build.

**DeepAgents runs with its own harness attached** — todo list, virtual filesystem, `execute`,
`task`. It is not trimmed back to a bare tool loop, because that harness is what the
framework is; the arm measures deepagents, not langgraph twice.

**This reopens** if a bake-off separates the candidates at a margin measured the same way,
or if the rubric is rated by a panel rather than one judge. Both need more judges per pack,
which is now a flag rather than a rewrite.
