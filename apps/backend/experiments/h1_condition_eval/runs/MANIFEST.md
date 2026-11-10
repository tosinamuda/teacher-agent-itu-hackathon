# What each run is

105 directories. One of them is the study's Part 1 data; the rest are the record of
getting there. The tiers below come from `run.json` and `fingerprint.json`, not from the
labels — a label says what someone meant, the fingerprint says what ran.

| tier | runs | what it is |
| --- | --- | --- |
| 1 | 1 | the reported Part 1 data |
| 2 | 6 | full-ladder runs superseded by it |
| 3 | 19 | judged ablations that fixed the design |
| 4 | 72 | unjudged sweeps, probes and smoke runs |

## Tier 1 — reported

**`c0c3-prism-objective`.** 72 cases, 6 lessons, C0–C3, three draws per cell.
`deepseek-v4-flash` under `compose-v2`, corrected notes, context variant `v7-full`.
Judged twice by the model judge, and the source of every pack the expert panel rated —
named as `h1_run` in `human_rating/delivered/build.json`, which is what settles it.

Part 2 is `h2_personalisation_eval/runs/h2-deepseek-clean`, based on this run's **C3,
repeat 1**.

## Tier 2 — the same design, an earlier configuration

These reached the full ladder and were replaced. What separates each from the reported
run, counted over fingerprint inputs:

| run | differs in | what changed |
| --- | --- | --- |
| `c0c3-deepseek-native` | **1 of 44** | `plan.t3-w05` alone. The immediate predecessor: one lesson plan was corrected and all six lessons re-run. |
| `clean-six` | 13 of 45 | model, provider, context variant, and the section-writing signatures |
| `c0c3-worksheet` | 34 of 51 | note source, figures, signatures, provider — a different arm |
| `c0c3-renumbered` | 34 of 51 | as above |
| `c0c3-worksheet-2026-08-11T1538` | — | a second draw of `c0c3-worksheet`, recovered from an uncommitted working copy |
| `c0c3-worksheet-2026-08-11T1603` | — | a third draw of the same |

`c0c3-deepseek-native` is worth keeping visible: a one-input difference between two
72-pack runs is the cleanest available demonstration that the fingerprint tracks what it
claims to.

## Tier 3 — judged ablations

Nineteen runs that carry rating packets and judgments, at partial ladder scale. These are
where the design decisions were made, and they are the interesting half of the record:
they show what did *not* separate.

`c1-clean-control`, `c1-clean-payload`, `c1-corrected-b`, `c1-semantics`, `diag-v3`,
`diag-v4`, `diag-v4-noassess`, `full-v3`, `full-v3-deepseek`, `full-v3-deepseek-native`,
`full-v3-enriched`, `full-v7`, `full-v7-deepseek`, `full-v7-deepseek-native`,
`full-v7-enriched`, `t3w02-deepseek`, `t3w02-dspy`, `t3w05-prism-declared`,
`t3w05-prism-objective`.

## Tier 4 — sweeps, probes and smoke runs

Seventy-two directories with no rating packets: 42 `h1-<hash>` parameter sweeps, seven
prompt captures holding no cases at all (`prompt-audit*`, `prompt-current`,
`diet-before`, `diet-after`), and the rest single-lesson probes, format checks and smoke
runs. Kept because they cost nothing and a negative result is only citable if the run
behind it still exists.

## Reading any of this

Nothing here is the study's data except tier 1. Before quoting a number from a tier 2, 3
or 4 run, check its `fingerprint.json` against `c0c3-prism-objective`'s: a run that
differs in `arm.note_source` was generated from a different corpus, and a run that
differs in `arm.model` answers a different question.
